from __future__ import with_statement

from ConfigParser import SafeConfigParser
from com.ziclix.python.sql import zxJDBC

import LTEOpt.LTEOptMain as LTEOptMain
import VoLTE.VoLTEMain as VoLTEMain
import VoWIFI.VoWIFIMain as VoWIFIMain
import Energy.EnergyMain as EnergyMain
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os
#1st
import datetime

import os
import sys
path =os.getcwd()


from urllib import pathname2url

global url
global headerNmeArr
headerNmeArr=[]
import webbrowser
sys.stdout.flush()
import argparse
noNode=0 #set to 1 if there is no node_name given in the config file
helpCom=0 #variable that is set to 1 if any other command line argument aside from help (-h) is used
config_path= path+"\\configFiles\\"
config_pathAll=path+"\\configFiles\\multiFeatures.ini"
config_pathSystem=path+"\\configFiles\\systemConfig.ini"
result_path= path+"\\Results"
headerFilePath=path+"\\src\\headerName.txt"
configNode=""
configDate=""
nodePick=''
noSpace=''
rows=[]
typeArr=[]
allArr=[]
KPIList=[]
erbsNmeArr=[]
KPINmeArr=[]
dashHeaderNmeArr=[]
dashNmeArr=[]
test=''
test2=0
test1=0
counterArr=0
headerline="<tr>\n"
headerlineX=""
dataline="<tr>\n"
dateTime=[]
erbsArr=[]
Fail=0
Pass=0
Empty=0
countSum=0
multiCom=0

#2ndStart
allArr=["LTEOpt","VoLTE","VoWIFI","Energy"]
#2ndEnd


HTMLFile="""<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
}
</style>
</head>
<body>
<h1>Summary Of The Latest Configuration Run</h1>

<table style="width:100%">
    <tr>
        <th></th>
        <th></th>
        <th colspan="4">Source</th>
        <th></th>
        <th colspan="4">Target</th>
    <tr>
    <tr>
        <th>Result</th>
        <th>Configuration: KPI, Datetime_id, Node_Name</th>
        <th>Matches</th>
        <th>Partial Matches</th>
        <th>Non Matches</th>
        <th>Total</th>
        <th></th>
        <th>Matches</th>
        <th>Partial Matches</th>
        <th>Non Matches</th>
        <th>Total</th>
    </tr>
"""
HTMLMultiSummary="""<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
}
</style>
</head>
<body>
<h1>Summary Of The Latest Multi Feature Configuration Run</h1>

<table style="width:100%">
    <tr>
        <th>Result</th>
        <th>Feature</th>
        <th></th>
        <th>Passes</th>
        <th>Empties</th>
        <th>Fails</th>
    </tr>
    """
configParser = SafeConfigParser()
configParser.read(headerFilePath)
nodeNameList=configParser.get('Lists', 'nodeName')
headerNameList=configParser.get('Lists', 'headerName')
KPINameList=configParser.get('Lists', 'KPIName')
dashList=configParser.get('Lists', 'dash')
dashHeaderList=configParser.get('Lists', 'dashHeader')



configParser = SafeConfigParser()
configParser.read(config_pathSystem) #reads the information found in the config file
cnxnStr=configParser.get('settings', 'Server')
username=configParser.get('settings', 'Username')
password=configParser.get('settings', 'Password')
popUp=configParser.get('settings', 'popUp')
day=configParser.get('timing','day')
hour=configParser.get('timing','hour')
minute=configParser.get('timing','minute')





if day != "" and hour == "" and minute=="":
    configTime="days"
    timeElem=int(day)
elif day == "" and hour != "" and minute=="":
    configTime="hours"
    timeElem=int(hour)
elif day == "" and hour == "" and minute!="":
    configTime="minutes"
    minute=int(minute)
else:
    hour=1
    configTime="hourNone"
    timeElem=int(hour)

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)
    
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-k",help="Used to pick the KPI value")
    parser.add_argument("-d", nargs='+',type=str, help="Used to pick the datetime_id")
    parser.add_argument("-n", help="Used to pick the node_name value")
    parser.add_argument("-n19",help="Used to pick the node_name value for LTEOpt KPI 19")
    parser.add_argument("-c",help="Used to choose what config file to use") #Used to choose the config file to be used
    parser.add_argument("-a",help="Used to choose to run multiple features at once")
    parser.add_argument("-t",help="Used to choose the feature type")
    args = parser.parse_args() #set a variable equal to the command line arguements that were read in
    configType=args.c
    #Check to see if the user choose to use config files or command line arguements
    if args.k != None and args.d != None and args.t != None:
        helpCom=1
        sys.stdout.write('Working...')
        sys.stdout.flush()
        #sets the values given as command line arguements equal to some variables
        KPI_VALUE=args.k
        DATETIME_ID= " ".join(str(b) for b in args.d)
        NODE_NAME=args.n
        NODE_NAME19=args.n19
        TYPE=args.t
        typeArr.append(TYPE)
    elif configType == "multi": #config files are used    
        helpCom=1
        multiCom=1
        KPI_VALUE="all"
        sys.stdout.write('Working...')
        sys.stdout.flush()
        configFile=config_pathAll #sets the directory of the configFile chosen equal to a variable
        configParser = SafeConfigParser()
        configParser.read(configFile) #reads the information found in the config file
        NODE_NAME=''
        TYPE=configParser.get('configuration','TYPE')
        decimalPlaces=configParser.get('configuration', 'decimalPlaces')
        decimalPlaces=int(decimalPlaces)
        if decimalPlaces<=1:
            decmalPlaces=10
        elif decimalPlaces==2:
            decimalPlaces=100
        elif decimalPlaces==3:
            decimalPlaces=1000
        elif decimalPlaces==4:
            decimalPlaces=10000
        elif decimalPlaces>=5:
            decimalPlaces=100000
        if TYPE=="all":
            typeArr=allArr
        else:
            typeArr=TYPE.split(",")
        DATETIME_ID=configParser.get('configuration', 'DATETIME_ID')
    elif configType != None: #config files are used    
        helpCom=1
        sys.stdout.write('Working...')
        sys.stdout.flush()
        configFile=config_path+configType #sets the directory of the configFile chosen equal to a variable
        configFile=configFile.replace(",","\\") #Replaces the , found in the -c command
        configParser = SafeConfigParser()
        configParser.read(configFile) #reads the information found in the config file
        KPI_VALUE=configParser.get('configuration', 'KPI_VALUE') #Sets the value for KPI_VALUE in the config file equal to a variable
        TYPE=configParser.get('configuration','TYPE')
        typeArr.append(TYPE)
        DATETIME_ID=configParser.get('configuration', 'DATETIME_ID')
        NODE_NAME=configParser.get('configuration', 'NODE_NAME')
        decimalPlaces=configParser.get('configuration', 'decimalPlaces')
        decimalPlaces=int(decimalPlaces)
        if decimalPlaces<=1:
            decmalPlaces=10
        elif decimalPlaces==2:
            decimalPlaces=100
        elif decimalPlaces==3:
            decimalPlaces=1000
        elif decimalPlaces==4:
            decimalPlaces=10000
        elif decimalPlaces>=5:
            decimalPlaces=100000
    dbDriver = "com.sybase.jdbc4.jdbc.SybDriver"
    cnxn = zxJDBC.connect(cnxnStr, username, password, dbDriver) #db connection
    crsr = cnxn.cursor(1) #crsr connection

    for counter,x in enumerate(typeArr):
        splitDate=""
        dateTime=[]
        TYPE=typeArr[counter] 
        if TYPE== 'LTEOpt':
            NODE_NAME19=configParser.get('configuration', 'NODE_NAME19')
            try:
                splitNode19=NODE_NAME19.split(',')
            except AttributeError:
                splitNode19=NODE_NAME19
            pass
        else:
            splitNode19=['']
        
        if TYPE=="LTEOpt":
            mainReturn=LTEOptMain.LTEOptMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="VoLTE":
            mainReturn=VoLTEMain.VoLTEMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="VoWIFI":
            mainReturn=VoWIFIMain.VoWIFIMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="Energy":
            mainReturn=EnergyMain.EnergyMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
#3rd
        lenKPI=mainReturn[0]
        Pass=mainReturn[1]
        Fail=mainReturn[2]
        Empty=mainReturn[3]
        result=mainReturn[4]
        splitKPI=mainReturn[5]
        splitDate=mainReturn[6]
        splitNode=mainReturn[7]
        HTMLFileM=mainReturn[8]
        resultDir=mainReturn[9]
        erbsArr=mainReturn[10]
        erbsHeadArr=mainReturn[11]
        KPIHeader=mainReturn[12]
        dashHeaderArr=mainReturn[13]
        dashArr=mainReturn[14]
        for elem in KPIHeader:
            if elem not in KPINmeArr:
                KPINmeArr.append(str(elem))
        for elem in erbsHeadArr:
            if elem not in headerNmeArr:
                headerNmeArr.append(str(elem))
        for elem in erbsArr:
            if elem not in erbsNmeArr:
                erbsNmeArr.append(str(elem))
        for elem in dashHeaderArr:
            if elem not in dashHeaderNmeArr:
                dashHeaderNmeArr.append(str(elem))
        for elem in dashArr:
            if elem not in dashNmeArr:
                dashNmeArr.append(str(elem))

        if multiCom==1:
            urlSum= os.path.join(result_path,"MultiSummary.html")
            FeatureHTML="<h4><a href='%s'>Features</a></h4>" %(urlSum)
            HTML_file= open(os.path.join(result,"Summary.html"),"w")
            url=result +"\\Summary.html"
            HTMLFileM=HTMLFile+FeatureHTML+HTMLFileM+"""
            </table>
            </body>
            </html>
            """
            HTML_file.write(HTMLFileM) #Writes HTML String to the HTML summary file
            HTML_file.close()
            HTMLFileM=""
            counterArr=0
            passNum=Pass
            failNum=Fail
            emptyNum=Empty
            if Pass !=0 and Fail==0 and Empty==0:
                HTMLMultiSummary=HTMLMultiSummary +'\n<tr bgcolor="#00FF00">\n'
                multiPassFail="Pass"
            elif Empty !=0 and Fail==0:
                HTMLMultiSummary=HTMLMultiSummary +'\n<tr bgcolor="#FFFF00">\n'
                multiPassFail="Empties"
            elif Fail !=0:
                HTMLMultiSummary=HTMLMultiSummary +'\n<tr bgcolor="#FF0000">\n'
                multiPassFail="Fail"                     
            Empty=0
            Fail=0
            Pass=0


            HTMLMultiSummary=HTMLMultiSummary+"""
                    <td>%s</td>
                    <td><a href="%s">%s</a></td>
                    <td></td>
                    <td>%d/%s</td>
                    <td>%d/%s</td>
                    <td>%d/%s</td>
                </tr>""" %(multiPassFail,url,TYPE,passNum,len(splitKPI)*len(splitDate)*len(splitNode),emptyNum,len(splitKPI),failNum,len(splitKPI)*len(splitDate)*len(splitNode))
        else:
            HTML_file= open(os.path.join(result,"Summary.html"),"w")
            urlSum=result +"\\Summary.html"
            HTMLFileM=HTMLFile+ HTMLFileM +"""
            </table>
            </body>
            </html>
            """
            HTML_file.write(HTMLFileM) #Writes HTML String to the HTML summary file
            HTML_file.close()
            
    if multiCom==1:
        HTMLMultiSummary=HTMLMultiSummary+"""
        </table>
        </body>
        </html>
        """
        HTML_MultiSum= open(os.path.join(result_path,"MultiSummary.html"),"w")
        urlSum= os.path.join(result_path,"MultiSummary.html")
        HTML_MultiSum.write(HTMLMultiSummary) #Writes HTML String to the HTML summary file
        HTML_MultiSum.close()
        print("\nResults can be found in the follow directory: %s" %(result_path)) #print to the command line where the results are found
    
    else:
        print("\nResults can be found in the following directory: %s" %(resultDir)) #print to the command line where the results are found
    erbsNmeString=','.join(map(str, erbsNmeArr))
    headerNmeString=','.join(map(str, headerNmeArr))
    KPINmeString=','.join(map(str, KPINmeArr))
    dashHeaderNmeString=','.join(map(str, dashHeaderNmeArr))
    dashNmeString=','.join(map(str, dashNmeArr))

    headerFile=open(headerFilePath,"w")
    headerFileString="[Lists]\nheaderName=%s\n\nNodeName=%s\n\nKPIName=%s\n\ndash=%s\n\ndashHeader=%s" %(headerNmeString,erbsNmeString,KPINmeString,dashNmeString,dashHeaderNmeString)
    headerFile.write(headerFileString)
    headerFile.close()    
finally:
    print("\nCompleted")
    crsr.close() #closes the cursor to the DB
    cnxn.close() #close the connection to the db
    """
    if helpCom==1 and popUp=="on": 
        #auto opens the summary page after the script has completed running
        urlSum = 'file:{}'.format(pathname2url(os.path.abspath(urlSum)))
        webbrowser.open_new_tab(urlSum)
    """