//------------------------------------------
// Invision Power Board v2.1
// Boards JS File
// (c) 2005 Invision Power Services, Inc.
//
// http://www.invisionboard.com
//------------------------------------------



/*--------------------------------------------*/
// Send request to update marker
// NO LONGER USED
/*--------------------------------------------*/

function boards_send_marker_update( fid, is_subforum )
{
	//----------------------------------
	// Get current image...
	//----------------------------------
	
	try
	{
		var imgsrc = document.getElementById( 'f-'+fid ).innerHTML;
	
		if ( imgsrc )
		{
			//----------------------------------
			// Find out what img its using...
			//----------------------------------
			
			var regex  = new RegExp( "src=['\"](.*/)("+regex_markers+")['\"]" );
			
			var results = imgsrc.match( regex );
			
			//----------------------------------
			// Got a replacement?
			//----------------------------------
			
			if ( img_markers[ results[2] ] )
			{
				imgsrc = imgsrc.replace( regex, "src='$1"+img_markers[ results[2] ]+"'" );
				
				document.getElementById( 'f-'+fid ).innerHTML = imgsrc;
			}
		}
	}
	catch(e){}
		
	//----------------------------------
	// Get new xhttp obj
	//----------------------------------
	
	xmlobj = new xmlrequest();
	
	/*--------------------------------------------*/
	// Main function to do on request
	// Must be defined first!!
	/*--------------------------------------------*/
	
	xmlrequest.do_request_functon = function()
	{
		//----------------------------------
		// Do nothing
		//----------------------------------
	}
	
	//----------------------------------
	// LOAD XML
	//----------------------------------
	
	xmlrequest.load_xml_document( ipb_var_base_url + 'act=xmlout&do=mark-forum&fid='+fid+'&sf='+is_subforum );
	
	if ( ! xmlrequest.allow_use )
	{
		window.location = document.getElementById( 'f-'+fid ).url;
	}
	
	return false;
}