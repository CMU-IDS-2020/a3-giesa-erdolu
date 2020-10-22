import string
import copy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TreebankWordTokenizer
import re
import pandas as pd
import streamlit as st
import altair as alt

##################################################################
## Text processing and extracting data: Part 1 
##################################################################

f = open("Debate_Data_Final.txt", encoding="utf8") 
raw = f.read()

actor1 = "Mod_Wallace"
actor2 = "VP_Biden"
actor3 = "P_Trump"

## List of words with no punctuation but with stamps
tokenizer = nltk.RegexpTokenizer(r"\w+")
wordsNoPunct = tokenizer.tokenize(raw)
# print(wordsNoPunct, len(wordsNoPunct))
# print("BREAK")

## List of words with punctuation and stamps
wordsWithPunct = TreebankWordTokenizer().tokenize(raw)
#print(wordsWithPunct, len(wordsWithPunct))
#print("BREAK")


## Function that gives List of words with no punctuation and no stamps
def removeStamps(raw):
    rawSplit = raw.split()
    
    for word in rawSplit:
        matched1 = re.match(r"\((\d{2}:\d{2})\)", word)
        matched2 = re.match(r"\((\d{2}:\d{2}:\d{2})\)", word)
        matched3 = re.match(r"\[crosstalk", word)
        is_match1 = bool(matched1)
        is_match2 = bool(matched2)
        is_match3 = bool(matched3)
        if is_match1 == True or is_match2 == True or is_match3 == True: 
            rawSplit.remove(word)
    
    for word in rawSplit:
        matched4 = re.match(r"\d{2}:\d{2}:\d{2}\]", word)
        is_match4 = bool(matched4)
        if is_match4 == True:
            rawSplit.remove(word)

    rawJoined = " ".join(rawSplit)
    wordsNoPunctNoStamp = tokenizer.tokenize(rawJoined)
    
    return wordsNoPunctNoStamp  #, len(wordsNoPunctNoStamp)


## Function that creates an actorInfo dictionary and adds actors' names
## --- { index: [actorName]
def addActors(words): ## wordsNoPunctNoStamp
    actorInfo = {}
    index = -1

    for i in range(len(words) - 1):
        if words[i] == actor1:
            index += 1
            actorInfoList = []
            actorInfoList.append(actor1)
            actorInfo[index] = actorInfoList
        elif words[i] == actor2:
            index += 1
            actorInfoList = []
            actorInfoList.append(actor2)
            actorInfo[index] = actorInfoList
        elif words[i] == actor3:
            index += 1
            actorInfoList = []
            actorInfoList.append(actor3)
            actorInfo[index] = actorInfoList
    
    return actorInfo


## Function that adds timeStamps to the dictionary 
## --- { index: [actorName, timeStamps]
def addTimeStamps(raw, dic): ## actorInfo
    rawSplit = raw.split()
    index = -1

    for word in rawSplit:
        matched1 = re.match(r"\((\d{2}:\d{2})\)", word)
        matched2 = re.match(r"\((\d{2}:\d{2}:\d{2})\)", word)
        is_match1 = bool(matched1)
        is_match2 = bool(matched2)
        if is_match1 == True or is_match2 == True:
            index += 1
            timeStampNoParenth = word.replace("(", "").replace(")", "")
            dic[index].append(timeStampNoParenth)
    
    return dic


## Function that adds numWords to the dictionary 
## --- { index: [actorName, timeStamps, numWords]
def addNumWordsByActor(words, dic):
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False
    
    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True

        ## Counting words in actors' phrases and add numWords in the dictionary
        if actor1_On == True and word != actor1:
            countActor1 += 1
            if len(dic[index]) == 2:
                dic[index].append(countActor1)
            elif len(dic[index]) == 3: 
                dic[index][2] = countActor1     
        elif actor2_On == True and word != actor2:
            countActor2 += 1
            if len(dic[index]) == 2:
                dic[index].append(countActor2)
            elif len(dic[index]) == 3: 
                dic[index][2] = countActor2 
        elif actor3_On == True:
            if word != actor3:
                countActor3 += 1
            if len(dic[index]) == 2:
                    dic[index].append(countActor3)
            if len(dic[index]) == 3: 
                dic[index][2] = countActor3

    return dic


## Function that adds numInterruptions to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions] }
def addNumInterruptionsByActor(words, dic): 
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0

    for i in range(len(words) - 1):
        ## Capturing actors' name in the corpus, incrementing the index, adding the interruption count
        if words[i] == actor1:
            index += 1
            if len(dic[index]) == 3:
                dic[index].append(countActor1)
            elif len(dic[index]) == 4: 
                dic[index][3] = countActor1
        
        elif words[i] == actor2:
            index += 1
            if len(dic[index]) == 3: 
                dic[index].append(countActor2)
            elif len(dic[index]) == 4: 
                dic[index][3] = countActor2
        
        elif words[i] == actor3:
            index += 1
            if len(dic[index]) == 3: 
                dic[index].append(countActor3)
            elif len(dic[index]) == 4: 
                dic[index][3] = countActor3
        
        ## If there is interruption (at the end of the sentence)
        elif words[i] == "-" or words[i][-1] == "-":
            ## Finding the following actorName (the interrupter)
            if words[i + 1] == actor1:
                countActor1 += 1
                dic[index + 1].append(countActor1)
            elif words[i + 1] == actor2:
                countActor2 += 1
                dic[index + 1].append(countActor2)
            elif words[i + 1] == actor3:
                countActor3 += 1
                dic[index + 1].append(countActor3)

    return dic


## Function that adds numCrossTalks to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks] }
def addNumCrossTalksByActor(raw, dic):
    rawSplit = raw.split()
    index = -1
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in rawSplit:
        ## Capturing actors' name in the corpus, incrementing the index
        if word == actor1 + ":":
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 4:
                dic[index].append(countActor1)
        elif word == actor2 + ":":
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 4:
                dic[index].append(countActor2)
        elif word == actor3 + ":":
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 4:
                dic[index].append(countActor3)
        
        ## Finding the following crossTalk instance:
        matched = re.match(r"\[crosstalk", word)
        is_match = bool(matched)
        if is_match == True and actor1_On == True:
            countActor1 += 1
            dic[index][4] = countActor1
        elif is_match == True and actor2_On == True:
            countActor2 += 1
            dic[index][4] = countActor2
        elif is_match == True and actor3_On == True:
            countActor3 += 1
            dic[index][4] = countActor3

    return dic


## Function that adds numNumberUse to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse] }
def addNumNumberUseByActor(words, dic):
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 5:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 5:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 5:
                dic[index].append(countActor3)
        
        elif actor1_On == True and word.isnumeric() == True:
            countActor1 += 1
            dic[index][5] = countActor1
        
        elif actor2_On == True and word.isnumeric() == True:
            countActor2 += 1
            dic[index][5] = countActor2
        
        elif actor3_On == True and word.isnumeric() == True:
            countActor3 += 1
            dic[index][5] = countActor3
        
    return dic


## Function that adds numOfHealthcare words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare] }
def numOfHealthcare(words, dic):
    healthCareList = ["Obamacare", "Affordable Care", "insurance", "cost"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 6:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 6:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 6:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == healthCareList[0] or word == healthCareList[1] or \
                word == healthCareList[2] or word == healthCareList[3]:
                countActor1 += 1
                dic[index][6] = countActor1
        
        elif actor2_On == True:
            if word == healthCareList[0] or word == healthCareList[1] or \
                word == healthCareList[2] or word == healthCareList[3]:
                countActor2 += 1
                dic[index][6] = countActor2
        
        elif actor3_On == True:
            if word == healthCareList[0] or word == healthCareList[1] or \
                word == healthCareList[2] or word == healthCareList[3]:
                countActor3 += 1
                dic[index][6] = countActor3

    return dic


## Function that adds numOfCovid words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare, numOfCovid] }
def numOfCovid(words, dic):
    covidList = ["covid", "vaccine", "mask", "death", "dying"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 7:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 7:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 7:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == covidList[0] or word == covidList[1] or \
                word == covidList[2] or word == covidList[3] or \
                    word == covidList[4]:
                countActor1 += 1
                dic[index][7] = countActor1
        
        elif actor2_On == True:
            if word == covidList[0] or word == covidList[1] or \
                word == covidList[2] or word == covidList[3] or \
                    word == covidList[4]:
                countActor2 += 1
                dic[index][7] = countActor2
        
        elif actor3_On == True:
            if word == covidList[0] or word == covidList[1] or \
                word == covidList[2] or word == covidList[3] or \
                    word == covidList[4]:
                countActor3 += 1
                dic[index][7] = countActor3

    return dic


## Function that adds numOfEnvironment words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare, numOfCovid, numOfEnv] }
def numOfEnvironment(words, dic):
    envList = ["environment", "fire", "jobs", "energy", "green"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 8:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 8:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 8:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == envList[0] or word == envList[1] or \
                word == envList[2] or word == envList[3] or \
                    word == envList[4]:
                countActor1 += 1
                dic[index][8] = countActor1
        
        elif actor2_On == True:
            if word == envList[0] or word == envList[1] or \
                word == envList[2] or word == envList[3] or \
                    word == envList[4]:
                countActor2 += 1
                dic[index][8] = countActor2
        
        elif actor3_On == True:
            if word == envList[0] or word == envList[1] or \
                word == envList[2] or word == envList[3] or \
                    word == envList[4]:
                countActor3 += 1
                dic[index][8] = countActor3

    return dic


## Function that adds numOfElection words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare, numOfCovid, numOfEnv, numOfElection] }
def numOfElection(words, dic):
    electionList = ["fraud", "mail", "rigged", "transition"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 9:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 9:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 9:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == electionList[0] or word == electionList[1] or \
                word == electionList[2] or word == electionList[3]:
                countActor1 += 1
                dic[index][9] = countActor1
        
        elif actor2_On == True:
            if word == electionList[0] or word == electionList[1] or \
                word == electionList[2] or word == electionList[3]:
                countActor2 += 1
                dic[index][9] = countActor2
        
        elif actor3_On == True:
            if word == electionList[0] or word == electionList[1] or \
                word == electionList[2] or word == electionList[3]:
                countActor3 += 1
                dic[index][9] = countActor3

    return dic


## Function that adds numOfEconomy words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare, numOfCovid, numOfEnv, numOfElection, \
# numOfEcononmy] }
def numOfEconomy(words, dic):
    econList = ["jobs", "unemployment", "taxes", "manufacturing", "inequality"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 10:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 10:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 10:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == econList[0] or word == econList[1] or \
                word == econList[2] or word == econList[3] or \
                    word == econList[4]:
                countActor1 += 1
                dic[index][10] = countActor1
        
        elif actor2_On == True:
            if word == econList[0] or word == econList[1] or \
                word == econList[2] or word == econList[3] or \
                    word == econList[4]:
                countActor2 += 1
                dic[index][10] = countActor2
        
        elif actor3_On == True:
            if word == econList[0] or word == econList[1] or \
                word == econList[2] or word == econList[3] or \
                    word == econList[4]:
                countActor3 += 1
                dic[index][10] = countActor3

    return dic


## Function that adds numOfRace words to the dictionary 
## --- { index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, \
# numOfHealthcare, numOfCovid, numOfEnv, numOfElection, \
# numOfEcononmy, numOfRace] }
def numOfRace(words, dic):
    raceList = ["violence", "law", "order", "peace"]
    index = -1 
    countActor1 = 0
    countActor2 = 0
    countActor3 = 0
    actor1_On = False
    actor2_On = False
    actor3_On = False

    for word in words:
        ## Capturing actors' names in the corpus
        if word == actor1:
            index += 1
            actor1_On = True
            actor2_On = False
            actor3_On = False
            if len(dic[index]) == 11:
                dic[index].append(countActor1)
        elif word == actor2:
            index += 1
            actor1_On = False
            actor2_On = True
            actor3_On = False
            if len(dic[index]) == 11:
                dic[index].append(countActor2)
        elif word == actor3:
            index += 1
            actor1_On = False
            actor2_On = False
            actor3_On = True
            if len(dic[index]) == 11:
                dic[index].append(countActor3)
        
        elif actor1_On == True:
            if word == raceList[0] or word == raceList[1] or \
                word == raceList[2] or word == raceList[3]:
                countActor1 += 1
                dic[index][11] = countActor1
        
        elif actor2_On == True:
            if word == raceList[0] or word == raceList[1] or \
                word == raceList[2] or word == raceList[3]:
                countActor2 += 1
                dic[index][11] = countActor2
        
        elif actor3_On == True:
            if word == raceList[0] or word == raceList[1] or \
                word == raceList[2] or word == raceList[3]:
                countActor3 += 1
                dic[index][11] = countActor3

    return dic


## Converts the dictionary for dataframe, adds a column of indeces (for slider)
def dictConverter(dic):
    dicNew = {}
    indexList = []
    actorNameList = []
    timeStampList = []
    numWordsList = []
    numInterruptionsList = []
    numCrosstalksList = []
    numNumberUseList  = []
    numOfHealthcareList  = []
    numOfCovidList  = []
    numOfEnvList = []
    numOfElectionList  = []
    numOfEconList = []
    numOfRaceList = []

    for i in range(len(dic)):
        index = i
        indexList.append(index)
        dicNew["Order of Speech"] = indexList

        actorName = dic[i][0]
        if actorName == actor1:
            actorName = "Chris Wallace"
            actorNameList.append(actorName)
            dicNew["Actor"] = actorNameList
        elif actorName == actor2:
            actorName = "Joe Biden"
            actorNameList.append(actorName)
            dicNew["Actor"] = actorNameList
        elif actorName == actor3:
            actorName = "Donald J. Trump"
            actorNameList.append(actorName)
            dicNew["Actor"] = actorNameList

        timeStamp = dic[i][1]
        timeStampList.append(timeStamp)
        dicNew["Time"] = timeStampList 

        numWordsByActor = dic[i][2]
        numWordsList.append(numWordsByActor)
        dicNew["Number of Words"] = numWordsList 

        numInterruptionsByActor = dic[i][3]
        numInterruptionsList.append(numInterruptionsByActor)
        dicNew["Number of Interruptions"] = numInterruptionsList 

        numCrosstalksByActor = dic[i][4]
        numCrosstalksList.append(numCrosstalksByActor)
        dicNew["Number of Crosstalks"] = numCrosstalksList 

        numNumberUseByActor = dic[i][5]
        numNumberUseList.append(numNumberUseByActor)
        dicNew["Number of Number Use"] = numNumberUseList 

        numOfHealthCare = dic[i][6]
        numOfHealthcareList.append(numOfHealthCare)
        dicNew["Number of Healthcare"] = numOfHealthcareList

        numOfCovid = dic[i][7]
        numOfCovidList.append(numOfCovid)
        dicNew["Number of Covid"] = numOfCovidList 

        numOfEnv = dic[i][8]
        numOfEnvList.append(numOfEnv)
        dicNew["Number of Environment"] = numOfEnvList 

        numOfElection = dic[i][9]
        numOfElectionList.append(numOfElection)
        dicNew["Number of Election"] = numOfElectionList 

        numOfEcon = dic[i][10]
        numOfEconList.append(numOfEcon)
        dicNew["Number of Economy"] = numOfEconList 

        numOfRace = dic[i][11]
        numOfRaceList.append(numOfRace)
        dicNew["Number of Race"] = numOfRaceList 

    return dicNew




##################################################################
## Calling the functions that create the dictionary 
##################################################################

## Returns list of words (wordsNoPunctNoStamp)
wordsNoPunctNoStamp = removeStamps(raw) 
# print(wordsNoPunctNoStamp) 
# print("BREAK")

## Returns actorInfo = {index: [actorName], ...}
actorInfo = addActors(wordsNoPunctNoStamp) 
# print(actorInfo) 
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp], ...}
dic_V1 = addTimeStamps(raw, actorInfo) 
# print(dic_V1) 
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords], ...}
dic_V2 = addNumWordsByActor(wordsNoPunctNoStamp, dic_V1)
# print(dic_V2)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions], ...}
dic_V3 = addNumInterruptionsByActor(wordsWithPunct, dic_V2)
# print(dic_V3)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks], ...}
dic_V4 = addNumCrossTalksByActor(raw, dic_V3)
# print(dic_V4)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse], ...}
dic_V5 = addNumNumberUseByActor(wordsNoPunctNoStamp, dic_V4)
# print(dic_V5)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare], ...}
dic_V6 = numOfHealthcare(wordsNoPunctNoStamp, dic_V5)
# print(dic_V6)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare, \
# numOfCovid], ...}
dic_V7 = numOfCovid(wordsNoPunctNoStamp, dic_V6)
# print(dic_V7)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare, \
# numOfCovid, numOfEnvironment], ...}
dic_V8 = numOfEnvironment(wordsNoPunctNoStamp, dic_V7)
# print(dic_V8)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare, \
# numOfCovid, numOfEnvironment, numOfElection], ...}
dic_V9 = numOfElection(wordsNoPunctNoStamp, dic_V8)
# print(dic_V9)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare, \
# numOfCovid, numOfEnvironment, numOfElection, numOfEconomy], ...}
dic_V10 = numOfEconomy(wordsNoPunctNoStamp, dic_V9)
# print(dic_V10)
# print("BREAK")

## Returns actorInfo = {index: [actorName, timeStamp, numWords, \
# numInterruptions, numCrossTalks, numNumberUse, numOfHealthcare, \
# numOfCovid, numOfEnvironment, numOfElection, numOfEconomy, numOfRace], ...}
dic_V11 = numOfRace(wordsNoPunctNoStamp, dic_V10)
# print(dic_V11)
# print("BREAK")




##################################################################
## Creating the dataframe 1 (from the dictionary)
##################################################################

## dictConverter also adds the column of indeces (important!)
dic_Final = dictConverter(dic_V11)
# print(dic_Final)
# print("BREAK")

df1 = pd.DataFrame(dic_Final)
print(df1)




##################################################################
## Text processing and extracting data: Part 2
##################################################################

def readMeIn(file):
    with open(file, 'r', encoding = 'utf8', 
                                    errors = 'ignore') as readMe:
        entry = readMe.readlines()
    entries = [e.strip().split('\n\n') for e in entry 
            if e.strip().split('\n')!=['']
            and e.strip().split('\n') != ["Part 2"]]
    
    return entries


## Function that makes dictionaries of speaker: statement and speaker: word: word count
def makeDictionaries(entries):
    wordCountDict = {"Biden": {}, "Trump": {}, "Chris": {}}
    presDi = {}

    for e in (range(0, len(entries) - 2, 2)):
        keyL = entries[e]
        key = ' '.join([word for word in keyL]) 
        statement = entries[e + 1]
        listOfWordsStr = ''.join([word for word in statement]);
        listOfWords = listOfWordsStr.split(" ")
        if ("Biden" in key): 
            for word in listOfWords : 
                wordCount = wordCountDict.get("Biden").get(word, 0) + 1 
                wordCountDict["Biden"][word] = wordCount
        elif ("Trump" in key):
            for word in listOfWords: 
                wordCount = wordCountDict.get("Trump").get(word, 0) + 1
                wordCountDict["Trump"][word] = wordCount
        elif ("Chris" in key):
            for word in listOfWords : 
                wordCount = wordCountDict.get("Chris").get(word, 0) + 1
                wordCountDict["Chris"][word] = wordCount 
        presDi[key] = statement
    
    return presDi, wordCountDict


def makeDataFrames(presDi, wordCountDict):
    dfDict = {}
    for speaker in ["Biden", "Trump", "Chris"]:
        speakerDict = wordCountDict.get(speaker)
        dfDict[speaker] = pd.DataFrame.from_dict(speakerDict, 
                            orient = 'index', columns = ["wordCounted"])
        dfDict[speaker].index.name = "word"
    # merge data frames, by word # 
    dfWords = dfDict["Biden"].merge(dfDict["Trump"], 
                            how = "outer", on = "word", 
                            suffixes = ("Biden", "Trump"))
    dfWords = dfWords.merge(dfDict["Chris"], how = "outer", 
                        on = "word", suffixes = ("", "Chris"))
    dfPres = pd.DataFrame.from_dict(presDi, orient = 'index', 
                            columns = ["statement"])
    dfPres.index.name = "speaker"
    dfPres["tempDup"] = dfPres.index
    dfPres[["name", "time"]] = dfPres["tempDup"].str.split(": ", expand = True)
    
    return dfPres, dfWords


def findThemes(masterList, dfPres):
    for theme, words in masterList.items(): 
        for word in words:
            dfPres[word] = dfPres.statement.str.contains(word, case = False)
    #START WORD COUNT SUMS#
    themeWordCount = dfPres.groupby(["name"]).\
                    agg({'Obamacare': 'sum'}).reset_index()
    for theme, words in masterList.items():
        for word in words:
            if word == 'Obamacare': pass 
            else:
                countTemp = dfPres.groupby(["name"])\
                    .agg({word: 'sum'}).reset_index()
                themeWordCount = themeWordCount.merge(countTemp, 
                                how = "outer", on = "name")
    
    return dfPres, themeWordCount


## Function that makes dictionaries of speaker: statement and speaker: word: word count
## wordCountDict = {"Biden": {}, "Trump": {}, "Chris": {}}
def youHeIDict(trans):
    punct = set(string.punctuation)
    youMe = ["you", "he", "i"]
    youMeDict = {"Joe Biden": {}, "Donald J. Trump": {}}
    
    for e in (range(0, len(trans) - 2, 2)):
        keyL = trans[e]
        key = ' '.join([word for word in keyL]) 
        statement = trans[e + 1]
        listOfWordsStr = ''.join([word for word in statement if 
                                word not in punct])
        listOfWords = listOfWordsStr.split(" ")
        if ("Biden" in key): 
            for word in listOfWords : 
                word = str.lower(word)
                if word in youMe:
                    wordCount = youMeDict.get("Joe Biden").get(word, 0) + 1 
                    youMeDict["Joe Biden"][word] = wordCount
        elif ("Trump" in key):
            for word in listOfWords: 
                word = str.lower(word)
                if word in youMe:
                    wordCount = youMeDict.get("Donald J. Trump").get(word, 0) + 1
                    youMeDict["Donald J. Trump"][word] = wordCount
        else: pass
    
    dfYouMe = pd.DataFrame.from_dict(youMeDict)
    dfYouMe.index.name = "youHeI"
    dfYouMe["youHeI"] = dfYouMe.index
    
    return dfYouMe 


def themeCount(themeWordCount):
    themeWordCount = themeWordCount.set_index('name').T  
    themeWordCount['themeWord'] = themeWordCount.index
    for theme, listWords in masterList.items():
        for index, row in themeWordCount.iterrows(): 
            if row.themeWord in listWords:
                themeWordCount.loc[index, "broadTheme"] = theme
            else : 
                pass
    
    return themeWordCount


def broadCount(themeWordCount):
    broadThemeData = themeWordCount.groupby(["broadTheme"])\
                        .agg({'President Donald J. Trump': 'sum', 
                             'Vice President Joe Biden': 'sum'}).reset_index()
    
    return broadThemeData


## Thematic Groupings
healthCareList = ["Obamacare", "Affordable Care", "Insurance", "Cost"]
covidList = ["covid", "vaccine", "mask", "death", "dying"]
enviorList = ["environment", "fire", "energy", "green"]
electionList = ["fraud", "mail", "rigged", "transition", "vot"]
economyList = ["job", "unemployment", "taxes", "manufacturing"]
raceList = ["violence", "law", "order", "peace", "fund"]
masterList ={"healthcare": healthCareList, 
            "covid": covidList, 
            "environment": enviorList, 
            "election": electionList, 
            "economy": economyList, 
            "race": raceList}




##################################################################
## Creating the dataframe 2 
##################################################################

trans = readMeIn("presidentialTranscript.txt")
presDi, wordCountDict = makeDictionaries(trans)
dfYouMe = youHeIDict(trans)
dfPres, dfWords = makeDataFrames(presDi, wordCountDict)
dfPres, themeWordCount = findThemes(masterList, dfPres)
themeWordCount = themeCount(themeWordCount)
broadThemeData = broadCount(themeWordCount)

themeWordCount = themeWordCount.melt(id_vars = ["themeWord", "broadTheme"], 
                                var_name = "name", value_name = "wordCount")

## Funtion that changes the name strings of actors 
def renameActors(themeWordCount):
    themeWordCount = themeWordCount[themeWordCount.name != "Chris Wallace"]
    themeWordCount = themeWordCount[themeWordCount.name != "Chris Wallace:"]
    for index, row in themeWordCount.iterrows():
        if row['name'] == "President Donald J. Trump":
            themeWordCount.loc[index, 'name'] = "Donald J. Trump"
        elif row['name'] == "Vice President Joe Biden":
            themeWordCount.loc[index, 'name'] = "Joe Biden"
    
    return themeWordCount

themeWordCount = renameActors(themeWordCount)
# print(themeWordCount)
# print("BREAK")

dfYouMe = dfYouMe.melt(id_vars = ["youHeI"], var_name = "name", value_name = "wordCountHeI")




##################################################################
## Visualization 
##################################################################

## Title
st.write("## Tracing the Presidential Debate 2020")
st.write("###### Choose 'Show app in wide mode' in the 'Settings' on the top right corner.")
st.write("# \n")

## Youtube video
st.video('https://www.youtube.com/watch?v=ofkPfm3tFxo')
st.write("\n")

## Data table
st.write(df1)
st.write("\n")

## Creating a filter slider
order = st.sidebar.slider("Order of Speech", 0, 789) ## min and max values


## Bar graphs
## Drawing ActorTime (bar) minimap
viz0_ActorTimeSmall = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None, axis = None, title = None),
    alt.Y("Actor", sort = None, axis = None, title = None),
    alt.Color("Actor", legend = None),
).properties(
    width = 300
    )

## Drawing ActorTime (bar) (change via minimap and slider) 
viz0_ActorTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None, axis = None, title = None),
    alt.Y("Actor", sort = None),
    alt.Color("Actor"),
)

## Drawing NumWordsTime (bar) (change via minimap and slider)
viz0_NumWordsTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Words", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Words')]
)

## Drawing NumInterruptionTime (bar) (change via minimap and slider) 
viz0_NumInterruptionsTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Interruptions", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Interruptions')]
)

## Drawing NumCrosstalksTime (bar) (change via minimap and slider) 
viz0_NumCrosstalksTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Crosstalks", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Crosstalks')]
)

## Drawing NumHealthcareTime (bar) (change via minimap and slider)
viz0_NumHealthcareTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Healthcare", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Healthcare')]
)

## Drawing NumCovidTime (bar) (change via minimap and slider)
viz0_NumCovidTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Covid", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Covid')]
)

## Drawing NumEnvTime (bar) (change via minimap and slider)
viz0_NumEnvTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Environment", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Environment')]
)

## Drawing NumElectionTime (bar) (change via minimap and slider)
viz0_NumElectionTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Election", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Election')]
)

## Drawing NumEconomyTime (bar) (change via minimap and slider)
viz0_NumEconomyTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Economy", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Economy')]
)

## Drawing NumRaceTime (bar) (change via minimap and slider)
viz0_NumRaceTime = alt.Chart(df1).mark_bar().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Time", sort = None),
    alt.Y("Number of Race", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Actor'), alt.Tooltip('Number of Race')]
)


## Line graphs
## Drawing NumWordsTime (line graph) (zoom and slider)
viz1_NumWordsTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Words", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Words')]
)

## Drawing NumInterruptionsTime (line graph) (zoom and slider)
viz1_NumInterruptionsTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Interruptions", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Interruptions')]
)

## Drawing NumCrosstalksTime (line graph) (zoom and slider)
viz1_NumCrosstalksTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Crosstalks", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Crosstalks')]
)

## Drawing NumHealthcareTime (line graph) (zoom and slider)
viz1_NumHealthcareTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Healthcare", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Healthcare')]
)

## Drawing NumCovidTime (line graph) (zoom and slider)
viz1_NumCovidTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Covid", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Covid')]
)

## Drawing NumEnvTime (line graph) (zoom and slider)
viz1_NumEnvTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Environment", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Environment')]
)

## Drawing NumElectionTime (line graph) (zoom and slider)
viz1_NumElectionTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Election", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Election')]
)

## Drawing NumEconomyTime (line graph) (zoom and slider)
viz1_NumEconomyTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Economy", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Economy')]
)

## Drawing NumRaceTime (line graph) (zoom and slider)
viz1_NumRaceTime = alt.Chart(df1).mark_line().transform_filter(
    alt.datum["Order of Speech"] >= order
).encode(
    alt.X("Order of Speech", sort = None),
    alt.Y("Number of Race", sort = None),
    alt.Color("Actor"),
    tooltip = [alt.Tooltip('Number of Race')]
)


## Writing the graphs and interface

## Mouseover interaction to highlight 
picked = alt.selection_single(on = "mouseover")
## Brush interaction to draw partially
brush = alt.selection_interval(encodings = ["x"])
## Scale interaction
scales = alt.selection_interval(bind = "scales", encodings = ["x"])

st.write("### Through the debate")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
## Number of words
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumWordsTime.transform_filter(brush)) 

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumWordsTime.add_selection(scales))

## Number of interruptions
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumInterruptionsTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumInterruptionsTime.add_selection(scales))

## Number of interruptions
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumCrosstalksTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumCrosstalksTime.add_selection(scales))

st.write("# \n")
st.write("### Weights within the debate")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
## Healthcare
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumHealthcareTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumHealthcareTime.add_selection(scales))

## Covid
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumCovidTime.transform_filter(brush)) 

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumCovidTime.add_selection(scales))

## Economy
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumEconomyTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumEconomyTime.add_selection(scales))

## Environment 
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumEnvTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumEnvTime.add_selection(scales))

## Race
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumRaceTime .transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumRaceTime.add_selection(scales))

## Election
st.write("# \n")
st.write("###### Create a window on the rectangle with your mouse. Move it to travel through the debate.")
st.write("# \n")
st.write(viz0_ActorTimeSmall.add_selection(brush) & viz0_ActorTime.transform_filter(brush) \
    & viz0_NumElectionTime.transform_filter(brush))

st.write("###### Keep your mouse on the chart to zoom in / out and travel through the debate.")
st.write("# \n")
st.write(viz1_NumElectionTime.add_selection(scales))


## Theme word charts
brush = alt.selection_single(fields = ["broadTheme"])
domain = ["Joe Biden", "Donald J. Trump"]
range_ = ["#e45756", "#f58518"]
color = alt.condition(brush, 
            alt.Color('name:N', 
                    legend = None,
                    scale = alt.Scale(domain = domain, range = range_ )), 
            alt.value('lightgray'))

broadTheme1 = alt.Chart(themeWordCount).mark_bar().encode(
    x = alt.X("broadTheme:N", title = "Theme", 
    sort = ["healthcare", "covid", "economy", "environment", "race", "election"]),
    y = alt.Y("wordCount:Q", title = "Word Count"),
    color = color,
    tooltip = [alt.Tooltip('name', title = "Actor")]
)

specificWord1 = alt.Chart(themeWordCount).mark_bar().encode(
    x = alt.X("name:N", title = None),
    y = alt.Y("wordCount:Q", title = "Word Count"),
    color = color,
    column = alt.Column("themeWord:N", title = "Theme Words"),
    tooltip = [alt.Tooltip('wordCount', title = "Word Count")]
)

pickedName = alt.selection_single(fields = ["name"])
colorYouMe = alt.condition(pickedName, 
            alt.Color("name:N", 
                legend = alt.Legend(title = "Actor"),
                scale = alt.Scale(domain = domain, range = range_)),
            alt.value('lightgray'))

youMe = alt.Chart(dfYouMe).mark_bar().encode(
    x = alt.X("name:N", title = None),
    y = alt.Y("wordCountHeI:Q", title = "Word Count"), 
    tooltip = [alt.Tooltip("wordCountHeI", title = "Word Count")],
    color = colorYouMe,
    column = alt.Column("youHeI:N", sort = ["you", "he", "i"], 
    title = "Pointing to self and others")
)


st.write("# \n")
st.write("###### Click on the bars to see the words by theme.")
st.write("# \n")
st.write(broadTheme1.add_selection(brush) & specificWord1.transform_filter(brush))
st.write("# \n")
st.write("###### Click on the bars to see the word count by actor.")
st.write("# \n")
st.write(youMe.add_selection(pickedName))
