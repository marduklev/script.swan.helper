# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import urllib.parse
import sys



def decode(kname=None,source=None,property=True):
    # if xbmc.getCondVisibility( '!String.IsEmpty(Container.Folderpath) + String.Contains(Container.Folderpath,xsp)'):
    if xbmc.getCondVisibility( '!String.IsEmpty(Container.Folderpath)'):
        source = xbmc.getInfoLabel( "container.folderpath" )
        result = urllib.parse.unquote(source)
        DIALOG.textviewer('encode ','  source: %s  \n  result: %s ' % (source,result))
    else:
        xbmc.executebuiltin('notification(log ,  %s)' % source)     
    # log(loginfo)
  
def encode(kname=None,source=None,property=None):
    # source = 'Smashin"""""g Pum"§$pkins über äll>is' 
    result = urllib.parse.quote(source.encode())
    DIALOG.textviewer('encode ','  source: %s  \n  result: %s ' % (source,result))
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))   
    # log(loginfo)

def createselect(kname=None,heading=None):
    list = ['one','two']
    list.append('tres')
    DIALOG.select(heading, list)
    
    # Function: xbmcgui.Dialog().select(heading, list[, autoclose, preselect, useDetails])
    # Select dialog
    #    Show of a dialog to select of an entry as a key
    #    
    # Parameters
    #    heading	string or unicode - dialog heading.
    #    list	list of strings / xbmcgui.ListItems - list of items shown in dialog.
    #    autoclose	[opt] integer - milliseconds to autoclose dialog. (default=do not autoclose)
    #    preselect	[opt] integer - index of preselected item. (default=no preselected item)
    #    useDetails	[opt] bool - use detailed list instead of a compact list. (default=false)
    # Returns
    #    Returns the position of the highlighted item as an integer.
    
    # log(loginfo)

def checkexist(kname=None,file=None,property=True):
    # DIALOG.textviewer('checkexist ','  kname: %s  \n  file to search for : %s \n property : %s ' % (kname,file,property))
    # file =  xbmc.getInfoLabel( "listitem.path" ) + xbmc.getInfoLabel( "listitem.FolderName" ) + "-trailer" + ".mp4"
    if xbmcvfs.exists(file):
        xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,file))
    else:
        xbmc.executebuiltin('notification(log Nothing Found in,  %s)' % file)    
    
    # log(loginfo)
    

def main():
    
    if ACTION == 'checkexist':
        property = sys.argv[3].split('=')[1]
        checkexist(KNAME,KVALUE,property)
        
    elif ACTION == 'encode':
        property = sys.argv[3].split('=')[1]
        encode(KNAME,KVALUE,property)
    
    elif ACTION == 'decode':
        property = sys.argv[3].split('=')[1]
        decode(KNAME,KVALUE,property)
        
    # elif ACTION == 'createselect':
        # createselect(KNAME,KVALUE)
    
    else:
        print('error')


if __name__ == '__main__':
    
    # CONSTANTS
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    #    
    DIALOG = xbmcgui.Dialog()
    #
    ARGS = sys.argv[1:]
    # dont know about usage of n how to use quotation in args
    ACTION = sys.argv[1].split('action=')[1]
    # action.keyname - almost irrelevant codewise ? , defined method for action - by xml  file or string etc
    KNAME = sys.argv[2].split('=')[0]
    # action.keyvalue - param action.keyname e.g. string for encode, the file for lookup
    KVALUE = sys.argv[2].split('=')[1]
    
    main()