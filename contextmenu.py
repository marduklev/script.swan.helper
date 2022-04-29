# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

import sys

def playlistitem_fn():
    container_id = xbmc.getInfoLabel('system.currentcontrolid')
    position1 = int(xbmc.getInfoLabel('container(%s).currentitem' % container_id)) - 1
    size = int(PLAYLIST.size()) - 1
    
    xbmc.executebuiltin('setproperty(playlist_updating,true,home)')
    
    if METHOD == 'minus':
        if position1 == 0:
            position2 = size
        else:
            position2 = int(xbmc.getInfoLabel('container(%s).currentitem' % container_id)) -2
    
    elif METHOD == 'plus':
        if position1 == size:
            position2 = 0
        else:
            position2 = xbmc.getInfoLabel('container(%s).currentitem' % container_id)
    
    if METHOD == 'minus' or METHOD == 'plus':
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Swap", "params": { "playlistid": %s, "position1": %s, "position2": %s }, "id": 1}' % (PLAYLIST_ID,position1,position2))
        playlist_regainfocus(container_id,position2)
        
    if METHOD == 'delete':
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.Remove", "params": { "playlistid": %s, "position": %s}}' % (PLAYLIST_ID,position1))
        playlist_regainfocus(container_id,position1)

def playlist_regainfocus(container_id,index):
    xbmc.sleep(100)
    xbmc.executebuiltin('clearproperty(playlist_updating,home)')
    xbmc.executebuiltin(f'alarmclock(delayedfocus,setfocus({container_id},{index}),00:00,silent)')

def execute(): 
    # context_actions.py
    if METHOD == 'playmedia_dir':
        if xbmc.getCondVisibility('!string.isequal(listitem.dbtype,artist)'):
            url = xbmc.getInfoLabel('listitem.folderpath')
            xbmc.executebuiltin('playmedia(%s,isdir,1)' % url)
        
        elif xbmc.getCondVisibility('string.isequal(listitem.dbtype,artist)'):
            artistid = xbmc.getInfoLabel('listitem.dbid')
            xbmc.executebuiltin('playmedia(musicdb://artists/%s/-1/-2/?albumartistonly=false&amp;artistid=%s,isdir,1)' % (artistid,artistid))
    
    if METHOD == 'open_playlist':
        xbmc.executebuiltin('action(playlist)')
    
    if METHOD == 'save_playlist':
        xbmc.executebuiltin('setproperty(addon_forcedaction,back,home)')
   
        xbmc.executebuiltin('Action(playlist)')
        xbmc.executebuiltin('SendClick(21)')
    
    if METHOD == 'open_playercontrol':
        xbmc.executebuiltin('activatewindow(playercontrols)')

def playlist_queuing():
    dbid = xbmc.getInfoLabel('listItem.dbid') if xbmc.getCondVisibility('!string.isempty(listitem.dbid)') else 0
    dbtype = xbmc.getInfoLabel('listItem.dbtype') if xbmc.getCondVisibility('!string.isempty(listitem.dbtype)') else None
    
    item_artist = xbmc.getInfoLabel('listitem.artist')
    item_title = xbmc.getInfoLabel('listitem.title') if dbtype == 'song' else xbmc.getInfoLabel('listItem.album')
    item_label = xbmc.getInfoLabel('listItem.label')
    item_thumb = xbmc.getInfoLabel('listItem.icon')
    
    xbmc.executebuiltin('setproperty(playlist_updating,true,home)')
    
    if xbmc.getCondVisibility('!player.hasaudio'):
        PLAYLIST.clear()
    
    index = PLAYLIST.size() + 1 if METHOD == 'add' else PLAYLIST.getposition() + 1
    
    if int(dbid) > 0:
        json_result_addtolist = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.Insert", "params": { "item": { "%sid": %s}, "playlistid": %s, "position": %s}}' % (dbtype,dbid,PLAYLIST_ID,index))
    elif int(dbid) == 0:
        item = 'file' if xbmc.getCondVisibility('!string.isempty(listitem.filenameandpath)') else 'directory'
        url = xbmc.getInfoLabel('listitem.filenameandpath') if xbmc.getCondVisibility('!string.isempty(listitem.filenameandpath) + [!string.isequal(listitem.dbtype,year) + !string.isequal(listitem.dbtype,genre)]') else xbmc.getInfoLabel('listitem.folderpath')
        xbmc.executeJSONRPC('{"jsonrpc": "2.0",  "id": 1, "method": "Playlist.Insert", "params": { "item": { "%s": "%s"}, "playlistid": %s, "position": %s}}' % (item,url,PLAYLIST_ID,index))
    
    if dbtype == 'song' or dbtype == 'album':
        xbmc.executebuiltin('notification(%s %s by %s,  Added to Playlist at position %s,,%s)' % (dbtype,item_title,item_artist,index,item_thumb))
    elif dbtype == 'artist':
        xbmc.executebuiltin('notification($LOCALIZE[625] %s,  Added to Playlist at position %s,,%s)' % (item_artist,index,item_thumb))
    else:
        xbmc.executebuiltin('notification($LOCALIZE[625] %s: %s,  Added to Playlist at position %s,,%s)' % (dbtype,item_label,index,item_thumb))    
    
    if xbmc.getCondVisibility('!player.hasaudio'):
        xbmc.Player().play(PLAYLIST)
    
    xbmc.executebuiltin('clearproperty(playlist_updating,home)')

def main():
    if ACTION == 'queue':
        playlist_queuing()

    if ACTION == 'execute':
        execute()
    
    if ACTION == 'playlistitem_fn':
        playlistitem_fn()

if __name__ == '__main__':
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    
    PLAYLIST_ID = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    PLAYLIST = xbmc.PlayList(PLAYLIST_ID)
    
    # xml syn used args="queue,method=add" , COMMA gets ignored n result in 1 arg contain comma
    ACTION = sys.argv[1].split(',method=')[0]
    METHOD = sys.argv[1].split(',method=')[1]
    
    main()