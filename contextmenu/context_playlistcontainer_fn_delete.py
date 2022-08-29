# -*- coding: utf-8 -*-
import xbmc

def main():
    xbmc.executebuiltin('setproperty(playlist_updating,true,home)')
   
    playlistid = 1 if xbmc.getCondVisibility('player.hasvideo') else 0
    playlist = xbmc.PlayList(playlistid)
    container_id = xbmc.getInfoLabel('system.currentcontrolid')
    position1 = int(xbmc.getInfoLabel('container(%s).currentitem' % container_id)) - 1
    size = int(playlist.size()) - 1
    
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Playlist.Remove", "params": { "playlistid": %s, "position": %s}}' % (playlistid,position1))
    # check for issue, refocus container based on pos
    xbmc.executebuiltin('clearproperty(playlist_updating,home)')

if __name__ == '__main__':
   main()