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

$globalMTRFA250StagingTeamStatus = Hash.new()
$globalMTRFA250StagingTag = "RFA250Staging"



SCHEDULER.every '2m', :first_in => 0 do

	properties=load_properties()
	$globalMTRFA250StagingURL="#{properties["MTRFA250StagingURL"]}"
	
	lastProcessedBuildNumber=getLastProcessedMaintrackRFA250StagingBuildNumber()

	jenkins = Jenkins.new()
	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTRFA250StagingURL/lastCompletedBuild/api/json")

	#for i in 1440..1440
	#	puts "#$globalMTRFA250StagingURL/#{i}/api/json"l
	#	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTRFA250StagingURL/#{i}/api/json")
	#	processLastMTRFA250StagingRun(expectedBuildJsonResult,i)
	#	sleep(5)
	#end

	lastCompletedBuildNumber=expectedBuildJsonResult['number']
	#auditLastRFA250StagingRun()
	# Look at the lastCompletedBuild "number" if it is greater than the last one processed then obviously it's new :)
	if (lastCompletedBuildNumber>lastProcessedBuildNumber)
			system  "echo #{lastCompletedBuildNumber} > ./lastProcessedBuildNumberFile_#{$globalMTRFA250StagingTag}" 
			processLastMTRFA250StagingRun(expectedBuildJsonResult,lastCompletedBuildNumber)
	else
		#Nothing has change so just refresh dashing
		sendStagingAreaEvents()
	end
		
end


# Method   
def sendStagingAreaEvents ()
		log = Log.instance
		for key in $globalMTRFA250StagingTeamStatus.keys()
			data =key.split("$")
			items = []
			items << { label: "Test Suite:", value: data[0] }
			items << { label: "Status:", value: "#{$globalMTRFA250StagingTeamStatus[key]}" }
			send_event("#{key}_#{$globalMTRFA250StagingTag}", {status: getStatus("#{$globalMTRFA250StagingTeamStatus[key]}"), items: items})
			log.info("Maintrack RFA 250 Staging Status is: Team name->#{data[1]}, Test suite->#{data[0]}, Status-> #{$globalMTRFA250StagingTeamStatus[key]}")
		end
end  



#This is the top level view of RFA and RFA250 (Any one team failure is an overall failure)
def getLastProcessedMaintrackRFA250StagingBuildNumber ()
	#If the file doesn't exist then we are running for the first time hence we need to be careful
	lastProcessedBuildNumber=`cat ./lastProcessedBuildNumberFile_#{$globalMTRFA250StagingTag} 2> /dev/null`
	if lastProcessedBuildNumber ==""
	   lastProcessedBuildNumber=0
	else
	   lastProcessedBuildNumber=Integer(`cat ./lastProcessedBuildNumberFile_#{$globalMTRFA250StagingTag} 2> /dev/null`)
	end
	return lastProcessedBuildNumber
end

def processLastMTRFA250StagingRun (jsonResult,urlVersion)

	properties=load_properties()
	#Clear the contents of the global hash
	$globalMTRFA250StagingTeamStatus.clear
	$globalMTRFA250StagingTeamStatus=createDefaultRFA250TeamStatus()
		
	#Create a readable time/date from EPOCH
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution="#{Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')} (UTC)"
	
	#Create the URL for the build 
	currentbuildNumber=jsonResult['number']
	buildURL="<a href=\"#$globalMTRFA250StagingURL/#{currentbuildNumber}\">#{currentbuildNumber}</a>"
	
	
	enmRFA250StagingConfulenceTrendPage=properties["ENMRFA250StagingConfulenceTrendPage"]
	mtLlBuildTrendsPageURL="<a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=#{enmRFA250StagingConfulenceTrendPage}\">RFA 250 Staging Trends</a>"
	
	
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
	
	#Create the URL link for Allure
	if ("#{parameterHashmap["TE_ALLURE_LOG_URL"]}" == "")
		allureReportURL="No Report Available"
	else
		allureReportURL="<a href=\"#{parameterHashmap["TE_ALLURE_LOG_URL"]}\">Allure</a>"
	end	
	parameterHashmap["TE_ALLURE_LOG_URL"]=allureReportURL
	
	#URL trends page
	parameterHashmap["RFA 250 Staging Trends"]=mtLlBuildTrendsPageURL
	
	
	
	
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
  { cols: [ {value: 'RFA 250 Staging Trends'}, {value: "#{parameterHashmap["RFA 250 Staging Trends"]}"} ]}
]

	send_event('rfa-250-staging-information-table', { hrows: tableHeader, rows: tableData } )
		
    uri = URI.parse("#$globalMTRFA250StagingURL/#{urlVersion}/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)
	
	#print ("************************** Start Longloop Status********************* \n")

	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}
	
	#Create a list of features (test suites) that are monitored 
	testSuitesToMonitor=createDefaultRFA250TestSuitesToMonitor()
	
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
				if($globalMTRFA250StagingTeamStatus.has_key? "#{key}")
					$globalMTRFA250StagingTeamStatus["#{key}"] = "#{value}"
				else 
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"
				end
			end
		else
			#print "\nThe '#{key}' key was found on the console output but was NOT specified/miss spelled in the configuration file!"
		end
	end
	#If the deployment is a valid maintrck deployment and the test phase is a valid deployment then proceed. 
	if(parameterHashmap["Test_Phase"] =~ /#{properties["RFA250StagingTestPhaseTag"]}/)	
		sendStatusMail("#{$globalMTRFA250StagingTag}",parameterHashmap,$globalMTRFA250StagingTeamStatus)
		updateConfluence(parameterHashmap,$globalMTRFA250StagingTeamStatus,enmRFA250StagingConfulenceTrendPage)
		sendStagingAreaEvents()
	end

end

