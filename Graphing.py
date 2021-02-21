from matplotlib import pyplot as plt
import sqlquery as query
import numpy as np
from botexception import BotException

# Class for graphing the data
class Grapher:

	# Static function, creates and saves image of select data
	def graph(args, queryThing):

		#Initialize lists of stats and locations
		locations = []
		stats = []

		# If @ is at this location, there is one stat and multiple locations. This will be a bar graph
		if args[1] == "@":
			# Add the single stat to the list of stats
			stats.append(args[0])
			#Add all locations to the list of locations
			for i in range(2, len(args)):
				locations.append(args[i])

		# If @ is anywhere else, it is assumed there is one location and multiple stats
		else:
			#  Add the stats, when you find the @, take the next element because that is your only location
			for i in range(0, len(args)):
				if args[i] == "@":
					locations.append(args[i + 1])
					break
				stats.append(args[i])

		# If there is more than one location, there has to be one stat and vice versa. This creates the bar graph.
		if len(locations) > 1 and not len(stats) > 1:

			# Some setup
			plt.rcdefaults()
			fig, ax = plt.subplots()

			# Pointless, honestly
			labels = locations

			# Initialize list of locations numbers
			locationNumbers = []

			# Add to the list of the locations numbers
			for i in range(len(locations)):
				locationNumbers.append(queryThing.requestStatAtLocation([stats[0], locations[i]]))

			# Create the bar graph
			plt.bar(locations, locationNumbers)

			# Make it look official
			plt.title(stats[0] + " per country")
			plt.xlabel("Location")
			plt.ylabel(stats[0])
			plt.xticks(rotation=45)

			# Save the image
			plt.savefig('image\\graph.png', bbox_inches='tight')

		# This creates the pie chart
		elif len(stats) > 1 and not len(locations) > 1:

			plt.title(locations[0])

			# Also pointless, just lazy
			labels = stats

			# intialize the stat numbers
			statNumbers = []

			# add to the stat numbers
			for i in range(len(stats)):
				num = queryThing.requestStatAtLocation([stats[i], locations[0]])
				statNumbers.append(num)

			# some setup
			gig1, ax1 = plt.subplots()

			# Create the pie chart
			ax1.pie(statNumbers, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)

			# Idk what this does
			ax1.axis('equal')

			ax1.set_title(locations[0])

			# Redundant
			plt.savefig('image\\graph.png', bbox_inches='tight')

		# This screams at you if you try to break it
		else:
			BotException("Invalid argments. Check spelling and make sure there is either one" + 
				"stat and multiple countries, or multiple stats and one country")