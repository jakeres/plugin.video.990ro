import urllib,urllib2,re,xbmc,xbmcplugin,xbmcaddon,xbmcgui,os,sys,commands,HTMLParser,jsunpack,time

website = 'http://www.990.ro/';

__version__ = "1.0.4"
__plugin__ = "990.ro" + __version__
__url__ = "www.xbmc.com"
settings = xbmcaddon.Addon( id = 'plugin.video.990ro' )

search_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'search.png' )
movies_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'movies.png' )
movies_hd_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'movies-hd.png' )
tv_series_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'tv.png' )
next_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'next.png' )

try:
   import StorageServer
except:
   import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("990ro", 24)


def ROOT():
    addDir('Filme','http://www.990.ro/toate-filmele.php?pagina=1',1,movies_thumb)
    addDir('Filme pe genuri','http://www.990.ro/toate-filmele.php?pagina=1',11,movies_thumb)
    addDir('Filme actualizate','http://www.990.ro/',2,movies_hd_thumb)
    addDir('Seriale','http://www.990.ro/seriale.php?pagina=1',5,tv_series_thumb)
    addDir('Seriale pe genuri','http://www.990.ro/seriale.php?pagina=1',51,tv_series_thumb)
    addDir('Cauta filme','http://www.990.ro/',3,search_thumb)
    
    xbmc.executebuiltin("Container.SetViewMode(500)")

def afisare_genuri(gen, url, link, linkto, dirid):
    
    if (gen == None):
      match=re.compile("<li><a href='\?afisare=.+?&amp;gen=([a-z].+?)&amp;.+?>", re.IGNORECASE).findall(link)
      for name in match:
          fgen=name
          the_link = linkto+'?pagina=1'+'&gen='+fgen
          addDir(name,the_link,dirid,movies_thumb)
      return;

    match=re.compile("&gen=(.+?)$", re.IGNORECASE).findall(url)
    if (match):
        gen=match[0]
        
    return gen;

def FILME(url, gen = None):
    link=get_url(url)
    
    gen=afisare_genuri(gen, url, link, 'http://www.990.ro/toate-filmele.php', 1)
    if (gen == None): return;
    
    match=re.compile("<a href='(filme-[0-9]+-.+?.html)'><img src='../(poze/filme/.+?)' alt='(.+?)'", re.IGNORECASE|re.MULTILINE).findall(link)
        
    for legatura, thumbnail, name in match:
        the_link = 'http://www.990.ro/'+legatura
        image = 'http://www.990.ro/'+thumbnail
        sxaddLink(name,the_link,image,name,10)
    # pagina urmatoare
    match=re.compile('pagina=([0-9]+)', re.IGNORECASE).findall(url)
    nr_pagina = match[0]
    
    if (gen == None): gen = "";

    addNext('Next','http://www.990.ro/toate-filmele.php?gen='+gen+'&pagina='+str(int(nr_pagina)+1), 1, next_thumb)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def FILME_CALITATE_BUNA(url):
    link=get_url(url)
    match = re.compile("<div style='position:relative; float:left; padding-left:5px; width:235px; border:0px solid #000; font:14px Tahoma; color:#666;'>\s+<a class='link' href='(filme-.+?)'>(.+?)</a>", re.IGNORECASE).findall(link)
    for legatura, name in match:
        #the_link = urllib.quote(url+legatura)
        the_link = url+legatura
        sxaddLink(name,the_link,'',name,10)
        #print 'legatura: '+url+legatura
    xbmc.executebuiltin("Container.SetViewMode(500)")

def CAUTA(url):
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
            sxaddLink(name,the_link,image,name,10)

    match=re.compile("<a href='(seriale-[0-9]+-.+?.html)'><li class='search'><div id='auth_img'><img class='search' width='40' height='60' src='../(.+?)'></div><div id='rest'>(.+?)<", re.IGNORECASE).findall(link)
    if len(match) > 0:
        for legatura, thumbnail, name in match:
            the_link = 'http://www.990.ro/'+legatura
            image = 'http://www.990.ro/'+thumbnail
            #sxaddLink("Serial: " + name,the_link,image,name,10)
            addDir("Serial: " + name,the_link,6,image)
            
    xbmc.executebuiltin("Container.SetViewMode(500)")
    

def SERIALE(url, gen = None):
    link=get_url(url)
    
    #print "SERIALE"
    #print url
    
    gen=afisare_genuri(gen, url, link, 'http://www.990.ro/seriale.php', 5)
    if (gen == None): return;
    
    match=re.compile('<a href=\'(seriale-[0-9]+-.+?.html)\'><img src=\'../poze/(.+?)\' alt=\'(.+?)\' title=', re.IGNORECASE).findall(link)
    for legatura,image,name  in match:
        the_link = 'http://www.990.ro/'+legatura
        image = 'http://www.990.ro/poze/'+image
        addDir(name,the_link,6,image)

    # pagina urmatoare
    match=re.compile('pagina=([0-9]+)', re.IGNORECASE).findall(url)
    nr_pagina = match[0]
    
    #print nr_pagina
    if (gen == None): gen = "";

    addNext('Next','http://www.990.ro/seriale.php?gen='+gen+'&pagina='+str(int(nr_pagina)+1), 5, next_thumb)
    xbmc.executebuiltin("Container.SetViewMode(500)")

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
        #addDir(nr+' - '+titlu,'http://www.990.ro/'+legatura,8,'')
        sxaddLink(nr+' - '+titlu,'http://www.990.ro/'+legatura,'',nr+' - '+titlu,9)

        
def SXVIDEO_EPISOD_PLAY(url):
    SXSHOWINFO("Playing episode...")
    match=re.compile("seriale2-([0-9]+-[0-9]+)-(.+?)-(online|download)", re.IGNORECASE).findall(url)
    id_episod = match[0][0]
    nume = match[0][1]

    # episode title
    try:
        link=get_url(url)
        #match=re.compile("<div align='left' style='position:relative; float:left; border:0px solid #000; width:410px; padding-left:20px; margin-top:15px; font:16px Tahoma;'>\s+(.*?)\s+</div>", re.IGNORECASE).findall(link)    
        #episode_title = match[0]
        
        match=re.compile("<meta property='og:title' content='(.+?) - S (.+?), Ep (.+?) - (.+?) online'/>", re.IGNORECASE).findall(link)
        episode_title = match[0][0] + " - s" + match[0][1] + "e" + match[0][2] + " - " + match[0][3]
    except:
        episode_title = ''

    SXSHOWINFO("Found video links for " + episode_title + "...")

    # links
    sxurls = [
      ("fu_source", 'http://www.990.ro/player-serial-'+id_episod+'-sfast.html'),
      ("xv_source", 'http://www.990.ro/player-serial-'+id_episod+'-sxvid.html')]
    SXVIDEO_GENERIC_PLAY(sxurls, episode_title)
    

def SXVIDEO_GENERIC_PLAY(sxurls, seltitle, linksource="fu_source"):
    listitem = xbmcgui.ListItem(seltitle)
    listitem.setInfo('video', {'Title': seltitle})
    
    source_link = None
    for u in sxurls:
      if u[0] == linksource:
        source_link = u[1]
        break;
        
    if linksource == "trailer":
      SXVIDEO_PLAY_THIS(source_link, listitem, None)
      
    elif linksource == "fu_source":
      # link fusource
      fu_source  = get_fu_link(source_link)
      selurl     = fu_source['url']
      SXVIDEO_PLAY_THIS(selurl, listitem, fu_source)
        
    elif linksource == "xv_source":
      # link xvidstage
      xv_source  = get_xvidstage_link(source_link)
      selurl     = xv_source['url']+'?.flv'
      SXVIDEO_PLAY_THIS(selurl, listitem, xv_source)
    
    return
      
def SXVIDEO_PLAY_THIS(selurl, listitem, source):
    player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ) 
    player.play(selurl, listitem)
    
    print source
    
    #while not player.isPlaying():
    #  time.sleep(1) 

    try:
          print "-"
          player.setSubtitles(source['subtitle'])
    except:
        pass

    #while player.isPlaying:
    #  xbmc.sleep(100);
      
    return player.isPlaying()


def SXSHOWINFO(text):
    #progress = xbmcgui.DialogProgress()
    #progress.create("kml browser", "downloading playlist...", "please wait.")
    print ""
    
def SXVIDEO_FILM_PLAY(url):
    SXSHOWINFO("Playing movie...")
    
    # thumbnail
    src = get_url(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
    match = re.compile("<div style='position:relative; float:left; border:0px solid #000;'><img src='../(.+?)'", re.IGNORECASE).findall(src)
    thumbnail = 'http://www.990.ro/'+match[0]
    
    # calitate film
    match=re.compile("<div align='center' style='position:relative; float:left; width:50px; height:30px; background-color:#999; color:#fff; font-size:20px; padding-top:3px;'><b>(.+?)</b>", re.IGNORECASE).findall(src)
    calitate_film = match[0]
    
    #aparitie film
    match=re.compile("<b>Aparitie</b>: (.\d+)", re.IGNORECASE).findall(src)
    aparitie_film = match[0]

    #gen film
    match=re.compile("<b>Gen</b>: (.+?)[\n<>]", re.IGNORECASE).findall(src)
    gen_film = match[0]

    #nota imdb
    match=re.compile("Nota IMDb: <br>\n.+?<b>(.+?)</b>/10 \((.+?) voturi\)", re.IGNORECASE).findall(src)
    nota_film = match[0]

    
        
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

    SXSHOWINFO("Found video links for " + movie_title + " ...")

    # links
    sxurls = [
      ("fu_source", 'http://www.990.ro/player-film-'+video_id+'-sfast.html'),
      ("xv_source", 'http://www.990.ro/player-film-'+video_id+'-sxvid.html')]

    ret = -1
    
    # link trailer
    if link_video_trailer != '':
        #addLink('Trailer film', link_video_trailer+'?.mp4', thumbnail, movie_title+' (trailer)')
        SXSHOWINFO("Playing trailer...")
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Select', ['Ruleaza trailer', 'Ruleaza film', 
          "----", 
          "Calitate audio/video: " + calitate_film, 
          "Aparitie: " + aparitie_film,
          "Gen: " + gen_film,
          "Nota imdb: " + str(nota_film[0]) + "; Voturi: " + str(nota_film[1])
          ])
        if (ret == 0):
          SXVIDEO_GENERIC_PLAY([("trailer", link_video_trailer+'?.mp4')], movie_title, "trailer")
      
    #print sxurls
    if (ret == 1):
      SXVIDEO_GENERIC_PLAY(sxurls, movie_title)
    

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
    match = re.compile("(http://(superweb|superweb.rol).ro/video/.+?.html)", re.IGNORECASE).findall(link)
    try:
        fu_link = match[0][0]
    except:
        return {'url': '', 'referer': ''}
    
    #print fu_link
    fu_source = get_url(fu_link)
    if fu_source == False:
        return {'url': '', 'referer': ''}
    # fastupload flv url
    match=re.compile("&flv=(.+?\.(mp4|flv))&getvar=", re.IGNORECASE).findall(fu_source)
    #print "FUL"
    #print match
    url_flv = match[0][0]
    url_ext = match[0][1]
    
    #req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

    if (url_ext == "mp4"):
      url_flv = url_flv+'|User-Agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3|referer='+fu_link
    elif (url_ext == "flv"):
      url_flv = url_flv+'?.flv|User-Agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3|referer='+fu_link
    
 
    #prepare
    fu = {}
    fu['url']       = url_flv
    fu['url_ext']   = url_ext
    fu['referer']   = fu_link 
    fu['subtitle']  = None
    
    match=re.compile("'captions.file': '(.+?)',", re.IGNORECASE).findall(fu_source)
    #print "FULSRT"
    #print match
    if match:
        url_srt = match[0]
        fu['subtitle']  = url_srt 
    
    return fu


def get_xvidstage_link(legatura):
    link = get_url(legatura)
    match = re.compile("(http://xvidstage.com/.+?)' target='_blank'", re.IGNORECASE).findall(link)
    try:
        xv_link = match[0]
    except:
        return {'title': '', 'url': ''}
    id = xv_link.split('/')[3]  
    postData = {"op":"download1","usr_login":"","id":id,"referer":"http://sh.st/w25V3","method_free":"Continue to video / Continue to Free Download"}
    data = urllib.urlencode(postData)    
    # xvidstage flv url
    result = urllib2.urlopen(xv_link, data)
    xv_source = result.read()
    result.close()
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
    xv['subtitle'] = None
    
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

def sxaddLink(name,url,iconimage,movie_name,mode=4):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": movie_name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addLink(name,url,iconimage,movie_name):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": movie_name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addNext(name,page,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(page)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        ROOT()
       
elif mode==1:
        FILME(url, "toate")

elif mode==11:
        FILME(url)
        
elif mode==2:
        FILME_CALITATE_BUNA(url)

elif mode==3:
        CAUTA(url)

elif mode==4:
        VIDEO(url,name)

elif mode==5:
        SERIALE(url, "toate")

elif mode==51:
        SERIALE(url)

elif mode==6:
        SEZON(url)

elif mode==7:
        EPISOADE(url)

elif mode==8:
        VIDEO_EPISOD(url)

elif mode==9:
        SXVIDEO_EPISOD_PLAY(url)

elif mode==10:
        SXVIDEO_FILM_PLAY(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
