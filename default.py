# -*- coding: utf-8 -*-
from resources.lib.utils import *

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import json
import urllib.parse
import sys

# blur
import os
from PIL import ImageFilter, Image

def blur(img_source,prop_name="blurredimg",radius=int(15)):
    
    # reminder : better outsourcing to sub function, dont need to check everytime when run 'blur' fn ?
    # ADDON_DATA_IMG_PATH = os.path.join(xbmcvfs.translatePath(f'special://profile//addon_data//{ADDON_ID}//img'))
    ADDON_DATA_IMG_PATH = xbmcvfs.translatePath(f'special://profile//addon_data/{ADDON_ID}/img')
    
    # if not os.path.exists(ADDON_DATA_IMG_PATH):
    if not xbmcvfs.exists(ADDON_DATA_IMG_PATH):
        # os.makedirs(ADDON_DATA_IMG_PATH)
        xbmcvfs.mkdir(ADDON_DATA_IMG_PATH)
    else:
        pass
    
    '''
     foldername  is bad idea, because whats when user dont use folders containing single movie,   also used foldername as radius is not handled via os.path.join(),and whats when main fanart changed - use fsize as additional identifyer ?
      - blur usecases - use identifyer an call identifyer (spotlight=hardcoded_strong, userdefined=globalbackground ~ skin.string, shutdownmenu=hardcoded_soft)  , BUT use radius string as identifyer / folderlookup - 3 folder , when change user radius, just del the one which is not hardcoded usecase and not doubled
                      - use md5 hash, as ident, will not work if artwork changed
      - blur cache    - identifyer=radius indicate cache folder
    '''
    
    '''
    radius 100 = spotlight
    radius 15 = shutdown menu = default
    radius unknow = user defined
    '''
    
    # target_fn = xbmc.getInfoLabel('listitem.foldername') + '-blurredart.png'
    target_fn = md5hash(img_source) + '.png' # result in huge cahce when fanart change, old img will be persistent
    
    target_fnp = f'{ADDON_DATA_IMG_PATH}\\{int(radius)}\\{target_fn}'
    # target_fnp = os.path.join(ADDON_DATA_IMG_PATH, target_fn)
    
    
    if not xbmcvfs.exists(target_fnp):
        xbmcvfs.copy(img_source, target_fnp)
        image = Image.open(target_fnp)
        # image.thumbnail((256, 256), Image.ANTIALIAS)                                             
        image = image.filter(ImageFilter.GaussianBlur(int(radius))).save(target_fnp)
    else:
        pass
    
    set_winprop(prop_name,target_fnp)
    
    # log(f'ACTION: {ACTION}\n  locals: {locals()}')
    log(f'ADDON_DATA_IMG_PATH = {ADDON_DATA_IMG_PATH} \n img_source = {img_source} \n prop_name = {prop_name} \n radius = {int(radius)}')
    
def get_trailer(folderpath="",play=False,plugin=False):
    f_check = []
    trailer = None
    
    if plugin == False:
        f_check = xbmcvfs.listdir(folderpath)[1]
        f_check = [s for s in f_check if "trailer" in s]
    
    if len(f_check) > 0:
        # need check for formatting issues \\
        trailer = folderpath + f_check[0]
        set_winprop('listitemtrailer',trailer)
    
    elif len(f_check) == 0 and xbmc.getCondVisibility('!string.isequal(system.internetstate,$LOCALIZE[13297])'):
        
        if xbmc.getCondVisibility('!string.isempty(listitem.trailer)'):
            trailer = xbmc.getInfoLabel('listitem.trailer')
            set_winprop('listitemtrailer',trailer)
        
        elif xbmc.getCondVisibility('skin.hassetting(trailer_yt_fallback) + system.hasaddon(plugin.video.youtube)'):
            local_language = xbmc.getInfoLabel('System.Language')
            title = xbmc.getInfoLabel('listitem.title')
            query = f"{title} {local_language} trailer"
            result = xbmc.executeJSONRPC(' {"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": { "limits": { "start" : 0, "end": 1 }, "directory": "plugin://plugin.video.youtube/kodion/search/query/?q=%s&search_type=videos", "media": "files"}, "id": 1}' % query )
            trailer = json.loads(result)["result"]["files"][0]["file"]
            set_winprop('listitemtrailer',trailer)
            
    if play == True and trailer is not None:
        set_winprop('trailer_isplaying','true')
        xbmc.executebuiltin(f'playmedia({trailer},1)')
    
    log(f'ACTION: {ACTION}\n locals: {locals()}')
 
def force_musicvideos():
    artist_id = xbmc.getInfoLabel('container().listItem.artist')
    # viewmode = xbmc.getInfoLabel('Container.Viewmode')
    exist_results = xbmc.executeJSONRPC(' {"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicvideos", "params": { "filter": {"field": "artist", "operator": "is", "value": "%s"}, "limits": { "start" : 0, "end": 1 }, "properties" : ["title"] }, "id": "libMusicVideos"} ' % artist_id).find('"total":0')
    if exist_results == int(-1):
        xbmc.executebuiltin( f"activatewindow(videos,videodb://musicvideos/titles/?xsp=%7b%22rules%22%3a%7b%22and%22%3a%5b%7b%22field%22%3a%22artist%22%2c%22operator%22%3a%22contains%22%2c%22value%22%3a%5b%22{artist_id}%22%5d%7d%5d%7d%2c%22type%22%3a%22musicvideos%22%7d,return)" )
    elif exist_results == int(77) and xbmc.getCondVisibility('System.HasAddon(plugin.video.youtube)'):
        xbmc.executebuiltin( f"activatewindow(videos,plugin://plugin.video.youtube/search/?hide_folders=true&amp;q={artist_id}%2B%0Aofficial%2B%0Amusicvideos,return)" )
        # xbmc.executebuiltin( f"Container.SetViewMode({viewmode})" )
    else:
        DIALOG.textviewer('Sorry', f'No Musicvideos by {artist_id} in your library')
    
    log(f'ACTION: {ACTION}\n  locals: {locals()}')
    
def decode(source=None,property='decoded_string'):
    result = urllib.parse.unquote(source)
    set_winprop(property,result)
    log(f'ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} \n     result is : {result} ')

def encode(source=None,property='encoded_string'):
    result = urllib.parse.quote(source.encode())
    set_winprop(property,result)
    log(f'ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} \n     result is : {result} ')

def checkexist(file=None,property='filesearch_result'):
    if xbmcvfs.exists(file):
        set_winprop(property,file)
    log(f'ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2}')

def playlist_playoffset():
    set_winprop('playlist_updating','true')
    playlistid = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    playlist = xbmc.PlayList(playlistid)   
    container_id = xbmc.getInfoLabel('system.currentcontrolid')
    current = playlist.getposition()
    selected = int(xbmc.getInfoLabel('container(%s).currentitem' % container_id)) - 1
    index = int(selected) - int(current)
    xbmc.executebuiltin(f'playlist.playoffset({index})')
    clear_winprop('playlist_updating')
    
    log(f'ACTION: {ACTION}\n  locals: {locals()}')

def select():
    playlistid = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    playlist = xbmc.PlayList(0)
    
    set_winprop('playlist_updating','true')
    
    dbid = xbmc.getInfoLabel('listItem.dbid') if xbmc.getCondVisibility('!string.isempty(listitem.dbid) + !string.isequal(listitem.dbtype,year)') else 0
    dbtype = xbmc.getInfoLabel('listItem.dbtype') if xbmc.getCondVisibility('!string.isempty(listitem.dbtype)') else None
    
    item_artist = xbmc.getInfoLabel('listitem.artist')
    item_title = xbmc.getInfoLabel('listitem.title') if dbtype == 'song' else xbmc.getInfoLabel('listItem.album')
    item_label = xbmc.getInfoLabel('listItem.label')
    item_thumb = xbmc.getInfoLabel('listItem.icon')
    
    if xbmc.getCondVisibility('!player.hasaudio'):
        playlist.clear()
    
    index = playlist.getposition() + 1
    
    if int(dbid) > 0:
        if xbmc.getCondVisibility('!player.hasaudio'):
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params": {"item": {"%sid": %s} }}' % (dbtype,dbid))
        else:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.Insert", "params": { "item": {"%sid": %s}, "playlistid": %s, "position": %s}}' % (dbtype,dbid,playlistid,index))
            if xbmc.getCondVisibility('!skin.hassetting(%s_select_queue)' % dbtype):
                xbmc.executebuiltin('playlist.playoffset(1)')
    
    if int(dbid) == 0:
        item = 'file' if xbmc.getCondVisibility('!string.isempty(listitem.filenameandpath)') else 'directory'
        url = xbmc.getInfoLabel('listitem.filenameandpath') if xbmc.getCondVisibility('!string.isempty(listitem.filenameandpath) + [!string.isequal(listitem.dbtype,year) + !string.isequal(listitem.dbtype,genre)]') else xbmc.getInfoLabel('listitem.folderpath')
        
        if xbmc.getCondVisibility('!player.hasaudio'):
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params": {"item": { "%s": "%s"}}}' % (item,url))
        else:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0",  "id": 1, "method": "Playlist.Insert", "params": { "item": { "%s": "%s"}, "playlistid": %s, "position": %s}}' % (item,url,playlistid,index))
    
    if xbmc.getCondVisibility('skin.hassetting(%s_select_queue)' % dbtype):
        if dbtype == 'song' or dbtype == 'album':
            xbmc.executebuiltin('notification(%s %s by %s,  Added to Playlist at position %s,,%s)' % (dbtype,item_title,item_artist,index,item_thumb))
        elif dbtype == 'artist':
            xbmc.executebuiltin('notification($LOCALIZE[625] %s,  Added to Playlist at position %s,,%s)' % (item_artist,index,item_thumb))
        else:
            xbmc.executebuiltin('notification($LOCALIZE[625] %s: %s,  Added to Playlist at position %s,,%s)' % (dbtype,item_label,index,item_thumb)) 
    
    clear_winprop('playlist_updating')
    log(f'ACTION: {ACTION}\n  locals: {locals()}')

def textviewer(header='header',txt='txt'):
    DIALOG.textviewer(header,txt[2:-2])
    log(f'ACTION: {ACTION} \n    heaer: {header}\n    txt : {txt}')


if __name__ == '__main__':
    
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    DIALOG = xbmcgui.Dialog()
    
    ARGS = sys.argv[1:]
    ACTION = sys.argv[1].split('action=')[1]
    
    # need simpler way to auto-handle args !!!
    if len(ARGS) > 1:
        KNAME = ARGS[1].split('=')[0]
        KVALUE1 = ARGS[1].split(f'{KNAME}=')[1][2:-2]
        
        if len(ARGS) > 2:
            KNAME2 = ARGS[2].split('=')[0]
            KVALUE2 = ARGS[2].split(f'{KNAME2}=')[1]
            
            if len(ARGS) > 3:
                KNAME3 = ARGS[3].split('=')[0]
                KVALUE3 = ARGS[3].split(f'{KNAME3}=')[1]
                
                if len(ARGS) > 4:
                    KNAME4 = ARGS[4].split('=')[0]
                    KVALUE4 = ARGS[4].split(f'{KNAME4}=')[1]
                    locals()[ACTION](KVALUE1,KVALUE2,KVALUE3,KVALUE4)
                
                else:
                    locals()[ACTION](KVALUE1,KVALUE2,KVALUE3)
            
            else:
                locals()[ACTION](KVALUE1,KVALUE2)
            
        else:
            locals()[ACTION](KVALUE1)
    
    else:
        locals()[ACTION]()