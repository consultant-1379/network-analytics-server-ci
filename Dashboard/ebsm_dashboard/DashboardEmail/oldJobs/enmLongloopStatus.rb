#!/usr/bin/env ruby
#Encoding: UTF-8
require 'rubygems'
require "selenium-webdriver"
require 'json'
require 'open-uri'
require 'date'
require 'time'

require File.expand_path('../../lib/logging', __FILE__)
require File.expand_path('../../lib/jenkins', __FILE__)

require_relative './email'

$globalMTLongloopTeamStatus = Hash.new()
$globalMTLongloopTeamDateExecute = ""
$globalMTLongloopTag = "Longloop"


SCHEDULER.every '4m', :first_in => 0 do
#SCHEDULER.every '1m', :first_in => 0 do

	properties=load_properties()
	$globalMTLongloopURL="#{properties["MTLongloopURL"]}"
	
	jenkins = Jenkins.new()
	
	
	#for i in 442..446
	#	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTLongloopURL/#{i}/api/json")
	#	processLastMTLLRun(expectedBuildJsonResult,i)
	#	sleep(5)
	#end


	lastProcessedBuildNumber=getLastProcessedMaintrackLlBuildNumber()
	jenkins = Jenkins.new()
	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTLongloopURL/lastCompletedBuild/api/json")
	lastCompletedBuildNumber=expectedBuildJsonResult['number']
	
	#auditLastMTLLRun()
	
	# Look at the lastCompletedBuild "number" if it is greater than the last one processed then obviously it's new :)
	if (lastCompletedBuildNumber>lastProcessedBuildNumber)
			system  "echo #{lastCompletedBuildNumber} > ./lastProcessedBuildNumberFile_#{$globalMTLongloopTag}" 
			processLastMTLLRun(expectedBuildJsonResult,lastCompletedBuildNumber)
	else
		#Nothing has change so just refresh dashing
		sendEventsLongloop()
	end
	#setOverallLongloopStatus()
end

#This is the top level view of RFA and RFA250 (Any one team failure is an overall failure)
def setOverallLongloopStatus()
	if($globalMTLongloopTeamStatus.has_value?('FAILURE'))  
		send_event("MT_Longloop", {status: getStatus("FAILURE"), :text => "Breakdown By Team", :link => "mt-ll"})
	elsif($globalMTLongloopTeamStatus.has_value?('SUCCESS'))
		send_event("MT_Longloop", {status: getStatus("SUCCESS"), :text => "Breakdown By Team", :link => "mt-ll"})
	else
		send_event("MT_Longloop", {status: "danger", :text => "Breakdown By Team", :link => "mt-ll"})	
	end
end

# Method   
def sendEventsLongloop ()
	log = Log.instance
	for key in $globalMTLongloopTeamStatus.keys()
		data =key.split("$")
		items = []
		items << { label: "Test Suite:", value: data[0] }
		items << { label: "Status:", value: "#{$globalMTLongloopTeamStatus[key]}" }
		send_event("#{key}_#{$globalMTLongloopTag}", {status: getStatus("#{$globalMTLongloopTeamStatus[key]}"), items: items})
		log.info("Maintrack Longloop Status is: Team name->#{data[1]}, Test suite->#{data[0]}, Status-> #{$globalMTLongloopTeamStatus[key]}")
	end
end  

def getLastProcessedMaintrackLlBuildNumber ()
	#If the file doesn't exist then we are running for the first time hence we need to be careful
	lastProcessedBuildNumber=`cat ./lastProcessedBuildNumberFile_#{$globalMTLongloopTag} 2> /dev/null`
	if lastProcessedBuildNumber ==""
	   lastProcessedBuildNumber=0
	else
	   lastProcessedBuildNumber=Integer(`cat ./lastProcessedBuildNumberFile_#{$globalMTLongloopTag} 2> /dev/null`)
	end
	return lastProcessedBuildNumber
end

def processLastMTLLRun (jsonResult,urlVersion)

	properties=load_properties()

	#Clear the contents of the global hash
	$globalMTLongloopTeamStatus.clear
	$globalMTLongloopTeamStatus=createDefaultLongLoopTeamStatus()
		
	#Create a readable time/date from EPOCH
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution="#{Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')} (UTC)"
	
	#Create the URL for the build
	currentbuildNumber=jsonResult['number']
	buildURL="<a href=\"#$globalMTLongloopURL/#{currentbuildNumber}\">#{currentbuildNumber}</a>"
	
	trendsPageID=properties["ENMLongLoopConfulenceTrendPage"]
	#trendsPageID=163775815 #Test Page
	mtLlBuildTrendsPageURL="<a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=#{trendsPageID}\">Longloop Trends</a>"
	
	
	#################################
	parameterHashmap = Hash.new
	actionsArray=jsonResult["actions"]
	actionsArray.each do |actionsKey|
		for key in actionsKey.keys()
			if("#{key}"=="parameters")
				parameterHashmap = createParameterHashmap(actionsKey[key])
			end
		end
	end
	
	#Create URL for the Build
	parameterHashmap["Date/Time Started"] = "#{formattedForDisplayDateOfExecution}"
	parameterHashmap["Build Number"] = "#{buildURL}"
	parameterHashmap["EPOCH Time Started"]="#{epochDateTimeStamp}"
	
	#Create the URL link for Allure
	if ("#{parameterHashmap["TE_ALLURE_LOG_URL"]}" == "")
		allureReportURL="No Report Available"
	else
		allureReportURL="<a href=\"#{parameterHashmap["TE_ALLURE_LOG_URL"]}\">Allure</a>"
	end	
	parameterHashmap["TE_ALLURE_LOG_URL"]=allureReportURL
	
	#URL for the LL trends
	parameterHashmap["Longloop Trends"]=mtLlBuildTrendsPageURL
	
	
	
	
	tableHeader = [{ cols: [ {value: 'Attribute'}, {value: 'Value'} ] }]

tableData = [
  { cols: [ {value: 'Date/Time Started'}, {value: formattedForDisplayDateOfExecution }]},
  { cols: [ {value: 'Build Number'}, {value: buildURL} ]},
  { cols: [ {value: 'Allure Report'}, {value: allureReportURL} ]},
  { cols: [ {value: 'Minimum TAF Version'}, {value: "#{parameterHashmap["MINIMUM_TAF_VERSION"]}"} ]},
  { cols: [ {value: 'Drop'}, {value: "#{parameterHashmap["DROP"]}"} ]},
  { cols: [ {value: 'Product Set Version'}, {value: "#{parameterHashmap["Product_Set_Version"]}"} ]},
  { cols: [ {value: 'TAF Version'}, {value: "#{parameterHashmap["TAF_Version"]}"} ]},
  { cols: [ {value: 'ENM ISO Version'}, {value: "#{parameterHashmap["ENM_ISO_Version"]}"} ]},
  { cols: [ {value: 'Cluster ID'}, {value: "#{parameterHashmap["clusterId"]}"} ]},
  { cols: [ {value: 'Longloop Trends'}, {value: "#{parameterHashmap["Longloop Trends"]}"} ]}
]

	send_event('mt-ll-information-table', { hrows: tableHeader, rows: tableData } )
		
    uri = URI.parse("#$globalMTLongloopURL/#{urlVersion}/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}

	#Create a list of features (test suites) that are monitored 
	testSuitesToMonitor=createDefaultLongLoopTestSuitesToMonitor()	
	
	# Split this string on a space.
	fullResponseArray = fullResponse.split(",")
	
	# Check each value
	fullResponseArray.each do |value|
		#Look for a team names		
		if value.downcase() =~ /#{testSuitesToMonitor}/
			dataArray = value.split(' - ')
			#Need 3 elements 1. Team Name 2. Suite Name 3. Status
			if(dataArray.size()==3)
				key="#{dataArray[0].strip}$#{dataArray[1].strip}"
				value="#{dataArray[2].strip}"
				if($globalMTLongloopTeamStatus.has_key? "#{key}")
					$globalMTLongloopTeamStatus["#{key}"] = "#{value}"
				else 
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"
				end
			end
		else
			#print "\nThe '#{key}' key was found on the console output but was NOT specified/miss spelled in the configuration file!"
		end
	end
		
	#If the deployment is a valid maintrck deployment and the test phase is a valid deployment then proceed. 
	if(parameterHashmap["Test_Phase"] =~ /#{properties["LongLoopTestPhaseTag"]}/)
		sendEventsLongloop()
		sendStatusMail("#{$globalMTLongloopTag}",parameterHashmap,$globalMTLongloopTeamStatus)	
		updateConfluence(parameterHashmap,$globalMTLongloopTeamStatus,trendsPageID)			
	end

end

