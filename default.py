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
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME3}\n param2 value: {KVALUE3} is : {result} ')
  
def encode(source=None,property='encoded_string'):
    result = urllib.parse.quote(source.encode())
    xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,result))   
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME3}\n param2 value: {KVALUE3} is : {result} ')

def checkexist(file=None,property='filesearch_result'):
    if xbmcvfs.exists(file):
        xbmc.executebuiltin("SetProperty(%s,%s,home)" % (property,file))
    log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n Param1: {KNAME}\n Param1 value: {KVALUE}\n param2: {KNAME3}\n param2 value: {KVALUE3}')
    

def main():
    if ACTION == 'checkexist':
        checkexist(KVALUE,KVALUE3)
        
    elif ACTION == 'encode':
        encode(KVALUE,KVALUE3)
    
    elif ACTION == 'decode':
        decode(KVALUE,KVALUE3)
        
    elif ACTION == 'textviewer':
        DIALOG.textviewer(KVALUE, KVALUE3[2:-2])
    
    else:
        log(f'Addon: {ADDON_ID}\n ACTION: {ACTION}\n KNAME: {KNAME}\n KVALUE: {KVALUE}\n KNAME3: {KNAME3}\n KVALUE3: {KVALUE3}')

def log(logmsg):
    # level = xbmc.LOGDEBUG
    level = True
    xbmc.log(logmsg , level)
    
if __name__ == '__main__':
    
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    DIALOG = xbmcgui.Dialog()
    
    ARGS = sys.argv[1:]
    ACTION = sys.argv[1].split('action=')[1]
    # action.keyname - almost irrelevant codewise, just easier to set up script calls
    KNAME = sys.argv[2].split('=')[0]
    # action.keyvalue - always escaping strings for arg2
    KVALUE = sys.argv[2].split(f'{KNAME}=')[1][2:-2]
    
    if sys.argv[3]:
        KNAME3 = sys.argv[3].split('=')[0]
        KVALUE3 = sys.argv[3].split(f'{KNAME3}=')[1]
    
    main()