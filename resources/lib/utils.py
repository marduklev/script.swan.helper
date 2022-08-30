# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

def log(logmsg):
    if ADDON.getSettingBool('debug_log') == True:
        level = xbmc.LOGNOTICE
        xbmc.log('[ %s ]  \n%s\n' % (ADDON_ID,logmsg), level)
    else:
        pass