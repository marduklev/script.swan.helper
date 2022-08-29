# -*- coding: utf-8 -*-
import xbmc

def main():
    xbmc.executebuiltin('setproperty(addon_forcedaction,back,home)')
    xbmc.executebuiltin('Action(playlist)')
    xbmc.executebuiltin('SendClick(21)')

if __name__ == '__main__':
    main()