import discord
import os
from dotenv import load_dotenv
import sqlquery as query
import Graphing
import statprint
from botexception import BotException
from numclass import CounterNumber
from seg4DigitDisplay import *
import threading

delay, selDigit, display_list, digitDP, arrSeg = setup()
counter = CounterNumber()
#set_counter(counter)

class ThreadThing(threading.Thread):
    def __init__():
        Thread.__init__(self)
    def run(self):
        tick(counter, delay, selDigit, display_list, digitDP, arrSeg)

#x=threading.Thread(target=tick, args=(counter, delay, selDigit, display_list, digitDP, arrSeg,))
#x.start()

# Set up the connection to the SQL by passing information about
# the server to the SQLQuery class
queryThing = query.SQLQuery(
			"classdb.it.mtu.edu",
			"bahansen",
			"password",
			"teamnoname",
			"3307")
#'''

# Loads the .env file that resides on the same level as the script.
load_dotenv()

# Create the bot
bot = discord.Client()


# Log the bot login
@bot.event
async def on_ready():
	print("We have logged in as {0.user}".format(bot))

# Listen for commands
@bot.event
async def on_message(message):

	# Ignore its own messages
	if message.author == bot.user:
		return

	# Handle commands
	#if message.content.startswith("csb!"):
	if message.content.startswith(str(f'<@!{bot.user.id}>')):
        
		counter.count += 1
		#tick(counter, delay, selDigit, display_list, digitDP, arrSeg)
		command = message.content.upper()

		#'''
		args = command.split(" ")
		args.remove(args[0])
		print("Command Recieved: " + message.content)

		if args[0] == "RESTRICTIONS":
			args.remove(args[0])
			try:
				thing = queryThing.requestStateRestrictions(args)
				await message.channel.send(thing)
			except:
				await message.channel.send("Unable to process request, check syntax and spelling")
			return
		# Generate a graph
		if args[0] == "GRAPH":
			args.remove(args[0])
			# please remind me to change this shit
			try:
				Graphing.Grapher.graph(args, queryThing)
			except:
				await message.channel.send("Unable to process request, check values")
				return
			print("Graph Generated, sending image")
			await message.channel.send(file=discord.File("image\\graph.png"))
		if args[0] == "GET":
			args.remove(args[0])
			try:
				thing = statprint.StatPrint.statQuery(args, queryThing)
				await message.channel.send(thing)
			except:
				await message.channel.send("Invalid Command, check syntax or spelling or try ```@CovidStatBot help```")
			return

		if args[0] == "HELP":

			await message.channel.send(
				"```" +
				"COMMANDS:\n" +
				"graph\tGraphs statistics for one country on a pie char, or a statistic for multiple countries on a bar graph.\n" +
				"EXAMPLE 1: @CovidStatBot graph STATS_SEPARATED_BY_SPACE @ COUNTRY\n" +
				"EXAMPLE 2: @CovidStatBot graph STAT @ LIST_OF_COUNTRY,PROVINCE_SEPARATED_BY_SPACE\n\n" +

				"get\tGet a specific statistic from a region\n" +
				"EXAMPLE: @CovidStatBot get STAT COUNTRY,PROVINCE\n\n" +

				"help\tDisplays this message\n\n" +

				"source\tDisplays source attribution\n\n" +

				"NOTE: Province and Country Arguments are Optional\n" +




				"```"
				)

		if args[0] == "SOURCE":
			await message.channel.send(

				"```" +
				"DataSet used with permission from COVID-19 Data Repository by the " +
				"Center for Systems Science and Engineering (CSSE) at Johns Hopkins University\n\n" +
				"Can be found at https://github.com/CSSEGISandData/COVID-19" +
                		"State Guidelines and Restrictions arweb scraped from the following New York Times list that is updated regularly\n\n" +
                		"Can be found at https://www.nytimes.com/interactive/2020/us/states-reopen-map-coronavirus.html"
				"```"

				)

			return

		#'''
		return

@bot.event
async def tickDisplay():
	tick(counter, delay, selDigit, display_list, digitDP, arrSeg)

bot.loop.create_task(tickDisplay())

token = "ODEyNTEwMjU5NjcxMzM0OTQy.YDBzJQ.RD4-gmel96o79zddu3ZVuE0kq8g"

# Run the bot
bot.run(token)
#'''
