import urllib,urllib2,re,xbmc,xbmcplugin,xbmcaddon,xbmcgui,os,sys,commands,HTMLParser,jsunpack

website = 'http://www.990.ro/';

__version__ = "1.0.3"
__plugin__ = "990.ro" + __version__
__url__ = "www.xbmc.com"
settings = xbmcaddon.Addon( id = 'plugin.video.990ro' )

search_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'search.png' )
movies_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'movies.png' )
movies_hd_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'movies-hd.png' )
tv_series_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'tv.png' )
next_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'next.png' )

def ROOT():
    addDir('Filme','http://www.990.ro/toate-filmele-pagina-1.html',1,movies_thumb)
    addDir('Filme actualizate','http://www.990.ro/',2,movies_hd_thumb)
    addDir('Seriale','http://www.990.ro/',5,tv_series_thumb)
    addDir('Cauta filme','http://www.990.ro/',3,search_thumb)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def FILME(url):
    link=get_url(url)
    match=re.compile("<a href='(filme-[0-9]+-.+?.html)'><img src='../(poze/filme/.+?)' alt='(.+?)'", re.IGNORECASE).findall(link)
    for legatura, thumbnail, name in match:
        the_link = 'http://www.990.ro/'+legatura
        image = 'http://www.990.ro/'+thumbnail
        addDir(name,the_link,4,image)
    # pagina urmatoare
    match=re.compile('toate-filmele-pagina-([0-9]+).html', re.IGNORECASE).findall(url)
    nr_pagina = match[0]
    addNext('Next','http://www.990.ro/toate-filmele-pagina-'+str(int(nr_pagina)+1)+'.html', 1, next_thumb)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def FILME_CALITATE_BUNA(url):
    link=get_url(url)
    match = re.compile("<div style='position:relative; float:left; padding-left:5px; width:235px; border:0px solid #000; font:14px Tahoma; color:#666;'>\s+<a class='link' href='(filme-.+?)'>(.+?)</a>", re.IGNORECASE).findall(link)
    for legatura, name in match:
        #the_link = urllib.quote(url+legatura)
        the_link = url+legatura
        addDir(name,the_link,4,'')
        print 'legatura: '+url+legatura
    xbmc.executebuiltin("Container.SetViewMode(500)")

def CAUTA(url):
    print 'Cauta'
    keyboard = xbmc.Keyboard( '' )
    keyboard.doModal()
    if ( keyboard.isConfirmed() == False ):
        return
    search_string = keyboard.getText()
    if len( search_string ) == 0:
        return
    
    link = get_search(search_string)

    match=re.compile("<a href='(filme-[0-9]+-.+?.html)'><li class='search'><div id='auth_img'><img class='search' width='40' height='60' src='../(.+?)'></div><div id='rest'>(.+?)<", re.IGNORECASE).findall(link)
    if len(match) > 0:
        for legatura, thumbnail, name in match:
            the_link = 'http://www.990.ro/'+legatura
            image = 'http://www.990.ro/'+thumbnail
            addDir(name,the_link,4,image)
    xbmc.executebuiltin("Container.SetViewMode(500)")
    

def SERIALE(url):
    link=get_url(url)
    match=re.compile('<div class=\'ss\'><a.*? href="(seriale-[0-9]+-.+?.html)" title="(.+?)">.+?</a></div>', re.IGNORECASE).findall(link)
    for legatura,name in match:
        the_link = url+legatura
        addDir(name,the_link,6,'')

def SEZON(url):
    link=get_url(url)
    match=re.compile("<img src='images/seriale-sezoane/sez([0-9]+).gif' alt='(.+?)'>", re.IGNORECASE).findall(link)
    for nr, sezon in match:
        addDir(sezon,url+'?sezon='+nr,7,'')

def EPISOADE(url):
    link=get_url(url)
    match=re.compile("sezon=([0-9]+)", re.IGNORECASE).findall(url)
    sezon = '0'+match[0] if int(match[0]) < 10 else match[0]

    pattern = "<div style='position:relative; float:left; margin-left:100px; border:0px solid #000; width:180px; font:15px Tahoma;'>Sezonul "+sezon+", (Episodul .+?)</div>"
    pattern += "\s+<div style='position:relative; float:left; border:0px solid #000; width:20px; height:18px; font:15px Tahoma; margin-top:2px;'></div>"
    pattern += "\s+<div style='position:relative; float:left; border:0px solid #000; width:20px; height:18px; font:15px Tahoma; margin-top:2px;'></div>"
    pattern += "\s+<div style='position:relative; float:left; margin-left:10px; border:0px solid #000; width:295px;'>"
    pattern += "<a href='(seriale2-[0-9]+-[0-9]+-.+?.html)' class='link'>(.*?)</a>"

    match=re.compile(pattern, re.IGNORECASE).findall(link)
    for nr, legatura, titlu in match:
        addDir(nr+' - '+titlu,'http://www.990.ro/'+legatura,8,'')

def VIDEO_EPISOD(url):
    match=re.compile("seriale2-([0-9]+-[0-9]+)-(.+?)-(online|download)", re.IGNORECASE).findall(url)
    id_episod = match[0][0]
    nume = match[0][1]

    # episode title
    link=get_url(url)
    match=re.compile("<div align='left' style='position:relative; float:left; border:0px solid #000; width:420px; padding-left:20px; margin-top:30px; font:16px Tahoma;'>\s+(.*?)\s+</div>", re.IGNORECASE).findall(link)    
    episode_title = match[0]

    # link fu
    #legatura = 'http://www.990.ro/player-serial-'+id_episod+'-'+nume+'-sfast.html'
    legatura = 'http://www.990.ro/player-serial-'+id_episod+'-sfast.html'
    # fu source
    fu_source = get_fu_link(legatura)
    addLink('Server FastUpload', fu_source['url']+'?.flv|referer='+fu_source['referer'], '', episode_title)

    '''
    # link xvidstage
    legatura = 'http://www.990.ro/player-serial-'+id_episod+'-sxvid.html'
    # xvidstage source - if it is alive
    xv_source = get_xvidstage_link(legatura)
    if xv_source['url'] != '' :
        addLink('Server Xvidstage', xv_source['url']+'?.flv', '', episode_title)
    '''

def VIDEO(url, name):
    #print 'url video '+url
    #print 'nume video '+name
    # thumbnail
    src = get_url(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
    match = re.compile("<div style='position:relative; float:left; border:0px solid #000;'><img src='../(.+?)'", re.IGNORECASE).findall(src)
    thumbnail = 'http://www.990.ro/'+match[0]
    # calitate film
    match=re.compile("<div align='center' style='position:relative; float:left; width:50px; height:30px; background-color:#999; color:#fff; font-size:20px; padding-top:3px;'><b>(.+?)</b>", re.IGNORECASE).findall(src)
    calitate_film = match[0]
    #link trailer
    try:
        match=re.compile("<iframe width='595' height='335' src='.+?/embed/(.+?)' frameborder='0'>", re.IGNORECASE).findall(src)
        link_youtube = 'http://www.youtube.com/watch?v='+match[0]
        link_video_trailer = youtube_video_link(link_youtube)
    except:
        link_video_trailer = ''
    # video id
    match=re.compile('990.ro/filme-([0-9]+)-.+?.html', re.IGNORECASE).findall(url)
    video_id = match[0]

    # movie title
    match=re.compile("<div align='left' style='position:relative; float:left; border:0px solid #000; width:420px; padding-left:10px; margin-top:5px; font:24px Tahoma; font-weight:bold;'>\s+(.*?)\s+</div>", re.IGNORECASE).findall(src)
    movie_title = match[0]

    # fu source
    source_link = 'http://www.990.ro/player-film-'+video_id+'-sfast.html'
    fu_source = get_fu_link(source_link)
    if fu_source['url'] != '':
        addLink('Server FastUpload (calitate video: nota '+calitate_film+')', fu_source['url']+'?.flv|referer='+fu_source['referer'], thumbnail, movie_title)

    '''
    # xvidstage source
    source_link = 'http://www.990.ro/player-film-'+video_id+'-sxvid.html'
    xv_source = get_xvidstage_link(source_link)
    if xv_source['url'] != '' :
        addLink('Server Xvidstage (calitate video: nota '+calitate_film+')', xv_source['url']+'?.flv', thumbnail, xv_source['title'])
    '''

    # link trailer
    if link_video_trailer != '':
        addLink('Trailer film', link_video_trailer+'?.mp4', thumbnail, movie_title+' (trailer)')
    

def get_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except:
        return False

def get_fu_link(legatura):
    link = get_url(legatura)
    match = re.compile("(http://fastupload.ro/.+?.html)' target='_blank'", re.IGNORECASE).findall(link)
    fu_link = match[0]
    fu_source = get_url(fu_link)
    if fu_source == False:
        return {'title': '', 'url': ''}
    # fastupload flv url
    match=re.compile("'file': '(.+?).flv',", re.IGNORECASE).findall(fu_source)
    url_flv = match[0] + '.flv'
    #prepare
    fu = {}
    fu['url']     = url_flv
    fu['referer'] = fu_link 
    return fu

def get_xvidstage_link(legatura):
    link = get_url(legatura)
    match = re.compile("(http://xvidstage.com/.+?)' target='_blank'", re.IGNORECASE).findall(link)
    if match[0] == False:
        return {'title': '', 'url': ''}
    xv_link = match[0]
    # xvidstage flv url
    xv_source = get_url(xv_link)
    if xv_source == False:
        return {'title': '', 'url': ''}
    match=re.compile("src='http://xvidstage.com/player/swfobject.js'></script>.+?<script type=\'text/javascript\'>(.*?)</script>", re.DOTALL + re.IGNORECASE).findall(xv_source)
    if(match):
        sJavascript = match[0]
        string = jsunpack.unpack(sJavascript)
        string = string.replace("\\", "")
        match = re.compile("'file','(.+?)'", re.DOTALL + re.IGNORECASE).findall(string)
        xvidstage_flv = match[0]
    else:
        xvidstage_flv = ''
    #prepare
    xv = {}
    xv['url'] = xvidstage_flv
    return xv

def get_search(keyword):
    url = 'http://www.990.ro/functions/search3/live_search_using_jquery_ajax/search.php'
    params = {'kw': keyword}
    req = urllib2.Request(url, urllib.urlencode(params))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Content-type', 'application/x-www-form-urlencoded')
    try:
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except:
        return False

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def yt_get_all_url_maps_name(url):
    conn = urllib2.urlopen(url)
    encoding = conn.headers.getparam('charset')
    content = conn.read().decode(encoding)
    s = re.findall(r'"url_encoded_fmt_stream_map": "([^"]+)"', content)
    if s:
        s = s[0].split(',')
        s = [a.replace('\\u0026', '&') for a in s]
        s = [urllib2.parse_keqv_list(a.split('&')) for a in s]

    n = re.findall(r'<title>(.+) - YouTube</title>', content)
    return  (s or [], 
            HTMLParser.HTMLParser().unescape(n[0]))

def yt_get_url(z):
    #return urllib.unquote(z['url'] + '&signature=%s' % z['sig'])
    return urllib.unquote(z['url'])

def youtube_video_link(url):
    # 18 - mp4
    fmt = '18'
    s, n = yt_get_all_url_maps_name(url)
    for z in s:
        if z['itag'] == fmt:
            if 'mp4' in z['type']:
                ext = '.mp4'
            elif 'flv' in z['type']:
                ext = '.flv'
            found = True
            link = yt_get_url(z)
    return link


def addLink(name,url,iconimage,movie_name):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": movie_name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addNext(name,page,mode,iconimage):
    u=sys.argv[0]+"?url="+str(page)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        ROOT()
       
elif mode==1:
        print ""+url
        FILME(url)
        
elif mode==2:
        print ""+url
        FILME_CALITATE_BUNA(url)

elif mode==3:
        print ""+url
        CAUTA(url)

elif mode==4:
        print ""+url+" si nume "+name
        VIDEO(url,name)

elif mode==5:
        print ""+url
        SERIALE(url)

elif mode==6:
        print ""+url
        SEZON(url)

elif mode==7:
        print ""+url
        EPISOADE(url)

elif mode==8:
        print ""+url
        VIDEO_EPISOD(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
                       
