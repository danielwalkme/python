import os
import sys, getopt

# This scirpt was written by Daniel Chechik 21/10/2013
# This script export a given database, search a string and replace it, afterwards uploads it again back to the database 
# make sure to have python and execute this script from the folder of mysql if you don't have it your default path
# Follow me on Twitter @daniel chechik

def main(argv):

	table =""
	database =""
	username =""
	password =""
	search_string =""
	replace_string =""

	if (len(argv) == 0):
		print "Add -h for help"
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "hs:r:u:p:d:t", ["search=", "replace=", "user=", "password=", "database=", "table="])
	except getopt.GetoptError:
		print "searchindb.py -s <search text> -r <replace text> -u <database user> -p <database password> -d <database name> -t <table name>"
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == '-h':
			usage()
		elif opt in ("-s", "--search"):
			search_string = arg
		elif opt in ("-r", "--replace"):
			replace_string = arg
		elif opt in ("-u", "--user"):
			username = arg
		elif opt in ("-p", "--password"):
			password = arg
		elif opt in ("-d", "--database"):
			database = arg
		elif opt in ("-t", "--table"):
			table = arg

	if (username == "" or password == "" or database == "" or search_string == "" or replace_string == ""):
		usage()
		
	# Download database content
	os.system("mysqldump -u %s -p%s %s %s > tmp.sql" % (username, password, database, table))
	
	# load database
	file = open('tmp.sql', 'r')
	data = file.read()
	
	# replace content
	data = data.replace(search_string,replace_string)
	file.close()
	
	# save database to file
	file = open('tmp_new.sql', 'w')
	file.write(data)
	file.close()
	
	# Upload the new database
	os.system("mysql -u %s -p%s %s %s < tmp_new.sql" % (username, password, database, table))
	
def usage():
	print 'Welcome to Search and Replace in Database'
	print 'You should enter the following arguments'
	print '-s [--search] search a text in database/table'
	print '-r [--replace] replace this text search a text in database/table'
	print '-u [--user] user name of the database'
	print '-p [--password] password of the database'
	print '-d [--database] name of the database\n'
	print 'Optional: '
	print '-t [--table] name of the table'
	sys.exit()
	
if __name__ == "__main__":
   main(sys.argv[1:])