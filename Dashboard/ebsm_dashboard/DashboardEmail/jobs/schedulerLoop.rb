#!/usr/bin/env ruby
#Encoding: UTF-8
require 'rubygems'
require 'json'
require 'open-uri'
require 'date'
require 'time'

SCHEDULER.every '1m', :first_in => 0 do
    if (File.size?(File.open('config.yml', "r"))!=nil)
        properties=loadProperties()
        puts "Config File Found"
        properties['builds'].each do |build|
            jenkinsBuildJson=parseJenkinsJson(build[0])
            if jenkinsBuildJson['BUILD_NUMBER'].to_i > build[1]['buildLastProcessedBuildNumber'].to_i
                if build[1]['buildPhaseTags'].include?("#{jenkinsBuildJson['test_phase']}")
                    jenkinsData = parseJenkinsConsole(build[0])
                    confluenceData = mergeNewData(jenkinsData, build[0], jenkinsBuildJson)
                    cullData(confluenceData)
                    emailCreation(build[0], confluenceData, jenkinsBuildJson)
                    createConfluencePage(confluenceData, build[0])
                    build[1]['buildLastProcessedBuildNumber'] = jenkinsBuildJson['BUILD_NUMBER']
                    saveProperties(properties)
                    dashboardCreator(build, jenkinsBuildJson, confluenceData)
                end


            end
        end


    else
        puts "No Config File!"
        puts "Creating default config file!"
        defaultConfigFile()
    end

end
