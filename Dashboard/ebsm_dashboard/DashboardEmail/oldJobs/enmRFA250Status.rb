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

$globalMTRFA250TeamStatus = Hash.new()

$globalMTRFA250Tag = "RFA250"





SCHEDULER.every '3m', :first_in => 0 do

	properties=load_properties()
	$globalMTRFA250URL="#{properties["MTRFA250URL"]}"

	lastProcessedBuildNumber=getLastProcessedBuildNumber()

	jenkins = Jenkins.new()
	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTRFA250URL/lastCompletedBuild/api/json")
	lastCompletedBuildNumber=expectedBuildJsonResult['number']



	#for i in 1814..1820
	#	expectedBuildJsonResult = jenkins.retrieve_json("#$globalMTRFA250URL/#{i}/api/json")
	#	processLastRFARun(expectedBuildJsonResult,i)
	#	sleep(5)
	#end

	#auditLastRFA250Run()

	# Look at the lastCompletedBuild "number" if it is greater than the last one processed then obviously it's new :)
	#print "#{lastCompletedBuildNumber}>#{lastProcessedBuildNumber}"
	if (lastCompletedBuildNumber>lastProcessedBuildNumber)
			#print "\nProcessing!\n"
			system  "echo #{lastCompletedBuildNumber} > ./lastProcessedBuildNumberFile_#{$globalMTRFA250Tag}"
			processLastRFARun(expectedBuildJsonResult,lastCompletedBuildNumber)
	else
		#print "\nNothing has change so just refresh dashing!\n"
		sendEvents()
	end

	temp=parseJenkinsConsole("RFA250")
	temp2=mergeNewData(temp, "RFA250")
	temp3=createConfluencePage(temp2, "RFA250")
	#puts "#{temp[1][0]}"
	#puts "#{temp}"

	#setOverallRFA250Status()
end


def setOverallRFA250Status()
	if($globalMTRFA250TeamStatus.has_value?('FAILURE'))
			send_event("MT_RFA250", {status: getStatus("FAILURE"), :text => "Breakdown By Team", :link => "mt-rfa-250"})
		elsif($globalMTRFA250TeamStatus.has_value?('SUCCESS'))
			send_event("MT_RFA250", {status: getStatus("SUCCESS"), :text => "Breakdown By Team", :link => "mt-rfa-250"})
		else
			send_event("MT_RFA250", {status: "danger", :text => "Breakdown By Team", :link => "mt-rfa-250"})
	end
end

# Method
def sendEvents ()
		log = Log.instance
		for key in $globalMTRFA250TeamStatus.keys()
			data =key.split("$")
			items = []
			items << { label: "Test Suite:", value: data[0] }
			items << { label: "Status:", value: "#{$globalMTRFA250TeamStatus[key]}" }
			send_event("#{key}_#{$globalMTRFA250Tag}", {status: getStatus("#{$globalMTRFA250TeamStatus[key]}"), items: items})
			log.info("Maintrack RFA 250 Status is: Team name->#{data[1]}, Test suite->#{data[0]}, Status-> #{$globalMTRFA250TeamStatus[key]}")

		end
end


def getLastProcessedBuildNumber ()
	#If the file doesn't exist then we are running for the first time hence we need to be careful
	lastProcessedBuildNumber=`cat ./lastProcessedBuildNumberFile_#{$globalMTRFA250Tag} 2> /dev/null`
	if lastProcessedBuildNumber ==""
	   lastProcessedBuildNumber=0
	else
	   lastProcessedBuildNumber=Integer(`cat ./lastProcessedBuildNumberFile_#{$globalMTRFA250Tag} 2> /dev/null`)
	end
	return lastProcessedBuildNumber
end


def processLastRFARun (jsonResult,urlVersion)

	properties=load_properties()

	#Clear the contents of the global hash
	$globalMTRFA250TeamStatus.clear
	$globalMTRFA250TeamStatus=createDefaultRFA250TeamStatus()

	#Create a readable time/date from EPOCH
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution="#{Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')} (UTC)"

	#Create the URL for the build
	currentbuildNumber=jsonResult['number']
	buildURL="<a href=\"#$globalMTRFA250URL/#{currentbuildNumber}\">#{currentbuildNumber}</a>"

	enmRFA250ConfulenceTrendPage=properties["ENMRFA250ConfulenceTrendPage"]
	mtRFA250BuildTrendsPageURL="<a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=#{enmRFA250ConfulenceTrendPage}\">RFA 250 Trends</a>"

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
	parameterHashmap["TE_ALLURE_LOG_URL"]="#{allureReportURL}"

	#URL for the LL trends
	parameterHashmap["RFA 250 Trends"]=mtRFA250BuildTrendsPageURL

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
	  { cols: [ {value: 'RFA 250 Trends'}, {value: "#{parameterHashmap["RFA 250 Trends"]}"} ]}
	]

	send_event('rfa250-information-table', { hrows: tableHeader, rows: tableData } )

	uri = URI.parse("#$globalMTRFA250URL/#{urlVersion}/consoleText/")
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Get.new(uri.request_uri)
	response = http.request(request)

	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}

	#Create a list of features (test suites) that are monitored
	testSuitesToMonitor=createDefaultRFA250TestSuitesToMonitor()

	# Split this string on a space.
	fullResponseArray = fullResponse.split(",")
	print "\n"
	# Check each value
	fullResponseArray.each do |value|
		#Look for a team names
		if value.downcase() =~ /#{testSuitesToMonitor}/
			dataArray = value.split(' - ')
			#Need 3 elements 1. Team Name 2. Suite Name 3. Status
			if(dataArray.size()==3)
				key="#{dataArray[0].strip}$#{dataArray[1].strip}"
				value="#{dataArray[2].strip}"
				if($globalMTRFA250TeamStatus.has_key? "#{key}")
					$globalMTRFA250TeamStatus["#{key}"] = "#{value}"
					#print "#{key}=#{value}\n"
				else
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"
				end
			end
		else
			#print "\nThe '#{key}' key was found on the console output but was NOT specified/miss spelled in the configuration file!"
		end
	end


	#If the deployment is a valid maintrck deployment and the test phase is a valid deployment then proceed.
	if(parameterHashmap["Test_Phase"] =~ /#{properties["RFA250TestPhaseTag"]}/)
		#print "\nIs a valid MT deployment!\n"
		sendEvents()
		sendStatusMail("#{$globalMTRFA250Tag}",parameterHashmap,$globalMTRFA250TeamStatus)
		updateConfluence(parameterHashmap,$globalMTRFA250TeamStatus,enmRFA250ConfulenceTrendPage)
	else
		#print "\n#{parameterHashmap["clusterId"]} is NOT a valid MT deployment!\n"
	end

end
