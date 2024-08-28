def sourceWriteVoLTE(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):
    import os
    import math
    from operator import itemgetter
    from numbers import Number
    crsr.execute("%s" %(sourceResults))#executes the SQL
    global sourceHyper#hyper link used in the htnml tables
    global targetHyper#hyper link used in the htnml tables
    global resultHyper#hyper link used in the htnml tables
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
    rows=[] #array used to store the source information needed to match up with the target table
    if not os.path.exists(result):
        os.makedirs(result)
    SourceFile= open(os.path.join(result,'%s_%s_%s_Source_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w+') #opens/creates the file need to write the results of the source Query       
    sourceHyper='.\\%s_%s_%s_Source_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)
    targetHyper='.\\%s_%s_%s_Target_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)
    resultHyper='.\\%s_%s_%s_Results_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)
    summaryHyper='.\\Summary.HTML'
    headerlineS = ''
    #For a column in the headers add it onto headerlineS
    for column in descSour:
        headerlineS=headerlineS + "\n<th>%s</th>" %(str(column[0]))
        headerName.append(str(column[0]))
        
    headerlineS=headerlineS + "\n<tr>\n" #Ends the row of headers
    HTMLTest=HTMLTest+headerlineS #add the headers into the HTML string
    #Loops through the reults of the SQL row by row
    for row in rowSour:
        datalineS="\n<tr>\n"#html code to start row in a table
        cnt=0
		#loops trough the individualvalues in the current row
        for column in row:
			#checks if certain character(s) are found in that value and if so adds it to an array. used for auto matching
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
            datalineS=datalineS + "<td>%s</td>\n" %(str(column))#Add in the current value into the current row in the html table
        datalineS=datalineS +"<tr>\n"#finishes the current row
        HTMLTest=HTMLTest+datalineS #adds row to the html table   
        #Checks to see what KPI_ID values has been chosen of this instance and adds the relevant value for matching to an array of that value's header name.

        if SQLConfig[0]=='1':
            col1.append(row[1])
            col3.append(row[3])

        if SQLConfig[0]=='2':
            col1.append(row[1])
            col3.append(row[3])
        
        if SQLConfig[0]=='3':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='4':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='5':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='6':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='7':
            col0.append(row[0])
            col3.append(row[3])

        if SQLConfig[0]=='8':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='9':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='10':
            col1.append(row[1])
            col2.append(row[2])
                    
        if SQLConfig[0]=='11':
            col1.append(row[1])
            col3.append(row[3])

        if SQLConfig[0]=='12':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='14':
            col4.append(row[4])
            col3.append(row[3])

        if SQLConfig[0]=='15':
            col3.append(row[3])
            col2.append(row[2])
        
        if SQLConfig[0]=='17':
            col4.append(row[4])
            col3.append(row[3])

        if SQLConfig[0]=='18':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='19':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='20':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='21':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='22':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='23':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='24':
            col1.append(row[1])
            col3.append(row[3])
        
        if SQLConfig[0]=='25':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='26':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='27':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='28':
            col0.append(row[0])
            col2.append(row[2])
        
        if SQLConfig[0]=='29':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='30':
            col1.append(row[1])
            col2.append(row[2])
        
        if SQLConfig[0]=='31':
            col0.append(row[0])
            col2.append(row[2])

        if SQLConfig[0]=='32':
            col1.append(row[1])
            col2.append(row[2])
        
        if SQLConfig[0]=='33':
            col3.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='34':
            col1.append(row[1])
            col2.append(row[2])
        
        if SQLConfig[0]=='35':
            col0.append(row[0])
            col2.append(row[2])
#1st
    #adds the rounded kpi value and the other values for matching into an array and then adds that array to another array
    if SQLConfig[0]=='1':
        test1=list(col1)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test1,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='2':
        test1=list(col1)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test1,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='3':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='4':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='5':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='6':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='7':
        test0=list(col0)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test0,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='8':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='9':
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

    if SQLConfig[0]=='10':
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

    if SQLConfig[0]=='11':
        test1=list(col1)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test1,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='12':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='14':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='15':
        test2=list(col2)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test2,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='17':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='18':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='19':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='20':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='21':
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

    if SQLConfig[0]=='22':
        test0=list(col0)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test0,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='23':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='24':
        test1=list(col1)
        test3=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test1,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='25':
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

    if SQLConfig[0]=='26':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='27':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='28':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='29':
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

    if SQLConfig[0]=='30':
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

    if SQLConfig[0]=='31':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='32':
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

    if SQLConfig[0]=='33':
        test3=list(col2)	#edit- test3 was set where test2 is set and vis versa
        test2=list(col3)
        ForTest3=[]
        for number in range(len(test3)):
            if test3[number] is not None:
                ForTest3.append(math.floor(test3[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest3.append(test3[number])
        rows = zip(test2,ForTest3)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='34':
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

    if SQLConfig[0]=='35':
        test0=list(col0)
        test2=list(col2)
        ForTest2=[]
        for number in range(len(test2)):
            if test2[number] is not None:
                ForTest2.append(math.floor(test2[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest2.append(test2[number])
        rows = zip(test0,ForTest2)
        rows =sorted(rows,key=itemgetter(1))

#2nd

    HTMLTest =HTMLTest +"\n<h1>Source results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>\n"%(SQLConfig[0],SQLConfig[1],SQLConfig[2]) #Adds a header to above the table of the source file displaying the configuration chosen.
    HTMLTest=HTMLTest +"<h4><a href='%s'>Target</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></h4>\n"% (targetHyper,resultHyper,summaryHyper)
    SourceFile.write(HTMLTest)# Writes the HTML string to the file.
    #Checks to see what KPI_ID value was chosen and then places the data need for matching against the target table into and array named rows.
    SourceFile.close() #close the file that was written to.
    return rows #return the array full of the variables needed to compare against the values found in the target table

def targetWriteVoLTE(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader):  
    from numbers import Number
    import os
    import math
    from operator import itemgetter
    crsr.execute("%s" %(targetResults))
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

    HTMLTest=HTMLTable # Local variable version of HTMLTable
    if not os.path.exists(result):
        os.makedirs(result)  
    targetSQL= open(os.path.join(result,'%s_%s_%s_Target_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w') #opens the file needed to write the results
    #Some arrays named after the headers found in the tables for the different 
    headerName=[]
    headerlineT = ''
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
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='2':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='3':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='4':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='5':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='6':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='7':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='8':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='9':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='10':
            col3.append(row[3])
            col4.append(row[4])
                    
        if SQLConfig[0]=='11':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='12':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='14':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='15':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='17':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='18':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='19':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='20':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='21':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='22':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='23':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='24':
            col1.append(row[1])
            col2.append(row[2])
        
        if SQLConfig[0]=='25':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='26':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='27':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='28':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='29':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='30':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='31':
            col3.append(row[3])
            col4.append(row[4])

        if SQLConfig[0]=='32':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='33':
            col1.append(row[1])
            col2.append(row[2])

        if SQLConfig[0]=='34':
            col3.append(row[3])
            col4.append(row[4])
        
        if SQLConfig[0]=='35':
            col3.append(row[3])
            col4.append(row[4])
#3rd  
    #Makes the arrays with the elements for comparison into lists and rounds the KPI_Value to two decimal places and then sorts them

    if SQLConfig[0]=='1':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='2':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='3':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='4':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='5':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='6':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows = sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='7':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='8':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='9':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='10':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='11':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='12':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='13':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='14':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='15':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='16':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='17':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='18':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='19':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='20':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='21':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='22':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='23':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='24':
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

    if SQLConfig[0]=='25':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='26':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='27':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='28':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='29':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='30':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='31':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='32':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='33':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='33':
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

    if SQLConfig[0]=='34':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

    if SQLConfig[0]=='35':
        test3=list(col3)
        test4=list(col4)
        ForTest4=[]
        for number in range(len(test4)):
            if test4[number] is not None:
                ForTest4.append(math.floor(test4[number]*decimalPlaces)/decimalPlaces)
            else:
                ForTest4.append(test4[number])
        rows = zip(test3,ForTest4)
        rows =sorted(rows,key=itemgetter(1))

#4th
    HTMLTest =HTMLTest +"\n<h1>Target results for configuration KPI: %s, Datetime_ID: %s, Node_Name: %s </h1>"%(SQLConfig[0],SQLConfig[1],SQLConfig[2]) #Adds a summary of the specific configuration to the file above the table
    HTMLTest=HTMLTest +"<h4><a href='%s'>Source</a><span> </span><a href='%s'>      Results</a><span> </span><a href='%s'>      Summary</a></H4>\n"% (sourceHyper,resultHyper,summaryHyper)
    targetSQL.write(HTMLTest)  #Write the HTML code found inside the HTML string  to the file. 
    targetSQL.close()
    return rows #returns the list of elements needed for the comparison against the source Table

def resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig,serverNum,serverName,dateTag):
    import os
    import sys
    import emailAlert as sendEmail
    rowsx =rowsTarget
    global sourceHyper
    global targetHyper
    global resultHyper
    global summaryHyper
    global failFlag
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
    results= open(os.path.join(result,'%s_%s_%s_Results_VoLTE.HTML' %(SQLConfig[0],SQLConfig[2],noSpace)),'w')
    #Checks if there was a node_name selected in the config file and writes a summary depending 
    if SQLConfig[1] != "" and SQLConfig[2] == "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s </h1>\n" %(SQLConfig[0],SQLConfig[1])
    elif SQLConfig[1] != "" and SQLConfig[2] != "":
        HTMLResults=HTMLResults + "<h1>RESULTS CONFIGURED BY KPI_ID: %s AND DATE AND TIME: %s AND NODE_NAME: %s </h1>\n"%(SQLConfig[0],SQLConfig[1],SQLConfig[2])
    HTMLResults=HTMLResults +"<h4><a href='%s'>Source</a><span> </span><a href='%s'>      Target</a><span> </span><a href='%s'>      Summary</a></H4>\n"% (sourceHyper,targetHyper,summaryHyper)


    if SQLConfig[0]=='1':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='2':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='3':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='4':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='5':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='6':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='7':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='8':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='9':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='10':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='11':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='12':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='13':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='14':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='15':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='16':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='17':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='18':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='19':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='20':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='21':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='22':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='23':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='24':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='25':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='26':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='27':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='28':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='29':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='30':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='31':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='32':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='33':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='34':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


    if SQLConfig[0]=='35':
        ColumnNameSour=[u'Node_Name', u'KPI_VALUE']
        ColumnNameTar=[u'Node_Name', u'KPI_VALUE']            
        numColumn=2
        HTMLResults=HTMLResults + "<tr>\n<th>Match Type</th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n<th></th>\n<th>Node_Name</th>\n<th>KPI_VALUE</th>\n</tr>\n" #Adds the headers for VoLTE to the table in the file
        HTMLResults=HTMLResults + "<tr>\n<th></th>\n<th colspan='2'><a href='%s'>Source</a></th>\n<th></th>\n<th colspan='2'><a href='%s'>Target</a></th>\n</tr>\n"%(sourceHyper,targetHyper)


#5th
    
    headerName=["Match Type"]+ColumnNameSour+[""]+ColumnNameTar
    if numColumn==2:
        rowResults.append(("","Source","","","Target","",""))
    elif numColumn==3:
        rowResults.append(("","Source","","","","Target","",""))
    elif numColumn==4:
        rowResults.append(("","Source","","","","","Target","","",""))

    for counter,n in enumerate(rowsSource): #loops through the array with values from source table for matching
        if len(rowsTarget)==0:
            noMatchSour.append(rowsSource[counter])
        for counter1,m in enumerate(rowsTarget): #loops through the array with values from target table for matching
			#checks if the current loop values match and if so adds row to html table
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
			#if the target loop reaches the end and no match for the source result is found. Add it to an array
			if counter1 == len(rowsTarget)-1:
				parMatch.append(rowsSource[counter])
	#formatting depending on number of columns
    if numColumn==2:
        rowResults.append(("","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='6'></th></tr>\n"
    elif numColumn==3:
        HTMLResults=HTMLResults + "<tr><th colspan='8'></th></tr>\n"
        rowResults.append(("","","","","","","",""))

    elif numColumn==4:
        rowResults.append(("","","","","","","","","",""))
        HTMLResults=HTMLResults + "<tr><th colspan='10'></th></tr>\n"
	#loops through the array of source values that didnt have a match and checks if it has a partail matches with a value in the target array
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
			#If no partial match is found adds to another array 
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
	
	#loops through array of no matches and adds them to the html table
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
	#Loops through the same process for the target vlaues for matching
    for counter5,g in enumerate(rowsx):
        if len(rowsSource)==0:
            noMatchTar.append(rowsx[counter5])
        for counter6,h in enumerate(rowsSource):
            if g[0]==h[0] and g[1] == h[1]:
                break
            elif counter6== len(rowsSource)-1:
                noMatchTar.append(rowsx[counter5])
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
        if failFlag==0:	#only allow one run
            failFlag=failFlag+1
            sendEmail.sendAlertEmail('VoLTE',serverNum,serverName,SQLConfig[0],dateTag)
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
	
def VoLTEMain(DATETIME_ID,configTime,path,timeElem,configType,KPI_VALUE,NODE_NAME,splitNode19,typeFeat,crsr,decimalplaces,nodeNameList,headerNameList,KPINameList,dashHeaderList,dashList,serverNum,serverName):
    from ConfigParser import SafeConfigParser
    from com.ziclix.python.sql import zxJDBC
    from operator import is_not
    from VoLTESQLFunction import SQLFunctionSource
    from VoLTESQLFunction import SQLFunctionTarget
    import datetime
    import sys
    sys.stdout.flush()
    global failFlag
    failFlag=0
    noNode=0 #set to 1 if there is no node_name given in the config file
    decimalPlaces=decimalplaces
    TYPE=typeFeat
    #6thStart
    VoLTEKPI=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15", "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35"]
    #6thEnd
    lenKPI=len(VoLTEKPI)
    returnArr=[]

	#counters for the different kind of results
    Fail=0
    Pass=0
    Empty=0
    dateTag=DATETIME_ID.replace(":","_")
    result_pathVoLTE= path+"\\Results\\"+serverName+"\\VoLTE\\"    #path to the result folder for this feature
    HTMLFileM=""#string that holds code fo a html file
    counterArr=0

    dateTime=[]
	#splits the strings found in headernames.txt into arrays 
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

    #code need to begin a html table
    HTMLTable="""<!DOCTYPE html>
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
    """

    
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
            dateStart = map(int,dateStart ) #Converts the year, month and day array to have int values for the start datetime
            timeStart=map(int,timeStart)#Converts thr timr array to have int values for the start datetime
            dateFin=map(int,dateFin)#Converts the year, month and day array to have int values for the start datetime
            timeFin=map(int,timeFin)#Converts thr timr array to have int values for the start datetime
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
            dateTime.append(splitDate[x]) #if no arrow was found add the individual date to the array of datetimes
    splitDate=dateTime
    noSpace =','.join(splitDate) #converts the list into a string to be used for the names of the files-
    #checks if this run was multiple features
    if configType !="multi":
		#if the config file's KPI_VALUE paramater was set to "all" sets split kpi equal to all the valid KPI Numbers
        if KPI_VALUE =="all":
            splitKPI=VoLTEKPI
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
        splitKPI=VoLTEKPI
    splitNode=[""]
    #checks to see if a node name was given in the config file to configure by
    if NODE_NAME =='' or NODE_NAME== None:
        #nested for loops to go through all the possibly configrations of the multiple KPI's and Dates
        for x,i in enumerate(splitKPI):
            counterArr=counterArr+1
            for a,b in enumerate(splitDate):
                sys.stdout.write('.')
                sys.stdout.flush()
                noSpace = splitDate[a].replace(":", "_") #Replace the : character in the datetime with a _ for compatibility 
                result= result_pathVoLTE+"\\%s" %(noSpace)#result path used to separate the results from each other depending on the datetime_id value

                SQLConfig=[] #array used to store the configuration information ie. KPI and Datetime_id
                
                #Add relevant values for that nested configuration run to SQLConfig
                SQLConfig.append(splitKPI[x])
                SQLConfig.append(splitDate[a])
                SQLConfig.append("")
                SQLConfig.append(splitNode19[0])
                SQLConfig.append(TYPE)
                noNode=1#flag that is set if no node_name was set in the conifgfile
                if SQLConfig[0] in VoLTEKPI:
					sourceResults=SQLFunctionSource(SQLConfig,noNode)#Call to SQL function to return the source SQL
					targetResults=SQLFunctionTarget(SQLConfig,noNode)
					#Calls to the write functions to create the source and target tables and returns the values for match checking
					rowsSource= sourceWriteVoLTE(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
					rowsTarget= targetWriteVoLTE(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
					#Call to results function where results table is created and where matching takes place
					resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig,serverNum,serverName,dateTag)
					HTMLFileM +=resultReturn[0]
					Pass+=resultReturn[1]
					Fail+=resultReturn[2]
					Empty+=resultReturn[3]
					#array that returns values to the scripts main file
					returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_pathVoLTE,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]

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
                    result= result_pathVoLTE+"\\%s" %(noSpace)#result path used to separate the results from each other depending on the datetime_id value of each
                    SQLConfig=[] #array used to store the configuration information ie. KPI and Datetime_id
                    #Add relevant values for that nested configuration run to SQLConfig
                    SQLConfig.append(splitKPI[l])
                    SQLConfig.append(splitDate[a])
                    SQLConfig.append(splitNode[y])
                    SQLConfig.append("")
                    SQLConfig.append(TYPE)
                    if SQLConfig[0] in VoLTEKPI:
                        sourceResults=SQLFunctionSource(SQLConfig,noNode)
                        targetResults=SQLFunctionTarget(SQLConfig,noNode)
                        rowsSource= sourceWriteVoLTE(sourceResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        rowsTarget= targetWriteVoLTE(targetResults,crsr,SQLConfig,noSpace,HTMLTable,erbsArr,erbsHeadArr,result,decimalPlaces,KPIHeader,dashArr,dashHeader)
                        resultReturn=resultsWrite(rowsSource,rowsTarget,noSpace,HTMLTable,result,SQLConfig,serverNum,serverName,dateTag)
                        HTMLFileM +=resultReturn[0]
                        Pass += resultReturn[1]
                        Fail +=resultReturn[2]
                        Empty +=resultReturn[3]
                        returnArr=[lenKPI,Pass,Fail,Empty,result,splitKPI,splitDate,splitNode,HTMLFileM,result_pathVoLTE,erbsArr,erbsHeadArr,KPIHeader,dashHeader,dashArr]
    return returnArr

