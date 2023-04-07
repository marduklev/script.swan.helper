# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

import hashlib

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

def md5hash(value):
    value = str(value).encode()
    return hashlib.md5(value).hexdigest()

def log(logmsg):
    if ADDON.getSettingBool('debug_log') == True:
        level = xbmc.LOGINFO
        xbmc.log(f'[ {ADDON_ID} ]\n{logmsg}\n' , level)
    else:
        pass

def set_winprop(name,value,window='home'):  
    xbmc.executebuiltin(f'setproperty({name},"{value}",{window})')
    return

def clear_winprop(name,window='home'):  
    xbmc.executebuiltin(f'clearproperty({name},{window})')
    return

def notify(header='TOP',info='Bottom',time=1500,img='defaultaddonmusic.png'):  
    xbmc.executebuiltin(f'notification({header},{info},{time},{img})')
    # add/get identifyer if return is neccessary
    return
    
# maybe usefull idea?idk , but good to learn stuff
# def get_labels(values='a string, which then be split by commatas to add items to a dict'):
    
    # loop trough a list which will be string storing various labels seperated by commata and return the results as dict ??
    '''e.g.
    
    label_dictionary =	{}
    
    for len(label) in ARGS
        label_dictionary["listitem.trailer"] = xbmc.getInfoLabel('listitem.trailer')
    

    
    
    return label_dictionary
        {
         "listitem.trailer": "url",
         "listitem.filenameandpath": "url",
         "container.folderpath":: "url"
        }
    '''
    
    # xbmc.getInfoLabel('window(home).property(prop_name)')