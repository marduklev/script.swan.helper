# script.swan.helper
 - provide some functions for kodi xml skins
 NOTE:  i am still learning py and cross xbmc usecases

#### skin
 - usage 
 RunScript(script.swan.helper,action=*action definition,*parameter1 KEY*='*parameter1 VALUE*',*parameter2 KEY=*parameter2 VALUE)
 | action              | param1<br>key1=value1                                                 | param2<br>key2=value2                                                                                      | example                                                                                                                                                                                                                                                                                     | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|---------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| checkexist          | [required]<br>file='"a file-, or directory- path"'                    | [optional]<br>property=*choose name for your property*                                                     | RunScript(script.swan.helper,action=checkexist,file='"$VAR[extrasLocation_lookup]"',property=propertyname)<br><br><br><br>RunScript(script.swan.helper,action=checkexist,file='"$VAR[extrasLocation_lookup]"')                                                                              | check for existence of a specific file or folder<br><br><br>when lookup succeed:<br><br>!String.IsEmpty(Window(home).Property(propertyname))<br>will be True<br><br>or<br><br>when propertyname is ommitted<br>!String.IsEmpty(Window(home).Property(filesearch_result))<br>will be True                                                                                                                                                                                                                                             |
| get_trailer         | [required]<br>fp='*an filepath to check for a local trailer*'         | [optional]<br>play=True<br><br>or<br><br>play=Skin.HasSetting(*whatever_when true it'll play the trailer*) | RunScript(script.swan.helper,action=get_trailer,fp='$ESCINFO[container.listitem.path]')<br><br>optional you can perform a windowed playback, when use <br>play=True as parameter :<br><br>RunScript(script.swan.helper,action=get_trailer,fp='$ESCINFO[container.listitem.path],play=True') | first lookup if local trailer exist<br><br>if not check for listitem.trailer,<br>if listitem trailer empty than perform a youtube* lookup<br><br>in any case,if a video is found it store its url as<br>'window(home).property(listitemtrailer)' infolabel<br><br>* youtube lookup will just performed if <br>Skin.HasSetting(trailer_yt_fallback)<br>is True                                                                                                                                                                        |
| force_musicvideos   |                                                                       |                                                                                                            | RunScript(script.swan.helper,action=force_musicvideos)                                                                                                                                                                                                                                      | navigates in videos window<br>and list musicvideos of an artist ( using 'container().listItem.artist' )<br>for the lookup<br><br>if no musicvideos found in the local db it will lookup via youtube plugin  use <br>' container().listItem.artist' official musicvideos'<br>as the query                                                                                                                                                                                                                                             |
| encode              | [required]<br>string='"Büllebü & Bülleba, or other String to encode"' | [optional]<br>property=*choose name for your property*                                                     | RunScript(script.swan.helper,action=encode,string='"$VAR[EncodeTitle]"',property=videoinfo_encoded_title)<br><br><br><br><br><br><br><br>RunScript(script.swan.helper,action=encode,string='"$VAR[EncodeTitle]"')                                                                           | encode a string given by an param <br>to an percent encoded string<br><br>which can then be used <br>via:<br>$INFO[window(home).Property(paramvalue2)]<br><br>or if param 2 is omitted<br>the result can be returned via<br>$INFO[window(home).Property(encoded_string)]                                                                                                                                                                                                                                                             |
| playlist_playoffset |                                                                       |                                                                                                            | RunScript(script.swan.helper,action=playlist_playoffset)                                                                                                                                                                                                                                    | used to play specific item when current container is filled by either<br>playlistmusic:// or playlistvideo://<br><br>will need skin integration<br>as container refresh (without reload.skin() or activate playlistwindow )is a bit cumbersome<br><br>use<br>string.isempty(window(home).property(playlist_updating))" to evalute show playlistmusic://<br>to true                                                                                                                                                                   |
| select              |                                                                       |                                                                                                            | RunScript(script.swan.helper,action=select)                                                                                                                                                                                                                                                 | will play specific item or folder, without clearing the current playlist<br><br>default = add item or folder to playlist and start play immediatly<br><br>if<br>skin.hassetting([dbtype]_select_queue)<br><br>it will just queue the [dbtype]item to next position in playlist<br><br>skinsetting possibilitys:<br>Skin.ToggleSetting(song_select_queue)<br>Skin.ToggleSetting(album_select_queue)<br>Skin.ToggleSetting(genre_select_queue)<br>Skin.ToggleSetting(year_select_queue)<br>Skin.ToggleSetting(musicvideo_select_queue) |
| textviewer          | [required]<br>header='"I will be The Header"'                         | [required]<br>text='"i am the text below the header, you know"'                                            | RunScript(script.swan.helper,action=textviewer,header='"$VAR[ArtistOrTitle]"',text='"$VAR[plot]"')<br><br><br>RunScript(script.swan.helper,action=textviewer,header='$ESCINFO[ListItem.Title]',text='$ESCINFO[ListItem.Plot]"')                                                             | opens the textviewer dialog                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

 
#### contextmenu
 - queue the current focused item to either last or next playlistposition	- if not in a media window for custom dynamic content containers
 - move playlistitems up/down or remove playlistitem from playlist - when use a dynamic container filled with currently playing playlist (playlistmusic:// ; playlistvideo://)																			

    to	indicate if a container is used for playlist content you'll need to set a property (playlist_itemcontrol) in the skin
				so the contextitem for switch playlist items : is just visible if 

	>   string.isequal(window(home).property(playlist_itemcontrol),enable)

    example

					<control type="panel" id="12345">
					    <description>dynamic container provide playlistcontent</description>
						<onfocus>SetProperty(playlist_itemcontrol,enable,home)</onfocus>
						<onunfocus>ClearProperty(playlist_itemcontrol,home)</onunfocus>
						.. 
						<content>$VAR[playlistmusic]</content>
					</control>
					
					<variable name="playlistmusic">
						<value condition="string.isempty(window(home).property(playlist))">playlistmusic://</value>
						<value>-</value>
					</variable>
    >    the custom container for playlist wont refresh properly till window reload or open playlistwindow, therefore using a variable to toggle between visible states to force a proper refresh n your skin
    >    
    >   the script set a window property  ''setproperty(playlist,update,home)'' when do queue,delete or switch functions, which can then be used to refresh the container content by using a variable
				
			
 - save currently active playlist : just activates window and send click to control 21 (save button) and set a window property  ''setproperty(addon_forcedaction,back,home)'' 

    > if you dont wanna move back manually just add following onunload commands to 'dialogkeyboard.xml'
	
	    <onunload condition="String.IsEqual(Window(home).Property(addon_forcedaction),back)">Action(back)</onunload>
		<onunload condition="!String.IsEmpty(Window(home).Property(addon_forcedaction))">ClearProperty(addon_forcedaction,home)</onunload>
			

- activate playlist window
- activate the playercontrols dialog
- play all songs by artis
  >    if either media window and on '. all albums' listitem entry,
       or
       if not media window for artist or album items (clears playlist, and start plaing folder)

						 


TO DO:
- hide items based upon addon setting
- playlist save code - look at docs
- get better diff of current playlist by getting an identifyer - look at docs/jsonrpc get.playlistidentifyer?
  ( currently just checks if a video is playing, no matter which playlist id is active (its absolutely possible to have video files within a active music playlist, even if rare case))
