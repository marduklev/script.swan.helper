# script.swan.helper
 script.swan.helper - i am just learning py and cross xbmc usecases
 
 usage 
 RunScript(script.swan.helper,action=*action definition,*parameter1 KEY*='*parameter1 VALUE*',*parameter2 KEY=*parameter2 VALUE)
 
	action_definition				parameter1_key		parameter1_value						parameter2_key												parameter2_value
														(	ALWAYS AN ESCAPED STRING..	)		
													
		checkexist					file			   										 	 property													optional : wished name for property, default: filesearch_result
			
			RunScript(script.swan.helper,action=checkexist,file='"$INFO[listitem.path]$INFO[listitem.FolderName,,-trailer.mp4]"',property=trailer_avail)
		
			Set a window(home)property, when given folder or file found.
			Has to be cleared in skin.
		
		
		
		
		encode						string													 	 property													optional : wished name for property, default: filesearch_result
			RunScript(script.swan.helper,action=encode,string='"$INFO[ListItem.Label]"',property=encoded_string)
			
			Set a window(home)property, returning the encoded string ,which then can be used. like '$INFO[window(home).property(*parameter2_value*)]' 
			Has to be cleared in skin.
		
		
		
		
		decode						string													 	 property													optional : wished name for property, default: filesearch_result
			RunScript(script.swan.helper,action=decode,string='"$INFO[Container.Folderpath]"',property=decoded_string)
			
			Set a window(home)property, returning the decoded string
			Has to be cleared in skin.
			
		
		
		textviewer					header			escaped string representing the text 		 text														required : escaped string representing the text which shold be shown
														which shold be used as header	 	 	 
														
			RunScript(script.swan.helper,action=textviewer,header='"$INFO[ListItem.Label]"',text='$ESCINFO[ListItem.Plot]')
			RunScript(script.swan.helper,action=textviewer,header='$ESCINFO[ListItem.Label]',text='$ESCINFO[ListItem.Plot] , something else [CR] &quot; $COMMA end of text dont forget closing via quotation mark"')
			
			Open Textviewer Dialog with the wished labels.
 
################################################
###  Onclick Actions playlist  ###
################################################

- addon provides 2 functions which can be used as onclick actions (it can be any file or directory)
- and provides several contexmenu items (see below)




	1. override onclick actions 
		
		use 'RunScript(script.playlist.helper,action=select)'
		
		• by default = add the selected mediatype to playlist as next item and play it immediatly
		
		• if a skin provides settings like 'skin.hassetting(<media type>_select_queue)' is true - it just queues the selected item as next item to be played in playlist
		
			e.g. 
				skin.hassetting(album_select_queue) - add as next title, playback after current title ends
				!skin.hassetting(song_select_queue) - add as next title and play it immediatly
		
	2. - for skins, which use a dynamic container filled with currently playing playlist (playlistmusic:// ; playlistvideo://)
		you can play the selected media item from that list, without 'clear/destroy' the current playlist
		
		<onclick>RunScript(script.playlist.helper,action=playlist_playoffset)</onclick>
		

					- example for a playlist container
	
					<control type="panel" id="12345">
						<include>playlist_container_atts</include>
						...
							< the other skinning stuff >
						...
						<content>$VAR[playlistmusic]</content>
					</control>
					
					<include name="playlist_container_atts">
						<onfocus>SetProperty(playlist_itemcontrol,enable,home)</onfocus>
						<onunfocus>ClearProperty(playlist_itemcontrol,home)</onunfocus>
						<onclick>RunScript(script.playlist.helper,action=playlist_playoffset)</onclick>
					</include>
					<variable name="playlistmusic">
						<value condition="string.isempty(window(home).property(playlist))">playlistmusic://</value>
						<value>-</value>
					</variable>
	
################################################
###  Context Menu Items and Functions  ###
################################################

- queue item to last playlistposition	- if not media window
- queue item to next playlistposition 	- if not media window
	
	NOTE
			- using touch device ; GOT ISSUES GETTING INFOLABELS (dbid,dbtype) - FAILS IN CUSTOM WINDOW, BUT NOT IF RUN IT IN Media WINDOW, which is strange
			- use via keyboard/remote all is fine
			
- for skins, which use a dynamic container filled with currently playing playlist (playlistmusic:// ; playlistvideo://)																					
	- switch playlistitems (move up/down)
	- delete playlistitem
	
	INFO for Skinners
			
			- switch playlist position (+/- 1) the only way for indicate if a container is used for playlist content is via set property in the skin
				so the contextitem for switch playlist items : is just visible if 'string.isequal(window(home).property(playlist_itemcontrol),enable)'
					simple add 
					
					<control type="panel" id="12345">
						<onfocus>SetProperty(playlist_itemcontrol,enable,home)</onfocus>
						<onunfocus>ClearProperty(playlist_itemcontrol,home)</onunfocus>
						.. 
					</control>
					
					for the container goup 
						
			- playlist container refresh - when add items to list
				the custom container for playlist wont refresh properly till window reload, therefore using a variable to "switch" between visible state
				
				the script set a window property  ''setproperty(playlist,update,home)'' at start and clears it at end of a playlist script when use (queue,delete,switch) functions
					
					<variable name="playlistmusic">
						<value condition="string.isempty(window(home).property(playlist))">playlistmusic://</value>
						<value>-</value>
					</variable>
			
			
			- the playlist save function just activates window and send click to control 21 (save button)
		      and set a window property  ''setproperty(addon_forcedaction,back,home)'' 
			  
			  if you dont wanna move back manually just add following onunload commands to 'dialogkeyboard.xml'
			  
					  <onunload condition="String.IsEqual(Window(home).Property(addon_forcedaction),back)">Action(back)</onunload>
					  <onunload condition="!String.IsEmpty(Window(home).Property(addon_forcedaction))">ClearProperty(addon_forcedaction,home)</onunload>
			
				
				
- activate playlist window - if playlist filled
- activate playercontrols dialog

- save currently active playlist - if playlist filled					TODO: change , check possibility in docs  

- play next song 	 				- if playlist has next item			TODO: add setting for disable
- play previous song 				- if playlist has previous item		TODO: add setting for disable
- play all songs by artist 												TODO: add setting for disable
		if either media window and on '. all albums' listitem entry,
		or if not media window for artist or album items (clears playlist, and start plaing folder)

						 
TO DO:
- hide items based upon addon setting
- playlist save code - look at docs
- get better diff of current playlist by getting an identifyer - look at docs/jsonrpc get.playlistidentifyer?
  ( currently just checks if a video is playing, no matter which playlist id is active (its absolutely possible to have video files within a active music playlist, even if rare case))
