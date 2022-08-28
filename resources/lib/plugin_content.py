# -*- coding: utf-8 -*-
# info - https://romanvm.github.io/Kodistubs/_autosummary/xbmcplugin.html

from resources.lib.utils import log

import xbmc
import xbmcplugin
import xbmcgui

import sys
import urllib.parse
import json


class PluginContent:
    params = {}
    
    def __init__(self):
        self.params = dict(urllib.parse.parse_qsl(sys.argv[2].replace('?', '').lower()))
        self.main()

    def main(self):
        action = self.params.get("action")
        
        try:
            getattr(self, action)()
        except:
            log(f'PLUGIN EXCEPTION : locals = [{locals()}')
    
    def get_cast(self):
        dbtype = self.params["dbtype"]
        dbid = self.params["dbid"]
        
        # later auto detect
        # dbtype = xbmc.getInfoLabel('container().listitem.dbtype')
        # dbid = xbmc.getInfoLabel('container().listitem.dbid')
        
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
                cast_l_cache = json.loads(result)["result"]["moviedetails"]["cast"][:5]
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
        
        log(f'{locals()}\n   cast_list {cast_list}')        
        # process listing with the results ,  maybe need look here too https://github.com/xbmc/xbmc/pull/19459#issuecomment-806450382
        for actor in cast_list:
            list_item = xbmcgui.ListItem(label=actor.get("name"), label2=actor.get("role"), offscreen=True)
            list_item.setArt({"thumb":actor.get("thumbnail")})
            
            cast_list_names = [(actor.get("name"))]
            list_item.setArt({"thumb":actor.get("thumbnail")})
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url="", listitem=list_item, isFolder=True)
                
        # finish it
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
