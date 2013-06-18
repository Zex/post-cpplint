"""
post_cpplint.py

post processor for cpplint

Author: Zex<top_zlynch@yahoo.com>
"""

import matplotlib.pyplot as mlp
from string import Template
import numpy as np
import os
#
#latestall = "latest-all"
#latestcate = "latest-category"
#
#res = []
#
#fd = file( latestall, 'r' )
#buf = fd.readlines()
#fd.close()
#
#for l in buf:
#res = l.split('\n')
#
#for l in buf:
##	print l
#	res += [l]
#
#print type(res[5])

post_cpplint = "/tmp/post-cpplint"
category_list = []
category_count_list = []
shortname = []
figure_n = 5
error_prefix = "E00" # total error type 51 currently
# default path for generating html
latest_figure = post_cpplint + "/post-cpplint.png"
latest_html = post_cpplint + "/post-cpplint.html"

def further_analysis( res, project_path, **errors_by_category ):
	global category_list
	global category_count_list
	global latest_figure
	global latest_html

	latest_figure = project_path + "/post-cpplint.png"
	latest_html = project_path + "/post-cpplint.html"

	for (k, v) in errors_by_category.items():
		category_list += [k]
		category_count_list += [v]

	if not os.path.exists( post_cpplint ):
		os.mkdir( post_cpplint )
	if not os.path.exists( project_path ):
		os.mkdir( project_path )
	
	draw_figure( category_list, category_count_list )
	gen_html( res )

def draw_figure( name, count ):
	global figure_n
	global shortname

	if not len( name ) or not len( count ): return

	step = max( count )/10

	# get fixed step
	if step <= 0:
		step = ( max(count) % 10 ) / len( count )

	# get fixed offset and width 
	ind = np.arange( len(name) ) # the x locations for the groups
	left_offset = ind + 1 
	width_s = 0.5#left_offset / 2

	if 1 == len( left_offset ):
		width_s = 10 

	fig = mlp.figure( figure_n, ( len(name), len(name) ) )
	figure_n += 1
#	fig.patch.set_facecolor( 'red' )
#	ax = fig.add_subplot( 1, 1, 1, axisbg='lightblue' )
#	ax = fig.add_subplot( 112 )
#	mlp.plot( count, 'rD' )

	# left, height, width=width, bottom=bottom, **kwargs
	plot_cat = mlp.bar( left_offset, count, width=width_s, color='r' )
	#plot_cat = mlp.bar( 0, 50, 0.25, 100, count, color='r' , orientation='horizontal' )
	
	# get shot name for displaying
	mlp.ylabel( 'Count' )
	for x in name:
#		shortname += [x.split('/')[1]]
		shortname += [ error_prefix + str(len(shortname)+1) ]

	mlp.xticks( left_offset, (shortname) )
	mlp.yticks( np.arange( 0, max( count ) + 1, step ) )
#	mlp.legend( (plot_cat[0],), ( "Category", ) )
#	mlp.set_backgroundcolor( "lightblue" ) 
#	fig.gca().set_frame_on( False )
	# save to file
	fd = file( latest_figure, 'w' )
	mlp.savefig( fd, transparent=True, bbox_inches='tight' )
	fd.close()

#	mlp.show()

def gen_html( res ):
	global category_list
	global category_count_list
	global shortname

	# head
	temp_str = \
		"<!DOCTYPE html>"\
		"<html>"\
		"<body bgcolor=\'lightgrey\'>"\
		"<h1>${name}</h1>"\
		"<li><a href=\"#Overview\">Overview</a></li>"\
		"<li><a href=\"#Bar Chart\">Bar Chart</a></li>"\
		"<li><a href=\"#Total Errors\">Total Errors</a></li>"\
		"<li><a href=\"#Details\">Details</a></li>"\
		"<h1><a id=\"Overview\">Overview</a></h1>"\
		"<h2><a id=\"Bar Chart\">Bar Chart</a></h2>"\
		"<img src=\"./post-cpplint.png\" align=\"center\"alt=\"LatestFigure\">"
#		" width=\"70%\" height=\"500\" \"align=\"right\">"
	temp_str += "<br>"

	# add total result of cpplint
	temp_str += "<h2><a id=\"Total Errors\">Total Errors</a></h2>"
	temp_str += "<table style=\"margin-right:auto;margin-left:0px\" border=\"1\""\
		"bgcolor=\'lightblue\' align=center "\
		"cellpadding=\"3\" cellspacing=\"3\">"\
		"<th>Short Name</th><th>Category</th><th>Count</th>"\
	
	for z, x, y in zip( shortname, category_list, category_count_list ):
		temp_str += "<tr>"\
		"<td><font color=\'blue\'><b>" + z + "<b></font></td>"\
		"<td><font color=\'red\'><b>" + x + "</b></font></td>"\
		"<td>" + str( y ) + "</td>"\
		"</tr>"
	
	temp_str += "<tr>"\
		"<td colspan=3><b>Total errors found: " +\
		str( sum( category_count_list ) )+\
		"</b></td>"\
		"</tr>"\
		"</table>"

	temp_str += "<br>"
	# add file paths
    	#      filename, linenum, message, category, confidence)
	temp_str += "<h1><a id=\"Details\">Details</a></h1>"\
		"<table style=\"margin-right:auto;margin-left:0px\"border=\"3\""\
		"cellpadding=\"3\" cellspacing=\"3\""\
		"bgcolor=\"0xfffff0\""\
		"align=\"center\""\
		"width=\"100%\">"\
		"<th>File</th><th>Line</th><th>Error Message</th>"\
		"<th>Category of Error</th><th>Confidence</th>"
	# detail result of cpplint	
	for item in res:
		temp_str += \
		"<tr>"\
		"<td><a href=\"file://" + str( item[0] ) + "\">" + str( item[0]) + "</a></td>"
		# the rests
		for x in item[1:]:
			temp_str += "<td>" + str( x ) + "</td>"
		"</tr>"
	temp_str += "</table>"

	temp_str += "<br>"
	
	# tail
	temp_str += \
		"</body>"\
		"</html>"

	template = Template( temp_str )
	fd = file( latest_html, 'w' )	
	fd.write( template.substitute( name='Post Processing for Cpplint' ) )
	fd.close()
