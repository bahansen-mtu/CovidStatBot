import mysql.connector
from botexception import BotException

# Class for Querying the SQL server and database
class SQLQuery:


	def __init__(self, _host, _user, _password, _database, _port):

		# Connect to the SQL server	
		self.mydb = mysql.connector.connect(
			host = _host,
			user = _user,
			password = _password,
			database = _database,
			port = _port
			)

		# Create the cursor for executing commands
		self.mycursor = self.mydb.cursor()

	# Selects columns from a table and returns the contents in a tuple
	def selectColumn(self, columns, table):

		# Parse the arguments (names of the columns)
		args = columns[0]
		for m, i in enumerate(columns):
			if m == 0:
				continue
			args += ", " + i

		# Select and return contents
		self.mycursor.execute("SELECT {} FROM {}".format(args, table))
		return self.mycursor.fetchall()

	def requestStateRestrictions(self, args):
		state = args[0].replace("_", " ")
		self.mycursor.execute("SELECT Masks, Businesses, Home FROM restrictions WHERE State=\'{}\'".format(state))
		
		thing = self.mycursor.fetchall()

		return("In {}, masks are {}, businesses are {}, and the stay-at-home order status is {}".format(state.capitalize(), thing[0][0], thing[0][1], thing[0][2]))

	# Request data from a location ex.) "csb! deaths US Indiana"
	# not all arguments are needed, but you cannot have one without
	# the previous
	def requestStatAtLocation(self, args):

		# Set default arguments
		country = "%"
		province = "%"
		county = "%"

		if len(args) > 0:
			stat = args[0]
		else:
			#print("Invalid Command")
			return
		if len(args) > 1:
			country = args[1]
			country = country.replace("_", " ")

		# This splits the location into a country and a province, this makes
		# it easier if we had a city thingy
		if len(args[1].split(",")) > 1:
			country = args[1].split(",")[0]
			province = args[1].split(",")[1]
			province = province.replace("_", " ")
		if len(args[1].split(",")) > 2:
			county = args[1].split(",")[2]

		#print(country)
		if (country == "GLOBAL"):
			command = "SELECT sum({}) FROM dataset".format(stat)

		#changed from if to elif recently
		elif country == "US" or province != "%":
			command = "SELECT sum({}) FROM dataset WHERE Country_Region LIKE \'{}\' AND Province_State LIKE \'{}\' AND Admin2 LIKE \'{}\'".format(stat, country, province, county)
		else:
			command = ("SELECT IF( ( SELECT COUNT(*) FROM dataset as d WHERE Country_Region = \'{c}\' AND" + 
			" Province_State = \'\') = 1, ( SELECT {s} FROM dataset as d WHERE Country_Region = \'{c}\' AND" + 
			" Province_State = \'\' ), ( SELECT SUM({s}) FROM dataset as d WHERE Country_Region = \'{c}\' ))"+
			" as \'{s}\'").format(s=stat, c=country)
		#print(command)
		info = self.mycursor.execute(command)

		s = self.mycursor.fetchall()[0][0]
		return int(s)

	def request(self, args):
		country = "%"
		province = "%"
		county = "%"

		if len(args) > 0:
			stat = args[0]
		else:
		#	print("Invalid Command")
			return
		if len(args) > 1:
			country = args[1]
			country = country.replace("_", " ")

		# This splits the location into a country and a province, this makes
		# it easier if we had a city thingy
		if len(args[1].split(",")) > 1:
			country = args[1].split(",")[0]
			province = args[1].split(",")[1]
			province = province.replace("_", " ")
		if len(args[1].split(",")) > 2:
			county = args[1].split(",")[2]
		
		# Hard coded for specific statistics on a global scale if requested
		if (country == "GLOBAL"):
			command = "SELECT sum({}) FROM dataset".format(stat)
		
		# Different for the purpose of accuracy. If the country isnt the US and doesn't have a province
		# (triggering the else) then we exclude any terrirtories the country might have from its final
		# sum.
		elif country == "US" or province != "%":
			command = "SELECT sum({}) FROM dataset WHERE Country_Region LIKE \'{}\' AND Province_State LIKE \'{}\' AND Admin2 LIKE \'{}\'".format(stat, country, province, county)
		else:
			command = ("SELECT IF( ( SELECT COUNT(*) FROM dataset as d WHERE Country_Region = \'{c}\' AND" + 
			" Province_State = \'\') = 1, ( SELECT {s} FROM dataset as d WHERE Country_Region = \'{c}\' AND" + 
			" Province_State = \'\' ), ( SELECT SUM({s}) FROM dataset as d WHERE Country_Region = \'{c}\' ))"+
			" as \'{s}\'").format(s=stat, c=country)
		info = self.mycursor.execute(command)

		return self.mycursor.fetchall()
