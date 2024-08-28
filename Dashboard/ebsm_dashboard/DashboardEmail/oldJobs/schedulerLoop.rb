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

SCHEDULER.every '3m', :first_in => 0 do

	properties=load_properties()
	buildTypes="#{properties["builds"]}".split("|")

	lastProcessedBuildNumbers="#{properties["buildNumbers"]}".split("|")

	# temp=parseJenkinsConsole("RFA250")
	# temp2=mergeNewData(temp, "RFA250")
	# temp3=createConfluencePage(temp2, "RFA250")
	#puts "#{temp[1][0]}"
	#puts "#{temp}"

  buildTypes.each_with_index do |build, i|
    if(newBuildNumber(build) > lastProcessedBuildNumbers[i])
      createConfluencePage(mergeNewData(parseJenkinsConsole(build), build), build)
    else
      puts "No new build for #{build}"
    end
  end

end
