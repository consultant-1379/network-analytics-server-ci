def sourceWritetest(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):
    crsr.execute("%s" %(sourceResults))
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
    rowSour = crsr.fetchall() #Rows of data found in the SQL command results    
    if not os.path.exists(result):
        os.makedirs(result)
    SourceFile= open(os.path.join(result,'%s_%s_%s_Source_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w+')
    sourceHyper=os.path.join(result,'%s_%s_%s_Source_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace))
    targetHyper=os.path.join(result,'%s_%s_%s_Target_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace))
    resultHyper=os.path.join(result,'%s_%s_%s_Results_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace))
    summaryHyper=os.path.join(result,'Summary.HTML')
    headerlineS = ''
    for column in descSour:
        headerlineS=headerlineS + "\n<th>%s</th>" %(str(column[0]))
        headerName.append(str(column[0]))
      
    headerlineS=headerlineS + "\n<tr>\n" #Ends the row of headers
    HTMLTest=HTMLTest+headerlineS #add the headers into the HTML string


    #For a row in the row of data and a row and then add this row to the HTML String
    for row in rowSour:
        datalineS="\n<tr>\n"
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
            datalineS=datalineS + "<td>%s</td>\n" %(str(column))
        datalineS=datalineS +"<tr>\n"
        HTMLTest=HTMLTest+datalineS

    
        if SQLConfig[0]=='1':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='2':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='3':
            col1.append(row[1])
            col2.append(row[2])

#1st

    if SQLConfig[0]=='1':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
    if SQLConfig[0]=='2':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
    if SQLConfig[0]=='3':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
#2nd
 
    HTMLTest =HTMLTest +"\n<h1>Source results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>"%(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    HTMLTest=HTMLTest +"<h4><a href='%s'>Target</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></h4>\n"% (targetHyper,resultHyper,summaryHyper)
    SourceFile.write(HTMLTest)    
    SourceFile.close()
    return rows
def targetWritetest(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):  
    crsr.execute("%s" %(targetResults))
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
    datalineT=dataline
    if not os.path.exists(result):
        os.makedirs(result)  
    targetSQL= open(os.path.join(result,'%s_%s_%s_Target_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w') #opens the file needed to write the results
    #Some arrays named after the headers found in the tables for the different 
    headerlineT = ''
    headerName=[]
    #For a column/header in the row of headers add the header to headerlineT
    for column in descTar:
        headerlineT=headerlineT + "\n<th>%s</th>" %(str(column[0]))
        headerName.append(str(column[0]))
    headerlineT=headerlineT + "\n<tr>\n"
    HTMLTest=HTMLTest+headerlineT #Add the row of headers to the HTML string
    
    #For a individual row in a the group of rows add the elements in the row one by one to the HTML string 
    for row in rowTar:
        cnt=0
        datalineT="\n<tr>\n"
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
            datalineT=datalineT + "<td>%s</td>\n" %(str(column))
        datalineT=datalineT +"<tr>\n"
        HTMLTest=HTMLTest+datalineT
    
        if SQLConfig[0]=='1':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='2':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='3':
            col1.append(row[1])
            col2.append(row[2])

#3rd

    if SQLConfig[0]=='1':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
    if SQLConfig[0]=='2':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
    if SQLConfig[0]=='3':
        test1=list(col1)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test1,ForTest2)
        rows =sorted(rows,key=itemgetter(1))
#4th

    HTMLTest =HTMLTest +"\n<h1>Target results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>"%(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    HTMLTest=HTMLTest +"<h4><a href='%s'>Source</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></H4>\n"%(sourceHyper,resultHyper,summaryHyper)
    targetSQL.write(HTMLTest) 
    targetSQL.close()
    return rows
def resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig):
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
    results= open(os.path.join(result,'%s_%s_%s_Results_test.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w')
    if SQLConfig[1] != "" and SQLConfig[2] == "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s </h1>" %(SQLConfig[0],SQLConfig[1])
    elif SQLConfig[1] != "" and SQLConfig[2] != "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s AND NODE_NAME: %s </h1>"%(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    
    
    if SQLConfig[0]=='1':
        ColumnNameSour=[u'MeasureValue', u'UTC_DATETIME_ID']
        ColumnNameTar=[u'MeasureValue', u'UTC_DATETIME_ID']
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n<th></th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n</tr>" #Adds the headers for the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n" %(sourceHyper,targetHyper)
        

    if SQLConfig[0]=='2':
        ColumnNameSour=[u'MeasureValue', u'UTC_DATETIME_ID']
        ColumnNameTar=[u'MeasureValue', u'UTC_DATETIME_ID']
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n<th></th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n</tr>" #Adds the headers for the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n" %(sourceHyper,targetHyper)
        

    if SQLConfig[0]=='3':
        ColumnNameSour=[u'MeasureValue', u'UTC_DATETIME_ID']
        ColumnNameTar=[u'MeasureValue', u'UTC_DATETIME_ID']
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n<th></th>\n<th>MeasureValue</th>\n<th>UTC_DATETIME_ID</th>\n</tr>" #Adds the headers for the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n" %(sourceHyper,targetHyper)
        

#5th

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
                    HTMLResults=HTMLResults + "<tr bgcolor='#00FF00'><td>MATCH</td>\n<td>%s</td>\n<td>%s</td>\n<th></th>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(n[0]),str(n[1]),str(m[0]),str(m[1]))
                elif numColumn==3:
                    HTMLResults=HTMLResults + "<tr bgcolor='#00FF00'><td>MATCH</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<th></th>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(n[0]),str(n[1]),str(n[2]),str(m[0]),str(m[1]),str(m[2]))
                elif numColumn==4:
                    HTMLResults= HTMLResults+ "<tr bgcolor='#00FF00'>\n<th>MATCH</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th></th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n</tr>" %(str(n[0]),str(n[1]),str(n[2]),str(n[3]),str(m[0]),str(m[1]),str(m[2]),str(m[3])) 
                x=x+1
                break
            if counter1 == len(rowsTarget)-1:
                parMatch.append(rowsSource[counter])
    if numColumn==2:
        rowResults.append(("","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='6'></th></tr>\n"
    elif numColumn==3:
        HTMLResults=HTMLResults + "<tr><th colspan='8'></th></tr>\n"
        rowResults.append(("","","","","","","",""))
    elif numColumn==4:
        rowResults.append(("","","","","","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='10'></th></tr>\n"

    for counter2,p in enumerate(parMatch):
        for counter3,q in enumerate(rowsTarget):
            if p[0] == q[0]:
                rowResults.append((("PARTIAL MATCH",)+p+("",)+q))
                if numColumn==2:
                    HTMLResults=HTMLResults + "<tr bgcolor='#FF0000'><td>PARTIAL MATCH</td>\n<td>%s</td>\n<td>%s</td>\n<td></td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(p[0]),str(p[1]),str(q[0]),str(q[1]))
                elif numColumn==3:
                    HTMLResults=HTMLResults + "<tr bgcolor='#FF0000'><td>PARTIAL MATCH\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<th></th>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(p[0]),str(p[1]),str(p[2]),str(q[0]),str(q[1]),str(q[2]))
                elif numColumn==4:
                    HTMLResults= HTMLResults+ "<tr bgcolor='#FF0000'>\n<th>PARTIAL MATCH</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th></th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n</tr>" %(str(p[0]),str(p[1]),str(p[2]),str(p[3]),str(q[0]),str(q[1]),str(q[2]),str(q[3])) 
                z=z+1
                break
            elif counter3 == len(rowsTarget)-1:
                noMatchSour.append(parMatch[counter2])
    if numColumn==2:
        rowResults.append(("","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='6'></th></tr>\n"
    elif numColumn==3:
        HTMLResults=HTMLResults + "<tr><th colspan='8'></th></tr>\n"
        rowResults.append(("","","","","","","",""))
    elif numColumn==4:
        rowResults.append(("","","","","","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='10'></th></tr>\n"

    for counter,b in enumerate(noMatchSour):
        if numColumn==2:
            rowResults.append((("NO MATCH",)+b+("","","")))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\n<td>NO MATCH</td>\n<td>%s</td>\n<td>%s</td>\n<td></td>\n<th colspan='2'></th>\n</tr>\n" %(str(b[0]),str(b[1]))
        elif numColumn==3:
            rowResults.append((("NO MATCH",)+b+("","","","")))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\n<td>NO MATCH</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td></td>\n<th colspan='3'></th>\n</tr>\n" %(str(b[0]),str(b[1]),str(b[2]))
        elif numColumn==4:
            rowResults.append((("NO MATCH",)+b+("","","","","")))
            HTMLResults= HTMLResults+ "<tr bgcolor='#FFFF00'>\n<th>NO MATCH</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th></th>\n<th></th>\n<th colspan='6'></th>\n</tr>" %(str(b[0]),str(b[1]),str(b[2]),str(b[3])) 
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
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\n<td>NO MATCH</td>\n<th colspan='2'></th>\n<td></td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(c[0]),str(c[1])) 
        elif numColumn==3:
            rowResults.append((("NO MATCH",)+("","","","")+c))
            HTMLResults=HTMLResults + "<tr bgcolor='#FFFF00'>\n<td>NO MATCH</td>\n<th colspan='3'></th>\n<td></td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n" %(str(c[0]),str(c[1]),str(c[2])) 
        elif numColumn==4:
            rowResults.append((("NO MATCH",)+("","","","","",)+c))
            HTMLResults= HTMLResults+ "<tr bgcolor='#FFFF00'>\n<th>NO MATCH</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th>%s</th>\n<th></th>\n<th></th>\n<th colspan='6'></th>\n</tr>" %(str(c[0]),str(c[1]),str(c[2]),str(c[3])) 
        y=y+1

    HTMLResults=HTMLResults+"\n</table>\n</body>\n</html>"
    results.write(HTMLResults)
    sys.stdout.write('.')
    sys.stdout.flush()

    results.close() 
    if z>0:
        passFail="Fail"
        HTMLFileMix=HTMLFileMix +'\n<tr bgcolor="#FF0000">\n' #changes color of row in summary table
        Fail=Fail+1
    elif (x+z+w)==0 and (x+z+y)==0:
        passFail="Empty Sour & Tar"
        HTMLFileMix=HTMLFileMix +'\n<tr bgcolor="#FFFF00">\n'
        Empty=Empty+1
    elif (x+z+y)==0:
        passFail="Empty Tar"
        HTMLFileMix=HTMLFileMix +'\n<tr bgcolor="#FFFF00">\n'
        Empty=Empty+1
    elif (x+z+w)==0:
        passFail="Empty Sour"
        HTMLFileMix=HTMLFileMix +'\n<tr bgcolor="#FFFF00">\n'
        Empty=Empty+1
    else:
        passFail="Pass"
        HTMLFileMix=HTMLFileMix +'\n<tr bgcolor="#00FF00">\n'
        Pass=Pass+1
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
    
def testMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,typeFeat,crsr,decimalplaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList):
    from ConfigParser import SafeConfigParser
    from com.ziclix.python.sql import zxJDBC
    from operator import is_not
    from testSQLFunction import SQLFunctionSource
    from testSQLFunction import SQLFunctionTarget

    import datetime
    import sys
    global dataline
    dataline="<tr>\n"
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
    HTMLFileM=""
    typeArr=[]
    decimalPlaces=decimalplaces
    TYPE=typeFeat
    #6thStart
    testKPI=['1', '2', '3']
    #6thEnd
    lenKPI=len(testKPI)
    
    noSpace=''
    result_pathtest= path+"\Results\\test"
    result=result_pathtest+"\%s" %(noSpace)

    counterArr=0

    headerline="<tr>\n"
    headerlineX=""

    dataline="<tr>\n"
    counterArr=0
    Fail=0
    Pass=0
    Empty=0
    multiCom=0
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
    <table style="width:100%">
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
    
            l= [t.strftime("%Y-%m-%d %H:%M") for t in l]
            dateTime=dateTime + l
        else:
            dateTime.append(splitDate[x]) #if not arrow was found add the indivual date to the array of datetimes
    splitDate=dateTime
    noSpace =','.join(splitDate) #converts the list into a string to be used for the names of the files-
        
    if configType !="multi":
        if KPI_VALUE =="all":
            splitKPI=testKPI
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
        splitKPI=testKPI
    
    if NODE_NAME =='' or NODE_NAME== None:
        splitNode=[""]
        #nested for loops to go through all the possibly configrations of the multiple KPI's and Dates
        for x,i in enumerate(splitKPI):
            counterArr=counterArr+1
            #for y, t in enumerate(splitNode19): #Used only for LTEOpt KPI19
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
                if SQLConfig[0] in testKPI: 
                    sourceResults=SQLFunctionSource(SQLConfig,noNode)
                    targetResults=SQLFunctionTarget(SQLConfig,noNode)
                    rowsSource= sourceWritetest(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                    rowsTarget= targetWritetest(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                    resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig)
                    HTMLFileM +=resultReturn[0]
                    Pass+=resultReturn[1]
                    Fail+=resultReturn[2]
                    Empty+=resultReturn[3]
                    returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_pathtest,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]

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
                    if SQLConfig[0] in testKPI:
                        sourceResults=SQLFunctionSource(SQLConfig,noNode)
                        targetResults=SQLFunctionTarget(SQLConfig,noNode)
                        rowsSource= sourceWritetest(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        rowsTarget= targetWritetest(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig)
                        HTMLFileM +=resultReturn[0]
                        Pass+=resultReturn[1]
                        Fail+=resultReturn[2]
                        Empty+=resultReturn[3]
                        returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_pathtest,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]
    return returnArr
    