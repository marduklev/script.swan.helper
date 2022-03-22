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
 
