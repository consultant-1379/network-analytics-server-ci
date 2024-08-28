def editFeatureFunction(action, fname):
    import csv
    import os
    import sys
    import shutil
    import argparse
    import re
    from ConfigParser import SafeConfigParser
    from tabulate import tabulate
    from numbers import Number
    from ConfigParser import SafeConfigParser
    from datetime import datetime
	
    global SQLConfig
    global colNameArrTar
    global colNameSour
    global KPIHeader
    global numColumn
    global colNameTar
    global colNameArrSour
    global nameFeature
	
    SQLArr=[]
    resultSource=[]#Holds the source SQLs after formatting
    resultTarget=[]#Holds the target SQLs after formatting
    SQLReturn=[]#holds the kpi number and source and target sql without node_name configured for that kpi number
    SQLReturnS=[]#holds the kpi number and source and target sql with node_name configured for that kpi number
    SQLConfig=["","","","",""]#Holds values to be put into SQL strings
    path =os.getcwd()#gets current path

    #Paths to the csv files for each feature
    excelNewFeature=path+"\\excel\\SQLNewFeature.csv"
    excelReplace=path+"\\excel\\SQLReplace.csv"
    excelNewKPI=path+"\\excel\\SQLNewKPI.csv"
    excelDeleteKPI=path+"\\excel\\SQLDeleteKPI.csv"

    configPath=path+"\\configFiles\\editInitialConfig.ini"#Path to config file
    oldCode=path+"\\OldCode"#Folder that holds old code

    if fname!=None:
        if action == '-f':#If user picked the new feature command
            print '\nAction: adding the new feature',fname
            d = csv.reader(open(excelNewFeature))
            functionFlag="newFeature"#Flag that holds the current function
            nameFeature=fname#Holds the name of the feature the function is working on
        elif action == '-r':#If user picked the replace SQL command
            print '\nAction: replacing KPI(s)'
            d=csv.reader(open(excelReplace))
            functionFlag="replace"
            nameFeature=fname
        elif action == '-k':#If user picked the new KPI command
            print '\nAction: adding KPI(s)'
            d=csv.reader(open(excelNewKPI))
            functionFlag="newKPI"
            nameFeature=fname
        elif action == '-d':#If user picked the delete command
            print '\nAction: deleting KPI(s)'
            d=csv.reader(open(excelDeleteKPI))
            functionFlag="deleteKPI"
            nameFeature=fname
        elif action == '-df':#If user picked the delete feature command
            print '\nAction: deleting the %s feature' % fname
            functionFlag="deleteFeature"
            nameFeature=fname
    else:
        print '\nYou must enter an action and a feature name'	
		
		
    KPI=0#Holds the kpi ID number
    KPIAll=[]#Holds all the valid KPI ID numbers
    #Holds values used for auto matching
    colNameSour=[]
    colNameArrSour=[]
    colNameArrTar=[]
    colNameTar=[]
    KPIHeader=[]
    configParser = SafeConfigParser()
    configParser.read(configPath) #reads the information found in the config file
    SQLConfig[1]=configParser.get('settings', 'datetime')
    SQLConfig[2]=configParser.get('settings', 'node_name')

    date=datetime.now().strftime ("%Y-%m-%d")#Gets current datetime
    oldCodeDate=oldCode+"\\%s" %(date)#Path to oldcode folder with date as name
    oldCodeFolder=oldCodeDate+"\\%s"%(functionFlag)
    if not os.path.exists(oldCodeFolder):
        os.makedirs(oldCodeFolder)
    mainPathOG=oldCodeFolder+"\\MainPre%s.py"%(nameFeature)#Path to old code file 

    SQLFunctionPath=path+"\\src\\SQLFunction.py"
    if SQLConfig[2]=="" or SQLConfig[2]==None:#If no node_name was given
        noNode=1
    else:
        noNode=0
    #Strings used to create the files
    startString="""
    elif SQLConfig[4]=='%s':
    """

    stringSource="""
#%sa
    if SQLConfig[0]=="%s":
        if noNode==1:
            sourceSQL="%s
        else:
            sourceSQL="%s
#%sb
    """
    stringTarget="""
#%sx
    if SQLConfig[0] == "%s":
        if noNode==1:
            targetSQL="%s
        else:
            targetSQL="%s
#%sy
    """

    returnSource="""
    return sourceSQL\n"""

    returnTarget="""
	
    return targetSQL\n
    """

    configFileString="""[configuration]\nTYPE=%s\nKPI_VALUE=all\nDATETIME_ID=%s\nNODE_NAME=%s\n\ndecimalplaces=4
    """
    
    #Function That creates the new SQL function file
    def SQLFuncWrite(SQL,stringType,SQLReturn,SQLReturnS):
        firstString="""def SQLFunctionSource(SQLConfig,noNode):\n"""
        secondString="""\ndef SQLFunctionTarget(SQLConfig,noNode):\n"""
        if SQL=="source":
            returnStr=returnSource
            functionString=firstString
            startFile=""
            testopen=open(SQLFunctionPath,"w")
            testopen.close()
        elif SQL=="target":
            testopen=open(SQLFunctionPath,"r")
            startFile=testopen.read()
            testopen.close()
            returnStr=returnTarget
            functionString=secondString
        addin=""#string that holds the code to be written to the file
        
        #loops through array that holds the SQL
        for o,p in enumerate(SQLReturn):
            arr=SQLReturn[o]    #Gets the source and target sqls with only datetime configurable SQLReturn[o] =[kpi_ID,SourceSQL,targetSQL]
            arrS=SQLReturnS[o]  #Gets the source and target sqls with node_name and datetime configurable
            if SQL=="source":
                SQLCon=arr[1]
                SQLConS=arrS[1]

            elif SQL=="target":
                SQLCon=arr[2]
                SQLConS=arrS[2]

            KPI=arr[0]#gets the kpi number for current loop
            #depedning on what loop it is adds strings to addin with the sqls etc
            if o==0:
                addin=addin + functionString + stringType %(KPI,KPI,SQLConS,SQLCon,KPI)
            elif o==len(SQLReturn)-1:
                addin=addin+stringType %(KPI,KPI,SQLConS,SQLCon,KPI) + returnStr
            else:
                addin=addin+stringType %(KPI,KPI,SQLConS,SQLCon,KPI)
        #Write new code to file
        startFile=startFile+addin
        testopen=open(SQLFunctionPath,"w")
        testopen.write(startFile)
        testopen.close()

    #Function that excutes the SQLs and trys to automatch the columns
    def tableFunction(KPIAll,headerNameList,nodeNameList,KPINameList,dashList,dashHeaderList):
        from com.ziclix.python.sql import zxJDBC
        from SQLFunction import SQLFunctionSource
        from SQLFunction import SQLFunctionTarget
        from ConfigParser import SafeConfigParser
##leave strings unchanged or the script will not be generated in the correct format
        rowsSource=[]
        rowsTarget=[]
        sourceRows=[]
        targetRows=[]
        columnNameTar=[]
        columnNameSour=[]
        SQLConfig[4]=nameFeature
        colNameTar=[]
        colNameSour=[]
        #Flags used to see if the headers found from excuting the new sql were found in the lists that can be used for automatching
        KPIFlagTarget=0
        KPIFlagSource=0 
        headerFlagSource=0
        headerFlagTarget=0 
        dashHeaderFlagSource=0 
        dashHeaderFlagTarget=0
        EndappendSour=""
        EndappendTar=""
        EndListSour=""
        EndListTar=""
        rowConfig="""
        if SQLConfig[0]=='%s':\n"""
        appendCol="""            col%s.append(row[%s])\n"""
    
        appendListIf="""
    if SQLConfig[0]=='%s':
    """
    
        appendList="""    test%s=list(col%s)
    """
        decimalString="""    ForTest%s=[]
        for number in range(len(test%s)):
            if test%s[number] is not None:
                ForTest%s.append(math.floor(test%s[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest%s.append(test%s[number])"""
        rowsString="""
        rows = zip(%s)
        rows =sorted(rows,key=itemgetter(1))
"""
        returnString=[]
        try:
            print 'my test 2'
            cnxnStr =  "jdbc:sybase:Tds:atvts3464.athtem.eei.ericsson.se:2640/dwhdb"
            dbDriver = "com.sybase.jdbc4.jdbc.SybDriver"
            cnxn = zxJDBC.connect(cnxnStr, "dc", "dc", dbDriver) #db connection
            print 'Where the wild things play'
            crsr = cnxn.cursor(1)
            for p,y in enumerate(KPIAll):
                SQLConfig[0]=KPIAll[p]
                sourceResults=SQLFunctionSource(SQLConfig,noNode)
                targetResults=SQLFunctionTarget(SQLConfig,noNode)
                stringTest=""
                crsr.execute("%s" %(sourceResults)) #Executes the Chosen SQL command from SQLFunction
                descSour = crsr.description #Headings/description of the rows found in the SQL command results
                rowSour = crsr.fetchall() #Rows of data found in the SQL command results

                headerlineX=[]
                rowSourArr=[]
                colNumArrS=[]
                colNumArrT=[]
                rowTarArr=[]
                #For a column in the headers add it onto headerlineS
                for column in descSour:
                    headerlineX.append(column[0])
                for x,y in enumerate(headerlineX):
                    if headerlineX[x] in headerNameList:
                        headerFlagSource=1
                        headerColSource=x
                    elif headerlineX[x] in KPINameList:
                        KPIFlagSource=1
                        KPIColSource=x
                    elif headerlineX[x] in dashHeaderList:
                        dashHeaderFlagSource=1
                        dashHeaderSource=x
                    rowSourArr.append(str(rowSour[0][x]))
                    colNumArrS.append("column %s"%(x))
                    colNameSour.append(str(headerlineX[x]))
                for x,y in enumerate(rowSourArr):
                    if isinstance(rowSourArr[x], Number):
                        if headerlineX[x] not in KPIHeader and 'ID' not in headerlineX[x] and 'CELL' not in headerlineX[x] and 'NODE' not in headerlineX[x]:
                            KPIFlagSource=1
                            KPIColSource=x
                    if "_" in rowSourArr[x] and ("_oss_" not in rowSourArr[x] or "eniq" not in rowSourArr[x]):
                        underscore=rowSourArr[x].rfind("_")
                        erbsName=rowSourArr[x][:underscore]
                        if erbsName in nodeNameList:
                            headerFlagSource=1
                            headerColSource=x
                    if "-" in rowSourArr[x]:
                        dash=rowSourArr[x].rfind("-")
                        preDash=rowSourArr[x][:dash]
                        try:
                            test=int(preDash)
                            dashHeaderFlagSource=1
                            dashHeaderSource=x
                        except ValueError:
                            pass            

                HeaderSourList=headerlineX
                crsr.execute("%s" %(targetResults)) #Executes the Chosen SQL command from SQLFunction
                descTarget = crsr.description #Headings/description of the rows found in the SQL command results
                rowTar = crsr.fetchall() #Rows of data found in the SQL command results
                headerlineX=[]

                #For a column in the headers add it onto headerlineS
                for column in descTarget:
                    headerlineX.append(column[0])
                #Checks if the column header is found in the previous lists and if it is sets the relevant flags
                for x,y in enumerate(headerlineX):
                    if headerlineX[x] in headerNameList:
                        headerFlagTarget=1
                        headerColTarget=x
                    elif headerlineX[x] in KPINameList:
                        KPIFlagTarget=1
                        KPIColTarget=x
                    elif headerlineX[x] in dashHeaderList:
                        dashHeaderFlagTarget=1
                        dashHeaderTarget=x
                    rowTarArr.append(str(rowTar[0][x]))
                    colNameTar.append(str(headerlineX[x]))
                    colNumArrT.append("column %s"%(x))
                for x,y in enumerate(rowTarArr):
                    if isinstance(rowTarArr[x], Number):
                        if headerlineX[x] not in KPIHeader and 'ID' not in headerlineX[x] and 'CELL' not in headerlineX[x] and 'NODE' not in headerlineX[x]:
                            KPIFlagTarget=1
                            KPIColTarget=x
                    if "_" in rowTarArr[x] and ("_oss_" not in rowTarArr[x]  or "eniq" not in rowTarArr[x]):
                        underscore=rowTarArr[x].rfind("_")
                        erbsName=rowTarArr[x][:underscore]
                        if erbsName in nodeNameList:
                            headerFlagTarget=1
                            headerColTarget=x

                    if "-" in rowTarArr[x] and rowTarArr[x] != "EutrancellTDD" :
                        dash=rowTarArr[x].rfind("-")
                        preDash=rowTarArr[x][:dash]
                        try:
                            test=int(preDash)
                            dashHeaderFlagTarget=1
                            dashHeaderTarget=x
                        except ValueError:
                            pass

                if KPIFlagTarget==1 and KPIFlagSource ==1 and((headerFlagSource==1 and headerFlagTarget==1) or (dashHeaderFlagSource==1 and dashHeaderFlagTarget==1)): #If the flags that are needed to succesfully automatch the columns are set adds the column numbers to an array to be used when writing the code strings to the file
                    if headerFlagSource==1 and headerFlagTarget==1:
                        rowsSource.append(headerColSource)
                        rowsTarget.append(headerColTarget)
                    if dashHeaderFlagSource==1 and dashHeaderFlagTarget==1:
                        rowsSource.append(dashHeaderSource)
                        rowsTarget.append(dashHeaderTarget)
                    if KPIFlagTarget ==1 and KPIFlagSource==1:
                        rowsSource.append(KPIColSource)
                        rowsTarget.append(KPIColTarget)
                else:#if not enough of the flag were set prints put a sample table of the source and target where the user has to auto choose which columns to match
                    tableSour=[colNumArrS,colNameSour,rowSourArr]
                    print("\n\n\nKPI %s:\n\nSOURCE" %(SQLConfig[0]))
                    print tabulate(tableSour,tablefmt="grid")
                    
                    tableTar=[colNumArrT,colNameTar,rowTarArr]
                    print("\nTARGET")
                    print tabulate(tableTar,tablefmt="grid")
        
                    matchRow=raw_input("\nPlease choose the column numbers to match: ")
                    splitMatch=matchRow.split(",")

                    for x,y in enumerate(splitMatch):
                        splitMatch1=splitMatch[x].split("=")
                        rowsSource.append(splitMatch1[0])
                        rowsTarget.append(splitMatch1[1])
                   
                HeaderTarList=headerlineX
    #The code strings are then formatted using the column numbers provided above from auto matching or user defined
                for elem in rowsSource:
                    columnNameSour.append(HeaderSourList[int(elem)])
                for elem in rowsTarget:
                    columnNameTar.append(HeaderTarList[int(elem)]) 

                colNameTar1=[SQLConfig[0],columnNameTar]
                colNameArrTar.append(colNameTar1)
                colNameSour1=[SQLConfig[0],columnNameSour]
                colNameArrSour.append(colNameSour1)
                results=map(int,SQLConfig[0])
                #colArrTar.append(results+rowsTarget)

                testStrSour=rowConfig %(SQLConfig[0])
                testStr2Sour=appendListIf %(SQLConfig[0])
                for x,y in enumerate(rowsSource):
                    testStrSour=testStrSour+appendCol %(rowsSource[x],rowsSource[x])
                    if x<=len(rowsSource)-1:
                        sourceRows.append(rowsSource[x])
                    testStr2Sour=testStr2Sour +appendList %(rowsSource[x],rowsSource[x])
                    if x <len(rowsSource)-1:
                        stringTest=stringTest +"test%s," %(rowsSource[x])
                    elif x==len(rowsSource)-1:
                        stringTest=stringTest +"ForTest%s" %(rowsSource[x])
                        cntS=rowsSource[x]
                rowStringSour=rowsString %(stringTest)
                stringTest=""
                testStrTar=rowConfig %(SQLConfig[0])
                testStr2Tar=appendListIf %(SQLConfig[0])
                for x,y in enumerate(rowsTarget):
                    testStrTar=testStrTar+appendCol %(rowsTarget[x],rowsTarget[x])
                    if x<=len(rowsTarget)-1:
                        targetRows.append(rowsTarget[x])
                    testStr2Tar=testStr2Tar +appendList %(rowsTarget[x],rowsTarget[x])
                    
                    if x <len(rowsTarget)-1:
                        stringTest=stringTest +"test%s," %(rowsTarget[x])
                    elif x==len(rowsTarget)-1:
                        stringTest=stringTest +"ForTest%s" %(rowsTarget[x])
                        cntT=rowsTarget[x]
                rowStringTar=rowsString %(stringTest)
                stringTest=""
                if p==len(KPIAll)-1:
                    EndappendSour=EndappendSour+testStrSour+"\n#1st\n"
                    EndListSour=EndListSour+testStr2Sour+decimalString %(cntS,cntS,cntS,cntS,cntS,cntS,cntS)+rowStringSour+"\n#2nd\n"
                    EndappendTar=EndappendTar+testStrTar+"\n#3rd\n"
                    EndListTar=EndListTar+testStr2Tar+decimalString %(cntT,cntT,cntT,cntT,cntT,cntT,cntT)+rowStringTar+"\n#4th\n"
                else:
                    EndappendSour=EndappendSour+testStrSour
                    EndListSour=EndListSour+testStr2Sour+decimalString %(cntS,cntS,cntS,cntS,cntS,cntS,cntS)+rowStringSour
                    EndappendTar=EndappendTar+testStrTar
                    EndListTar=EndListTar+testStr2Tar+decimalString %(cntT,cntT,cntT,cntT,cntT,cntT,cntT)+rowStringTar

                EndTar=EndappendTar+EndListTar#Segment of code used in the sourcewrite function 
                EndSour=EndappendSour+EndListSour#segment in code used in the targetwrite function
                testStrSour=""
                testStr2Sour=""
                testStrTar=""
                testStr2Tar=""
                rowsSource=[]
                rowsTarget=[]
                targetRows=[]
                sourceRows=[]
                colNameSour=[]
                colNameTar=[]
                columnNameTar=[]
                columnNameSour=[]
            returnString.append(EndSour)
            returnString.append(EndTar)

            return returnString
        except SQLException, msg:
            print 'Error 2: ', msg
        finally:
            print("\nCompleted")
            crsr.close() #closes the cursor to the DB
            cnxn.close() #close the connection to the db

    #function that creates the new feature main file using strings with sample code modified useing the new features name
    def featureMainFunc(KPIAll,nameFeature,sourReturn,tarReturn):
        global readMain
        startFile=""
        #Used to keep string formatters in a string for future use
        qouteString='"""'
        String="%s"
        float="%d"
        PercenString="%"

        testopen=open(mainPathOG,"r+")
        testopen.close()
        sourceStringA="""def sourceWrite%s(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):
    crsr.execute("%s" %s(sourceResults))
    import os
    import math
    from operator import itemgetter
    from numbers import Number
    global sourceHyper#hyper link used in the html tables
    global targetHyper#hyper link used in the html tables
    global resultHyper#hyper link used in the html tables
    global summaryHyper#hyper link used in the htnml tables
    HTMLTest=HTMLTable #Local variable version of HTMLTable
    #List of different array names named after the headers found in the various KPI_ID tables that are needed for comparing against the target tables
    col0=[]
    col1=[]
    col2=[]
    col3=[]
    col4=[]
    col5=[]
    headerName=[]
    descSour = crsr.description #Headings/description of the rows found in the SQL command results
    rowSour = crsr.fetchall() #Rows of data found in the SQL command results""" %(nameFeature,String,PercenString)
    
        sourceStringB="""    
    if not os.path.exists(result):
        os.makedirs(result)
    SourceFile= open(os.path.join(result,'%s_%s_%s_Source_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace)),'w+')
    sourceHyper=os.path.join(result,'%s_%s_%s_Source_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace))
    targetHyper=os.path.join(result,'%s_%s_%s_Target_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace))
    resultHyper=os.path.join(result,'%s_%s_%s_Results_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace))
    summaryHyper=os.path.join(result,'Summary.HTML')""" %(String,String,String,nameFeature,PercenString,String,String,String,nameFeature,PercenString,String,String,String,nameFeature,PercenString,String,String,String,nameFeature,PercenString)
    
        sourceStringC="""
    headerlineS = ''
    for column in descSour:
        headerlineS=headerlineS + "\\n<th>%s</th>" %(str(column[0]))
        headerName.append(str(column[0]))
      
    headerlineS=headerlineS + "\\n<tr>\\n" #Ends the row of headers
    HTMLTest=HTMLTest+headerlineS #add the headers into the HTML string


    #For a row in the row of data and a row and then add this row to the HTML String
    for row in rowSour:
        datalineS="\\n<tr>\\n"
        cnt=0
        for column in row:
            try:
                if isinstance(column, Number):
                    if headerName[cnt] not in KPIHeader and 'ID' not in headerName[cnt] and 'CELL' not in headerName[cnt] and 'NODE' not in headerName[cnt]:
                        KPIHeader.append(headerName[cnt])
                if "_" in column and ("_oss_" not in column or "eniq" not in column):
                    underscore=column.rfind("_")
                    erbsName=column[:underscore]
                    if headerName[cnt] not in erbsHeadArr:
                        erbsHeadArr.append(headerName[cnt])
                    if erbsName not in erbsArr:
                        erbsArr.append(erbsName)
                if "-" in column:
                    dash=column.rfind("-")
                    preDash=column[:dash]
                    try:
                        test=int(preDash)
                        if headerName[cnt] not in dashHeader:
                            dashHeader.append(headerName[cnt])
                        if preDash not in dashArr:
                            dashArr.append(preDash)
                    except ValueError:
                        pass
            except TypeError:
                pass
            cnt=cnt+1
            datalineS=datalineS + "<td>%s</td>\\n" %(str(column))
        datalineS=datalineS +"<tr>\\n"
        HTMLTest=HTMLTest+datalineS

    """
        sourceStringD=""" 
    HTMLTest =HTMLTest +"\\n<h1>Source results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>"%s(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    HTMLTest=HTMLTest +"<h4><a href='%s'>Target</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></h4>\\n"%s (targetHyper,resultHyper,summaryHyper)
    SourceFile.write(HTMLTest)    
    SourceFile.close()
    return rows\n"""%(String,String,String,PercenString,String,String,String,PercenString)
        
        targetStringA="""def targetWrite%s(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):  
    crsr.execute("%s" %s(targetResults))
    from numbers import Number
    import os
    import math
    from operator import itemgetter
    descTar= crsr.description
    rowTar= crsr.fetchall()
    global targetHyper
    global sourceHyper
    global resultHyper
    global summaryHyper
    col0=[]
    col1=[]
    col2=[]
    col3=[]
    col4=[]
    col5=[]
    HTMLTest=HTMLTable
    datalineT=dataline"""%(nameFeature,String,PercenString)
    
        targetStringB="""
    if not os.path.exists(result):
        os.makedirs(result)  
    targetSQL= open(os.path.join(result,'%s_%s_%s_Target_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace)),'w') #opens the file needed to write the results
    #Some arrays named after the headers found in the tables for the different 
    headerlineT = ''
    headerName=[]
    #For a column/header in the row of headers add the header to headerlineT
    for column in descTar:
        headerlineT=headerlineT + "\\n<th>%s</th>" %s(str(column[0]))
        headerName.append(str(column[0]))
    headerlineT=headerlineT + "\\n<tr>\\n"
    HTMLTest=HTMLTest+headerlineT #Add the row of headers to the HTML string
    
    #For a individual row in a the group of rows add the elements in the row one by one to the HTML string 
    for row in rowTar:
        cnt=0
        datalineT="\\n<tr>\\n"
        for column in row:
            try:
                if isinstance(column, Number) :
                    if headerName[cnt] not in KPIHeader and 'ID' not in headerName[cnt] and 'CELL' not in headerName[cnt] and 'NODE' not in headerName[cnt]:
                        KPIHeader.append(headerName[cnt])
                if "_" in column and ("_oss_" not in column or "eniq" not in column):
                    underscore=column.rfind("_")
                    erbsName=column[:underscore]
                    if headerName[cnt] not in erbsHeadArr:
                        erbsHeadArr.append(headerName[cnt])
                    if str(erbsName) not in erbsArr:
                        erbsArr.append(erbsName)
                if "-" in column:
                    dash=column.rfind("-")
                    preDash=column[:dash]
                    try:
                        test=int(preDash)
                        if headerName[cnt] not in dashHeader:
                            dashHeader.append(headerName[cnt])
                        if preDash not in dashArr:
                            dashArr.append(preDash)
                    except ValueError:
                        pass
            except TypeError:
                pass
            cnt=cnt+1
            datalineT=datalineT + "<td>%s</td>\\n" %s(str(column))
        datalineT=datalineT +"<tr>\\n"
        HTMLTest=HTMLTest+datalineT
    """ %(String,String,String,nameFeature,PercenString,String,PercenString,String,PercenString)
        
        targetStringC="""
    HTMLTest =HTMLTest +"\\n<h1>Target results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>"%s(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    HTMLTest=HTMLTest +"<h4><a href='%s'>Source</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></H4>\\n"%s(sourceHyper,resultHyper,summaryHyper)
    targetSQL.write(HTMLTest) 
    targetSQL.close()
    return rows\n""" %(String,String,String,PercenString,String,String,String,PercenString)
    
        resultsStringA="""def resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig):
    import os
    import sys
    rowsBx =rowsTarget
    global sourceHyper
    global targetHyper
    global resultHyper
    global summaryHyper
    HTMLResults=HTMLTable
    HTMLFileMix=""
    rowResults=[]
    HTMLFileM=""
    resultReturn=[]
    Fail=0
    Pass=0
    Empty=0
    w=0 #counter used for non matches for source table
    x=0 #counter used for total matches
    y=0 #counter used for non matches for target table
    z=0 #counter used for total partial matches
    noMatchSour=[] #array that source values are added to if no match or partial match is found for the value
    noMatchTar=[] #array that target values are added to if no match or partial match is found for the value
    parMatch = [] #array that values are added to after no full match is found between the source and target tables    
    results= open(os.path.join(result,'%s_%s_%s_Results_%s.HTML' %s(SQLConfig[0],SQLConfig[2],noSpace)),'w')
    if SQLConfig[1] != "" and SQLConfig[2] == "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s </h1>" %s(SQLConfig[0],SQLConfig[1])
    elif SQLConfig[1] != "" and SQLConfig[2] != "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s AND NODE_NAME: %s </h1>"%s(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    
    """%(String,String,String,nameFeature,PercenString,String,String,PercenString,String,String,String,PercenString)
    
        resultsStringB2="""
    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\\n<th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>" #Adds the headers for the table in the file
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='2'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='2'><a href='%s'>Target</a></th>\\n</tr>\\n" %s(sourceHyper,targetHyper)
        \n"""%(String,String,String,String,String,String,String,String,String,String)

        resultsStringB3="""
    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=3
        HTMLResults=HTMLResults + "<tr><th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>"
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='3'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='3'><a href='%s'>Target</a></th>\\n</tr>" %s(sourceHyper,targetHyper)"""%(String,String,String,String,String,String,String,String,String,String,String,String)
    
        resultsStringB4="""
    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=4
        HTMLResults=HTMLResults + "<tr><th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th><th>%s</th>\\n</th>\\n<th>%s</th>\\n<th>%s</th><th>%s</th>\\n\\n<th>%s</th>\\n</tr>"
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='4'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='4'><a href='%s'>Target</a></th>\\n</tr>\\n" %s(sourceHyper,targetHyper)""" %(String,String,String,String,String,String,String,String,String,String,String,String,String,String)
    
        resultStringC="""
    headerName=["Match Type"]+ColumnNameSour+[""]+ColumnNameTar
    if numColumn==2:
        rowResults.append(("","Source","","","Target","",""))
    elif numColumn==3:
        rowResults.append(("","Source","","","","Target","",""))
    elif numColumn==4:
        rowResults.append(("","Source","","","","","Target","","",""))    
    for counter,n in enumerate(rowsSource): #For the array of values for comparison from the source table if there is no values found in the target list add the specific source elemnent to noMatchSour
        if len(rowsTarget)==0:
            noMatchSour.append(rowsSource[counter])
        for counter1,m in enumerate(rowsTarget): #nested for loop to go through the entire array of elements in the comparison array for the target table 
            if rowsSource[counter] == rowsTarget[counter1]:
                rowResults.append((("MATCH",)+n+("",)+m))
                if numColumn==2:
                    HTMLResults=HTMLResults + "<tr bgcolor='#00FF00'><td>MATCH</td>\\n<td>%s</td>\\n<td>%s</td>\\n<th></th>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(n[0]),str(n[1]),str(m[0]),str(m[1]))
                elif numColumn==3:
                    HTMLResults=HTMLResults + "<tr bgcolor='#00FF00'><td>MATCH</td>\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n<th></th>\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(n[0]),str(n[1]),str(n[2]),str(m[0]),str(m[1]),str(m[2]))
                elif numColumn==4:
                    HTMLResults= HTMLResults+ "<tr bgcolor='#00FF00'>\\n<th>MATCH</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>" %(str(n[0]),str(n[1]),str(n[2]),str(n[3]),str(m[0]),str(m[1]),str(m[2]),str(m[3])) 
                x=x+1
                break
            if counter1 == len(rowsTarget)-1:
                parMatch.append(rowsSource[counter])
    if numColumn==2:
        rowResults.append(("","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='6'></th></tr>\\n"
    elif numColumn==3:
        HTMLResults=HTMLResults + "<tr><th colspan='8'></th></tr>\\n"
        rowResults.append(("","","","","","","",""))
    elif numColumn==4:
        rowResults.append(("","","","","","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='10'></th></tr>\\n"

    for counter2,p in enumerate(parMatch):
        for counter3,q in enumerate(rowsTarget):
            if p[0] == q[0]:
                rowResults.append((("PARTIAL MATCH",)+p+("",)+q))
                if numColumn==2:
                    HTMLResults=HTMLResults + "<tr bgcolor='#FF0000'><td>PARTIAL MATCH</td>\\n<td>%s</td>\\n<td>%s</td>\\n<td></td>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(p[0]),str(p[1]),str(q[0]),str(q[1]))
                elif numColumn==3:
                    HTMLResults=HTMLResults + "<tr bgcolor='#FF0000'><td>PARTIAL MATCH\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n<th></th>\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(p[0]),str(p[1]),str(p[2]),str(q[0]),str(q[1]),str(q[2]))
                elif numColumn==4:
                    HTMLResults= HTMLResults+ "<tr bgcolor='#FF0000'>\\n<th>PARTIAL MATCH</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>" %(str(p[0]),str(p[1]),str(p[2]),str(p[3]),str(q[0]),str(q[1]),str(q[2]),str(q[3])) 
                z=z+1
                break
            elif counter3 == len(rowsTarget)-1:
                noMatchSour.append(parMatch[counter2])
    if numColumn==2:
        rowResults.append(("","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='6'></th></tr>\\n"
    elif numColumn==3:
        HTMLResults=HTMLResults + "<tr><th colspan='8'></th></tr>\\n"
        rowResults.append(("","","","","","","",""))
    elif numColumn==4:
        rowResults.append(("","","","","","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='10'></th></tr>\\n"

    for counter,b in enumerate(noMatchSour):
        if numColumn==2:
            rowResults.append((("NO MATCH",)+b+("","","")))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\\n<td>NO MATCH</td>\\n<td>%s</td>\\n<td>%s</td>\\n<td></td>\\n<th colspan='2'></th>\\n</tr>\\n" %(str(b[0]),str(b[1]))
        elif numColumn==3:
            rowResults.append((("NO MATCH",)+b+("","","","")))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\\n<td>NO MATCH</td>\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n<td></td>\\n<th colspan='3'></th>\\n</tr>\\n" %(str(b[0]),str(b[1]),str(b[2]))
        elif numColumn==4:
            rowResults.append((("NO MATCH",)+b+("","","","","")))
            HTMLResults= HTMLResults+ "<tr bgcolor='#FFFF00'>\\n<th>NO MATCH</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th></th>\\n<th colspan='6'></th>\\n</tr>" %(str(b[0]),str(b[1]),str(b[2]),str(b[3])) 
        w=w+1    
    for counter5,g in enumerate(rowsBx):
        if len(rowsSource)==0:
            noMatchTar.append(rowsBx[counter5])
        for counter6,h in enumerate(rowsSource):
            if g[0]==h[0] and g[1] == h[1]:
                break
            elif counter6== len(rowsSource)-1:
                noMatchTar.append(rowsBx[counter5])
    for counter,c in enumerate(noMatchTar):
        if numColumn==2:
            rowResults.append((("NO MATCH",)+("","","")+c))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\\n<td>NO MATCH</td>\\n<th colspan='2'></th>\\n<td></td>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(c[0]),str(c[1])) 
        elif numColumn==3:
            rowResults.append((("NO MATCH",)+("","","","")+c))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\\n<td>NO MATCH</td>\\n<th colspan='3'></th>\\n<td></td>\\n<td>%s</td>\\n<td>%s</td>\\n<td>%s</td>\\n</tr>\\n" %(str(c[0]),str(c[1]),str(c[2])) 
        elif numColumn==4:
            rowResults.append((("NO MATCH",)+("","","","","",)+c))
            HTMLResults= HTMLResults+ "<tr bgcolor='#FFFF00'>\\n<th>NO MATCH</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th></th>\\n<th colspan='6'></th>\\n</tr>" %(str(c[0]),str(c[1]),str(c[2]),str(c[3])) 
        y=y+1

    HTMLResults=HTMLResults+"\\n</table>\\n</body>\\n</html>"
    results.write(HTMLResults)
    sys.stdout.write('.')
    sys.stdout.flush()

    results.close() 
    if z>0:
        passFail="Fail"
        HTMLFileMix=HTMLFileMix +'\\n<tr bgcolor="#FF0000">\\n' #changes color of row in summary table
        Fail=Fail+1
    elif (x+z+w)==0 and (x+z+y)==0:
        passFail="Empty Sour & Tar"
        HTMLFileMix=HTMLFileMix +'\\n<tr bgcolor="#FFFF00">\\n'
        Empty=Empty+1
    elif (x+z+y)==0:
        passFail="Empty Tar"
        HTMLFileMix=HTMLFileMix +'\\n<tr bgcolor="#FFFF00">\\n'
        Empty=Empty+1
    elif (x+z+w)==0:
        passFail="Empty Sour"
        HTMLFileMix=HTMLFileMix +'\\n<tr bgcolor="#FFFF00">\\n'
        Empty=Empty+1
    else:
        passFail="Pass"
        HTMLFileMix=HTMLFileMix +'\\n<tr bgcolor="#00FF00">\\n'
        Pass=Pass+1"""
    
        resultStringD="""
    HTMLFileMix= HTMLFileMix + '''

        <td>%s</td>
        <td><a href="%s">%s,%s,%s</a></td>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
        <td>%s</td>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
    </tr> ''' %(passFail,resultHyper,SQLConfig[0],SQLConfig[1],SQLConfig[2],x,z,w,x+z+w,"    ",x,z,y,x+y+z,)
    
    HTMLFileM=HTMLFileM+HTMLFileMix

    y=0
    x=0
    w=0
    z=0
    resultReturn=[HTMLFileM,Pass,Fail,Empty]
    return resultReturn 
    """

        MainStringA="""\ndef %sMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,typeFeat,crsr,decimalplaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList):
    from ConfigParser import SafeConfigParser
    from com.ziclix.python.sql import zxJDBC
    from operator import is_not
    from %sSQLFunction import SQLFunctionSource
    from %sSQLFunction import SQLFunctionTarget

    import datetime
    import sys
    global dataline
    dataline="<tr>\\n"
    sys.stdout.flush()
    global noNode #set to 1 if there is no node_name given in the config file
    noNode=0
    global helpCom
    helpCom=0 #variable that is set to 1 if any other command line argument aside from help (-h) is used  
    counterArr=0
    dateTime=[]
    Fail=0
    Pass=0
    Empty=0
    multiCom=0
    decimalPlaces=decimalplaces
    TYPE=typeFeat
    #6thStart
    %sKPI=%s
    #6thEnd
    lenKPI=len(%sKPI)
    """ %(nameFeature,nameFeature,nameFeature,nameFeature,KPIAll,nameFeature)
    
        MainStringB="""
    noSpace=''
    result_path%s= path+"\\Results\\\%s"
    result=result_path%s+"\\%s" %s(noSpace)

    counterArr=0

    headerline="<tr>\\n"
    headerlineX=""

    HTMLFileM=""
    typeArr=[]
    erbsArr=[]
    if len(nodeNameList)>0:
        erbsArr=nodeNameList.split(",")
    else:
        erbsArr=[]
    if len(headerNameList)>0:
        erbsHeadArr=headerNameList.split(",")
    else:
        erbsHeadArr=[]
    if len(KPINameList)>0:
        KPIHeader=KPINameList.split(",")
    else:
        KPIHeader=[]
    if len(dashHeaderList)>0:
        dashHeader=dashHeaderList.split(",")
    else:
        dashHeader=[]
    if len(dashList)>0:
        dashArr=dashList.split(",")
    else:
        dashArr=[]

    multiCom=0
    
    #Part of the HTML code for the Summary File

    #Part of the Html code needed for a HTML Table (Used in source and target tables)
    
    HTMLTable='''<!DOCTYPE html>
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
    <table style="width:100%s">
    '''
    splitDate= DATETIME_ID.split(',') #splits the string of datetime_id on the commas so multiple date time values can be used
    for x,y in enumerate(splitDate):
        if ">" in splitDate[x]: #Checks if a range of values is wanted
            dateSF=splitDate[x].split(">") #Splits the string on the arrow to get the start date time and end date time
            dateSF[0]=dateSF[0].split(" ") #Splits the start date and the start time
            dateStart=dateSF[0][0].split("-") #Splits the start date into an array that holds year, month and day
            timeStart=dateSF[0][1].split(":") #Sets a variable equal to the time that was used
            dateSF[1]=dateSF[1].split(" ") #Splits the end date and the end time
            timeFin=dateSF[1][1].split(":")
            dateFin=dateSF[1][0].split("-") #Splits the end date into an array that holds year, month and day
            dateStart = map(int,dateStart ) #Converts the year, month and day array to have int values
            timeStart=map(int,timeStart)
            dateFin=map(int,dateFin)
            timeFin=map(int,timeFin)
            d1 = datetime.datetime(dateStart[0], dateStart[1], dateStart[2],timeStart[0],timeStart[1],timeStart[2]) #Places the start year month and day into the date function
            d2 = datetime.datetime(dateFin[0], dateFin[1], dateFin[2],timeFin[0],timeFin[1],timeFin[2]) #Places the end year month and day into the date function
            l=[]
            while d1<=d2:
                l.append(d1)
                if configTime=="days":
                    d1+=datetime.timedelta(days=timeElem) 
                elif configTime=="hours":
                    d1+=datetime.timedelta(hours=timeElem)
                elif configTime=="minutes":
                    d1+=datetime.timedelta(minutes=timeElem)
                elif configTime=="hoursNone":
                    d1+=datetime.timedelta(hours=timeElem)
    
            l= [t.strftime("%sY-%sm-%sd %sH:%sM") for t in l]
            dateTime=dateTime + l
        else:
            dateTime.append(splitDate[x]) #if not arrow was found add the indivual date to the array of datetimes
    splitDate=dateTime
    noSpace =','.join(splitDate) #converts the list into a string to be used for the names of the files-
    """ %(nameFeature,nameFeature,nameFeature,String,PercenString,PercenString,PercenString,PercenString,PercenString,PercenString,PercenString)

        MainStringC="""    
    if configType !="multi":
        if KPI_VALUE =="all":
            splitKPI=%sKPI
        else:
            splitKPI= KPI_VALUE.split(',') #splits the string of KPI_values on the commas so multiple date time values can be used
            for x,y in enumerate(splitKPI):
                if ">" in splitKPI[x]: # Checks if a dash is found which indicates a range of values is desired
                    splitKPI[x]= "ww"+splitKPI[x]+"zz"
                    dash=splitKPI[x].index(">") #splits the enumerated element on the dash for the start KPI and end KPI
                    try:
                        test=int(splitKPI[x][dash+2])
                        high=int(splitKPI[x][dash+1]+splitKPI[x][dash+2]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    except ValueError:
                        high=int(splitKPI[x][dash+1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    try:
                        test=int(splitKPI[x][dash-2])
                        low=int(splitKPI[x][dash-2]+splitKPI[x][dash-1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    except ValueError:
                        low=int(splitKPI[x][dash-1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    
                    KPIrange=(range(low,high+1)) #Creates a list of the numbers between the high and low KPI
    
                    for elem,i in enumerate(KPIrange): #for the values in KPI range, converts them to strings and then adds them to splitKPI
                        KPIrange[elem]=str(KPIrange[elem])
                    splitKPI=splitKPI + KPIrange
                    del splitKPI[x] #Deletes the element in splitKPI that was used to find the range as its not needed
                elif ">" in splitKPI[x-1] : #Similar to above if statement but checks the previous element from the counter x. This is due to possibly deleting a range value previously
                    dash=splitKPI[x-1].index(">")
                    try:
                        test=int(splitKPI[x][dash+2])
                        high=int(splitKPI[x][dash+1]+splitKPI[x][dash+2]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    except IndexError:
                        high=int(splitKPI[x][dash+1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    try:
                        low=int(splitKPI[x][dash-2]+splitKPI[x][dash-1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    except IndexError:
                        test=int(splitKPI[x][dash-2])
                        low=int(splitKPI[x][dash-2]+splitKPI[x][dash-1]) #Finds the end KPI using the index of the dash in the string and setting 'high' equal to the next two characters
                    KPIrange=(range(low,high+1))
                    for elem,i in enumerate(KPIrange):
                        KPIrange[elem]=str(KPIrange[elem])
                    splitKPI=splitKPI + KPIrange
                    del splitKPI[x-1]
    else:
        splitKPI=%sKPI
    """%(nameFeature,nameFeature)
    
        MainStringD="""
    if NODE_NAME =='' or NODE_NAME== None:
        splitNode=[""]
        #nested for loops to go through all the possibly configrations of the multiple KPI's and Dates
        for x,i in enumerate(splitKPI):
            counterArr=counterArr+1
            for a,b in enumerate(splitDate):
                sys.stdout.write('.')
                sys.stdout.flush()
                noSpace = splitDate[a].replace(":", "_") #Replace the : character in the datetime with a _ for compatibility 
                SQLConfig=[] #array used to store the configuration information ie. KPI and Datetime_id
                #Add relevant values for that nested configuration run to SQLConfig
                SQLConfig.append(splitKPI[x])
                SQLConfig.append(splitDate[a])
                SQLConfig.append("")
                SQLConfig.append(splitNode19[0])
                SQLConfig.append(TYPE)
                noNode=1
                #Checks what feature was choosen in the configFiles
                if SQLConfig[0] in %sKPI: 
                    sourceResults=SQLFunctionSource(SQLConfig,noNode)
                    targetResults=SQLFunctionTarget(SQLConfig,noNode)
                    rowsSource= sourceWrite%s(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                    rowsTarget= targetWrite%s(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                    resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig)
                    HTMLFileM +=resultReturn[0]
                    Pass+=resultReturn[1]
                    Fail+=resultReturn[2]
                    Empty+=resultReturn[3]
                    returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_path%s,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]

    #8th
    else: #if a node name is given to configure by
        NODE_NAME.split(",")# split the string on the , to allow for multiple node_names to be used
        #Nested for loops to go through all the possible configurations for multiple KPI,Date and Node_name values
        for l,i in enumerate(splitKPI):
            counterArr=counterArr+1
            for y,p in enumerate(splitNode):
                for a,b in enumerate(splitDate):
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    noSpace = splitDate[a].replace(":", "_") #Replace the : character in the datetime with a _ for compatibility 
                    SQLConfig=[] #array used to store the configuration information ie. KPI and Datetime_id
                    #Add relevant values for that nested configuration run to SQLConfig
                    SQLConfig.append(splitKPI[l])
                    SQLConfig.append(splitDate[a])
                    SQLConfig.append(splitNode[y])
                    SQLConfig.append("")
                    SQLConfig.append(TYPE)
                    if SQLConfig[0] in %sKPI:
                        sourceResults=SQLFunctionSource(SQLConfig,noNode)
                        targetResults=SQLFunctionTarget(SQLConfig,noNode)
                        rowsSource= sourceWrite%s(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        rowsTarget= targetWrite%s(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig)
                        HTMLFileM +=resultReturn[0]
                        Pass+=resultReturn[1]
                        Fail+=resultReturn[2]
                        Empty+=resultReturn[3]
                        returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_path%s,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]
    return returnArr
    """ %(nameFeature,nameFeature,nameFeature,nameFeature,nameFeature,nameFeature,nameFeature,nameFeature)

        startFile=startFile+sourceStringA+sourceStringB+sourceStringC+sourReturn+sourceStringD#Adds the source string to string holder
        startFile=startFile+targetStringA+targetStringB+tarReturn+targetStringC#adds the target code strings to the string holder
        startFile=startFile+resultsStringA#adds one of the results strings
        #Adds the next results string depending on how many columns were used for matching
        for x,y in enumerate(colNameArrTar):
            kpi=colNameArrTar[x][0]
            colNmeTar=colNameArrTar[x][1]
            colNmeSour=colNameArrSour[x][1]
            numColumn=len(colNmeTar)

            if numColumn==2:
                startFile=startFile+resultsStringB2 %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeTar[0],colNmeTar[1],String,String,PercenString)
            elif numColumn==3:
                startFile=startFile+resultsStringB3 %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeSour[2],colNmeTar[0],colNmeTar[1],colNmeTar[2],String,String,PercenString)
            elif numColumn==4:
                startFile=startFile+resultsStringB4 %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeSour[2],colNmeSour[3],colNmeTar[0],colNmeTar[1],colNmeTar[2],colNmeTar[3],String,String,PercenString)
        startFile=startFile+"\n#5th\n"+resultStringC+resultStringD
        startFile=startFile+MainStringA+MainStringB+MainStringC+MainStringD
    #Writes the new feature main file         
        testopen=open(featureSrcMain,"w")
        testopen.write(startFile)
        testopen.close()    
    #Function that modifies the main scripts main file to add compataility with the new feature
    def scriptWriteMain(nameFeature,srcMainPath):
        print 'The scriptWriteMain is running!'
        if functionFlag=="newFeature":
            #Three strings that are used to modify the main file
            firstString="import %s.%sMain as %sMain\n" %(nameFeature,nameFeature,nameFeature)
            secondString='"%s",' %(nameFeature)
            thirdString="""        elif TYPE=="%s":
            mainReturn=%sMain.%sMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,TYPE,crsr,decimalPlaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList)\n""" %(nameFeature,nameFeature,nameFeature)
            #Reads in the files contents and looks for the comment number then adds in the relevant string from above depending on what comment number it is
            testopen=open(srcMainPath,"r+")
            read=testopen.read()
            testopen.close()
            d=read.find("#1st")
            startFile=read[:d]
            startFile=startFile+firstString
            endFile=read[d:]
            replaceFile=startFile+endFile
            testopen=open(srcMainPath,"w")
            testopen.write(replaceFile)
            testopen.close()
            
            testopen=open(srcMainPath,"r+")
            read=testopen.read()
            testopen.close()
            startD=read.find("#2ndStart")
            EndD=read.find("#2ndEnd")
            startFile=read[:startD+18]
            endFile=read[EndD-2:]
            array=read[startD+18:EndD-2]
            startFile=startFile+secondString
            replaceFile=startFile+array+endFile
            testopen=open(srcMainPath,"w")
            testopen.write(replaceFile)
            testopen.close()
            
            testopen=open(srcMainPath,"r+")
            read=testopen.read()
            testopen.close()
            d=read.find("#3rd")
            startFile=read[:d]
            startFile=startFile+thirdString
            endFile=read[d:]
            replaceFile=startFile+endFile
            testopen=open(srcMainPath,"w")
            testopen.write(replaceFile)
            testopen.close()
        #For deleteing a feature it does the opposite of above and looks for the comment numbers and deletes the features line/part of the code found there
        elif functionFlag=="deleteFeature":
        
            section=["#1st","#2ndStart","#3rd"]
            fileString=""
            testopen=open(srcMainPath,"r")
            fileString=testopen.read()
            testopen.close()

			##remove the import
            featureImport="import %s.%sMain as %sMain" %(nameFeature,nameFeature,nameFeature)
            importIndex = fileString.find(featureImport)
            if importIndex!=-1:
                newlineIndex=fileString.find('\n',importIndex+1)
                fileString=fileString[:importIndex]+fileString[newlineIndex+1:]

            ##remove from array of features
            element='"%s"' % nameFeature
            indexInArr=fileString.find(element)
            if indexInArr!=-1:
                indexNextQuote=fileString.find('"',indexInArr+1)	#index of the quote to end the feature referance
                if indexNextQuote!=-1 and fileString[indexNextQuote+1]==',': #if a comma follows nameFeature
                    fileString=fileString[:indexInArr]+fileString[indexNextQuote+2:]	#remove from " to comma
                elif indexNextQuote!=-1: #no comma next
                    fileString=fileString[:indexInArr-1]+fileString[indexNextQuote:]	#remove from " before the nameFeature to the next "

            ##remove featureCall
            featureCall='        elif TYPE=="%s"' % nameFeature
            startIndex=fileString.find(featureCall)
            if startIndex!=-1:
                endIndex=fileString.find('dashList)',startIndex+1)
                nextlineIndex=fileString.find('\n',endIndex)
                fileString=fileString[:startIndex]+fileString[nextlineIndex+1:]
            testopen=open(srcMainPath,"w")
            testopen.write(fileString)
            testopen.close()

    #Function used to replace, add  or delete a kpi's sql found in the features sql file
    def replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag):
        startFile=''
        if functionFlag=="replace":
            replaceStringSource="""    if SQLConfig[0]=="%s":
        if noNode==1:
            sourceSQL="%s
        else:
            sourceSQL="%s\n"""
            replaceStringTarget="""    if SQLConfig[0]=="%s":
        if noNode==1:
            targetSQL="%s
        else:
            targetSQL="%s\n"""
            for o,p in enumerate(SQLReturn):
                arr=SQLReturn[o]
                arrS=SQLReturnS[o]
                KPI=arr[0]
                #looks for the kpi numbers a and b comment and then replaces what is found inside those comments with the new source sql
                if SQL=="source":
                    if arr[1]=="" or arr[1]==None:
                        break
                    else:
                        SQLCon=arr[1]
                        SQLConS=arrS[1]
                        start=updateString.find("#%sa" %(KPI))
                        end=updateString.find("#%sb" %(KPI))
                        startFile=updateString[:start+4]
                        endFile=updateString[end:]
                        updateString=startFile+replaceStringSource %(KPI,SQLConS,SQLCon) +endFile
                #looks for the kpi numbers x and y comment and then replaces what is found inside those comments with the new target sql
                elif SQL=="target":
                    if arr[2]=="" or arr[2]==None:
                        break
                    else:
                        SQLCon=arr[2]
                        SQLConS=arrS[2]
                        start=updateString.find("#%sx" %(KPI))
                        end=updateString.find("#%sy" %(KPI))
                        startFile=updateString[:start+4]
                        endFile=updateString[end:]
                        updateString=startFile+replaceStringTarget %(KPI,SQLConS,SQLCon) +endFile
            return updateString 
        #If a new featue is being added finds the last line of the source and target functions and adds in the new sql above this line
        elif functionFlag=="newKPI":
            replaceStringSource="""
#%sa
    if SQLConfig[0]=="%s":
        if noNode==1:
            sourceSQL="%s
        else:
            sourceSQL="%s	#the cows in the field eat grass
#%sb
    """
            replaceStringTarget="""
#%sx
    if SQLConfig[0]=="%s":
        if noNode==1:
            targetSQL="%s
        else:
            targetSQL="%s
#%sy
    """
            for o,p in enumerate(SQLReturn):
                arr=SQLReturn[o]
                arrS=SQLReturnS[o]
                KPI=arr[0]
                if SQL=="source":
        
                    if arr[1]=="" or arr[1]==None:
                        break
                    else:
                        SQLCon=arr[1]
                        SQLConS=arrS[1]
                        start=updateString.find("return sourceSQL")
                        startFile=updateString[:start]
                        endFile=updateString[start:]
                        updateString=startFile+replaceStringSource %(KPI,KPI,SQLConS,SQLCon,KPI) +endFile
                elif SQL=="target":
                    if arr[2]=="" or arr[2]==None:
                        break
                    else:
                        SQLCon=arr[2]
                        SQLConS=arrS[2]
                        start=updateString.find("return targetSQL")
                        startFile=updateString[:start]
                        endFile=updateString[start:]
                        updateString=startFile+replaceStringTarget %(KPI,KPI,SQLConS,SQLCon,KPI) +endFile
            return updateString
        #If its deleteing a kpi it finds the a and b comment and removes what is found between these and does the same with the x and y comments
        elif functionFlag=="deleteKPI":
            for x in SQLReturn:
                KPI=x
                print 'Deleting KPI', x
                start=updateString.find("#%sa" %(KPI))
                end=updateString.find("#%sb" %(KPI))
                startFile=updateString[:start]
                endFile=updateString[end+9:]	#remove #%s to #%s from the source, including the spaces ie the 9
                updateString=startFile+endFile

                start=updateString.find("#%sx" %(KPI))
                end=updateString.find("#%sy" %(KPI))
                startFile=updateString[:start]
                endFile=updateString[end+9:]	#remove #%s to #%s from the target, including the spaces ie the 9
                updateString=startFile+endFile
            return updateString

    # Function that is used to modify the features main file when the features replace new kpi or delete kpi is used. Very similar logic to function featureMainFunc above
    def tableFunctionReturn(KPIAll,headerNameList,nodeNameList,KPINameList,dashList,dashHeaderList,functionFlag):
        from com.ziclix.python.sql import zxJDBC
        from SQLFunction import SQLFunctionSource
        from SQLFunction import SQLFunctionTarget
        from ConfigParser import SafeConfigParser
        rowsSource=[]
        rowsTarget=[]
        sourceRows=[]
        targetRows=[]
        columnNameTar=[]
        columnNameSour=[]
        SQLConfig[4]=nameFeature
        colNameTar=[]
        colNameSour=[]
        KPIFlagTarget=0
        KPIFlagSource=0 
        headerFlagSource=0
        headerFlagTarget=0 
        dashHeaderFlagSource=0 
        dashHeaderFlagTarget=0
        EndappendSour=[]
        EndappendTar=[]
        EndListSour=[]
        EndListTar=[]
        resultString=[]
        String="%s"
        PercenString="%"
        rowConfig="""        if SQLConfig[0]=='%s':
"""
        appendCol="""            col%s.append(row[%s])
"""
    
        appendListIf="""    if SQLConfig[0]=='%s':
"""
    
        appendList="""        test%s=list(col%s)
"""
        decimalString="""        ForTest%s=[]
        for number in range(len(test%s)):
            if test%s[number] is not None:
                ForTest%s.append(math.floor(test%s[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest%s.append(test%s[number])"""

        rowsString="""
        rows = zip(%s)
        rows =sorted(rows,key=itemgetter(1))
"""
        returnString=[]

        resultsStringB2="""    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\\n<th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>" #Adds the headers for the table in the file
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='2'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='2'><a href='%s'>Target</a></th>\\n</tr>\\n" %s(sourceHyper,targetHyper)
        \n"""%(String,String,String,String,String,String,String,String,String,String)

        resultsStringB3="""    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=3
        HTMLResults=HTMLResults + "<tr><th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th></th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n</tr>"
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='3'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='3'><a href='%s'>Target</a></th>\\n</tr>" %s(sourceHyper,targetHyper)"""%(String,String,String,String,String,String,String,String,String,String,String,String)
    
        resultsStringB4="""    if SQLConfig[0]=='%s':
        ColumnNameSour=%s
        ColumnNameTar=%s
        numColumn=4
        HTMLResults=HTMLResults + "<tr><th>Match Type</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th>%s</th>\\n<th><th>%s</th>\\n</th>\\n<th>%s</th>\\n<th>%s</th><th>%s</th>\\n\\n<th>%s</th>\\n</tr>"
        HTMLResults=HTMLResults + "<tr>\\n<th></th>\\n<th colspan='4'><a href='%s'>Source</a></th>\\n<th></th>\\n<th colspan='4'><a href='%s'>Target</a></th>\\n</tr>\\n" %s(sourceHyper,targetHyper)""" %(String,String,String,String,String,String,String,String,String,String,String,String,String,String)

        try:
            cnxnStr =  "jdbc:sybase:Tds:atvts3464.athtem.eei.ericsson.se:2640/dwhdb"
            dbDriver = "com.sybase.jdbc4.jdbc.SybDriver"
            cnxn = zxJDBC.connect(cnxnStr, "dc", "dc", dbDriver) #db connection
            crsr = cnxn.cursor(1)
            for x in KPIAll:
                SQLConfig[0]=x
                sourceResults=SQLFunctionSource(SQLConfig,noNode)
                targetResults=SQLFunctionTarget(SQLConfig,noNode)
                stringTest=""
                crsr.execute("%s" %(sourceResults)) #Executes the Chosen SQL command from SQLFunction
                descSour = crsr.description #Headings/description of the rows found in the SQL command results
                rowSour = crsr.fetchall() #Rows of data found in the SQL command results
                headerlineX=[]
                rowSourArr=[]
                colNumArrS=[]
                colNumArrT=[]
                rowTarArr=[]

                #For a column in the headers add it onto headerlineS
                for column in descSour:
                    headerlineX.append(column[0])
                for x,y in enumerate(headerlineX):
                    if headerlineX[x] in headerNameList:
                        headerFlagSource=1
                        headerColSource=x
                    elif headerlineX[x] in KPINameList:
                        KPIFlagSource=1
                        KPIColSource=x
                    elif headerlineX[x] in dashHeaderList:
                        dashHeaderFlagSource=1
                        dashHeaderSource=x
                    rowSourArr.append(str(rowSour[0][x]))
                    colNumArrS.append("column %s"%(x))
                    colNameSour.append(str(headerlineX[x]))
                for x,y in enumerate(rowSourArr):
                    if isinstance(rowSourArr[x], Number):
                        if headerlineX[x] not in KPIHeader and 'ID' not in headerlineX[x] and 'CELL' not in headerlineX[x] and 'NODE' not in headerlineX[x]:
                            KPIFlagSource=1
                            KPIColSource=x
                    if "_" in rowSourArr[x] and ("_oss_" not in rowSourArr[x]  or "eniq" not in rowSourArr[x]):
                        underscore=rowSourArr[x].rfind("_")
                        erbsName=rowSourArr[x][:underscore]
                        if erbsName in nodeNameList:
                            headerFlagSource=1
                            headerColSource=x
                    if "-" in rowSourArr[x]:
                        dash=rowSourArr[x].rfind("-")
                        preDash=rowSourArr[x][:dash]
                        try:
                            test=int(preDash)
                            dashHeaderFlagSource=1
                            dashHeaderSource=x
                        except ValueError:
                            pass

                HeaderSourList=headerlineX
                crsr.execute("%s" %(targetResults)) #Executes the Chosen SQL command from SQLFunction
                descTarget = crsr.description #Headings/description of the rows found in the SQL command results
                rowTar = crsr.fetchall() #Rows of data found in the SQL command results
                headerlineX=[]

                #For a column in the headers add it onto headerlineS
                for column in descTarget:
                    headerlineX.append(column[0])
                for x,y in enumerate(headerlineX):
                    if headerlineX[x] in headerNameList:
                        headerFlagTarget=1
                        headerColTarget=x
                    elif headerlineX[x] in KPINameList:
                        KPIFlagTarget=1
                        KPIColTarget=x
                    elif headerlineX[x] in dashHeaderList:
                        dashHeaderFlagTarget=1
                        dashHeaderTarget=x
                    
                    
                    rowTarArr.append(str(rowTar[0][x]))
                    colNameTar.append(str(headerlineX[x]))
                    colNumArrT.append("column %s"%(x))
                for x,y in enumerate(rowTarArr):
                    if isinstance(rowTarArr[x], Number):
                        if headerlineX[x] not in KPIHeader and 'ID' not in headerlineX[x] and 'CELL' not in headerlineX[x] and 'NODE' not in headerlineX[x]:
                            KPIFlagTarget=1
                            KPIColTarget=x
                    if "_" in rowTarArr[x] and ("_oss_" not in rowTarArr[x]  or "eniq" not in rowTarArr[x]):
                        underscore=rowTarArr[x].rfind("_")
                        erbsName=rowTarArr[x][:underscore]

                        if erbsName in nodeNameList:
                            headerFlagTarget=1
                            headerColTarget=x

                    if "-" in rowTarArr[x] and rowTarArr[x] != "EutrancellTDD" :
                        dash=rowTarArr[x].rfind("-")
                        preDash=rowTarArr[x][:dash]
                        try:
                            test=int(preDash)
                            dashHeaderFlagTarget=1
                            dashHeaderTarget=x
                        except ValueError:
                            pass
                if KPIFlagTarget==1 and KPIFlagSource ==1 and((headerFlagSource==1 and headerFlagTarget==1) or (dashHeaderFlagSource==1 and dashHeaderFlagTarget==1)):
                    
                    if headerFlagSource==1 and headerFlagTarget==1:
                        rowsSource.append(headerColSource)
                        rowsTarget.append(headerColTarget)
                    if dashHeaderFlagSource==1 and dashHeaderFlagTarget==1:
                        rowsSource.append(dashHeaderSource)
                        rowsTarget.append(dashHeaderTarget)
                    if KPIFlagTarget ==1 and KPIFlagSource==1:
                        rowsSource.append(KPIColSource)
                        rowsTarget.append(KPIColTarget)
                else:
                    tableSour=[colNumArrS,colNameSour,rowSourArr]
                    print("\n\n\nKPI %s:\n\nSOURCE" %(SQLConfig[0]))
                    print tabulate(tableSour,tablefmt="grid")
                    
                    tableTar=[colNumArrT,colNameTar,rowTarArr]
                    print("\nTARGET")
                    print tabulate(tableTar,tablefmt="grid")
        
                    matchRow=raw_input("\nPlease choose the column numbers to match: ")
                    splitMatch=matchRow.split(",")

                    for x,y in enumerate(splitMatch):
                        splitMatch1=splitMatch[x].split("=")
                        rowsSource.append(splitMatch1[0])
                        rowsTarget.append(splitMatch1[1])
                   
                HeaderTarList=headerlineX
                for elem in rowsSource:
                    columnNameSour.append(HeaderSourList[int(elem)])
                for elem in rowsTarget:
                    columnNameTar.append(HeaderTarList[int(elem)]) 

                colNameTar1=[SQLConfig[0],columnNameTar]
                colNameArrTar.append(colNameTar1)
                colNameSour1=[SQLConfig[0],columnNameSour]
                colNameArrSour.append(colNameSour1)
                results=map(int,SQLConfig[0])

                testStrSour=rowConfig %(SQLConfig[0])
                testStr2Sour=appendListIf %(SQLConfig[0])
                for x,y in enumerate(rowsSource):
                    testStrSour=testStrSour+appendCol %(rowsSource[x],rowsSource[x])
                    if x<=len(rowsSource)-1:
                        sourceRows.append(rowsSource[x])
                    testStr2Sour=testStr2Sour +appendList %(rowsSource[x],rowsSource[x])
                    if x <len(rowsSource)-1:
                        stringTest=stringTest +"test%s," %(rowsSource[x])
                    elif x==len(rowsSource)-1:
                        stringTest=stringTest +"ForTest%s" %(rowsSource[x])
                        cntS=rowsSource[x]
                rowStringSour=rowsString %(stringTest)
                stringTest=""
                testStrTar=rowConfig %(SQLConfig[0])
                testStr2Tar=appendListIf %(SQLConfig[0])
                for x,y in enumerate(rowsTarget):
                    testStrTar=testStrTar+appendCol %(rowsTarget[x],rowsTarget[x])
                    if x<=len(rowsTarget)-1:
                        targetRows.append(rowsTarget[x])
                    testStr2Tar=testStr2Tar +appendList %(rowsTarget[x],rowsTarget[x])
                    if x <len(rowsTarget)-1:
                        stringTest=stringTest +"test%s," %(rowsTarget[x])
                    elif x==len(rowsTarget)-1:
                        stringTest=stringTest +"ForTest%s" %(rowsTarget[x])
                        cntT=rowsTarget[x]
                rowStringTar=rowsString %(stringTest)
                stringTest=""
                if functionFlag=="replace":
                    EndappendSour.append(testStrSour)
                    EndListSour.append(testStr2Sour+decimalString %(cntS,cntS,cntS,cntS,cntS,cntS,cntS)+rowStringSour)
                    EndappendTar.append(testStrTar)
                    EndListTar.append(testStr2Tar+decimalString %(cntT,cntT,cntT,cntT,cntT,cntT,cntT)+rowStringTar)
                    EndTar=[EndappendTar,EndListTar]
                    EndSour=[EndappendSour,EndListSour]
                elif functionFlag=="newKPI":
                    EndappendSour.append(testStrSour)
                    EndListSour.append(testStr2Sour+decimalString %(cntS,cntS,cntS,cntS,cntS,cntS,cntS)+rowStringSour)
                    EndappendTar.append(testStrTar)
                    EndListTar.append(testStr2Tar+decimalString %(cntT,cntT,cntT,cntT,cntT,cntT,cntT)+rowStringTar)
                    EndTar=[EndappendTar,EndListTar]
                    EndSour=[EndappendSour,EndListSour]

                testStrSour=""
                testStr2Sour=""
                testStrTar=""
                testStr2Tar=""
                rowsSource=[]
                rowsTarget=[]
                targetRows=[]
                sourceRows=[]
                colNameSour=[]
                colNameTar=[]
                columnNameTar=[]
                columnNameSour=[]
                for x in range(0,len(colNameArrTar)): #for x,y in enumerate(colNameArrTar):
                    kpi=SQLConfig[0]
                    colNmeTar=colNameArrTar[(len(colNameArrTar)-1)][1]
                    colNmeSour=colNameArrSour[(len(colNameArrTar)-1)][1]
                    numColumn=len(colNmeTar)
                    startFile=''

                    if numColumn==2:
                        startFile=resultsStringB2  %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeTar[0],colNmeTar[1],String,String,PercenString)
                    elif numColumn==3:
                        startFile=resultsStringB3 %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeSour[2],colNmeTar[0],colNmeTar[1],colNmeTar[2],String,String,PercenString)
                    elif numColumn==4:
                        startFile=resultsStringB4 %(kpi,colNmeSour,colNmeTar,colNmeSour[0],colNmeSour[1],colNmeSour[2],colNmeSour[3],colNmeTar[0],colNmeTar[1],colNmeTar[2],colNmeTar[3],String,String,PercenString)
                resultString.append(startFile)
            returnString.append(EndSour)
            returnString.append(EndTar)
            returnString.append(resultString)
            return returnString
        except SQLException, msg:      #to debug COMMENT these 2 lines
            print 'Error 3: ', msg
        finally:
            print("\nCompleted")
            crsr.close() #closes the cursor to the DB
            cnxn.close() #close the connection to the db

    #Function that is used to modify the features main file when the user is replaceing,adding or removing a kpi from a feature
    def MainReplace(returnString,KPIAll,nameFeature):
        if functionFlag!="deleteKPI":
            source=returnString[0]
            target=returnString[1]
            resultArr=returnString[2]
            sourceAppArr=source[0]
            sourceTestArr=source[1]
            targetAppArr=target[0]
            targetTestArr=target[1]
        section=["#1st","#2nd","#3rd","#4th","#5th","6th"]
        #Depending on what function was used by the user it searches through the feature main file for the numbered comments and then modifes the file at these positions ie adds or removes line of code
        if functionFlag=="replace":
            for e,d in enumerate(KPIAll):
                fileString=""
                cnt=5
                flag=0
                stringCnt=0
                lookup="if SQLConfig[0]=='%s':" %(KPIAll[e])
                with open(featureSrcMain) as myFile:	#goes through every line in the script, if it finds a match it will put in the new chunk of code and skip putting in the following lines associated with the old chunk
                    for num, line in enumerate(myFile, 0):
                        if lookup in line:
                            cnt=0
                            
                            if stringCnt==0:
                                fileString=fileString+sourceAppArr[e]+'\n'
                                flag=4
                            elif stringCnt==1:
                                fileString=fileString+sourceTestArr[e]+'\n'
                                flag=12
                            elif stringCnt==2:
                                fileString=fileString+targetAppArr[e]+'\n'
                                flag=4
                            elif stringCnt==3:
                                fileString=fileString+targetTestArr[e]+'\n'
                                flag=12
                            elif stringCnt==4:
                                cnt=-4	#this is to allow for extra lines needing removal
                                fileString=fileString+resultArr[e]+'\n'
                                flag=4

                            stringCnt=stringCnt+1
                        cnt=cnt+1

                        if cnt>flag or flag==0:
                            fileString=fileString+line
                            flag=0

                testopen=open(featureSrcMain,"w")
                testopen.write(fileString)
                testopen.close()
        elif functionFlag=="newKPI":
            fileString=""
            testopen=open(featureSrcMain,"r")
            fileString=testopen.read()
            testopen.close()
            for e,d in enumerate(KPIAll):
                secondString="'%s'," %(KPIAll[e])
                for x,y in enumerate(section):
                    if x==5:
                        startD=fileString.find("#6thStart")
                        EndD=fileString.find("#6thEnd")
                        startFile=fileString[:startD+(19+len(nameFeature))]
                        endFile=fileString[EndD-6:]
                        array=fileString[startD+(19+len(nameFeature)):EndD-6]
                        startFile=startFile+secondString
                        fileString=startFile+array+endFile
                    else:  
                        secString=fileString.find(section[x])
                        startFile=fileString[:secString]
                        endFile=fileString[secString:]
                    if x==0:
                        fileString=startFile+sourceAppArr[e]+"\n"+endFile
                    elif x==1:
                        fileString=startFile+sourceTestArr[e]+"\n"+endFile
                    elif x==2:
                        fileString=startFile+targetAppArr[e]+"\n"+endFile
                    elif x==3:
                        fileString=startFile+targetTestArr[e]+"\n"+endFile
                    elif x==4:
                        fileString=startFile+resultArr[e]+'\n'+endFile
            testopen=open(featureSrcMain,"w")
            testopen.write(fileString)
            testopen.close()

        elif functionFlag=="deleteKPI":
            fileString=""
            testopen=open(featureSrcMain,"r")
            fileString=testopen.read()
            testopen.close()
            for e,d in enumerate(KPIAll):	#remove the 5 referances to each kpi
                string="    if SQLConfig[0]=='%s':" %(KPIAll[e])
                x=0
                index1=fileString.find(string)
                if index1!=-1:
                    endString="])"
                    secondLine=fileString.find(endString,index1)
                    endIndex=fileString.find(endString,secondLine+2)
                    fileString=fileString[:index1-5]+fileString[endIndex+3:]
                    x+=1
                index2=fileString.find(string)
                if index2!=-1:
                    endString='itemgetter(1))'
                    sectionEnd=fileString.find(endString,index2)
                    endLine=fileString.find('\n',sectionEnd)
                    fileString=fileString[:index2]+fileString[endLine+2:]
                    x+=1
                index3=fileString.find(string)
                if index3!=-1:
                    endString="])"
                    secondLine=fileString.find(endString,index3)
                    endIndex=fileString.find(endString,secondLine+2)
                    fileString=fileString[:index3-5]+fileString[endIndex+3:]
                    x+=1
                index4=fileString.find(string)
                if index4!=-1:
                    endString='itemgetter(1))'
                    sectionEnd=fileString.find(endString,index4)
                    endLine=fileString.find('\n',sectionEnd)
                    fileString=fileString[:index4]+fileString[endLine+2:]
                    x+=1
                index5=fileString.find(string)
                if index5!=-1:
                    endString='(sourceHyper,targetHyper)'
                    endIndex=fileString.find(endString,index5)
                    newlineIndex=fileString.find('\n',endIndex)
                    fileString=fileString[:index5-10]+fileString[newlineIndex+1:]
                    x+=1
                arrIndex='%sKPI=[' % nameFeature
                index6=fileString.find(arrIndex)
                if index6!=-1:	#check if there is an array of KPIs
						
                    #check for the cases where the kpi is at the tail of an array
                    print 'let it go'
                    case1=",'%s']" % (KPIAll[e])	#single quotes without spaces
                    case2=", '%s']" % (KPIAll[e])	#single quotes with spaces
                    case3=',"%s"]' % (KPIAll[e])	#double quotes without spaces
                    case4=', "%s"]' % (KPIAll[e])	#double quotes with spaces

                    checkCase1=fileString.find(case1)	#check each case
                    checkCase2=fileString.find(case2)
                    checkCase3=fileString.find(case3)
                    checkCase4=fileString.find(case4)

                    if checkCase1!=-1:
                        print 'case1'
                        fileString=fileString[:checkCase1]+fileString[checkCase1+4:]
                    if checkCase2!=-1:
                        print 'case2'
                        fileString=fileString[:checkCase2]+fileString[checkCase2+5:]
                    if checkCase3!=-1:
                        print 'case3'
                        fileString=fileString[:checkCase3]+fileString[checkCase3+4:]
                    if checkCase4!=-1:
                        print 'case4'
                        fileString=fileString[:checkCase4]+fileString[checkCase4+5:]

                    if checkCase1==-1 and checkCase2==-1 and checkCase3==-1 and checkCase4==-1:	#if all the cases where the element is in the tail of the array are false
                        #regular expression concatination
                        regexString=r'''[ ]?['|"]''' +  KPIAll[e] + '''['|"][,]?'''
                        print 'Moo'
                        indexStart=re.search(regexString,fileString[index6:]).start()	#search for the start of the match to the srting after the start of the array (ie the index6)
                        indexEnd=re.search(regexString,fileString[index6:]).end()		#search for the end of the match to the string....
                        print 'Hoo'
                        if indexStart!=None and indexEnd!=None:	#if Regex found a match
                            fileString=fileString[:indexStart+index6]+fileString[indexEnd+index6:]	#concatinate the script string without the section where the kpi is referanced in the array (NOTE. index6 is added back to get to position in the overall script string)
                            print 'indexStart:',indexStart,'indexEnd:',indexEnd

            testopen=open(featureSrcMain,"w")
            testopen.write(fileString)
            testopen.close()
            
    editFeatureIndex=path.find("KPI_checker")   #Finds the absoulte path to the KPI_checker folder to find the main files src folder
    mainPath=path[:editFeatureIndex+11] #the 11 is to incorporate the KPI_checker into the path
    featureSrc=mainPath+"\src\\%s"%(nameFeature)    #path to the features folder inside the main scripts src folder

    #If the featurue src folder doesnt exist creates the folder and the __init__.py
    if not os.path.exists(featureSrc):
        os.makedirs(featureSrc)
        openFile=open(featureSrc+"\\__init__.py","w")
        openFile.close()
        
    featureSrcMain=featureSrc+"\\%sMain.py"%(nameFeature)#Path to the current feature being edited's main file
    featureSrcSQL=featureSrc+"\\%sSQLFunction.py"%(nameFeature)#Path to the current feature being edited's SQL file
    srcMainPath=mainPath+"\src\\Main.py"#path to Main scripts main file
    srcPath=mainPath+"\src"#path to src main folder
    srcConfigFolder=mainPath+"\configFiles\\%s" %(nameFeature)#path to configfile folder
    headerFilePath=mainPath+"\src\\headerName.txt"


    configParser = SafeConfigParser()
    configParser.read(headerFilePath)
    #Reads in the values uesed for automatching columns for source and target
    nodeNameList=configParser.get('Lists', 'nodeName')
    headerNameList=configParser.get('Lists', 'headerName')
    KPINameList=configParser.get('Lists', 'KPIName')
    dashList=configParser.get('Lists', 'dash')
    dashHeaderList=configParser.get('Lists', 'dashHeader')

    if functionFlag!="deleteFeature": #if the function choosed wasnt to delete a feature adds the values found in the excel file to arrays 
        for row in d:
            if functionFlag=="deleteKPI":
                KPIAll.append(row[0])
            elif row[1] !="" or row[2] !="":#if the 2nd column or third column arent blank of the row being looped over
                row[1]= ' '.join(row[1].split())
                row[2]= ' '.join(row[2].split())
                rows=[row[0],row[1],row[2]]#adds the values found in col1,col2,col3 into an array
                SQLArr.append(rows)#add the current loops row into an array

    #loops through the array with each rows information from the csv file
    for x in range(len(SQLArr)):
        arr = SQLArr[x]
        for counter in range(len(arr)-1):
            KPI=arr[0]
            emptyFlag=0#Flag that is used to check if a cell was found to be blank
            if counter==0 and arr[1] !="":#extracts the source sql if the cell wasnt blank
                s=arr[1]
            elif counter==1 and arr[2] !="":#extracts the target sql if the cell wasnt blank
                s=arr[2]
            else:#an empty cell was found 
                if arr[1]=="" or arr[1]==None and counter==0:
                    resultSourceS=""
                    resultSource=""
                elif arr[2]=="" or arr[2]==None and counter==1:
                    resultTargetS=""
                    resultTarget=""
                emptyFlag=1

            if emptyFlag==0:#if the cell wasnt blank
                endString='" %('
                endStringS='" %('

                sDatetime=s     #set sDatetime to the original string s

                #removes the char < and > from the sql
                index1Start = s.find("<")   #find the index of '<'
                s=s[:index1Start]+s[index1Start+1:]     # s now = s without the element at index1Start... the '<'
                index1End = s.find(">")
                s=s[:index1End]+s[index1End+1:]

                nextIndex = s.find('<', index1End)  #returns the index of the next '<', if there is no more '<' then the result is -1
                if nextIndex!=-1:   #if there is another '<'
                    index2Start=s.find("<", index1End+1)    #find index of '<'
                    s=s[:index2Start]+s[index2Start+1:]     #sets s to be s without the element at index2Start

                    index2End=s.find(">", index1End+1)      #same as above only for '>'
                    s=s[:index2End]+s[index2End+1:]         #sets s to be s without the element at index2End

                nextIndex = s.find('<', index1End)  #same as above
                if nextIndex!=-1:   #if there is another '<'
                    index2Start=s.find("<", index1End+1)    #find index of '<'
                    s=s[:index2Start]+s[index2Start+1:]     #sets s to be s without the element at index2Start
                    
                    index2End=s.find(">", index1End+1)      #same as above only for '>'
                    s=s[:index2End]+s[index2End+1:]         #sets s to be s without the element at index2End

                #this has been rehauled
                moreN = False   #this will be true if there is more than one n
                moreD = False   #this will be true if there is more than one d
                threeD = False
                threeN = False

                dIndex = s.find("'d'")  #finds the index of the substing 'd' in the sql that was put in the csv file
                if dIndex!=-1:
                    s=s[:dIndex] +"'%s'"+s[dIndex+3:]   #this is added to the first half of sqls(without nodeName) in both source and target

                    nextIndexD = s.find("'d'")
                    if nextIndexD!=-1:  #if there is another 'd', remove it
                        s=s[:nextIndexD] +"'%s'"+s[nextIndexD+3:]
                        moreD=True  #there is more then one d
                        nextIndexD = s.find("'d'")
                        if nextIndexD!=-1:  #if there is third 'd', remove it
                            s=s[:nextIndexD] +"'%s'"+s[nextIndexD+3:]
                            threeD=True  #there are three d's

                nIndex=s.find("'n'")    #finds the index of the substing 'n' in the sql that was put in the csv file
                if nIndex!=-1:
                    s=s[:nIndex]+"'%s'"+s[nIndex+3:]

                    nextIndexN = s.find("'n'")  #check for another 'n'
                    if nextIndexN!=-1:  #if there is another 'n', remove it
                        s=s[:nextIndexN] +"'%s'"+s[nextIndexN+3:]
                        moreN=True  #there is more then one n
                        nextIndexN = s.find("'n'")  #check for a third 'n'
                        if nextIndexN!=-1:  #if there is another 'n', remove it
                            print 'Pass the butter'
                            s=s[:nextIndexN] +"'%s'"+s[nextIndexN+4:]
                            threeN=True  #there are three n's

                #Need to check this for the config number
                if moreD==False:    #there is only 1 d
                    if moreN==False:    #there is only 1 n appropriate ending
                        s=s+endStringS +"SQLConfig[1], SQLConfig[2]"
                    elif moreN==True:   #there more than 1 n
                        if threeN==True:    #there is 1 d and 3 n's
                            s=s+endStringS +"SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2]"
                        elif threeN==False: #there is 1 d and 2 n's
                            s=s+endStringS +"SQLConfig[1], SQLConfig[2], SQLConfig[2]"
                elif moreD==True:   #there is more than one d
                    if threeD==True:    #there are 3 d's
                        if moreN==True:    #more than one n
                            if threeN==True:    #there are 3 n's and 3 d's
                                s=s+endStringS +"SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2]"
                            elif threeN==False: #there are 2 n's and 3 d's
                                s=s+endStringS +"SQLConfig[1], SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2]"
                        elif moreN==False:   #there is 1 n and 3 d's
                            s=s+endStringS +"SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2]"
                    elif threeD==False: #there are 2 d's
                        if moreN==True:
                            if threeN==True:    #there are 2 d's and 3 n's
                                print 'Param failure... there should be no sql with 5 configs'
                                s=s+endStringS +"SQLConfig[1], SQLConfig[1], SQLConfig[2], SQLConfig[2], SQLConfig[2]"
                            elif threeN==False: #there are 2 d's and 2 n's
                                s=s+endStringS +"SQLConfig[1], SQLConfig[2], SQLConfig[1], SQLConfig[2]"
                        elif moreN==False:  #there are 2 d's and 1 n
                            print 'Param failure... there should be no sql with 3 configs'
                            s=s+endStringS +"SQLConfig[1], SQLConfig[1], SQLConfig[2]"

                dIndex=0    #reset to be safe
                nIndex=0    #reset to be safe
                nextIndexD=0    #reset to be safe
                nextIndexN=0    #reset to be safe

                #Does the same thing but for the sql that doesnt need to be configured by node_name
                firstIndex = sDatetime.find('<')    #finds the index of the first '<'
                secondIndex = sDatetime.find('>')   #finds the index of the first '>'
                sDatetime = sDatetime[:firstIndex]+sDatetime[secondIndex+1:]    # sDatetime is to hold the SQL string without the and nodeName param... ie removing the "<'nodeNameParams'>"

                checkIndex = sDatetime.find('<', firstIndex+1)  #returns the index of the next '<', if there is no more '<' then the result is -1
                if checkIndex!=-1:  #if there is another '<'
                    newIndex1 = sDatetime.find('<') #finds the index of the next '<'
                    newIndex2 = sDatetime.find('>') #finds the index of the next '>'
                    sDatetime = sDatetime[:newIndex1]+sDatetime[newIndex2+1:]   #sDatetime should now hold the string SQL without the <...> sections

                    #check if there is a third <...> set
                    checkIndexThird = sDatetime.find('<', checkIndex+1)  #returns the index of the next '<', if there is no more '<' then the result is -1
                    if checkIndexThird!=-1:  #if there is another '<'
                       newIndex1 = sDatetime.find('<') #finds the index of the next '<'
                       newIndex2 = sDatetime.find('>') #finds the index of the next '>'
                       sDatetime = sDatetime[:newIndex1]+sDatetime[newIndex2+1:]   #sDatetime should now hold the string SQL without the <...> sections

                #remove 'd' for date only SQL's
                dIndex = sDatetime.find("'d'")  #holds the starting index of "'d'"
                if dIndex!=-1:
                    sDatetime=sDatetime[:dIndex] +"'%s'"+sDatetime[dIndex+3:]   #this is added to the first half of sqls(without nodeName) in both source and target

                    nextIndex = sDatetime.find("'d'")
                    if nextIndex==-1:   #if there is no other 'd' then add only one config
                        sDatetime=sDatetime+endStringS +"SQLConfig[1]"
                    elif nextIndex!=-1: #if there is another 'd', remove it and add two configs
                        sDatetime=sDatetime[:nextIndex] +"'%s'"+sDatetime[nextIndex+3:]

                        thirdD=sDatetime.find("'d'")
                        if thirdD==-1:  #there are only 2 d's
                            sDatetime=sDatetime+endStringS+"SQLConfig[1], SQLConfig[1]"
                        elif thirdD!=-1:    #there are 3 d's
                            sDatetime=sDatetime[:thirdD] +"'%s'"+sDatetime[thirdD+3:]+endStringS+"SQLConfig[1],SQLConfig[1], SQLConfig[1]"
                else:
                    sDatetime=sDatetime[:dIndex] +"'%s'"+sDatetime[dIndex+3:]+endStringS +",SQLConfig[1]"

                sDatetime=sDatetime+')' #finish the SQL string without nodeName parameters, with a bracket
                s=s+')'     #finish the SQL string with nodeName parameters, with a bracket

                if counter==0:
                    resultSource=s
                    resultSourceS=sDatetime
                elif counter==1:
                    resultTarget=s
                    resultTargetS=sDatetime
        #original
        KPISQLS=[arr[0],resultSourceS,resultTargetS]#holds the kpi ID the source sql with only datetime configured and the target with only datetime configured
        KPISQL=[arr[0],resultSource,resultTarget]#holds the kpi ID the source sql with datetime and node_name configured and the target with datetime and node_name configured
        KPIAll.append(arr[0])#array that holds all the valid kpi ID numbers
        SQLReturn.append(KPISQL)#holds the above arrays with the datetime id configured only
        SQLReturnS.append(KPISQLS)#holds the arrays with both datetime_id and node_name configured only
        resultSource=""
        resultTarget=""

    #Depending on what feature is used makes calls the the other functions
    if functionFlag=="newFeature":
        SQL="source"
        SQLFuncWrite(SQL,stringSource,SQLReturn,SQLReturnS)#makes call to file to make new sql file
        SQL="target"
        SQLFuncWrite(SQL,stringTarget,SQLReturn,SQLReturnS)

        sourTarReturn=tableFunction(KPIAll,headerNameList,nodeNameList,KPINameList,dashList,dashHeaderList)
        sourReturn=sourTarReturn[0]#Source code segment
        tarReturn=sourTarReturn[1]#target code segment
        shutil.copyfile(srcMainPath, mainPathOG)#copys the current un updated version of the main file to the old code folder
        featureMainFunc(KPIAll,nameFeature,sourReturn,tarReturn)#call to function that is used to create a new feature main file
        scriptWriteMain(nameFeature,srcMainPath)#call to the function that edits the scripts main file
        shutil.move(SQLFunctionPath, featureSrcSQL)#Moves the newly created sql file to the relevent folder and file location
        preMain=oldCode+"\\MainPre%s.py"%(nameFeature)#Path to old main file location in the old code folder
        if not os.path.exists(srcConfigFolder):#If the features config filder doesnt exist creates it and a sample config file inside the folder
            os.makedirs(srcConfigFolder)
            srcConfigFile= srcConfigFolder+"\\config.ini"
            configOpen=open(srcConfigFile,"w")
            configOpen.write(configFileString %(nameFeature,SQLConfig[1],SQLConfig[2]))
    elif functionFlag=="replace":
        replaceKPI=""
        for elem in KPIAll:
            replaceKPI=replaceKPI+"_%s"%(elem)
        oldSQLFunction=oldCodeFolder+"\\%sSQLFunctionReplaceKPI%s.py" %(nameFeature,replaceKPI)
        oldFeatureMain=oldCodeFolder+"\\%sMainReplaceKPI%s.py" %(nameFeature,replaceKPI)
        shutil.copyfile(srcMainPath, mainPathOG)
        shutil.copyfile(featureSrcSQL,oldSQLFunction)
        shutil.copy(featureSrcMain,oldFeatureMain)
        testopen=open(featureSrcSQL,"r")
        testopen.seek(0)
        updateString=testopen.read()
        testopen.close()

        SQL="source"
        updateString=replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag)
        SQL="target"
        updateString=replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag)
        testopen=open(featureSrcSQL,"w")
        testopen.write(updateString)
        testopen.close()
        shutil.copy(featureSrcSQL,SQLFunctionPath)
        sourTarReturn=tableFunctionReturn(KPIAll,headerNameList,nodeNameList,KPINameList,dashList,dashHeaderList,functionFlag)
        os.remove(SQLFunctionPath)
        MainReplace(sourTarReturn,KPIAll,nameFeature)
    elif functionFlag=="newKPI":
        newKPI=""
        for elem in KPIAll:
            newKPI=newKPI+"_%s"%(elem)
        oldSQLFunction=oldCodeFolder+"\\%sSQLFunctionNewKPI%s.py" %(nameFeature,newKPI)
        oldFeatureMain=oldCodeFolder+"\\%sMainNewKPI%s.py" %(nameFeature,newKPI)
        shutil.copyfile(srcMainPath, mainPathOG)
        shutil.copyfile(featureSrcSQL,oldSQLFunction)
        shutil.copy(featureSrcMain,oldFeatureMain)

        testopen=open(featureSrcSQL,"r")
        testopen.seek(0)
        updateString=testopen.read()
        testopen.close()
        SQL="source"
        updateString=replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag)
        SQL="target"
        updateString=replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag)
        testopen=open(featureSrcSQL,"w")
        testopen.write(updateString)
        testopen.close()
        shutil.copy(featureSrcSQL,SQLFunctionPath)
        sourTarReturn=tableFunctionReturn(KPIAll,headerNameList,nodeNameList,KPINameList,dashList,dashHeaderList,functionFlag)
        os.remove(SQLFunctionPath)
        MainReplace(sourTarReturn,KPIAll,nameFeature)
    elif functionFlag=="deleteKPI":
        deleteKPI=""
        for elem in KPIAll:
            deleteKPI=deleteKPI+"_%s"%(elem)
        oldSQLFunction=oldCodeFolder+"\\%sSQLFunctionDeleteKPI%s.py" %(nameFeature,deleteKPI)
        oldFeatureMain=oldCodeFolder+"\\%sMainDeleteKPI%s.py" %(nameFeature,deleteKPI)
        shutil.copyfile(srcMainPath, mainPathOG)
        shutil.copyfile(featureSrcSQL,oldSQLFunction)
        shutil.copy(featureSrcMain,oldFeatureMain)

        testopen=open(featureSrcSQL,"r")
        testopen.seek(0)
        updateString=testopen.read()
        testopen.close()
        SQL=None
        SQLReturn=KPIAll
        SQLReturnS=None
        updateString=replaceFunction(SQL,updateString,SQLReturn,SQLReturnS,functionFlag)
        testopen=open(featureSrcSQL,"w")
        testopen.write(updateString)
        testopen.close()
        shutil.copy(featureSrcSQL,SQLFunctionPath)
        sourTarReturn=None
        MainReplace(sourTarReturn,KPIAll,nameFeature)
    elif functionFlag=="deleteFeature":
        oldSQLFunction=oldCodeFolder+"\\%sSQLFunctionDeleteFeature%s.py" %(nameFeature,nameFeature)
        oldFeatureMain=oldCodeFolder+"\\%sMainDeleteFeature%s.py" %(nameFeature,nameFeature)
        shutil.copyfile(srcMainPath, mainPathOG)
        shutil.copyfile(featureSrcSQL,oldSQLFunction)
        shutil.copy(featureSrcMain,oldFeatureMain)
        sourTarReturn=None
        KPIAll=None
        scriptWriteMain(nameFeature,srcMainPath)
        deletedFeaturesConfigPath=path+"\\configFiles\\%s"%fname	#path to config file to be removed
        deletedFeaturesSrcPath=path+"\\src\\%s"%fname	#path to src file to be removed
##uncomment to allow the script to delete the inaccessible files
        shutil.rmtree(deletedFeaturesSrcPath)	#remove the feature src file
        shutil.rmtree(deletedFeaturesConfigPath)	#remove the features config file