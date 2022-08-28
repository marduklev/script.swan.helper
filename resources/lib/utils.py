# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

def log(logmsg):
    if ADDON.getSettingBool('debug_log') == True:
        level = xbmc.LOGINFO
        xbmc.log(f'[ {ADDON_ID} ]\n {logmsg}\n' , level)
    else:
        pass