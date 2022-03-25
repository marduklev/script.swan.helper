# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import urllib.parse
import sys


def decode(source=None,property='decoded_string'):
    result = urllib.parse.unquote(source)
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} is : {result} ')
  
def encode(source=None,property='encoded_string'):
    result = urllib.parse.quote(source.encode())
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))   
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2} is : {result} ')

def checkexist(file=None,property='filesearch_result'):
    if xbmcvfs.exists(file):
        xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,file))
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME2}\n param2 value: {KVALUE2}')

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
    
    log('playoffset msg')

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
    log('defaultselect_mediaitem msg')

def textviewer(header='header',txt='txt'):
    txt = txt[2:-2]
    DIALOG.textviewer(f'{header}',f'{txt}')
    
def log(logmsg):
    level = xbmc.LOGINFO
    xbmc.log(logmsg , level)
    
if __name__ == '__main__':
    
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    DIALOG = xbmcgui.Dialog()
    
    ARGS = sys.argv[1:]
    ACTION = sys.argv[1].split('action=')[1]
    
    '''
    docs.python.org locals | globals - used to call a function directly by value x as string itself is not callable
        log(f'locals: {locals()}\n globals: {globals()}')
    '''
    if len(sys.argv) > 2:
        KNAME = sys.argv[2].split('=')[0]
        KVALUE = sys.argv[2].split(f'{KNAME}=')[1][2:-2]
        
        if len(sys.argv) > 3:
            KNAME2 = sys.argv[3].split('=')[0]
            KVALUE2 = sys.argv[3].split(f'{KNAME2}=')[1]
            locals()[ACTION](KVALUE,KVALUE2)
            
        else:
            locals()[ACTION](KVALUE)
    
    else:
        locals()[ACTION]()