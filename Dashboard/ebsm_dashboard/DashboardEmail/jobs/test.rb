#!/usr/bin/env ruby
#Encoding: UTF-8
require 'rubygems'
require 'json'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'time'
require 'net/http'
require 'uri'
require 'csv'
require 'yaml'
# def loadProperties()
#     properties = YAML.load(File.open("configbase.yml", "r"))
#     return properties
# end
#
# properties=loadProperties()
# puts "Config File Found"
#
# properties['builds'].each do |build|
#     puts build[0]
# end
#

# def retrieve_json(full_url)
#     uri = URI.parse(full_url)
#     http = Net::HTTP.new(uri.host, uri.port)
#     http.use_ssl = true
#     request = Net::HTTP::Get.new(uri.request_uri)
#     response = http.request(request)
#
#   	if ("#{response.code}" != "404")
#   		return JSON.parse(response.body)
#   end
#
# end
#
# def createParameterHashmap (jsonParmeter)
# 	paramsHashmap = Hash.new
# 	jsonParmeter.each do |key|
#
# 	  paramsHashmap["#{key["name"]}"] = "#{key["value"]}"
#
# 	end
# 		paramsHashmap.delete("TE_JCAT_LOG_URLS")
# 		paramsHashmap.delete("TE_ACTUAL_SCHEDULE")
# 		paramsHashmap.delete("TE_TESTWARE")
# 		paramsHashmap.delete("SUT_RESOURCE")
# 		paramsHashmap.delete("ISO_DIFF")
# 		paramsHashmap.delete("TE_SCHEDULE_PATH_IN_ARTIFACT")
# 		paramsHashmap.delete("TE_ARM")
# 		paramsHashmap.delete("TE_SLAVE_HOSTS")
# 		paramsHashmap.delete("CI_TE_HOST_PROPERTY_FILE")
# 		paramsHashmap.dlelete("TE_TUNNELLING_ON")
# 		paramsHashmap.delete("TE_TESTWARE_PROPERTY_FILE")
# 		paramsHashmap.delete("TE_ADDITIONAL_TEST_PROPERTIES")
# 		paramsHashmap.delete("MINIMUM_TOR_OPERATORS_VERSION")
# 		paramsHashmap.delete("TE_CIFWK_HOST")
# 		paramsHashmap.delete("TE_HOSTNAME")
# 		paramsHashmap.delete("TE_PORT")
# 		paramsHashmap.delete("TE_CI_PACKAGES")
# 		paramsHashmap.delete("ISO_DETAILS")
# 		paramsHashmap.delete("TEST_ISO_DETAILS")
# 		paramsHashmap.delete("COMBINED_TEST_PROPERTIES")
# 		paramsHashmap.delete("TE_SCHEDULE_ARTIFACT")
# 		paramsHashmap.delete("TE_EXECUTION_ID")
# 		paramsHashmap.delete("TE_MISC_PROPERTIES")
# 	return paramsHashmap
# end
# # thing = YAML.load_file('config.yml')
# # puts thing['builds']['RFA250'].to_yaml.gsub("\n-", "\n\n-").gsub("---", "")
# #
# # newConfig=Hash.new()
# # newConfig['build']=nil
# # newConfig['email']=nil
# # newConfig['general']['buildsToMonitor']=nil
# # newConfig['general']['userName']=nil
# # newConfig['general']['userPass']=nil
# #
# # File.open('data.yml','w+') do |h|
# #    h.write newConfig.to_yaml
# # end
# jsonResult = retrieve_json("https://fem114-eiffel004.lmera.ericsson.se:8443/jenkins/job/MT_RFA250/3709/api/json")
# parameterHashmap = Hash.new
# 	actionsArray=jsonResult["actions"]
# 	actionsArray.each do |actionsKey|
# 		for key in actionsKey.keys()
# 			if("#{key}"=="parameters")
# 				parameterHashmap = createParameterHashmap(actionsKey[key])
# 			end
# 		end
# 	end
#
#   puts parameterHashmap['Test_Phase']
