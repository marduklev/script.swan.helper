# -*- coding: utf-8 -*-
# info - https://romanvm.github.io/Kodistubs/_autosummary/xbmcplugin.html

from resources.lib.utils import log

import xbmc
import xbmcplugin
import xbmcgui

import sys
from urlparse import parse_qsl       
import json


class PluginContent:
    params = {}
    
    def __init__(self):
        self.params = dict(parse_qsl(sys.argv[2][1:]))
        self.main()

    def main(self):
        action = self.params.get("action")
        
        try:
            getattr(self, action)()
        except:
            log('PLUGIN EXCEPTION : locals = %s' % locals())
    
    def get_cast(self):
        dbtype = self.params["dbtype"]
        dbid = self.params["dbid"]
        
        if dbtype == "set":
            result = xbmc.executeJSONRPC(' {"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieSetDetails", "params": {"setid": %s}, "id": 1} ' % (dbid))
            movies_from_set = json.loads(result)["result"]["setdetails"]["movies"]
            
            movie_id_list = []
            for index in range(len(movies_from_set)):
                movie_id_list.append(movies_from_set[index]["movieid"])
            
            cast_list = []
            for index in range(0,len(movies_from_set)-1):
                dbid = movie_id_list[index]
                result = xbmc.executeJSONRPC(' {"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %s, "properties": ["cast"]}, "id": 1} ' % dbid)
                cast_l_cache = json.loads(result)["result"]["moviedetails"]["cast"][:7]
                cast_list.extend(cast_l_cache)
            
            cast_l_cache = []
            for cast_member in cast_list:
                if cast_member not in cast_l_cache:
                    cast_l_cache.append(cast_member)
            cast_list = cast_l_cache
        
        else:
            result = xbmc.executeJSONRPC(' {"jsonrpc": "2.0", "method": "VideoLibrary.Get%sDetails", "params": {"%sid": %s, "properties": ["cast"]}, "id": 1} ' % (dbtype,dbtype,dbid))
            
            if dbtype == "tvshow":
                cast_list = json.loads(result)["result"]["tvshowdetails"]["cast"]
            elif dbtype == "movie":
                cast_list = json.loads(result)["result"]["moviedetails"]["cast"]
            elif dbtype == "episode":
                cast_list = json.loads(result)["result"]["episodedetails"]["cast"]
        
        log('%s\n   cast_list %s' % (locals(),cast_list))        
        for actor in cast_list:
            list_item = xbmcgui.ListItem(label=actor.get("name"), label2=actor.get("role"), offscreen=True)
            list_item.setArt({"thumb":actor.get("thumbnail")})
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="", listitem=list_item, isFolder=False, totalItems=0)
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


    def get_alphabetbar(self):
        if xbmc.getInfoLabel('container.numitems'):
            all_letters = []
            letter_item_dict ={}
            
            for i in range(int(xbmc.getInfoLabel('container.numitems'))):
                all_letters.append(xbmc.getInfoLabel("ListItemAbsolute(%s).SortLetter" % i).upper())
                letter_item = all_letters[i]
                if letter_item not in letter_item_dict:
                    letter_item_dict[all_letters[i]] = i
            
            for key_item in list(letter_item_dict):
                listitem = xbmcgui.ListItem(label=key_item)
                offset = letter_item_dict.get("%s" % key_item)
                lipath = "plugin://script.swan.helper/?action=jumpabsolute&id=%s" % offset
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), lipath, listitem, isFolder=False)
        
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))


    def jumpabsolute(self):
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=False, listitem=xbmcgui.ListItem())
        
        absolutepos = self.params.get("id")
        # didnt found any good way to get view id, than set label in skin
        fake_view_id = xbmc.getInfoLabel('window.property(viewid)')
        
        xbmc.executebuiltin('SetFocus(%s),%s,absolute)' % (fake_view_id,absolutepos))