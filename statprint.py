import discord
import sqlquery as query

class StatPrint:
    def __init__(self):
        pass

    # this function takes in a query from main, and will return a string
    # relevant to the query, and its results
    def statQuery(args, queryConnection):
        returnString = ""   # String to be sent back to main
        resultTypes = []    # May be one or more stat types to return (deaths, confirmed, etc.)
        locationTuples = [] # Locations, and data to be remembered for query and printing.

        #args come in the form {stat types....} "@" {location tuples...}
        c = 0
        while (args[c] != "@" and c < len(args)):
            #record state types until @ is encountered
            resultTypes.append(args[c])
            c += 1
        c += 1  # skip over @ symbol. Its not needed
        while (c < len(args)):
            # put rest of args into location tuples.
            locationTuples.append(args[c])
            c += 1

        s = 0

        # we will make may queries to server, document the parameters here
        queryResults = []
        # group by location first, and stat types secondary.
        while (s < len(resultTypes)):
            v = 0
            while (v < len(locationTuples)):
                requests = []
                requests.append(resultTypes[s])
                requests.append(locationTuples[v])

                # Query database, and store data
                queryResults.append(queryConnection.request(requests))
                v += 1
            s += 1

        # This is how I store multiple compare queries for printing
        queryInfo = []

        j = 0
        while (j < len(locationTuples)):
            # Append a location list to query Info, creating 2d list
            queryInfo.append(locationTuples[j].split(",")) # Tuples look like (Country, State(ifapplicable), County(ifapplicable)
            j += 1

        i = 0
        j = 0
        g = 0
        while (i < len(queryInfo)):
            #for each location listed
            while (g < len(resultTypes)):
                # for each data dtype to be collected
                while (j < len(queryInfo[i])):
                    #for each location specification listed (min is 1, max is 3)_
                    if (j == 0):
                        #country
                        returnString = returnString + str(queryInfo[i][j]).upper() + " has " + str(int(queryResults[i * len(resultTypes) + g][0][0])) + " " + str(resultTypes[g]).lower().capitalize()
                    elif (j == 1):
                        #province/state
                        returnString = returnString + " in the state/province of " + str(queryInfo[i][j]).lower().capitalize()
                    elif (j == 2):
                        #county (US only)
                        returnString = returnString + " within " + str(queryInfo[i][j]).lower().capitalize() + " county"
                    j += 1
                g += 1
                j = 0
                returnString = returnString + "\n"
            i += 1
            g = 0
            
        return returnString
