import urllib2
import re
from subprocess import call
from bs4 import BeautifulSoup

episodeName=""

def getSite(url):
	print "Getting", url
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	response = opener.open(url)
	return response.read()

def getVideositeVideo(videositeUrl):
	global episodeName
	videositePage = getSite(videositeUrl)
	domain = re.search('flashvars.domain="(.*)"', videositePage).group(1)
	fileArg = re.search('flashvars.file="(.*)"', videositePage).group(1)
	filekeyArg = re.search('flashvars.filekey="(.*)"', videositePage).group(1)
	print "Got URL args"
	resp = getSite(domain+'/api/player.api.php?user=undefined&codes=1&file='+fileArg+'&pass=undefined&key='+filekeyArg)
	respdict = {a.split('=')[0]:a.split('=')[1] for a in resp.split('&')}
	fileUrl, fileName = respdict['url'], reduce(lambda x, y: x+(y if y.isalnum() or y=='.' else ''), respdict['title'], '')+'.flv'
	fileName = episodeName+".flv"
#	if fileName == "26asdasdas.flv":
#		fileName = episodeName+".flv"
#	if fileName.endswith("26asdasdas.flv"):
#		fileName = fileName[:-14]+".flv"
	print "Got URL for video", fileName
	call(["axel","-a",fileUrl,"-o",fileName])

def getVideositeUrl(watchseriesUrl):
	watchseriesPage = getSite(watchseriesUrl)
	soup = BeautifulSoup(watchseriesPage)
	if soup.find("a", { "title" : "videoweed.es" }):
		tag = soup.find("a", { "title" : "videoweed.es" })
	else:
		tag = soup.find("a", { "class" : "buttonlink" })
	if tag==None:
		print "--------------\nNo videosite link!\n--------------"
		return None
	link1 = 'http://watchseries.lt'+tag.get('href')
	print "Got first link", link1
	watchseriesPage2 = getSite(link1)
	soup = BeautifulSoup(watchseriesPage2)
	tag = soup.find("a", { "class" : "myButton" })
	print "Got link to Videosite", tag.get('href')
	return tag.get('href')

def getVideo(watchseriesUrl):
	videositeUrl = getVideositeUrl(watchseriesUrl)
	if videositeUrl != None:
		getVideositeVideo(videositeUrl)

def getEpisode(show, season, episode):
	global episodeName
	episodeName = show.replace(" ","_").lower()+"_s"+str(season)+"_e"+str(episode)
	getVideo("http://watchseries.lt/episode/"+episodeName+".html")
