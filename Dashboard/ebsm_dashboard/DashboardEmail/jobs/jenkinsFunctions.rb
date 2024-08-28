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

def retrieve_json(full_url)
    uri = URI.parse(full_url)
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

    if ("#{response.code}" != "404")
        return JSON.parse(response.body)
    end

end

def parseJenkinsConsole(runType)

    properties=loadProperties()
    #runURL = properties['#{runType}URL']
    #puts properties
    runURL = properties['builds'][runType]['buildJenkinsURL']

    uri = URI.parse("#{runURL}/lastCompletedBuild/consoleText/")
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    request = Net::HTTP::Get.new(uri.request_uri)
    response = http.request(request)

    suiteTeamStatusText="#{response.body.scan(/^.*has finished.*$/)}"
    replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
    replacements.each {|replacement| suiteTeamStatusText.gsub!(replacement[0], replacement[1])}

    suiteTeamArray = suiteTeamStatusText.split(", ").map do |pair|
        pair.split(" - ")
    end

    File.open("suiteTeamStatusSplit", "w") do |f|
        f.write(suiteTeamArray)
    end

    return suiteTeamArray

end

def parseJenkinsJson(runType)

    properties=loadProperties()
    #puts properties['builds'][runType]['buildJenkinsURL']
    runURL = properties['builds'][runType]['buildJenkinsURL']

    jsonResult = retrieve_json("#{runURL}/lastCompletedBuild/api/json")

    paramsHashmap = Hash.new
    #p jsonResult['actions']
    jsonResult['actions'].each do |actionsKey|
        actionsKey.each do |key, value|
            if key == "parameters"
                value.each do |val|
                    paramsHashmap[val['name'].downcase()]=val['value']
                end
            end
        end
    end

    paramsHashmap.delete("TE_JCAT_LOG_URLS".downcase)
    paramsHashmap.delete("TE_ACTUAL_SCHEDULE".downcase)
    paramsHashmap.delete("TE_TESTWARE".downcase)
    paramsHashmap.delete("SUT_RESOURCE".downcase)
    paramsHashmap.delete("ISO_DIFF".downcase)
    paramsHashmap.delete("TE_SCHEDULE_PATH_IN_ARTIFACT".downcase)
    paramsHashmap.delete("TE_ARM".downcase)
    paramsHashmap.delete("TE_SLAVE_HOSTS".downcase)
    paramsHashmap.delete("CI_TE_HOST_PROPERTY_FILE".downcase)
    paramsHashmap.delete("TE_TUNNELLING_ON".downcase)
    paramsHashmap.delete("TE_TESTWARE_PROPERTY_FILE".downcase)
    paramsHashmap.delete("TE_ADDITIONAL_TEST_PROPERTIES".downcase)
    paramsHashmap.delete("MINIMUM_TOR_OPERATORS_VERSION".downcase)
    paramsHashmap.delete("TE_CIFWK_HOST".downcase)
    paramsHashmap.delete("TE_HOSTNAME".downcase)
    paramsHashmap.delete("TE_PORT".downcase)
    paramsHashmap.delete("TE_CI_PACKAGES".downcase)
    paramsHashmap.delete("ISO_DETAILS".downcase)
    paramsHashmap.delete("TEST_ISO_DETAILS".downcase)
    paramsHashmap.delete("COMBINED_TEST_PROPERTIES".downcase)
    paramsHashmap.delete("TE_SCHEDULE_ARTIFACT".downcase)
    paramsHashmap.delete("TE_EXECUTION_ID".downcase)
    paramsHashmap.delete("TE_MISC_PROPERTIES".downcase)


    #paramsHashmap.merge!(jsonResult['id'])
    paramsHashmap['BUILD_NUMBER']=jsonResult.delete('id')
    paramsHashmap['timestamp']=jsonResult.delete('timestamp')
    #puts paramsHashmap
    return paramsHashmap

end
