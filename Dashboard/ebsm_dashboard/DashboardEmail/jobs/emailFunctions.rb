# !/usr/bin/env rubyl
# Encoding: UTF-8
require 'rubygems'
require "selenium-webdriver"
require 'json'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'time'
require 'net/http'
require 'net/smtp'
require 'uri'
require 'csv'

def emailCreation(runType, data, jenkinsBuildJson)
  if (File.size?('email.yml')!=nil)
    emailProperties=loadEmailProperties()
  else
    emailProperties=defaultEmailFile()
  end
  header = data[0]
  p data
  data.drop(1).each_with_index do |row, i|
      teams=row[2].split("_")
      teams.each do |team|
      emailProperties=populateEmailConfig(emailProperties, row[1], team, runType)
      if emailProperties['teams'][team][runType][row[1]]['active']==true
        p "hello"
		if row[3].to_s=='FAILURE'
			teamEmail(header, row, emailProperties['teams'][team], runType)
		end
      end
    end
  end
  saveEmailProperties(emailProperties)
  finishEmail()
end

def populateEmailConfig(emailProperties, suiteName, team, runType)
  if emailProperties['teams'].has_key?(team.to_s)
    if emailProperties['teams'][team].has_key?(runType)
      if !emailProperties['teams'][team][runType].has_key?(suiteName)
          emailProperties['teams'][team][runType][suiteName]=Hash.new()
          emailProperties['teams'][team][runType][suiteName]['active']=false
      end
    else
      emailProperties['teams'][team][runType]=Hash.new()
      emailProperties['teams'][team][runType]['buildsToEmail']=3
      emailProperties['teams'][team][runType][suiteName]=Hash.new()
      emailProperties['teams'][team][runType][suiteName]['active']=false
    end
  else
    emailProperties['teams'][team]=Hash.new()
    emailProperties['teams'][team]['email']=Array.new()
    emailProperties['teams'][team][runType]=Hash.new()
    emailProperties['teams'][team][runType]['buildsToEmail']=3
    emailProperties['teams'][team][runType][suiteName]=Hash.new()
    emailProperties['teams'][team][runType][suiteName]['active']=false
  end
  return emailProperties
end

def teamEmail(header, rowData, rowProperties, runType)

  data = rowData.slice(0, (rowProperties[runType]['buildsToEmail']+3))
  newHeader=header.slice(0, (rowProperties[runType]['buildsToEmail']+3))
  if (!File.file?("./emails/#{data[2].gsub(/\s+/, "")}.sendMail"))
    File.open("./emails/#{data[2].gsub(/\s+/, "")}.sendMail",'w') do |h|
      h << "From: No-Reply@maintrack.status\n"
      h << "To: "
      rowProperties['email'].each do |email|
        h << "#{email}"
        if !(email == rowProperties['email'].last)
	  h << ", "
	end
      end
      h << "\n"
      h << "MIME-Version: 1.0\n"
      h << "Content-type: text/html\n"
      h << "Subject: #{runType.to_s} Status Email\n\n"

    end

    File.open("./emails/#{data[2].gsub(/\s+/, "")}.sendMail",'a') do |h|
      h << "<table style=\"vertical-align: center;\" border=\"1\" cellspacing=\"1\" cellpadding=\"1\" width=\"400\"\>"
      h << "<tr>"
      newHeader.each do |column|
        h << "<th bgcolor=\"#cccccc\">#{column}</th>"
      end
      h << "</tr>"
    end

  end

  File.open("./emails/#{data[2].gsub(/\s+/, "")}.sendMail",'a') do |h|
    h << "<tr>"
    data.each do |column|
      h << formatConfluencePage(column)
    end
    h << "</tr>"
  end
end

def finishEmail()
  i=0
  Dir.glob('./emails/**.sendMail') do |rb_file|
    p i
    i=i+1
    File.open("#{rb_file}",'a') do |h|
      h << "</table>"
    end
	system("cat #{rb_file} | /usr/sbin/sendmail -t")
  system("rm #{rb_file}")
  end
end
