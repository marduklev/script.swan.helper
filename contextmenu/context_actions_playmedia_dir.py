# -*- coding: utf-8 -*-
import xbmc

def main():
    if xbmc.getCondVisibility('!string.isequal(listitem.dbtype,artist)'):
        url = xbmc.getInfoLabel('listitem.folderpath')
        xbmc.executebuiltin('playmedia(%s,isdir,1)' % url)
    
    elif xbmc.getCondVisibility('string.isequal(listitem.dbtype,artist)'):
        artistid = xbmc.getInfoLabel('listitem.dbid')
        xbmc.executebuiltin('playmedia(musicdb://artists/%s/-1/-2/?albumartistonly=false&amp;artistid=%s,isdir,1)' % (artistid,artistid))

if __name__ == '__main__':
    main()