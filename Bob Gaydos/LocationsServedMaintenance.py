#
# Output keystroke strings suitable for pasting in Admin Corner's Locations Served tables to delete or add location codes.
#
# The strings output have embedded "d" characters for marking Locations Served location code entries for deletion en masse,
# and/or embedded "a" characters for adding location codes en masse.  These strings may be copied and pasted in the Locations
# Served groups in Sierra's Admin Corner to mimic the otherwise potentially voluminous keystrokes required for the maintenance
# of location code membership in the various Locations Served groups.
#
# usage: python LocationsServedMaintenance.py  [ -d range-of-position-numbers ]  [ -a list-of-location-codes ]  [ -b list-of-branch-codes ]
#
#            -d or --delete   Delete a range of location codes by numeric position
# range-of-position-numbers   Can be a compound range like 006,008,020-044,111
#                             It is the responsibility of the user to provide sufficient leading zeros in the range expression.
#               -a or --add   Add a series of location codes
#    list-of-location-codes   Can be a compound comma-separated list including ranges, LIKE expressions and/or embedded regexes
#                             as in 'sqanb,^sq[gt].*$,sqcfu-sqche,%anf'
#                             If your library uses dashes in its location codes, substitute vertical bars for dashes in ranges.
#                             Use of at least the ^ anchor or the $ anchor is mandatory for regexes.
#                             The presence of a % symbol will trigger treatment as a case-insensitive LIKE expression.
#                             The location codes are output in alphabetical order.
#            -b or --branch   Like --add, but acts upon one or more branch numbers instead of location codes.
#      list-of-branch-codes   One or more integer branch codes separated by commas.  As with --add, a series of location codes
#                             are output, those which have the supplied value(s) in sierra_view.location_myuser.branch_code_num.
#                             Ranges are permitted but no pattern matching is performed.  The typical use of this argument will
#                             be a single integer.
#
# Notes:  It is very likely that instead of Ctrl+V to paste, Admin Corner will require the Shift+Insert key combination.
#         Similarly use Ctrl+Insert to copy instead of Ctrl+C in Admin Corner, if you have the occasion to do so.
#         Your ssh client may behave differently, but this appears to be the default behavior for PuTTY.
#
#         Python coders may benefit from studying the use of the argparse module below.  Argparse helps manage command
#         line argument processing and once configured, outputs help on demand or when the usage syntax is violated.
#         Visit https://docs.python.org/3/library/argparse.html
#
#         Innovative internally refers to Locations Served as "portloca" and the internal ID of each group as the column
#         location_group_port_number in the Postgres views iii_user and agency_property_location_group.  The "portloca"
#         term appears in various places in the documentation.
#
#  author:  Bob Gaydos <bgaydos@starklibrary.org>
#    date:  May 3, 2026
#
import os
import sys
import psycopg2
import argparse
import textwrap
LOCATION_CODE = 0
FULL_LENGTH_LOCATION_CODE = 5
#
# Process args using the argparse module
#
parser = argparse.ArgumentParser(prog='LocationsServedMaintenance.py',
           description='Output strings which mimic keystrokes, suitable for pasting in Admin Corner\'s Locations Served groups '
           + 'to delete or add location codes',
           usage='python %(prog)s  [ -d range-of-position-numbers ]  [ -a list-of-location-codes ]  [ -b list-of-branch-codes ]',
           epilog=textwrap.indent('''*  range-of-position-numbers can be a compound range like 006,008,020-044,111
*  It is the responsibility of the user to provide sufficient leading zeros in the range expression
*  list-of-location-codes can be a compound comma-separated list including ranges, LIKE expressions
   and/or embedded regexes as in 'sqanb,^sq[gt].*$,sqcfu-sqche,%anf'
*  If your library uses dashes in its location codes, substitute vertical bars for dashes in ranges
*  Use of at least the ^ anchor or the $ anchor is mandatory for regexes
*  The presence of a % symbol will trigger treatment as a case-insensitive LIKE expression
*  list-of-branch-codes must be one or more integer branch codes or ranges thereof, separated by commas
*  The location codes are output in alphabetical order''', prefix='   '),
           formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-d', '--delete', type=ascii, metavar='range-of-position-numbers', help='Delete a range of location codes by numeric position')
parser.add_argument('-a', '--add', type=ascii, metavar='list-of-location-codes', help='Add a series of location codes')
parser.add_argument('-b', '--branch', type=ascii, metavar='list-of-branch-codes', help='Add a series of location codes associated with the supplied branch codes')
#
# Process arguments
#
args = parser.parse_args()
delete_range = add_locations = ''
where_clause = []
location_code_predicates = branch_code_predicates = 0
#
# Delete Location Codes from Locations Served.
# The string produced is to be pasted into a Locations Served window in Admin Corner.
#
if (args.delete != None):
	#
	# Parse the "delete" argument string of single location code positions or contiguous ranges of positions.
	#
	leading_zeros = '000'
	delete_range = args.delete[1:-1]
	#
	# Perform a dry run through the delete argument string looking for poorly-formed ranges.
	#
	for position in delete_range.split(','):
		if (position.find('-') != -1):
			begin_range = end_range = None
			for range_bound in position.split('-'):
				if (begin_range == None):
					if (not range_bound.isnumeric()):
						sys.stderr.write(sys.argv[0] + ' error:  range "' + position + '" lacks a numeric lower bound; exiting...\n')
						exit()
					else:
						begin_range = int(range_bound)
				else:
					if (not range_bound.isnumeric()):
						sys.stderr.write(sys.argv[0] + ' error:  range "' + position + '" lacks a numeric upper bound; exiting...\n')
						exit()
					else:
						end_range = int(range_bound)
	#
	# If the range expressions passed the tests, proceed
	#
	for position in delete_range.split(','):
		if (position.find('-') != -1):      # contiguous range
			begin_range = end_range = None
			for range_bound in position.split('-'):
				range_digits = len(range_bound)
				if (begin_range == None):
					begin_range = int(range_bound)
				else:
					end_range = int(range_bound)
			pos = begin_range
			while pos <= end_range:
				sys.stdout.write('d' + (leading_zeros + str(pos))[-range_digits:])
				pos += 1
		else:                               # single location code position number
			sys.stdout.write('d' + position)
	sys.stdout.write('\n')
#
# Add Location Codes to Locations Served
#
if (args.add != None):
	#
	# Parse the "add" argument string of individual location codes, ranges and/or regular expressions.
	#
	add_locations = args.add[1:-1]
	for loc_code in add_locations.split(','):
		if (loc_code[0:1] == '^' or loc_code[-1:] == '$'):   # regular expression
			where_clause.append(" OR code ~ '" + loc_code + "'")
			location_code_predicates += 1
		elif (loc_code.find('%') != -1):                     # LIKE expression
			where_clause.append(" OR code ILIKE '" + loc_code + "'")
			location_code_predicates += 1
		elif (loc_code.find('-') != -1):                     # contiguous range of location codes
			begin_range = end_range = None
			for range_bound in loc_code.split('-'):
				if (begin_range == None):
					begin_range = range_bound
				else:
					end_range = range_bound
			where_clause.append(" OR (code >= '" + begin_range + "' AND code <= '" + end_range + "')")
			location_code_predicates += 1
		elif (loc_code.find('|') != -1):   # alternate delimiter for contiguous range of location codes
			begin_range = end_range = None
			for range_bound in loc_code.split('|'):
				if (begin_range == None):
					begin_range = range_bound
				else:
					end_range = range_bound
			where_clause.append(" OR (code >= '" + begin_range + "' AND code <= '" + end_range + "')")
			location_code_predicates += 1
		else:                              # single location code
			where_clause.append(" OR code = '" + loc_code + "'")
			location_code_predicates += 1
if (args.branch != None):
	#
	# Specifying one or more branch numbers is an alternative way to generate location codeadd strings.
	# Parse the "branch" argument string of individual branch numbers or ranges of branch numbers.
	#
	branch_locations = args.branch[1:-1]
	for branch_code in branch_locations.split(','):
		if (branch_code.find('-') != -1):     # contiguous range of branch codes
			begin_range = end_range = None
			for range_bound in branch_code.split('-'):
				if (begin_range == None):
					begin_range = range_bound
				else:
					end_range = range_bound
			where_clause.append(' OR (branch_code_num >= ' + begin_range + ' AND branch_code_num <= ' + end_range + ' )')
			branch_code_predicates += 1
		elif (branch_code.find('|') != -1):   # alternate delimiter for contiguous range of branch codes
			begin_range = end_range = None
			for range_bound in branch_code.split('|'):
				if (begin_range == None):
					begin_range = range_bound
				else:
					end_range = range_bound
			where_clause.append(' OR (branch_code_num >= ' + begin_range + ' AND branch_code_num <= ' + end_range + ' )')
			branch_code_predicates += 1
		else:                                 # single branch code
			where_clause.append(' OR branch_code_num = ' + branch_code)
			branch_code_predicates += 1
if (len(where_clause) > 0):
	#
	# Build and run a dynamic SQL query.  The SierraDB module referenced below is a local module which
	# contains connection and authentication parameters for running queries on our hosted database server.
	# All Sierra-related Python programs at Stark Library use this model to separate the sensitive parameters
	# from the code itself.
	#
	basedir = os.path.abspath(os.path.dirname(__file__))
	sys.path.insert(0, basedir + '/../pymodules')
	from SierraDB import db_host, port, sierra_database, sierra_user, sierra_user_password
	sql_query = '''
		SELECT code
		FROM sierra_view.location_myuser
		WHERE False
	'''
	for predicate in where_clause:
		sql_query += predicate
	sql_query += '''
		ORDER BY code
		;
	'''
	#print(sql_query)
	conn = psycopg2.connect(host=db_host, port=port, database=sierra_database, user=sierra_user, password=sierra_user_password)
	cur = conn.cursor()
	cur.execute(sql_query)
	location_codes = cur.fetchall()
	conn.close()
	codes = location_codes.__len__()
	if (codes > 0):
		#from pprint import pprint
		#pprint(location_codes)
		pass
	else:
		if (location_code_predicates > 0 and branch_code_predicates == 0):
			sys.stderr.write('The expression "' + add_locations + '" did not match any location codes in the Sierra database.\n')
		elif (location_code_predicates == 0 and branch_code_predicates > 0):
			sys.stderr.write('The expression "' + branch_locations + '" did not match any branch codes in the Sierra database associated with location codes.\n')
		elif (location_code_predicates > 0 and branch_code_predicates > 0):
			sys.stderr.write('Neither of the expressions "' + add_locations + '" nor "' + branch_locations
              + '" matched any location/branch codes in the Sierra database.\n')
		exit()
	#
	# Output the "add" string of location codes.  This string is to be pasted into a Locations Served window in Admin Corner.
	#
	code = 0
	while code < codes:
		sys.stdout.write('a' + location_codes[code][LOCATION_CODE])
		if (len(location_codes[code][LOCATION_CODE]) < FULL_LENGTH_LOCATION_CODE):
			sys.stdout.write('\n')
		code += 1
	sys.stdout.write('\n')
exit()
