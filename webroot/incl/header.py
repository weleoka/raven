"""
HTML header generation functions.
"""


def get_header():
    """
    Generate an HTML5 header.

    parameters:
		Void

    return:
        html: list. All the header in one list item.
    """
    return ['''Content-type:text/html\n\n
    <!doctype html>
    <html lang="en">
    
    <!-- Header -->
    <head>
      <meta charset="utf-8">
    	<title> DipDap Library Handler </title>
    	
    	<!-- links to external stylesheets -->	
    	<link rel="stylesheet" href="style/stylesheet.css" title="General stylesheet">
    	
    	<!-- favicon -->
    	<link rel="shortcut icon" href="/favicon.png">
    </head>
    <body> 
    ''']