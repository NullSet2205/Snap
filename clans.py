# -*- coding: utf-8 -*-

#Created by ∅
#Grabs ~4 weeks of bounty totals for each member of the Alliance 

import os
path = os.getenv('APPDATA')+'\\..\\LocalLow\\Second Dinner\\SNAP\\Standalone\\States\\nvprod\\ClanState.json'
print(path)
import json

# For some reason, the first line is wonky?
# I assume it's some sort of header, but I don't know how to parse it. 
# If someone knows more, I'd love to learn what's up here. 
f = open(path)
lines = f.readlines()
text = "{"
for line in lines[1:]:
    text += line
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

longestName = min(longestName, 16)

#sort and prepare the list of weeks
weekList = list(weeks)
weekList.sort()
weekList = weekList[:-1] #skip the current, incomplete week
weeklyTotals = [0]*len(weekList)

# Currently all squished to fit into a single Discord message
columnWidth = 7

#set up the headers
out = "Name"+ " "*(longestName-4) #line up the columns
for week in weekList:
    out += " "*(columnWidth-5) + week[5:] #just month and day
out += " Average <"

numFormat = "{:>"+str(columnWidth)+"n}"
decimalFormat = "{:>"+str(columnWidth+1)+".1f}"
#and now, fill in the data
for name in members:
    pointsByWeek = members[name]
    
    out += "\n" + name[:longestName] #cap to fit in one Discord message
    out += " "*(longestName-len(name)) # same alignment deal

    weekCount = 0
    totalPoints = 0
    below2k = 0

    for i in range(len(weekList)):
        week = weekList[i]
        # Once they've started in the alliance
        if week in pointsByWeek and (pointsByWeek[week]> 0 or weekCount > 0):
            out += numFormat.format(pointsByWeek[week])

            weekCount += 1
            totalPoints += pointsByWeek[week]
            weeklyTotals[i] += pointsByWeek[week]
            if pointsByWeek[week] < 2000:
                below2k += 1

        # if they full skipped a week
        elif weekCount > 0:
            out += numFormat.format(0)

            weekCount += 1
            totalPoints += 0
            below2k += 1
            
        # before they joined  
        else:
            out += " " * columnWidth
    

    if weekCount > 0:
        out += decimalFormat.format(totalPoints/weekCount)

        if below2k > 0:
            out += "{:>2n} ".format(below2k)

out += "\nTotal"+" "*(longestName-5)
for i in range(len(weekList)):
    out += numFormat.format(weeklyTotals[i])

print(out)

input()
    


