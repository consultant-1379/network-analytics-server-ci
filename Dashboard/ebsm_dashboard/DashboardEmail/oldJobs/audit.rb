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



$globalMTLongloopTeamStatus = Hash.new()
$globalMTRFA250TeamStatus = Hash.new()
$globalMTRFA250StagingTeamStatus = Hash.new()

=begin
SCHEDULER.every '3m', :first_in => 0 do
#SCHEDULER.every '1m', :first_in => 0 do

	properties=load_properties()
	$globalMTLongloopURL="#{properties["MTLongloopURL"]}"
	$globalMTRFA250URL="#{properties["MTRFA250URL"]}"
	$globalMTRFA250StagingURL="#{properties["MTRFA250StagingURL"]}"

	puts "hello"
	auditLastMTLLRun()
	auditLastRFA250Run()
	auditLastRFA250StagingRun()

end
=end




def auditLastRFA250StagingRun ()

	properties=load_properties()

	#Clear the contents of the global hash
	$globalMTRFA250StagingTeamStatus.clear
	$globalMTRFA250StagingTeamStatus=createDefaultRFA250TeamStatus()


    uri = URI.parse("#$globalMTRFA250StagingURL/lastCompletedBuild/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

	#################################
	jenkins = Jenkins.new()
	jsonResult = jenkins.retrieve_json("#$globalMTRFA250StagingURL/lastCompletedBuild/api/json")
	#formattedForDisplayDateOfExecution
	#################################
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution=Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')
	print "\nCorrect Date:#{formattedForDisplayDateOfExecution}\n"



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



	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}

	#Create a list of features (test suites) that are monitored
	#testSuitesToMonitor=createDefaultLongLoopTestSuitesToMonitor()
	testSuitesToMonitor=createDefaultRFA250TestSuitesToMonitor()

	# Split this string on a space.
	fullResponseArray = fullResponse.split(",")

	missingFromPropertiesFile = Array.new

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
				missingFromPropertiesFile.push(key)
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"

				end
			end
		else
		end
	end

	puts "#{parameterHashmap["Test_Phase"]}<=>#{properties["RFA250TestPhaseTag"]}"
	if(parameterHashmap["Test_Phase"] =~ /#{properties["RFA250TestPhaseTag"]}/)
		#print "\n\nIn here!#{missingFromPropertiesFile.length}\n"

		puts "--------------------RFA250 Staging--------------------"
		puts "#$globalMTRFA250StagingURL/lastCompletedBuild/consoleText/"
		puts "--------------------Found on the command line therefore missing from the properties file! (Add them)--------------------"
		missingFromPropertiesFile.each { |x| puts x }

		puts "--------------------Nothing found on the command line for the following. Either didn't execute or not running (remove them from the properties file)--------------------"
		$globalMTRFA250StagingTeamStatus.each do |key, value|
			if("#{value}".eql?"Not Executed!")
				puts "#{key} -> #{value}"
			end
		end

	end


end


def auditLastRFA250Run ()

	properties=load_properties()

	#Clear the contents of the global hash
	$globalMTRFA250TeamStatus.clear
	$globalMTRFA250TeamStatus=createDefaultRFA250TeamStatus()


    uri = URI.parse("#$globalMTRFA250URL/lastCompletedBuild/consoleText/")
	#uri = URI.parse("https://fem114-eiffel004.lmera.ericsson.se:8443/jenkins/job/MT_RFA250/2379/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

	#################################
	jenkins = Jenkins.new()
	jsonResult = jenkins.retrieve_json("#$globalMTRFA250URL/lastCompletedBuild/api/json")
	#jsonResult = jenkins.retrieve_json("https://fem114-eiffel004.lmera.ericsson.se:8443/jenkins/job/MT_RFA250/2379/api/json")
	#formattedForDisplayDateOfExecution
	#################################
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution=Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')
	print "\nCorrect Date:#{formattedForDisplayDateOfExecution}\n"



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



	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"




	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}

	#Create a list of features (test suites) that are monitored
	#testSuitesToMonitor=createDefaultLongLoopTestSuitesToMonitor()
	testSuitesToMonitor=createDefaultRFA250TeamStatus()

	# Split this string on a space.
	fullResponseArray = fullResponse.split(",")


		#puts "\n\n\n\n#{fullResponseArray}\n\n\n\n"

	missingFromPropertiesFile = Array.new

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
				else
				missingFromPropertiesFile.push(key)
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"

				end
			end
		else
		end
	end

	puts "#{parameterHashmap["Test_Phase"]}<=>#{properties["RFA250TestPhaseTag"]}"
	if(parameterHashmap["Test_Phase"] =~ /#{properties["RFA250TestPhaseTag"]}/)
		#print "\n\nIn here!#{missingFromPropertiesFile.length}\n"

		puts "--------------------RFA250--------------------"
		puts "--------------------Found on the command line therefore missing from the properties file! (Add them)--------------------"
		missingFromPropertiesFile.each { |x| puts x }

		puts "--------------------Nothing found on the command line for the following. Either didn't execute or not running (remove them from the properties file)--------------------"
		$globalMTRFA250TeamStatus.each do |key, value|
			if("#{value}".eql?"Not Executed!")
				puts "#{key} -> #{value}"
			end
		end

	end


end


def auditLastMTLLRun ()

	properties=load_properties()

	#Clear the contents of the global hash
	$globalMTLongloopTeamStatus.clear
	$globalMTLongloopTeamStatus=createDefaultLongLoopTeamStatus()


	print "\n#$globalMTLongloopURL/lastCompletedBuild/consoleText/\n"
    uri = URI.parse("#$globalMTLongloopURL/lastCompletedBuild/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

	#################################
	jenkins = Jenkins.new()
	jsonResult = jenkins.retrieve_json("#$globalMTLongloopURL/lastCompletedBuild/api/json")
	#formattedForDisplayDateOfExecution
	#################################
	epochDateTimeStamp=jsonResult["timestamp"]
	formattedForDisplayDateOfExecution=Time.at(epochDateTimeStamp / 1000).strftime('%d-%m-%Y %H:%M:%S')
	print "\nCorrect Date:#{formattedForDisplayDateOfExecution}\n"



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



	fullResponse="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| fullResponse.gsub!(replacement[0], replacement[1])}

	#Create a list of features (test suites) that are monitored
	testSuitesToMonitor=createDefaultLongLoopTestSuitesToMonitor()

	# Split this string on a space.
	fullResponseArray = fullResponse.split(",")

	missingFromPropertiesFile = Array.new

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
				missingFromPropertiesFile.push(key)
					#print "\nFound a key similar with the name '#{key}' but NOT specified/miss spelled in the configuration file!"

				end
			end
		else
		end
	end

	#If the deployment is a valid maintrck deployment and the test phase is a valid deployment then proceed.
	if(parameterHashmap["Test_Phase"] =~ /#{properties["LongLoopTestPhaseTag"]}/)
		#print "\n\nIn here!#{missingFromPropertiesFile.length}\n"

		puts "--------------------Longloop--------------------"
		puts "--------------------Found on the command line therefore missing from the properties file! (Add them)--------------------"
		missingFromPropertiesFile.each { |x| puts x }

		puts "--------------------Nothing found on the command line for the following. Either didn't execute or not running (remove them from the properties file)--------------------"
		$globalMTLongloopTeamStatus.each do |key, value|
			if("#{value}".eql?"Not Executed!")
				puts "#{key} -> #{value}"
			end
		end

	end


end
