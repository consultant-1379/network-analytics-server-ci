#!/usr/bin/env rubyl
#Encoding: UTF-8
require 'rubygems'
require "selenium-webdriver"
require 'json'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'time'
require 'net/http'
require 'uri'
require 'csv'

def writeConfluence(confluenceData)





end

def tryupdateConfluence(newBuildData, runType)

	currentData=loadConfluencePage(runType)
	newData=newBuildData

	newData.each do |new|
		currentData.each do |old, index|
			if (new[1] == old[1])
				currentData[index].insert(2, new[2])
			else
				currentData.push(new)
			end
		end
	end
	return currentData

end

def addSuiteConfluence(teamStatus, raType, suiteName, teamName, runType, confluenceID)

	properties=load_properties()
	user="assure"
	passwd="assure"

	#uri = URI("http://confluence-nam.lmera.ericsson.se/rest/api/content/#{confulenceID}?expand=body.storage,version&os_authType=basic")
	uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confluenceID}?expand=body.storage,version")

	Net::HTTP.start(uri.host, uri.port,
	:use_ssl => uri.scheme == 'https',
	:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|

		request = Net::HTTP::Get.new uri.request_uri
		request.basic_auth "#{user}", "#{passwd}"

		response = http.request request # Net::HTTPResponse object

		jsonResult=JSON.parse(response.body)

		jsonResult['version']['number']+=1
		newSuite=jsonResult['body']['storage']['value']
		if(newSuite=="")
			newSuite.concat("<table><tbody><tr><th><p>&nbsp;<\/p><p>&nbsp;<\/p><p>&nbsp;<\/p><p>RA<\/p><\/th><th><p>&nbsp;<\/p><p>&nbsp;<\/p><p>&nbsp;<\/p><p>Suite Name - (<em>Team Names<\/em>)<\/p><\/th>")
		else
			p newSuite
			newSuite.gsub!("<
tbody></table>", "")
		end

		newSuite.concat("<tr><td colspan=\"1\">#{raType}<\/td><td colspan=\"1\"><strong>#{suiteName}<\/strong> - (<em>#{teamName}<\/em>)<\/td><\/tr>")
		newSuite.concat("<\/tbody><\/table>")

		jsonResult['body']['storage']['value']=newSuite
		confluencePageURI=jsonResult['_links']['self']

		File.open("jsonOutput", "w") do |f|
		f.write(jsonResult.to_json)
		end

		#system("echo #{jsonResult.to_json} > #{updatedTableFile}")

		system("curl -u '#{user}:#{passwd}' -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d @jsonOutput  #{confluencePageURI}")

	end

end

def updateConfluence(tableData,teamStatus,confulenceID)

	properties=load_properties()
	user="#{properties["UserName"]}"
	passwd="#{properties["UserPassword"]}"

	#One (1) is subtracted the 'numberOfBuildsMonitored' as it is an array referance hence starts from 0 therefore as a example monitoring 3 columns means 0,1,2
	numberOfBuildsMonitored=Integer("#{properties["NumberOfBuildsMonitored"]}")-1
	#Setting the minimium number of columns to monitor i.e. column 0 and column 1
	if(numberOfBuildsMonitored<2)
		numberOfBuildsMonitored=1
	end


	formattedDateOfExecution = "#{tableData["Date/Time Started"]}"

	#uri = URI("http://confluence-nam.lmera.ericsson.se/rest/api/content/#{confulenceID}?expand=body.storage,version&os_authType=basic")
	uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confulenceID}?expand=body.storage,version")

	Net::HTTP.start(uri.host, uri.port,
	:use_ssl => uri.scheme == 'https',
	:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|

	request = Net::HTTP::Get.new uri.request_uri
	request.basic_auth "#{user}", "#{passwd}"

	response = http.request request # Net::HTTPResponse object

	jsonResult=JSON.parse(response.body)

	#
	confulenceType=jsonResult['type']
	confulenceTitle=jsonResult['title']
	confulenceStatus=jsonResult['status']
	confulencePageURI=jsonResult['_links']['self']

	htmlTable=jsonResult['body']['storage']['value']
	newConfulenceVersion=jsonResult['version']['number'] += 1

	updatedTableFile="./newTableVersion_#{tableData["ENM_ISO_Version"]}_#{newConfulenceVersion}"

	updatedTable="{\"id\":\"#{confulenceID}\",\"type\":\"#{confulenceType}\",\"title\":\"#{confulenceTitle}\",\"status\":\"#{confulenceStatus}\",\"body\":{\"storage\":{\"value\":\""


	splitByTableRecords="</tr><tr>"
	dataByTableRecords = htmlTable.split(splitByTableRecords)

	#This is the header row (row zero) hence it needs to be update per build
	#Now that we have the headers we need to update the columns
    splitByTableHeaders="</th><th>"
	dataByTableHeaders = dataByTableRecords[0].split(splitByTableHeaders)

	#This is just the Tribe and Suite - Team neame header
	updatedTable=dataByTableHeaders[0].concat(splitByTableHeaders).concat(dataByTableHeaders[1]).concat("</th>")

	#The run run
	newHeader="<th><p style=\"text-align: center;\">#{tableData["ENM_ISO_Version"]}</p><p style=\"text-align: center;\">#{tableData["clusterId"]}</p><p style=\"text-align: center;\">#{formattedDateOfExecution}</p><p style=\"text-align: center;\">#{tableData["TE_ALLURE_LOG_URL"]}</p></th><th>"
	updatedTable=updatedTable.concat(newHeader)

	arrayTest = teamStatus.keys
	halfOfTheTeams=(arrayTest.length-1)/2

	#The actual number of columns needs to be calculate
	#teamColumnsOffset is the number of columna coontaining the team names/suites and the catorgiese PM/FM etc
	teamColumnsOffset=2
	maxNumberOfColumns=numberOfBuildsMonitored+1
	arraySize=(dataByTableHeaders.length-1)

	if(arraySize>maxNumberOfColumns)
		arraySize=maxNumberOfColumns
		addClosingHeaderTag=true
	end


	for i in 2..arraySize
		updatedTable=updatedTable.concat(dataByTableHeaders[i])
		#Need to stop the last append of 'splitByTableHeaders'
		if(i<arraySize)
			updatedTable=updatedTable.concat(splitByTableHeaders)
		end
	end

	if(addClosingHeaderTag)
		updatedTable=updatedTable.concat("</th>")
	end

	updatedTable=updatedTable.concat(splitByTableRecords)







	splitByTableData="</td>"

	#Contiue to output the remainder of the table rows (the header is in the first element of the array)
	dataByTableRecordsArraySize=dataByTableRecords.length-1
	for tableRecordsIndex in 1..dataByTableRecordsArraySize

		dataByTableData=dataByTableRecords[tableRecordsIndex].split(splitByTableData)

		if(tableRecordsIndex==halfOfTheTeams)
			referanceTableSplit="#{dataByTableData[1]}"
		end

		#if("#{dataByTableData[0]}".include? "rowspan") || ("#{dataByTableData[0]}".include? "colspan")
			updatedTable=updatedTable.concat("#{dataByTableData[0].concat(splitByTableData).concat(dataByTableData[1]).concat(splitByTableData).concat("<td>").concat("#{teamStatus[arrayTest[tableRecordsIndex-1]]}").concat(splitByTableData)}")
			rowStartPoint=2
		#else
		#	rowStartPoint=1
		#	updatedTable=updatedTable.concat("#{dataByTableData[0].concat(splitByTableData).concat("<td>").concat("#{teamStatus[arrayTest[tableRecordsIndex-1]]}").concat(splitByTableData)}")
		#end

		constrainedDataArraySize=(numberOfBuildsMonitored+rowStartPoint)-1
		actualDataArraySize=(dataByTableData.length-1)
		for x in rowStartPoint..constrainedDataArraySize
			if(x>actualDataArraySize) || ("#{dataByTableData[x]}".include? "</tr></tbody></table>")
				updatedTable=updatedTable.concat("#{dataByTableData[x]}")
			else
				updatedTable=updatedTable.concat("#{dataByTableData[x]}").concat(splitByTableData)
			end
		end


		#Need to stop the last append of 'splitByTableRecords'
		if(tableRecordsIndex<dataByTableRecordsArraySize)
			updatedTable=updatedTable.concat(splitByTableRecords)
		end
	end


	if(constrainedDataArraySize<actualDataArraySize)
		updatedTable.concat("</tr></tbody></table>")
	end


	#updatedTable="\",\"representation\":\"storage\"}},\"version\":{\"number\": #{newConfulenceVersion}}}"
	#system("echo '#{updatedTable}' >> #{updatedTableFile}")
	#updatedTable=""
	#system("cat #{updatedTableFile} | tr -d '\r\n' > #{updatedTableFile}_tmp ")
	#system("mv #{updatedTableFile}_tmp #{updatedTableFile}")

	updatedTable=createHtmlTableColours(updatedTable)
	#########print "\nFinal: #{updatedTable}\n\n"

	#newTableContents=jsonResult['body']['storage']['value'].concat(updatedTable.to_json)
	#newTableContents=updatedTable


	writeToFile=updatedTable.split(referanceTableSplit)
	firstFileString="{\"id\":\"#{confulenceID}\",\"type\":\"#{confulenceType}\",\"title\":\"#{confulenceTitle}\",\"status\":\"#{confulenceStatus}\",\"body\":{\"storage\":{\"value\":\""
	system("echo #{firstFileString.to_json} > #{updatedTableFile}")
	system("echo '#{writeToFile[0].to_json[1..-2]}' >> #{updatedTableFile}")
	system("echo '#{referanceTableSplit.to_json[1..-2]}' >> #{updatedTableFile}")
	system("echo '#{writeToFile[1].to_json[1..-2]}' >> #{updatedTableFile}")



	#
	#

	lastFileString="\",\"representation\":\"storage\"}},\"version\":{\"number\": #{newConfulenceVersion}}}"
	system("echo #{lastFileString.to_json} >> #{updatedTableFile}")

	system("cat #{updatedTableFile} | tr -d '\r\n' > #{updatedTableFile}_tmp ")
	system("mv #{updatedTableFile}_tmp #{updatedTableFile}")




	#system("echo '{\"id\":\"#{confulenceID}\",\"type\":\"#{confulenceType}\",\"title\":\"#{confulenceTitle}\",\"status\":\"#{confulenceStatus}\",\"body\":{\"storage\":{\"value\":#{newTableContents},\"representation\":\"storage\"}},\"version\":{\"number\": #{newConfulenceVersion}}}' > test.txt")



	system("curl -u '#{user}:#{passwd}' -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d @#{updatedTableFile}  #{confulencePageURI}")

	system("rm #{updatedTableFile}")
end




end




def createHtmlTableColours(htmlWitoutColours)

	replacements = [ ["<td>FAILURE", "<td style=\"text-align: center;\" bgcolor=\"#d95250\">FAILURE"] , ["<td>SUCCESS", "<td style=\"text-align: center;\" bgcolor=\"#5cb85c\">SUCCESS"], ["<td>Not Executed!", "<td style=\"text-align: center;\" bgcolor=\"#f0ad4f\">Not Executed!"]]
	replacements.each {|replacement| htmlWitoutColours.gsub!(replacement[0], replacement[1])}

return "#{htmlWitoutColours}"
end
