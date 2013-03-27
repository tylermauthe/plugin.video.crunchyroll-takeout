# -*- coding: utf-8 -*-
import sys
import os
import xbmc
import xbmcgui
import urllib
import urllib2
import StringIO
import cookielib
import gzip
import re
import datetime
import crunchy_main
import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout')
__language__ = __settings__.getLocalizedString
from BeautifulSoup import BeautifulSoup

__settings__ = sys.modules[ "__main__" ].__settings__

class _Info:
	
	def __init__( self, *args, **kwargs ):
		self.__dict__.update( kwargs )
        
class CrunchyParser:

	pattern_episode_id = re.compile('[0-9]{6}')
	
	def __init__(self):
		self.settings = {}
		self.settings['thumb_quality'] = int(__settings__.getSetting("thumb_quality"))
		print "CRUNCHY: --> Thumb Quality: " + str(self.settings['thumb_quality'])
		thumb_quality = ['_thumb', '_large', '_full']
		self.settings['thumb_quality'] = thumb_quality[self.settings['thumb_quality']]
	
	def parseSeries(self, feed, cat):
		info = []
		soup = BeautifulSoup(feed)
		series_list = soup.findAll('item')
		num_series = len(series_list)
		for series in series_list:
			item = {}
			item['name'] = series.title.string.encode('utf-8')
			if(series.description.string is not None):
                                item['description'] = series.description.string.encode('utf-8')
                        else:
                                item['description'] = " "
			item['img'] = series.find('boxee:property').string.replace("_large",self.settings['thumb_quality'])
			item['page_url'] = series.guid.string
			print item['page_url']
			temp = item['page_url'].split(".com/")
			print "\n\n"
			print temp
			item['id'] = temp[1]
			crunchy_main.UI().addItem({'Title':item['name'], 'mode':'series', 'Thumb':item['img'], 'id':item['id'], 'page_url':item['page_url'], 'plot':item['description']}, True, num_series)
		crunchy_main.UI().endofdirectory('none')

         #Added to parse Series HTML
	def parseSimulcasts(self, feed_simulcasts, anime_feed):
		print "Crunchyroll Takeout: --> in parseQueue"
		soup_simulcasts = BeautifulSoup(feed_simulcasts)
		soup_anime = BeautifulSoup(anime_feed)
		queue_list = soup_simulcasts.findAll('li',attrs={"group_id":True})
		num_series = len(queue_list)
		print "Crunchyroll Takeout: -->number of found series "+str(num_series)
		x = 0
		for queue_series_id in queue_list:
                        if queue_series_id is not None and x < (num_series - 5):
                                series_find = 'http://www.crunchyroll.com/'+queue_series_id["group_id"]
                                print 'Crunchyroll Takeout -> Series find = '+series_find
                                anime_isseries = soup_anime.find('guid', text={series_find:True})
                                series = None
                                if anime_isseries is not None:
                                        print 'Crunchyroll Takeout -> Found Anime'
                                        anime_serieslist = soup_anime.findAll('item')
                                        for anime_series in anime_serieslist:
                                                if anime_series.guid.string == series_find:
                                                        series = anime_series
                                if series is not None:
                                        #print series.string
                                        item = {}
                                        item['name'] = series.title.string.encode('utf-8')
                                        if(series.description.string is not None):
                                                item['description'] = series.description.string.encode('utf-8')
                                        else:
                                                item['description'] = " "
                                        item['img'] = series.find('boxee:property').string.replace("_large",self.settings['thumb_quality'])
                                        item['page_url'] = series.guid.string
                                        print item['page_url']
                                        temp = item['page_url'].split(".com/")
                                        print "\n\n"
                                        print temp
                                        item['id'] = temp[1]
                                        crunchy_main.UI().addItem({'Title':item['name'], 'mode':'series', 'Thumb':item['img'], 'id':item['id'], 'page_url':item['page_url'], 'plot':item['description']}, True, num_series)
                                else:
                                        print "not found"
                        x = x + 1
		crunchy_main.UI().endofdirectory('none')

        #Added to parse Queue HTML
	def parseQueue(self, feed_queue, anime_feed, drama_feed):
		print "Crunchyroll Takeout: --> in parseQueue"
		local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
		loginerror = local_string(70006)
		soup_queue = BeautifulSoup(feed_queue)
		soup_anime = BeautifulSoup(anime_feed)
		soup_drama = BeautifulSoup(drama_feed)
		queue_list = soup_queue.findAll('li',attrs={"series_id":True})
		num_series = len(queue_list)
		print "Crunchyroll Takeout: -->number of found series "+str(num_series)
		if num_series == 0:
                        title = soup_queue.html.head.title
                        print "Crunchyroll Takeout -> title.string '"+title.string+"'"
                        if title.string == 'Crunchyroll - Sign Up or Log In':
                                crunchy_main.UI().addItem({'Title':loginerror, 'mode':'series'}, True, num_series)
		for queue_series_id in queue_list:
                        if queue_series_id is not None:
                                series_find = 'http://www.crunchyroll.com/'+queue_series_id["series_id"]
                                print 'Crunchyroll Takeout -> Series find = '+series_find
                                anime_isseries = soup_anime.find('guid', text={series_find:True})
                                drama_isseries = soup_drama.find('guid', text={series_find:True})
                                series = None
                                if anime_isseries is not None:
                                        print 'Crunchyroll Takeout -> Found Anime'
                                        anime_serieslist = soup_anime.findAll('item')
                                        for anime_series in anime_serieslist:
                                                if anime_series.guid.string == series_find:
                                                        series = anime_series
                                if drama_isseries is not None:
                                        print 'Crunchyroll Takeout -> Found Drama'
                                        drama_serieslist = soup_drama.findAll('item')
                                        for drama_series in drama_serieslist:
                                                if drama_series.guid.string == series_find:
                                                        series = drama_series
                                if series is not None:
                                        #print series.string
                                        item = {}
                                        item['name'] = series.title.string.encode('utf-8')
                                        if(series.description.string is not None):
                                                item['description'] = series.description.string.encode('utf-8')
                                        else:
                                                item['description'] = " "
                                        item['img'] = series.find('boxee:property').string.replace("_large",self.settings['thumb_quality'])
                                        item['page_url'] = series.guid.string
                                        print item['page_url']
                                        temp = item['page_url'].split(".com/")
                                        print "\n\n"
                                        print temp
                                        item['id'] = temp[1]
                                        crunchy_main.UI().addItem({'Title':item['name'], 'mode':'series', 'Thumb':item['img'], 'id':item['id'], 'page_url':item['page_url'], 'plot':item['description']}, True, num_series)
                                else:
                                        print "not found"
                crunchy_main.UI().endofdirectory('none')

	def parseEpisodes(self, feed):
		info = []
		local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
		no_shows_error = local_string(70001)
		print "CRUNCHY: Parsing episodes..."
		soup = BeautifulSoup(feed)
		episode_list = soup.findAll('item')
		num_episodes = len(episode_list)
		if num_episodes is 0:
                        crunchy_main.UI().addItem({'Title':no_shows_error, 'mode':'episode', 'Thumb':'None', 'id':'None', 'page_url':'None', 'plot':'None', 'resolutions':'None'}, True, 0)
		for episode in episode_list:
			item = {}
			print "CRUNCHY: Parsing episode"
			if episode.title.string is not None:
                                item['episode_name'] = episode.title.string.encode('utf-8')
                        else:
                                item['episode_name'] = ""
			item['series_name'] = episode.find('boxee:property', attrs={'name':'custom:seriesname'}).string.encode('utf-8')
                        if episode.find('boxee:property', attrs={'name':'custom:episodenum'}) is not None:
                                item['episode_number'] = episode.find('boxee:property', attrs={'name':'custom:episodenum'}).string.encode('utf-8') + ": "
                        else:
                                item['episode_number'] = ""
			if episode.find('boxee:property', attrs={'name':'custom:premium_only'}) is not None:
                                # -*- coding: utf-8 -*-
                                #item['name'] = "☆" + item['episode_number'] + item['episode_name']
                                item['name'] = "/!\\ " + item['episode_number'] + item['episode_name']
                        else:
                                item['name'] = item['episode_number'] + item['episode_name']
			item['ordernum'] = ''
			if(episode.description.string is not None):
                                item['description'] = unicode(episode.description.string).encode('utf-8')
                        else:
                                item['description'] = " "
			item['img'] = episode.find('media:thumbnail')['url'].replace("_large",self.settings['thumb_quality'])
			item['page_url'] = episode.guid.string.encode('utf-8')
			ep_number = episode.find('boxee:property', attrs={'name':'custom:episodenum'})
			if ep_number:
				item['ordernum'] = ep_number.string.encode('utf-8')
			else:
				item['ordernum'] = None
			resolutions = episode.find('boxee:property', attrs={'name':'custom:available_resolutions'})
			if resolutions.string:
				item['resolutions'] = resolutions.string
			else:
				item['resolutions'] = '12,20,21,80'
			ep_id = self.pattern_episode_id.search(item['page_url'])
			ep_id = ep_id.group()
			item['ep_id'] = ep_id
			crunchy_main.UI().addItem({'Title':item['series_name']+' - '+item['name'], 'mode':'episode', 'Thumb':item['img'], 'id':item['ep_id'], 'page_url':item['page_url'], 'plot':item['description'], 'resolutions':item['resolutions']}, True, num_episodes)
		crunchy_main.UI().endofdirectory('none')

class CrunchyScraper:
	
	def __init__(self):
		self.base_path = os.path.join(xbmc.translatePath("special://masterprofile/"), "addon_data", os.path.basename(os.getcwd()))
		self.base_cache_path = os.path.join(self.base_path, "cache")
		if not os.path.exists(self.base_cache_path):
			os.makedirs(self.base_cache_path)
		self.episodes_list = []
		
	def getSeriesListing(self, cat='anime', subcat=None):
		if subcat:
			subcat = subcat.replace('_','%20')
			url = "http://www.crunchyroll.com/boxee_feeds/"+ cat +"/"+ subcat
		else:
			url = "http://www.crunchyroll.com/boxee_feeds/"+ cat
		file_path = os.path.join(self.base_cache_path, cat +".rss")
		refreshRSS = self.check_cache_time(file_path)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read()
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed)
			file_object.close()
		CrunchyParser().parseSeries(rssFeed, cat)
		
	def getEpisodeListing(self, id, url=None):
		print id
		full_url = "http://www.crunchyroll.com/boxee_feeds/showseries/"+str(id)
		if url:
			full_url = url
		file_path = os.path.join(self.base_cache_path, id+".rss")
		refreshRSS = self.check_cache_time(file_path)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(full_url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read().decode('utf-8','ignore')
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed.encode('utf-8'))
			file_object.close()
		CrunchyParser().parseEpisodes(rssFeed)
		
        #Added to Pull Simulcasts
	def getScrappedSeries(self, scrapper_mode, id=None):
		print id
		file_name = "Simulcasts.html"
		show_name = "anime.rss"
		path_url = "http://www.crunchyroll.com/boxee_feeds/genre_anime_all/"
		if str(scrapper_mode) == 'drama_withtag':
                       full_url =  "http://www.crunchyroll.com/videos/drama/genres/"+str(id)
                       file_name = str(id)+".html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_drama_all/"
                       show_name = "drama.rss"
                if str(scrapper_mode) == 'drama_seasons':
                       full_url =  "http://www.crunchyroll.com/videos/drama/seasons/"+str(id)
                       file_name = str(id)+".html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_drama_all/"
                       show_name = "drama.rss"
                if str(scrapper_mode) == 'pop_withtag':
                       full_url =  "http://www.crunchyroll.com/videos/pop/genres/"+str(id)
                       file_name = str(id)+".html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_pop_all/"
                       show_name = "pop.rss"
                if str(scrapper_mode) == 'poppop':
                       full_url = "http://www.crunchyroll.com/videos/pop"
                       file_name = "PopularPop.html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_pop_all/"
                       show_name = "pop.rss"
                if str(scrapper_mode) == 'pop_updated':
                       full_url = "http://www.crunchyroll.com/videos/pop/updated"
                       file_name = "PopularPop.html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_pop_all/"
                       show_name = "pop.rss"
                if str(scrapper_mode) == 'anime_simulcasts':
                       full_url = "http://www.crunchyroll.com/videos/anime/simulcasts"
                       file_name = "AnimeSimulcasts.html"
                if str(scrapper_mode) == 'drama_updated':
                       full_url = "http://www.crunchyroll.com/videos/drama/updated"
                       file_name = "dramaupdated.html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_drama_all/"
                       show_name = "drama.rss"
                if str(scrapper_mode) == 'drama_simulcasts':
                       full_url = "http://www.crunchyroll.com/videos/drama/simulcasts"
                       file_name = "dramasimulcasts.html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_drama_all/"
                       show_name = "drama.rss"
                if str(scrapper_mode) == 'drama_popular':
                       full_url = "http://www.crunchyroll.com/videos/drama/popular"
                       file_name = "dramapopular.html"
                       path_url = "http://www.crunchyroll.com/boxee_feeds/genre_drama_all/"
                       show_name = "drama.rss"
                if str(scrapper_mode) == 'anime_updated':
                       full_url = "http://www.crunchyroll.com/videos/anime/updated"
                       file_name = "animeupdated.html"
		file_path = os.path.join(self.base_cache_path, file_name)
		refreshRSS = self.check_cache_time(file_path)
		show_path = os.path.join(self.base_cache_path, show_name)
		refreshShow = self.check_cache_time(show_path)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(full_url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read().decode('utf-8','ignore')
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed.encode('utf-8'))
			file_object.close()
		if(os.path.exists(show_path) and refreshShow is False):
			usock = open(show_path, "r")
			rssShow = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(path_url)
			rssShow = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssShow = gzip.GzipFile(fileobj=StringIO.StringIO(rssShow)).read()
		usock.close()
		if (not os.path.exists(rssShow)):
			file_object = open(show_path, "w")
			file_object.write(rssShow)
			file_object.close()
		CrunchyParser().parseSimulcasts(rssFeed, rssShow)

        #Added to Pull Queue File; Throws error if no login found
	def getQueue(self):
                settings = {}
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                notice_msg = local_string(70000)
                login_try_msg = local_string(70002)
                setup_msg = local_string(70003)
                pullshow_msg = local_string(70004)
                dl_queue = local_string(70005)
		settings['username'] = __settings__.getSetting("crunchy_username")
		settings['password'] = __settings__.getSetting("crunchy_password")
		cj = cookielib.LWPCookieJar()
		if (settings['username'] != '' and settings['password'] != ''):
			print "CRUNCHYROLL: --> Attempting to log-in with your user account..."
			ex = 'XBMC.Notification("'+notice_msg+':","'+login_try_msg+'...", 3000)'
			xbmc.executebuiltin(ex)
			url = 'https://www.crunchyroll.com/?a=formhandler'
			data = urllib.urlencode({'formname':'RpcApiUser_Login', 'next_url':'','fail_url':'/login','name':settings['username'],'password':settings['password']})
			COOKIEFILE= os.path.join(self.base_cache_path, "crunchycookie.lwp")
                        try:
                                os.remove(COOKIEFILE)
                                print "delete ->" + COOKIEFILE
                        except Exception: 
                                pass
			self.cookie = cj
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			opener.addheaders = [('Referer', 'https://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
			self.opener = opener
			print "CRUNCHYROLL: --> saving new Cookie."
			urllib2.install_opener(opener)
			req = self.opener.open(url, data)
			req.close()
			cj.save(COOKIEFILE)
		else:
                        ex = 'XBMC.Notification("'+notice_msg+':","'+setup_msg+'.", 3000)'
                        xbmc.executebuiltin(ex)
			print "crunchyroll-takeout -> NO CRUNCHYROLL ACCOUNT FOUND!"
		full_url = "http://www.crunchyroll.com/queue"
		file_path = os.path.join(self.base_cache_path, "queue.html")
		refreshRSS = self.check_cache_time(file_path)
		ex = 'XBMC.Notification("'+notice_msg+':","'+dl_queue+'", 3000)'
		xbmc.executebuiltin(ex)
		if(os.path.exists(file_path) and refreshRSS is False):
			usock = open(file_path, "r")
			rssFeed = usock.read()
		else:
                        print "Crunchyroll Takeout: --> getting queue list"
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			opener.addheaders = [('Referer', 'https://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7')]
			usock = opener.open(full_url)
			rssFeed = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssFeed = gzip.GzipFile(fileobj=StringIO.StringIO(rssFeed)).read().decode('utf-8','ignore')
		usock.close()
		if (not os.path.exists(file_path)):
			file_object = open(file_path, "w")
			file_object.write(rssFeed.encode('utf-8'))
			file_object.close()
                anime_url = "http://www.crunchyroll.com/boxee_feeds/genre_anime_all/"
                drama_url = "http://www.crunchyroll.com/boxee_feeds/drama"
		anime_path = os.path.join(self.base_cache_path, "anime.rss")
		refreshAnime = self.check_cache_time(anime_path)
		drama_path = os.path.join(self.base_cache_path, "drama.rss")
		refreshDrama = self.check_cache_time(drama_path)
		ex = 'XBMC.Notification("'+notice_msg+':","'+pullshow_msg+'", 3000)'
		xbmc.executebuiltin(ex)
		if(os.path.exists(anime_path) and refreshAnime is False):
			usock = open(anime_path, "r")
			rssAnime = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(anime_url)
			rssAnime = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssAnime = gzip.GzipFile(fileobj=StringIO.StringIO(rssAnime)).read()
		usock.close()
		if (not os.path.exists(rssAnime)):
			file_object = open(anime_path, "w")
			file_object.write(rssAnime)
			file_object.close()
		if(os.path.exists(drama_path) and refreshDrama is False):
			usock = open(drama_path, "r")
			rssDrama = usock.read()
		else:
			opener = urllib2.build_opener()
			opener.addheaders = [('User-Agent','curl/7.16.3 (Windows  build 7600; en-US; beta) boxee/0.9.21.12594'),('Accept-Encoding','deflate, gzip'),('Accept-Charset','ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Accept-Language','en-us,en;q=0.5')]
			usock = opener.open(drama_url)
			rssDrama = usock.read()
			if usock.headers.get('content-encoding', None) == 'gzip':
				rssDrama = gzip.GzipFile(fileobj=StringIO.StringIO(rssDrama)).read()
		usock.close()
		if (not os.path.exists(rssDrama)):
			file_object = open(drama_path, "w")
			file_object.write(rssDrama)
			file_object.close()
		CrunchyParser().parseQueue(rssFeed, rssAnime, rssDrama)
        
		
	def getImages(self, url, file_path):
		file_path += ".jpg"
		full_path = os.path.join(self.base_cache_path, file_path)
		try:
			if(url):
				if(not os.path.exists(full_path) and url != ""):
					urllib.urlretrieve( url, full_path )
				img_path = full_path
				return img_path
		except:
			urllib.urlcleanup()
			remove_tries = 3
			while remove_tries and os.path.isfile(full_path):
				try:
					os.remove(full_path)
				except:
					remove_tries -=1
					xbmc.sleep(1000)
					
			
	def check_cache_time(self, filename):
		if os.path.exists(filename):
			mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
			cur_time = datetime.datetime.now()
			elapsed = cur_time - mod_time
			if(elapsed > datetime.timedelta(minutes=60)):
				print "CRUNCHY: --> Removing cached RSS feed..."
				os.remove(filename)
				return False
			else:
				print "CRUNCHY: --> RSS feed is still valid."
				return True
		else:
			print "CRUNCHY: --> RSS feed not found.  Downloading..."
			return False
