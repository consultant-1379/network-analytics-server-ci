#!/usr/bin/env ruby
#Encoding: UTF-8
require 'rubygems'


def createDefaultRFA250TeamStatus()
	properties=load_properties()
	tmpHashmap = Hash.new
	teamStatusDefaultKeys = properties['MonitoringSuiteTeamsRFA250'].split("|")	
	teamStatusDefaultKeys.each do |teamStatusKeys|
	#print "\nTeam:#{teamStatusKeys}"
	tmpHashmap["#{teamStatusKeys}"] = "Not Executed!"
	end	
	tmpHashmap.sort
	return  tmpHashmap
end

def createDefaultRFA250TestSuitesToMonitor()
	properties=load_properties()
	monitoring="#{properties['MonitoringSuiteTeamsRFA250']}"	
	monitoring = monitoring.gsub!(/\$[^|]*/, "") 
	return monitoring.downcase
end



def createDefaultLongLoopTeamStatus()
	properties=load_properties()
	tmpHashmap = Hash.new
	teamStatusDefaultKeys = properties['MonitoringSuiteTeamsLongLoop'].split("|")	
	teamStatusDefaultKeys.each do |teamStatusKeys|
	tmpHashmap["#{teamStatusKeys}"] = "Not Executed!"
	end	
	tmpHashmap.sort
	return  tmpHashmap
end

def createDefaultLongLoopTestSuitesToMonitor()
	properties=load_properties()
	monitoring="#{properties['MonitoringSuiteTeamsLongLoop']}"	
	monitoring = monitoring.gsub!(/\$[^|]*/, "") 
	return monitoring.downcase
end

# Method   
def createParameterHashmap (jsonParmeter)
	paramsHashmap = Hash.new
	jsonParmeter.each do |key|

	  paramsHashmap["#{key["name"]}"] = "#{key["value"]}"

	end
		paramsHashmap.delete("TE_JCAT_LOG_URLS")
		paramsHashmap.delete("TE_ACTUAL_SCHEDULE")
		paramsHashmap.delete("TE_TESTWARE")
		paramsHashmap.delete("SUT_RESOURCE")
		paramsHashmap.delete("ISO_DIFF")
		paramsHashmap.delete("TE_SCHEDULE_PATH_IN_ARTIFACT")
		paramsHashmap.delete("TE_ARM")
		paramsHashmap.delete("TE_SLAVE_HOSTS")
		paramsHashmap.delete("CI_TE_HOST_PROPERTY_FILE")
		paramsHashmap.delete("TE_TUNNELLING_ON")
		paramsHashmap.delete("TE_TESTWARE_PROPERTY_FILE")
		paramsHashmap.delete("TE_ADDITIONAL_TEST_PROPERTIES")
		paramsHashmap.delete("MINIMUM_TOR_OPERATORS_VERSION")
		paramsHashmap.delete("TE_CIFWK_HOST")
		paramsHashmap.delete("TE_HOSTNAME")
		paramsHashmap.delete("TE_PORT")
		paramsHashmap.delete("TE_CI_PACKAGES")
		paramsHashmap.delete("ISO_DETAILS")
		paramsHashmap.delete("TEST_ISO_DETAILS")
		paramsHashmap.delete("COMBINED_TEST_PROPERTIES")
		paramsHashmap.delete("TE_SCHEDULE_ARTIFACT")
		paramsHashmap.delete("TE_EXECUTION_ID")
		paramsHashmap.delete("TE_MISC_PROPERTIES")
	return paramsHashmap
end 


# Method  
def getStatus (testResults)
	if testResults.downcase().strip() == "failure"
		return 'warning'
	elsif testResults.downcase().strip() == "success"	
		return 'ok'
	end
	return 'danger'
end


# Check that the build is finished and it has not already been processed i.e. check the build number
def isANewMaintrackBuild (json)
	currentbuildResult=json['result']
	#If there is an ongoing job then the 'result' is not set
	if ( !currentbuildResult )
		return false
	end
	return true
end

#Check to see if the cluster ID is in the list of the ones that are required to be monitored
def isAMTDeployment(processingClusterId)
	properties=load_properties()
	listOfValidDeployments="#{properties['ValidMTDeployments']}"
	if processingClusterId =~ /#{listOfValidDeployments}/
		return true
	end
	return false
end