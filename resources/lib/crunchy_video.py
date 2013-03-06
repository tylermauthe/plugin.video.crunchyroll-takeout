import os
# -*- coding: utf-8 -*-
import re
import sys
import time
import xbmc
import xbmcgui
import urllib
import urllib2
import cookielib
import subprocess
import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout')
__language__ = __settings__.getLocalizedString
from crunchyDec import crunchyDec
from BeautifulSoup import BeautifulSoup

__settings__ = sys.modules[ "__main__" ].__settings__

class CrunchyPlayback:
	def __init__(self):
		self.base_cache_path = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", os.path.basename(os.getcwd()))
		self.subFormat = '.ass'
	
	def checkPlayer(self, url):
		hour = 3600
		max_age = 3*hour
		player_rev = None
		lastPlayerCheck = __settings__.getSetting("lastPlayerCheck")
		if not lastPlayerCheck:
			player_rev = self.returnPlayer(url)
			__settings__.setSetting("playerRevision", player_rev)
			new_time = time.time()
			print new_time
			__settings__.setSetting("lastPlayerCheck", str(new_time))
		else:
			time_now = time.time()
			if float(lastPlayerCheck) < (time_now - max_age):
				print "CRUNCHYROLL: --> Updating player version..."
				player_rev = self.returnPlayer(url)
				__settings__.setSetting("playerRevision", player_rev)
				__settings__.setSetting("lastPlayerCheck", str(time.time()))
			else:
				print "CRUNCHYROLL: --> Cache valid: using stored player version..."
				player_rev = __settings__.getSetting("playerRevision")
		return player_rev
		
	def returnPlayer(self, url):
		REGEX_PLAYER_REV = re.compile("(?<=swfobject\.embedSWF\(\").*(?:StandardVideoPlayer.swf)")
		cj = cookielib.CookieJar()
		intOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		request = urllib2.Request(url)
		response = intOpener.open(request)
		soup = BeautifulSoup(response)
		interstitial = soup.find('div', attrs={'id': 'adt_interstitial'})
		if interstitial:
			continueLink = soup.find('a', attrs={'style': 'font-size:14px;line-height:25px;'})
			continueLink = continueLink['href']
			response = intOpener.open(continueLink)
			soup = BeautifulSoup(response)
		match = REGEX_PLAYER_REV.search(str(soup))
		if match:
			print "CRUNCHYROLL: --> Found new Player Revision"
			playerTemp = str(match.group(0))
			player = playerTemp.split('\/')[4]
			print player
		else:
			print "CRUNCHYROLL: --> NO MATCHES FOUND for new Player Revision"
			player = '20110110190253.eaa2220a32da869f33f1cefc8dc91b3b'
		return player
	
	def downloadHTML(self, url):
		self.currenturl = url
		response = self.opener.open(self.currenturl)
		html = response.read()
		print "CRUNCHYROLL: --> Grabbing URL: "+self.currenturl
		self.referer = self.currenturl
		return html
	
	def startPlayback(self, vid_id, page_url, resolutions, series_name):
		stream = {}
		settings = {}
		cj = cookielib.LWPCookieJar()
		settings['username'] = __settings__.getSetting("crunchy_username")
		settings['password'] = __settings__.getSetting("crunchy_password")
		settings['quality'] = int(__settings__.getSetting("video_quality"))
		res_names = ['SD', '480p', '720p', '1080p']
		res_display = ['p360','p480','p720','p1080']
		res_format = ['102','106','108']
		res_quality = ['10','20','21','30','60','61','62','80']
		x=0

                if (settings['username'] != '' and settings['password'] != ''):
			print "CRUNCHYROLL: --> Attempting to log-in with your user account..."
			url = 'https://www.crunchyroll.com/?a=formhandler'
			data = urllib.urlencode({'formname':'RpcApiUser_Login', 'next_url':'','fail_url':'/login','name':settings['username'],'password':settings['password']})

			COOKIEFILE= os.path.join(self.base_cache_path, "crunchycookie.lwp")
			self.cookie = cj
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			opener.addheaders = [('Host','www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
			self.opener = opener
			print "CRUNCHYROLL: --> Cookie file doesn't exist; saving new one."
			urllib2.install_opener(opener)
			req = self.opener.open(url, data)
			req.close()
			cj.save(COOKIEFILE)
                        res_options = []
			for res in res_names:
				item = [res,x]
				x=x+1
				res_options.append(item)
			#If the user has selected 'Ask', display the quality select dialog
			if settings['quality'] == len(res_names):
				quality = xbmcgui.Dialog().select('Please select a quality level:', [opt[0] for opt in res_options])
			#If the user has selected 'Highest available quality', set it as such
			elif settings['quality'] > len(res_names):
				quality = len(res_names)-1
			#If the user has selected a specific resolution, use that instead
			elif settings['quality'] < 4:
				quality = settings['quality']
			else:
				quality = 0
			if(quality > (len(res_names)-1)):
				quality = len(res_names)-1;
			stream['video_format'] = '102'
                        stream['resolution'] = '10'
                        if quality != 0:
                                quality_page_url = page_url+"?"+res_display[quality]+"=1"
                                haystack = opener.open(quality_page_url)
                                str_haystack = haystack.read()
                                print haystack
                                for vid_format in res_format:
                                        format_find = 'video_format%3D'+vid_format+'%26'
                                        print "Crunchyroll Takeout -> format_fime " + format_find
                                        isformat = str_haystack.find(format_find)
                                        print isformat
                                        if isformat is not -1:
                                                stream['video_format'] = vid_format
                                                print "Crunchyroll Takeout -> found " + vid_format
                                for vid_quality in res_quality:
                                        quality_find = 'video_quality%3D'+vid_quality+'%26'
                                        isquality = str_haystack.find(quality_find)
                                        print "Crunchyroll Takeout -> quality_find " + quality_find
                                        print  isquality
                                        if isquality is not -1:
                                                stream['resolution'] = vid_quality
                                                print "Crunchyroll Takeout -> found " + vid_quality
	
		else:
			print "CRUNCHYROLL: --> No user account found..."
			opener = urllib2.build_opener()
			opener.addheaders = [('Host','www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
			self.opener = opener
			stream['video_format'] = '102'
			stream['resolution'] = '10'

                print stream['resolution']
                print stream['video_format']
                prhold = {}
		playlist = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetStandardConfig&media_id="+vid_id+"&video_format="+stream['video_format']+"&video_quality="+stream['resolution']+"&auto_play=1&show_pop_out_controls=1"
		print "CRUNCHYROLL: --> Playlist is: "+playlist
		print "CRUNCHYROLL: --> page_url is: "+page_url
		player_revision = self.checkPlayer(page_url)
		prhold['Referer'] = "http://static.lln.crunchyroll.com/flash/"+player_revision+"/StandardVideoPlayer.swf"
		prhold['current_page'] = page_url
		print "CRUNCHYROLL: --> page_url is: "+player_revision
		url_ref = urllib.urlencode(prhold)
		response = self.opener.open(playlist, url_ref)
		xmlSource = response.read()
		soup = BeautifulSoup(xmlSource)

		player_url = soup.find('default:chromelessplayerurl').string
		meta_info = soup.find('media_metadata')
		try:
			stream['episode_display'] = series_name +" - "+ meta_info.episode_number.string
			stream['series_name'] = series_name
			stream['episode'] = meta_info.episode_number.string
		except Exception as e:
			print '--------> Error', str(e)
			stream['episode_display'] = 'Crunchyroll.com'
		
		stream_info = soup.find('stream_info')
		if stream_info:
			try:
				stream['url'] = stream_info.host.string
				if stream_info.host.string is None:
					stream['url'] = "null.net/dummy"
				stream['token'] = stream_info.token.string
				stream['file'] = stream_info.file.string
				stream['page_url'] = page_url
				stream['swf_url'] = "http://static.lln.crunchyroll.com/flash/"+player_revision+"/"+player_url
				try:
					app = stream['url'].split('.net/')
					stream['app'] = app[1]
					print "CRUNCHYROLL: --> App - " + stream['app']
				except:
					print "Couldn't find App"
				
				useSubs = False
				mediaid = vid_id
				subtitles = soup.find('iv')
				print "CRUNCHYROLL: --> Attempting to find subtitles..."
				if(subtitles):
					print "CRUNCHYROLL: --> Found subtitles.  Continuing..."
					formattedSubs, formatSRT = crunchyDec().returnSubs(xmlSource)
					if formatSRT:
						print "CRUNCHYROLL: --> Using unstyled subs!"
						self.subFormat = '.srt'
					subfile = open(xbmc.translatePath('special://temp/crunchy_'+ mediaid + self.subFormat), 'w')
					subfile.write(formattedSubs.encode('utf-8'))
					subfile.close()
					useSubs = True
				else:
					print "CRUNCHYROLL: --> No subtitles available!"
					mediaid = ""
				
				self.playvideo(stream, mediaid, useSubs)
			except:
                                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                                Video_restricted = local_string(80001)
                                upsell_msg = local_string(80002)
                                mature = local_string(80003)
                                Login_msg = local_string(80004)
				if stream_info.find('upsell'):
					if stream_info.upsell.string == '1':
						ex = 'XBMC.Notification("'+Video_restricted+':","'+upsell_msg+'.", 3000)'
						xbmc.executebuiltin(ex)
						print "CRUNCHYROLL: --> Selected video quality is not available to your user account."
				elif stream_info.find('error'):
					if stream_info.error.code.string == '4':
						ex = 'XBMC.Notification("'+mature+':","'+Login_msg+'.", 3000)'
						xbmc.executebuiltin(ex)
						print "CRUNCHYROLL: --> This video is marked as Mature Content.  Please login to view it."
		else:
			print "Playback Failed!"
		
	def playvideo(self, stream, mediaid, useSubs):
		#rtmp_url = stream['url']+stream['file'].replace('&amp;','&') + " swfurl=" +stream['swf_url'] + " swfvfy=1 token=" +stream['token']+ " playpath=" +stream['file'].replace('&amp;','&')+ " pageurl=" +stream['page_url']+ " tcUrl=" +stream['url']
		if stream['url'] == "null.net/dummy":
			rtmp_url = stream['file'].replace('&amp;','&')
		else:
			rtmp_url = stream['url']+stream['file'].replace('&amp;','&') + " swfurl=" +stream['swf_url'] + " swfvfy=1 token=" +stream['token']+ " playpath=" +stream['file'].replace('&amp;','&')+ " pageurl=" +stream['page_url']+ " tcUrl=" +stream['url']
		item = xbmcgui.ListItem(stream['episode_display'])

		item.setInfo( type="Video", infoLabels={ "Title": stream['episode_display'] })
		item.setProperty('IsPlayable', 'true')

		subs = []
		if useSubs:
			subs.append(xbmc.translatePath('special://temp/crunchy_' + mediaid + self.subFormat))
		localSubs = self.findSubtitles(stream['series_name'], stream['episode'])

		if localSubs:
			subs.append(localSubs)
		xbmc.Player().play(rtmp_url, item)
		time.sleep(1)
		while not xbmc.Player().isPlaying():
			time.sleep(0.5)
		
		for sub in subs:
			print "--------------->>>>>Adding subs "+sub
			xbmc.Player().setSubtitles(sub)
	
	def findSubtitles(self, series, episode):
		subsFolder = xbmc.translatePath('special://subtitles')
		if not subsFolder:
			return None
		nameSearch = re.compile('.*'+series+'[ -_]*[0]*'+episode+'[\\D]{1}.*')
		#print "------------> RE:"+'.*'+series+'[ -_]*[0]*'+episode+'[\\D]{1}.*'
		for root, dirs, files in os.walk(subsFolder):
			
			for name in files:
				#print '------>Checking '+root+' '+name
				if nameSearch.match(name):
					return os.path.join(root, name)
		return None
