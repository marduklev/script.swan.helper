# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import urllib.parse
import sys

def force_musicvideos():
    # this will not work when advancedsettings - set jsonrpc to compactoutput false
    # may addon/skinsettigs  setting enable youtube fallback
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
    
def decode(source=None,property='decoded_string'):
    result = urllib.parse.unquote(source)
    xbmc.executebuiltin(f"SetProperty({property},{result},home)")
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} \n     result is : {result} ')

def encode(source=None,property='encoded_string'):
    result = urllib.parse.quote(source.encode())
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} \n     result is : {result} ')

def checkexist(file=None,property='filesearch_result'):
    if xbmcvfs.exists(file):
        xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,file))
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2}')

def playlist_playoffset():
    xbmc.executebuiltin('setproperty(playlist_updating,true,home)')
    playlistid = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    playlist = xbmc.PlayList(playlistid)   
    container_id = xbmc.getInfoLabel('system.currentcontrolid')
    current = playlist.getposition()
    selected = int(xbmc.getInfoLabel('container(%s).currentitem' % container_id)) - 1
    index = int(selected) - int(current)
    xbmc.executebuiltin('playlist.playoffset(%s)' % (index))
    xbmc.executebuiltin('clearproperty(playlist_updating,home)')
    
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION}')

def select():
    playlistid = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    playlist = xbmc.PlayList(0)
    
    xbmc.executebuiltin('setproperty(playlist_updating,true,home)')
    
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
    
    xbmc.executebuiltin('clearproperty(playlist_updating,home)')
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION}')

def textviewer(header='header',txt='txt'):
    txt = txt[2:-2]
    DIALOG.textviewer(header,txt)
    # log(f'[ {ADDON_ID} ]\n ACTION: {ACTION} \n    heaer: {header}\n    txt : {txt}')

def log(logmsg):
    level = xbmc.LOGINFO
    xbmc.log(f'\n{logmsg}\n' , level)

if __name__ == '__main__':
    
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
    DIALOG = xbmcgui.Dialog()
    
    ARGS = sys.argv[1:]
    ACTION = sys.argv[1].split('action=')[1]
    '''
        docs.python.org locals | globals - used to call a function directly
        log(f' Addon : {ADDON_ID} \n     locals: {locals()}\n     globals: {globals()}')
    '''
    if len(ARGS) > 1:
        KNAME = ARGS[1].split('=')[0]
        KVALUE = ARGS[1].split(f'{KNAME}=')[1][2:-2]
        
        if len(ARGS) > 2:
            KNAME2 = ARGS[2].split('=')[0]
            KVALUE2 = ARGS[2].split(f'{KNAME2}=')[1]
            locals()[ACTION](KVALUE,KVALUE2)
            
        else:
            locals()[ACTION](KVALUE)
    
    else:
        locals()[ACTION]()