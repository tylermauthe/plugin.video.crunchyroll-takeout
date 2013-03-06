import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import crunchy_scraper
import re
import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout')
__language__ = __settings__.getLocalizedString
from crunchy_video import CrunchyPlayback

class updateArgs:

	def __init__(self, *args, **kwargs):
		for key, value in kwargs.iteritems():
			if value == 'None':
				kwargs[key] = None
			else:
				kwargs[key] = urllib.unquote_plus(kwargs[key])
		self.__dict__.update(kwargs)

class UI:
	
	def __init__(self):
		self.main = Main(checkMode = False)
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')

	def Language(self):
                self.Language = xbmc.Language(os.getcwd())
	
	def endofdirectory(self, sortMethod = 'none'):
		# set sortmethod to something xbmc can use
		if sortMethod == 'title':
			sortMethod = xbmcplugin.SORT_METHOD_LABEL
		elif sortMethod == 'none':
			sortMethod = xbmcplugin.SORT_METHOD_NONE
		elif sortMethod == 'date':
			sortMethod = xbmcplugin.SORT_METHOD_DATE
		#Sort methods are required in library mode.
		xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod)
		#let xbmc know the script is done adding items to the list.
		dontAddToHierarchy = False
		xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), updateListing = dontAddToHierarchy)
			
	def addItem(self, info, isFolder=True, total_items = 0):
		#Defaults in dict. Use 'None' instead of None so it is compatible for quote_plus in parseArgs
		info.setdefault('url','None')
		info.setdefault('Thumb','None')
		info.setdefault('id','None')
		info.setdefault('page_url','None')
		info.setdefault('Icon','None')
		info.setdefault('resolutions','10')
		info.setdefault('plot','No description available.')
		print info
		#create params for xbmcplugin module
		u = sys.argv[0]+\
			'?url='+urllib.quote_plus(info['url'])+\
			'&mode='+urllib.quote_plus(info['mode'])+\
			'&name='+urllib.quote_plus(info['Title'])+\
			'&id='+urllib.quote_plus(info['id'])+\
			'&resolutions='+urllib.quote_plus(info['resolutions'])+\
			'&page_url='+urllib.quote_plus(info['page_url'])+\
			'&icon='+urllib.quote_plus(info['Thumb'])+\
			'&plot='+urllib.quote_plus(info['plot'])
		#create list item
		li=xbmcgui.ListItem(label = info['Title'], iconImage = info['Icon'], thumbnailImage = info['Thumb'])
		li.setInfo( type="Video", infoLabels={ "Title":info['Title'], "Plot":info['plot']})
		#for videos, replace context menu with queue and add to favorites
		if not isFolder:
			li.setProperty("IsPlayable", "true")#let xbmc know this can be played, unlike a folder.
			#add context menu items to non-folder items.
			contextmenu = [('Queue Video', 'Action(Queue)')]
		#for folders, completely remove contextmenu, as it is totally useless.
		else:
			li.addContextMenuItems([], replaceItems=True)
		#add item to list
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=isFolder, totalItems=total_items)

	def showCategories(self):
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                Anime = local_string(50000)
                Drama = local_string(50004)
                Queue = local_string(50005)
                Pop = local_string(50009)
                self.addItem({'Title':Queue, 'mode':'queue'})
		self.addItem({'Title':Anime, 'mode':'anime'})
		self.addItem({'Title':Drama, 'mode':'drama_list'})
		#self.addItem({'Title':Pop, 'mode':'pop'})
		self.endofdirectory()
		
	def showAnime(self):
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                All_Anime = local_string(50001)
                Recently_Added = local_string(50002)
                Simulcasts = local_string(50006)
                Most_Popular = local_string(50003)
                Browse_by_Genre = local_string(50007)
		self.addItem({'Title':All_Anime, 'mode':'genre_anime_all'})
		self.addItem({'Title':Recently_Added, 'mode':'anime_updated'})
		self.addItem({'Title':Simulcasts, 'mode':'anime_simulcasts'})
		self.addItem({'Title':Most_Popular, 'mode':'anime_popular'})
                self.addItem({'Title':Browse_by_Genre, 'mode':'anime_genre'})
		self.endofdirectory()
		
	def animeGenre(self):
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                Action = local_string(60001)
                Adventure = local_string(60002)
                Comedy = local_string(60003)
                Drama = local_string(60004)
                Ecchi = local_string(60005)
                Fantasy = local_string(60006)
                Harem = local_string(60007)
                Horror = local_string(60008)
                Magic = local_string(60009)
                Martial_Arts = local_string(60010)
                Mecha = local_string(60011)
                Military = local_string(60012)
                Parody = local_string(60013)
                Psychological = local_string(60014)
                Romance = local_string(60015)
                Science_Fiction = local_string(60016)
                Shoujo = local_string(60017)
                Slice_of_Life = local_string(60018)
                Space = local_string(60019)
                Sports = local_string(60020)
                Supernatural = local_string(60021)
                Tournament = local_string(60022) 
		self.addItem({'Title':Action, 'mode':'anime_withtag','id':'action'})
		self.addItem({'Title':Adventure, 'mode':'anime_withtag','id':'adventure'})
		self.addItem({'Title':Comedy, 'mode':'anime_withtag','id':'comedy'})
		self.addItem({'Title':Drama, 'mode':'anime_withtag','id':'drama'})
		self.addItem({'Title':Ecchi, 'mode':'anime_withtag','id':'ecchi'})
		self.addItem({'Title':Fantasy, 'mode':'anime_withtag','id':'fantasy'})
		self.addItem({'Title':Harem, 'mode':'anime_withtag','id':'harem'})
		self.addItem({'Title':Horror, 'mode':'anime_withtag','id':'horror'})
		self.addItem({'Title':Magic, 'mode':'anime_withtag','id':'magic'})
		self.addItem({'Title':Martial_Arts, 'mode':'anime_withtag','id':'martial_arts'})
		self.addItem({'Title':Mecha, 'mode':'anime_withtag','id':'mecha'})
		self.addItem({'Title':Military, 'mode':'anime_withtag','id':'military'})
		self.addItem({'Title':Parody, 'mode':'anime_withtag','id':'parody'})
		self.addItem({'Title':Psychological, 'mode':'anime_withtag','id':'psychological'})
		self.addItem({'Title':Romance, 'mode':'anime_withtag','id':'romance'})
		self.addItem({'Title':Science_Fiction, 'mode':'anime_withtag','id':'science_fiction'})
		self.addItem({'Title':Shoujo, 'mode':'anime_withtag','id':'shoujo'})
		self.addItem({'Title':Slice_of_Life, 'mode':'anime_withtag','id':'slice_of_life'})
		self.addItem({'Title':Space, 'mode':'anime_withtag','id':'space'})
		self.addItem({'Title':Sports, 'mode':'anime_withtag','id':'sports'})
		self.addItem({'Title':Supernatural, 'mode':'anime_withtag','id':'supernatural'})
		self.addItem({'Title':Tournament, 'mode':'anime_withtag','id':'tournament'})
		self.endofdirectory()

        def showDrama(self):                
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                All_Drama = local_string(50008)
                Recently_Added = local_string(50002)
                Simulcasts = local_string(50006)
                Most_Popular = local_string(50003)
                Browse_by_Genre = local_string(50007)
		self.addItem({'Title':All_Drama, 'mode':'drama'})
		self.addItem({'Title':Recently_Added, 'mode':'drama_updated'})
		self.addItem({'Title':Simulcasts, 'mode':'drama_simulcasts'})
		self.addItem({'Title':Most_Popular, 'mode':'drama_popular'})
                self.addItem({'Title':Browse_by_Genre, 'mode':'drama_genre'})
		self.endofdirectory()

	def dramaGenre(self):
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                Chinese = local_string(60023)
                Japanese = local_string(60024)
                Korean = local_string(60025)
                Action = local_string(60001)
                Comedy = local_string(60003)
                Crime = local_string(60026)
                Family = local_string(60027)
                Food = local_string(60028)
                Historical = local_string(60029)
                Horror = local_string(60008)
                Martial_Arts = local_string(60010)
                Romance = local_string(60015)
                Thriller = local_string(60030)
                Winter2012 = local_string(60031)
                Spring2012 = local_string(60032)
		self.addItem({'Title':Chinese, 'mode':'drama_withtag','id':'cdrama'})
		self.addItem({'Title':Japanese, 'mode':'drama_withtag','id':'jdrama'})
		self.addItem({'Title':Korean, 'mode':'drama_withtag','id':'kdrama'})
		self.addItem({'Title':Action, 'mode':'drama_withtag','id':'action'})
		self.addItem({'Title':Comedy, 'mode':'drama_withtag','id':'comedy'})
		self.addItem({'Title':Crime, 'mode':'drama_withtag','id':'crime'})
		self.addItem({'Title':Family, 'mode':'drama_withtag','id':'family'})
		self.addItem({'Title':Food, 'mode':'drama_withtag','id':'food'})
		self.addItem({'Title':Historical, 'mode':'drama_withtag','id':'historical'})
		self.addItem({'Title':Horror, 'mode':'drama_withtag','id':'horror'})
		self.addItem({'Title':Martial_Arts, 'mode':'drama_withtag','id':'martial_arts'})
		self.addItem({'Title':Romance, 'mode':'drama_withtag','id':'romance'})
		self.addItem({'Title':Thriller, 'mode':'drama_withtag','id':'thriller'})
		self.addItem({'Title':Winter2012, 'mode':'drama_seasons','id':'winter-2012'})
		self.addItem({'Title':Spring2012, 'mode':'drama_seasons','id':'spring-2012'})
		self.endofdirectory()

	def pop_genre(self):                
                local_string = xbmcaddon.Addon(id='plugin.video.crunchyroll-takeout').getLocalizedString
                Popular = local_string(50003)
                Recently_Added = local_string(50002)
                JMusic = local_string(60040)
                KPop = local_string(60041)
                Culture = local_string(60042)
                Reviews = local_string(60043)
                Fashion = local_string(60044)
                Cosplay = local_string(60045)
                Fodd = local_string(60046)
		self.addItem({'Title':Popular, 'mode':'poppop'})
		self.addItem({'Title':Recently_Added, 'id':'pop_updated'})
		self.addItem({'Title':JMusic, 'mode':'pop_withtag', 'id':'jmusic'})
		self.addItem({'Title':KPop, 'mode':'pop_withtag', 'id':'kpop'})
                self.addItem({'Title':Culture, 'mode':'pop_withtag', 'id':'culture'})
                self.addItem({'Title':Reviews, 'mode':'pop_withtag', 'id':'reviews'})
		self.addItem({'Title':Fashion, 'mode':'pop_withtag', 'id':'fashion'})
		self.addItem({'Title':Cosplay, 'mode':'pop_withtag', 'id':'cosplay'})
		self.addItem({'Title':Food, 'mode':'pop_withtag', 'id':'food'})
		self.endofdirectory()

	def series(self):
		crunchy_scraper.CrunchyScraper().getSeriesListing(self.main.args.mode, self.main.args.id)
		
	def episodes(self):
		crunchy_scraper.CrunchyScraper().getEpisodeListing(self.main.args.id)

	def queue(self):
                crunchy_scraper.CrunchyScraper().getQueue()

        def ScrappedSeries(self):
                crunchy_scraper.CrunchyScraper().getScrappedSeries(self.main.args.mode)

        def ScrappedSeriesID(self):
                crunchy_scraper.CrunchyScraper().getScrappedSeries(self.main.args.mode, self.main.args.id)
		
	def startVideo(self):
		print 
		CrunchyPlayback().startPlayback(self.main.args.id, self.main.args.page_url, self.main.args.resolutions)

class Main:

	def __init__(self, checkMode = True):
		#self.user = None
		self.parseArgs()
		if checkMode:
			self.checkMode()

	def parseArgs(self):
		# call updateArgs() with our formatted argv to create the self.args object
		if (sys.argv[2]):
			exec "self.args = updateArgs(%s')" % (sys.argv[2][1:].replace('&', "',").replace('=', "='"))
		else:
			# updateArgs will turn the 'None' into None.
			# Don't simply define it as None because unquote_plus in updateArgs will throw an exception.
			# This is a pretty ugly solution, but fuck it :(
			self.args = updateArgs(mode = 'None', url = 'None', name = 'None')

	def checkMode(self):
		mode = self.args.mode
		if mode is None:
			UI().showCategories()
		elif mode == 'episode':
			UI().startVideo()
		elif mode == 'anime':
			UI().showAnime()
		elif mode == 'genre_anime_all' or mode == 'anime_popular' or mode=='drama' or mode=='anime_withtag':
			UI().series()
		elif mode == 'anime_genre':
			UI().animeGenre()
		elif mode == 'drama_genre':
			UI().dramaGenre()
		elif mode == 'featured':
			UI().featured()
		elif mode == 'queue':
			UI().queue()
		elif mode == 'drama_popular' or mode == 'drama_simulcasts' or mode == 'anime_simulcasts' or mode == 'drama_updated' or mode == 'anime_updated' or mode =='poppop' or mode == 'pop_updated':
			UI().ScrappedSeries()
		elif mode == 'drama_withtag' or mode == 'drama_seasons' or mode == 'pop_withtag':
			UI().ScrappedSeriesID()
		elif mode == 'series':
			UI().episodes()
		elif mode == 'drama_list':
			UI().showDrama()
		elif mode == 'pop':
			UI().pop_genre()
