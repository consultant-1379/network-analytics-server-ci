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

def loadProperties()
  File.open("global.properties", 'r') do |properties_file|
    properties_file.read.each_line do |line|
      line.strip!
      if (line[0] != ?# and line[0] != ?=)
        i = line.index('=')
        if (i)
          properties[line[0..i - 1].strip] = line[i + 1..-1].strip
        else
          properties[line] = ''
        end
      end
    end
  end
  return properties
end


def createConfluencePage(confluenceData, runType)

  properties=loadProperties()
	user="#{properties['userName']}"
	passwd="#{properties['userPass']}"

  htmlTable="<table><tbody>"
  #puts confluenceData[0]
  confluenceData.each do |data|
    htmlTable.concat("<tr>")
    data.each do |row|

      htmlTable.concat("<td>")
      htmlTable.concat("#{row}")
      htmlTable.concat("<\/td>")
    end
    htmlTable.concat("<\/tr>")
  end

  htmlTable.concat("<\/tbody><\/table>")

  jsonResult=loadConfluencePage(runType)
  confluencePageURI=jsonResult['_links']['self']

  jsonResult['body']['storage']['value']=htmlTable
  jsonResult['version']['number']+=1
  File.open("jsonOutput", "w") do |f|
    f.write(jsonResult.to_json)
  end

  system("curl -u '#{user}:#{passwd}' -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d @jsonOutput  #{confluencePageURI}")


end

def mergeNewData(newData, runType)
  puts "NO"
  currentData=parseConfluencePage()
  puts "NO!!"
  puts"NOICE"
  #p currentData
  isDataUsed=0
  #if currentData!=[]
    newData.each do |data|
      #p isDataUsed
      #puts "HELLO"
      if data.size==3
          currentData.each_with_index do |value, i|

          if data[0] == value[0] && data[1] == value[1]
              currentData[i].delete_at(2)
              currentData[i].insert(2, data[2])
              isDataUsed=1
          end

        end
        if (isDataUsed!=1)
          currentData.push(data)
          isDataUsed=0
        end
        #p "END: #{isDataUsed}"
      end

    end
  # else
  #   puts "NOT WORKING"
  #   currentData=newData
  #end
  #puts currentData
  #p currentData
  return currentData



end

def loadConfluencePage(runType)

  properties=loadProperties()
  user="#{properties['userName']}"
	passwd="#{properties['userPass']}"
  confluenceID=197034522

  uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confluenceID}?expand=body.storage,version")

	Net::HTTP.start(uri.host, uri.port,
	:use_ssl => uri.scheme == 'https',
	:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|

		request = Net::HTTP::Get.new uri.request_uri
		request.basic_auth "#{user}", "#{passwd}"

		response = http.request(request) # Net::HTTPResponse object

		jsonResult=JSON.parse(response.body)

    #puts jsonResult
    return jsonResult
  end
end

def parseConfluencePage()

    jsonResult=loadConfluencePage()

		jsonTable=jsonResult['body']['storage']['value']

    if(jsonTable=="")
			puts "Load Confluence: Table does not exist!"
      return Array.new
    end

		html=Nokogiri::HTML(jsonTable)

		htmlTable=html.css('table').first
		tableRows=htmlTable.css('tr')
		#column_names = tableRows.shift.css('th').map(&:text)

		text_all_rows = tableRows.map do |rows|
	     rows.css('td').map(&:text)
       #rows.insert
		end
		#p column_names
		#p text_all_rows
    text_all_rows.each.collect do |rows|
      rows.insert(2, "Not Executed!")
    end

		puts "Confluence Load: Success!"
		#return text_all_rows.insert(0, column_names)
    return text_all_rows
end

def load_confluence_file(runType)

	teamSuites=""
	File.open("globalTeamsSuites") do |file|
		teamSuites = JSON.parse(file.read)['#{runType}']
	end
	return teamSuites

end

def save_confluence_file(confluenceArray, runType)
	#puts "HELLO"
	#p confluenceArray
	#puts "#{confluenceArray}"
	confluence= Hash.new
	confluence.merge!("#{runType}": confluenceArray)
	#p confluence
	File.open("globalTeamsSuites", "w") do |f|
		f.write(confluence.to_json)
	end

end

def parseJenkinsConsole(runType)

  properties=loadProperties()
  #runURL = properties['#{runType}URL']
  runURL = "https://fem114-eiffel004.lmera.ericsson.se:8443/jenkins/job/MT_RFA250"

  #uri = URI.parse("#{runURL}/#{urlVersion}/consoleText/")
  uri = URI.parse("#{runURL}/3665/consoleText/")
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	request = Net::HTTP::Get.new(uri.request_uri)
	response = http.request(request)

	suiteTeamStatusText="#{response.body.scan(/^.*has finished.*$/)}"
	replacements = [ ["\"", ""] , ["[", ""], ["]", ""] , [" has finished", ""] , [/<[^>]*>/,""] , [/&\b.*?;/, ""] , [/Testware failing.*?>/,""] , [/, TEST_SCHEDULER.*/,""] ]
	replacements.each {|replacement| suiteTeamStatusText.gsub!(replacement[0], replacement[1])}
  #puts suiteTeamStatusText

  # suiteTeamArray = suiteTeamStatusText.split(", ")
  #
  # suiteTeamArray.each do |row|
  #   row.collect{|row| row.split(" - ")}
  # end

  suiteTeamArray = suiteTeamStatusText.split(", ").map do |pair|
    pair.split(" - ")
  end

  #suiteTeamArray.each do |

  # suiteTeamStatusArray = suiteTeamStatusText.map do |rows|
  #   rows.split(' - ')
  # end

  File.open("suiteTeamStatusSplit", "w") do |f|
		f.write(suiteTeamArray)
	end

  return suiteTeamArray

end

def parseJenkinsJson(runType)

  properties=loadProperties()
  #runURL = properties['#{runType}URL']
  runURL = "https://fem114-eiffel004.lmera.ericsson.se:8443/jenkins/job/MT_RFA250"

  #jenkins = Jenkins.new()
  #jsonNewBuild = jenkins.retrieve_json("#{runURL}/lastCompletedBuild/api/json")
end
