from __future__ import with_statement

from ConfigParser import SafeConfigParser
from com.ziclix.python.sql import zxJDBC

import editFeature as editFeature
import LTEOpt.LTEOptMain as LTEOptMain
import VoLTE.VoLTEMain as VoLTEMain
import VoWIFI.VoWIFIMain as VoWIFIMain
import Energy.EnergyMain as EnergyMain
import RANCapacityManagement.RANCapacityManagementMain as RANCapacityManagementMain
import TWAMP.TWAMPMain as TWAMPMain
#1st
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys
path =os.getcwd()
from urllib import pathname2url
import webbrowser
sys.stdout.flush()
import argparse
noNode=0 #set to 1 if there is no node_name given in the config file
helpCom=0 #variable that is set to 1 if any other command line argument aside from help (-h) is used
config_path= path+"\\configFiles\\"#path to config file folder
config_pathAll=path+"\\configFiles\\multiFeatures.ini"#path to config file to run multiple features
config_pathSystem=path+"\\configFiles\\systemConfig.ini"#path to config file that holds the system setting
result_path= path+"\\Results"#path to result folder
headerFilePath=path+"\\src\\headerName.txt"#path to file that contains arrays used for auto mathcing
typeArr=[]#holds the features to be tested
erbsNmeArr=[]#holds values used for auto column matching
KPINmeArr=[]#holds values used for auto column matching
dashHeaderNmeArr=[]#holds values used for auto column matching
headerNmeArr=[]#holds values used for auto column matching
dashNmeArr=[]#holds values used for auto column matching
multiCom=0#Flag that is set to 1 if the current run is multiple features

#2ndStart
allArr=["TWAMP","RANCapacityManagement","LTEOpt","VoLTE","VoWIFI","Energy"]#holds the names of all the feature names
#2ndEnd

#HTML code used for result table creation
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
#Code used to create Multi feature summary html tables
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
configParser = SafeConfigParser()#Used to parse information being held in a file
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

#Used when a range of datetimes is found in the config file sets a variable equal to the timing ie. day hour or minute and another variable to the number defined in the config file
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

#function use to zip the results file
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
    parser.add_argument("-ef",help="Add a feature")	#edit- remove this
    parser.add_argument("-er",help="Replace one or multiple KPI's SQL")
    parser.add_argument("-edk",help="Delete one or multiple KPIs")
    parser.add_argument("-ek",help="Add one or multiple KPIs to a feature")
    parser.add_argument("-edf",help="Delete a feature")
    args = parser.parse_args() #set a variable equal to the command line arguements that were read in
    configType=args.c

    #Check to see if the user choose to use config files or command line arguements
    if args.ef != None:	#add feature call to editFeatureFunction
        action = '-f'
        editFeature.editFeatureFunction(action, args.ef)
        sys.exit()
    if args.er != None:	#replace kpi call to editFeatureFunction
        action = '-r'
        editFeature.editFeatureFunction(action, args.er)
        sys.exit()
    if args.edk != None:	#delete kpi call to editFeatureFunction
        action = '-d'
        editFeature.editFeatureFunction(action, args.edk)
        sys.exit()
    if args.ek != None:		#add kpi call to editFeatureFunction
        action = '-k'
        editFeature.editFeatureFunction(action, args.ek)
        sys.exit()
    if args.edf != None:	#delete feature call to editFeatureFunction
        action = '-df'
        editFeature.editFeatureFunction(action, args.edf)
        sys.exit()
#do for all edits 
		
    if args.k != None and args.d != None and args.t != None:
        helpCom=1#Flag that is set if anything besides the -h command is used
        sys.stdout.write('Working...')
        sys.stdout.flush()
        #sets the values given as command line arguements equal to some variables
        KPI_VALUE=args.k
        DATETIME_ID= " ".join(str(b) for b in args.d)
        NODE_NAME=args.n
        NODE_NAME19=args.n19
        TYPE=args.t
        typeArr.append(TYPE)

    elif configType == "multi": #config files are used and is a multi feature run 
        helpCom=1#Flag that is set if anything besides the -h command is used
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
		#divison factor based on how many decimal places
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
    elif configType != None: #config files are used  and is a single feature run  
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
	#loops over the array holding the features to be run
    for counter,x in enumerate(typeArr):
        splitDate=""
        TYPE=typeArr[counter]#feature for this current loop 
        if TYPE== 'LTEOpt':
            NODE_NAME19=configParser.get('configuration', 'NODE_NAME19')
            try:
                splitNode19=NODE_NAME19.split(',')
            except AttributeError:
                splitNode19=NODE_NAME19
            pass
        else:
            splitNode19=['']
        #calls to the feature main files
        if TYPE=="LTEOpt":
            mainReturn=LTEOptMain.LTEOptMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="VoLTE":
            mainReturn=VoLTEMain.VoLTEMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="VoWIFI":
            mainReturn=VoWIFIMain.VoWIFIMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="Energy":
            mainReturn=EnergyMain.EnergyMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="RANCapacityManagement":
            mainReturn=RANCapacityManagementMain.RANCapacityManagementMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
        elif TYPE=="TWAMP":
            mainReturn=TWAMPMain.TWAMPMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)
#3rd
        lenKPI=mainReturn[0]	#edit- checking if it works without being assigned
        Pass=mainReturn[1]#number of pass found for the feature run
        Fail=mainReturn[2]#number of fails found for the feature run
        Empty=mainReturn[3]#number of empty found for the feature run
        result=mainReturn[4]#holds the path to the result folder for this run
        splitKPI=mainReturn[5]#array of the kpi values that was run
        splitDate=mainReturn[6]#array of datetime values that was run
        splitNode=mainReturn[7]#array of node_name values that was run
        HTMLFileM=mainReturn[8]#feature summary file
        resultDir=mainReturn[9]
        erbsArr=mainReturn[10]#used for auto matching
        erbsHeadArr=mainReturn[11]#used for auto matching
        KPIHeader=mainReturn[12]#used for auto matching
        dashHeaderArr=mainReturn[13]#used for auto matching
        dashArr=mainReturn[14]#used for auto matching
		#if a new value that can be used for auto matching was found add it to the array to be written to the file
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
		#if multi features were run creates a summary table that shows the summary for multiple features
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
            passNum=Pass
            failNum=Fail
            emptyNum=Empty
			#sets colour of row depending if it was a pass fail or empty
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
        #if it was a single feature run finishes the html summary table and writes it to the file 
        else:
            HTML_file= open(os.path.join(result,"Summary.html"),"w")
            urlSum=result +"\\Summary.html"#sets what summary table to auto open post executrion
            HTMLFileM=HTMLFile+ HTMLFileM +"""
            </table>
            </body>
            </html>
            """
            HTML_file.write(HTMLFileM) #Writes HTML String to the HTML summary file
            HTML_file.close()
    #If it was a multi feature run finishes the multiple feature summary table        
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
    #converts the arrays to strings and writes it to a file
    erbsNmeString=','.join(map(str, erbsNmeArr))
    headerNmeString=','.join(map(str, headerNmeArr))
    KPINmeString=','.join(map(str, KPINmeArr))
    dashHeaderNmeString=','.join(map(str, dashHeaderNmeArr))
    dashNmeString=','.join(map(str, dashNmeArr))

    headerFile=open(headerFilePath,"w")
    headerFileString="[Lists]\nheaderName=%s\n\nNodeName=%s\n\nKPIName=%s\n\ndash=%s\n\ndashHeader=%s" %(headerNmeString,erbsNmeString,KPINmeString,dashNmeString,dashHeaderNmeString)
    headerFile.write(headerFileString)
    headerFile.close()
#except Exception, msg:		#to debug COMMENT these 2 lines
 #   print '\nError: %s' % msg
finally:
    print("\nCompleted")
    crsr.close() #closes the cursor to the DB
    cnxn.close() #close the connection to the db
	#FOR DEBUGGING ERRORS COMMENT OUT FOLLOWING CODE
    
    if helpCom==1 and popUp=="on": 
		#auto opens the summary page after the script has completed running
		urlSum = ''	#edit-
		urlSum = 'file:{}'.format(pathname2url(os.path.abspath(urlSum)))
		webbrowser.open_new_tab(urlSum)