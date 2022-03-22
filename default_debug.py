# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import urllib.parse
import sys


def decode(source=None,property='decoded_string'):
    result = urllib.parse.unquote(source)
    DIALOG.textviewer('encode ','  source: %s  \n  result: %s ' % (source,result))
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))
    # log(loginfo)
  
def encode(source=None,property='encoded_string'):
    # source = 'Smashin"""""g Pum"§$pkins über äll>is' 
    result = urllib.parse.quote(source.encode())
    DIALOG.textviewer('encode ','  source: %s  \n  result: %s ' % (source,result))
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))   
    # log(loginfo)

def checkexist(file=None,property='filesearch_result'):
    if xbmcvfs.exists(file):
        xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,file))
    else:
        xbmc.executebuiltin('notification(log Nothing Found in,  %s)' % file)    
    # log(loginfo)
    

def main():
    if ACTION == 'checkexist':
        checkexist(KVALUE,KNAMEVALUE3)
        
    elif ACTION == 'encode':
        encode(KVALUE,KNAMEVALUE3)
    
    elif ACTION == 'decode':
        decode(KVALUE,KNAMEVALUE3)
        
    elif ACTION == 'textviewer':
        DIALOG.textviewer(f'{KVALUE}', f'{KNAMEVALUE3[2:-2]}')
    
    else:
        log()

def log():
    DIALOG.textviewer('test ',' ACTION:\n%s\n\n KNAME:\n%s\n\n KVALUE:\n%s\n\n KNAME3:\n%s\n\n KNAMEVALUE3:\n%s\n\n' % (ACTION,KNAME,KVALUE,KNAME3,KNAMEVALUE3))
    
if __name__ == '__main__':
    
    # CONSTANTS
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    DIALOG = xbmcgui.Dialog()
    #
    ARGS = sys.argv[1:]
    ACTION = sys.argv[1].split('action=')[1]
    # action.keyname - almost irrelevant codewise, just easier to set up script calls
    KNAME = sys.argv[2].split('=')[0]
    # action.keyvalue - always escaping strings for arg2
    KVALUE = sys.argv[2].split(f'{KNAME}=')[1][2:-2]
    
    if sys.argv[3]:
        KNAME3 = sys.argv[3].split('=')[0]
        # KNAMEVALUE3 = sys.argv[3].split('=')[1][2:-2]
        KNAMEVALUE3 = sys.argv[3].split(f'{KNAME3}=')[1]
    
    main()