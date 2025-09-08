# -*- coding: utf-8 -*-

#Created by ∅
#Grabs ~4 weeks of bounty totals for each member of the Alliance 

import os
path = os.getenv('APPDATA')+'\\..\\LocalLow\\Second Dinner\\SNAP\\Standalone\\States\\nvprod\\ClanState.json'
import json

# For some reason, the first couple of character are wonky?
# If someone knows more, I'd love to learn what's up here. 
f = open(path)
text = f.read()[3:]
f.close()

data = json.loads(text)

# name -> list of point totals by week
members = {}
longestName = 0
weeks = set()

for player in data["ServerState"]['Members']:
    name = player["PlayerInfo"]["Name"]
    longestName = max(longestName, len(name))
    weekList = player["TimePeriodState"]["TimePeriodList"]
    totals = {} #week -> total
    for week in weekList:
        weeks.add(week["Key"])
        
        try:
            bounties = int(week["BountyPoints"])
        except:
            bounties = 0
            
        try:
            cubes = int(week["CubePoints"])
        except:
            cubes = 0
            
        totals[week["Key"]] = (bounties+cubes)
        
    members[name] = totals

#sort and prepare the list of weeks
weekList = list(weeks)
weekList.sort()
weekList = weekList[:-1] #skip the current, incomplete week
weeklyTotals = [0]*len(weekList)

#set up the headers
out = "Name"+ " "*(longestName-4) #line up the columns
for week in weekList:
    out += "   " + week[5:] #just month and day
out += "   Average <2k"

#and now, fill in the data
for name in members:
    pointsByWeek = members[name]
    out += "\n" + name + " "*(longestName-len(name)) # same alignment deal

    weekCount = 0
    totalPoints = 0
    below2k = 0

    for i in range(len(weekList)):
        week = weekList[i]
        # Once they've started in the alliance
        if week in pointsByWeek and (pointsByWeek[week]> 0 or weekCount > 0):
            out += "{:>8n}".format(pointsByWeek[week])

            weekCount += 1
            totalPoints += pointsByWeek[week]
            weeklyTotals[i] += pointsByWeek[week]
            if pointsByWeek[week] < 2000:
                below2k += 1

        # if they full skipped a week
        elif weekCount > 0:
            out += "{:>8n}".format(0)

            weekCount += 1
            totalPoints += 0
            below2k += 1
            
        # before they joined  
        else:
            out += " " * 8
    

    if weekCount > 0:
        out += "{:>10.2f}".format(totalPoints/weekCount)
    else:
        out += " "*10

    if below2k > 0:
        out += "{:>3n} ".format(below2k)
    else:
        out +=  " "*4

out += "\nTotal"+" "*(longestName-5)
for i in range(len(weekList)):
    out += "{:>8n}".format(weeklyTotals[i])

print(out)

input()
    


