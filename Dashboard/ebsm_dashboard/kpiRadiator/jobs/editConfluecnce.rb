require 'rubygems'
require 'json'
require 'open-uri'
require 'date'
require 'time'
require 'nokogiri'
require 'rubygems'
require "selenium-webdriver"
require 'net/http'
require 'rss/utils'
require 'uri'
require 'csv'
require 'cgi'
require "erb"

SCHEDULER.every '1440m', :first_in => 0 do
	failCount=0		#failCount will tell us if a fail has been noted
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))		#read in yaml file
	confID = properties["confluenceID"]
	uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confID}?expand=body.storage,version")
	jsonResult=Hash.new()
#Load Confluence Data
	Net::HTTP.start(uri.host, uri.port, :use_ssl => uri.scheme == 'https',:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		request = Net::HTTP::Get.new uri.request_uri
		request.basic_auth "assure", "assure"
		response = http.request(request)
		jsonResult = JSON.parse(response.body)
	end
	parseConfluenceData(jsonResult,failCount)
end

def parseConfluenceData(jsonResult,failCount)	#Parse Data To Array(jsonResult)
	jsonTable=jsonResult['body']['storage']['value']
	html=Nokogiri::HTML(jsonTable)
	if(jsonTable=="")	#if table in confluence is empty, create one
		puts "Load Confluence: Table does not exist!"
		newTable=Array.new()
		newTable.push(["Server", "Feature", "KPI"])
		mergeData(newTable,jsonResult,failCount)
	else
		tableRows=html.search('table')
		header=tableRows.search('tr').map do |rows, i|
			rows.css('th').map(&:text)
		end

		content=tableRows.search('tr').map do |rows, i|
			rows.css('td').map(&:text)
		end

		content.delete_at(0)
		fullTable=content.insert(0, header[0])
		mergeData(fullTable,jsonResult,failCount)
	end
end

def formatConfluencePage(columnData,row,headerDate)	#adds the colours to each KPIs status as well as a link
	serverNam=row[0]
	featureNam=row[1]
	kpiNum=row[2]

    colorColumn=""
    if columnData == "Fail"
        colorColumn.to_s.concat("<td bgcolor=\"#E32219\"><a href=\"http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{headerDate}/#{kpiNum}__#{headerDate}_Results_#{featureNam}.html\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</a></td>")
		failCount=1		#if a fail is noted, set failCount to true(true = 1)
        return colorColumn
    end
    if columnData == "Pass"
        colorColumn.to_s.concat("<td bgcolor=\"#89BA17\"><a href=\"http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{headerDate}/#{kpiNum}__#{headerDate}_Results_#{featureNam}.html\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</a></td>")
        return colorColumn
    end
    if columnData == "Not Executed"
        colorColumn.to_s.concat("<td bgcolor=\"#F68B1F\"><a href=\"http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{headerDate}/#{kpiNum}__#{headerDate}_Results_#{featureNam}.html\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</a></td>")
        return colorColumn
    end
    if columnData == "Empty Sour & Tar" or columnData == "Empty Sour &amp; Tar"
        colorColumn.to_s.concat("<td bgcolor=\"#FABB00\"><a href=\"http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{headerDate}/#{kpiNum}__#{headerDate}_Results_#{featureNam}.html\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</a></td>")
        return colorColumn
    end
    if columnData == "Empty Sour" or columnData == "Empty Tar"
        colorColumn.to_s.concat("<td bgcolor=\"#FABB00\"><a href=\"http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{headerDate}/#{kpiNum}__#{headerDate}_Results_#{featureNam}.html\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</a></td>")
        return colorColumn
    end

    colorColumn.to_s.concat("<td>")
    colorColumn.to_s.concat(columnData.to_s)
    colorColumn.to_s.concat("</td>")
    return colorColumn

end

def cullData(arrayData)
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))	

	arrayData.each_with_index do |row, i|
		while(row.length > (properties['buildsToMonitor']+3))
			row.pop
		end
	end
end

def mergeData(fullTable,jsonResult,failCount)
	latestRun = hashedStatus()	#hashedStatus will return back a hashmap holding all data from the results dir (using the html files)
	arrayServers = latestRun.keys
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))

	if fullTable != nil	#do not execute if there is no data in the table
		
		if fullTable[0][3] != properties['newestDate']	#if the last date upload to confluence is not the latest run that the yaml file says
			fullTable.each_with_index do |index|
				index.insert(3, "Not Executed")	#add a column of 'Not Executed' to the confluence table (they will be overwrite as their true values are read in)
			end
			fullTable[0][3] = properties['newestDate']	#overwrite the header of the new column for this new date
		end
		
		fullTable.each_with_index do |row, i|
			if i!=0
				latestRun.dig(row[0],row[1], properties['newestDate'], row[2])
				
				if latestRun.dig(row[0],row[1], properties['newestDate'], row[2]) != nil
					row[3]=latestRun[row[0]][row[1]][properties['newestDate']][row[2]]
					latestRun[row[0]][row[1]][properties['newestDate']].delete(row[2])
				end
			end
		end
	end
	
	fullTable = addNewKPI(latestRun,fullTable,properties['newestDate'])	#sends a hashmap of KPIs that are not in the confluence page to a function to append them to the end of the fullTable
	
	cullData(fullTable)	#removes old dates(confluence will have the last 7 runs)

	UpdateTable(fullTable,jsonResult,failCount)
end
	
def UpdateTable(fullTable,jsonResult,failCount)
	htmlTable="<table><tbody>"
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))
	
	headerDates=fullTable[0][3..(properties['buildsToMonitor']+3)]	#this will hold an array of the headers ie Date
	fullTable.each_with_index do |row, i|
		htmlTable.to_s.concat("<tr>")
		if i!=0
			row.each_with_index do |column,dateIndex|
				htmlTable.to_s.concat(formatConfluencePage(column.to_s,row,headerDates[dateIndex-3]))
			end
		else
			row.each do |column|
				htmlTable.to_s.concat("<th>")
				htmlTable.to_s.concat(column.to_s)
				htmlTable.to_s.concat("</th>")
			end
		end
		htmlTable.to_s.concat("</tr>")
	end

	htmlTable.to_s.concat("</tbody></table>")

	confluencePageURI=jsonResult['_links']['self']
	jsonResult['body']['storage']['value']=htmlTable
	jsonResult['version']['number']+=1	#increase the version number on the confluence page

	confluenceSend(jsonResult,failCount)	#call function to upload to confluence    
end

def confluenceSend(jsonResult,failCount)
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))
	confID = properties["confluenceID"]
	uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confID}")
	request = Net::HTTP::Put.new(uri)
	request.basic_auth("assure", "assure")
	request.content_type = "application/json"

	jsonHolder = JSON.generate(jsonResult)
	jsonHolder.gsub!(/&(?!amp;)/,'&amp;')

	request.body = jsonHolder
	
	response = Net::HTTP.start(uri.host, uri.port, :use_ssl => uri.scheme == 'https',:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		http.request(request)
		puts "Confluence Load: Success!"
	end
	
	#check whether a fail was noted and set status accordingly
	if failCount==1
		status = "Fail"
	elsif failCount==0
		status = "Pass"
	end
	status="Fail"
	statusUpdate(status)	#send result to statusUpdate() in miniStatus.rb (held in jobs dir)
	
	p
end