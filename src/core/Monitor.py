'''
Created on Mar 6, 2013

@author: Sujen
'''
from core.FileManager import FileManager
from core.Rule import Rule
from mimify import File
from core.QueryManager import QueryManager

class Monitor:
    '''
    classdocs
    '''
    def __init__(self):
        #fileManager.read()
        '''
        Constructor
        '''            
    #Recursive function in order to keep the process going infinitely.    
    def keepMonitoring(self,oldMaxLines,dirConfig,dirLog):
        import time
        fileManager = FileManager()
        monitorObj = Monitor()
        logLines = fileManager.read(dirLog)
        
        if(oldMaxLines == len(logLines)):
            print "The log file still hasn't changed."
            time.sleep(10)
            monitorObj.keepMonitoring(oldMaxLines,dirConfig,dirLog)
        else:
            print "The log file still has changed."
            startAt = oldMaxLines
            monitorObj.startMonitoring(dirConfig, dirLog, startAt)
        
    #This function checks log files for errors
    def startMonitoring(self,dirConfig,dirLog,startAt):
        from Trigger import Trigger
        import sys
        import re
        
        #
        sys.setrecursionlimit(10000)
       
        monitorObj = Monitor()
        triggerObj = Trigger()
        fileManager = FileManager()
        
        ruleLines = fileManager.stripNewLine(fileManager.read(dirConfig))
        logLines = fileManager.read(dirLog)
        
        strippedRules = fileManager.stripNewLine(ruleLines)
        
        ruleCount = fileManager.stripNewLine(ruleLines[0].split('='))
        ruleTime = fileManager.stripNewLine(ruleLines[1].split('='))
        
        # "\n"+str(strippedRules)+"\n"+str(ruleCount)+"\n"+str(ruleTime)

        regexIPAdress = "SRC=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" 
        regexTimeStamp = "\w+\s\d+\s\d+:\d+:\d+"
        regexTime = "\d+:\d+:\d+"
        
        IPAllowed = ['SRC=145.92.6.10','SRC=145.92.6.36','SRC=145.92.6.97']
        
        sourceIPAdress = []
        connectionTime = []
        
        dateTimeStart = ""
        dateTimeNow = ""

        count=0

        for i in range(startAt,len(logLines)):
            sourceIPAdress.append(re.findall(regexIPAdress, logLines[i]))
            connectionTime.append(re.findall(regexTimeStamp, logLines[i]))

            if(len(sourceIPAdress)>1):
                if(sourceIPAdress[-1]==sourceIPAdress[-2]):
                    count=count+1    
                else:
                    count=0
            #
            if(int(count)==(int(ruleCount[1]))):
                startElement=int(i-(int(ruleCount[1])))-int(startAt)
                print str(startElement)+" "+str(int(ruleCount[1])) + " " + str(int(startAt)) + " "+ str(len(connectionTime)) + " " + str(i)
                dateTimeStart=connectionTime[startElement]
                dateTimeNow=connectionTime[i-int(startAt)]
                timeStart=re.findall(regexTime,str(dateTimeStart))
                timeNow=re.findall(regexTime,str(dateTimeNow))
                timeStartSplitted=timeStart[0].split(":")
                timeNowSplitted=timeNow[0].split(":")
                
                if(int(timeNowSplitted[1])>int(timeStartSplitted[1])):
                    minutes=int(timeNowSplitted[1])-int(timeStartSplitted[1])
                    timeNowSplitted[2]=str(int(timeNowSplitted[2])+(60*minutes))
                
                timeRange=int(timeNowSplitted[2])-int(timeStartSplitted[2])  
                if(timeRange<int(ruleTime[1])and(int(count)==(int(ruleCount[1])))):
                    errorType = 1
                    errorMsg = 'Hello Admin,<br /><br />We have detected a possible threat.<br />The file concerning the error is: '+dirLog+'.<br /><br /><i>This mail has been automatically generated by the</i><b> Security Monitor</b>'
                    triggerObj.ExecuteTrigger(errorType,errorMsg)   
                    print "mail is triggered "+str(int(count))+"=="+str(int(ruleCount[1]))+"\n"+str(timeRange)+"<"+str(int(ruleTime[1]))  
                                                
        monitorObj.keepMonitoring(len(logLines),dirConfig,dirLog)
        
    def stopMonitoring(self):
        import time
        import sys
        
        print "Monitoring Ended!"
        time.sleep(10)
        sys.exit(0)
        
    def testMonitoring(self,dirConfig,dirLog,startAt):
        ruleManager = Rule()
        queryManager = QueryManager()
        ruleManager.readRules(dirConfig)
        print "Monitoring using the rule " + ruleManager.name + "...\n"
        print ruleManager.query
        regex = queryManager.execute(ruleManager.query)
        
        
        
    #TODO// Check Timestamps between a certain period for a IP and count connections, IDS should execute an action according to the number of connections