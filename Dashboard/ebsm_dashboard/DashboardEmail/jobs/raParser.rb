require 'rubygems'
require 'json'
require "selenium-webdriver"
require 'json'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'time'
require 'net/http'
require 'uri'
require 'csv'

def raParse
  arrayHash = JSON.parse(File.read("teams.json"))
  baseRAHash = Hash.new()
  arrayHash.each do |team|
    baseRAHash["#{team['name'].downcase}"] = team['programArea']
  end
  File.open("teamRA.json", "w") do |f|
    f.write(baseRAHash.to_json)
  end
end

def raAdd(rowData)
  hash = JSON.parse(File.read("teamRA.json"))
  if hash.has_key?(rowData[2].downcase)
    if hash[rowData[2].downcase]=="Assurance & Optimisation"
      puts "A&O"
      rowData[0]=CGI::escapeHTML("A&O")
    end
    if hash[rowData[2].downcase]=="Network Evolution & OSS Management"
      rowData[0]=CGI::escapeHTML("NE&O")
      puts "NE&O"
    end
    if hash[rowData[2].downcase]=="Security"
      rowData[0]=CGI::escapeHTML("Security")
      puts "SECURITY"
    end
    if hash[rowData[2].downcase]=="Transport"
      rowData[0]=CGI::escapeHTML("Transport")
      puts "TRANSPORT"
    end
    if hash[rowData[2].downcase]=="Planning & Configuration"
      rowData[0]=CGI::escapeHTML("P&C")
      puts "P&C"
    end
  end
  #p "HELLO", rowData
  #p rowData
  return rowData
end
