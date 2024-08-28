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
require 'rss/utils'
require 'uri'
require 'csv'
require 'cgi'
require "erb"


def createTableHeader(curTable, buildJSON)

    dateTimeStamp="#{Time.at(buildJSON['timestamp']/1000).strftime('%d-%m-%Y %H:%M:%S')} (UTC)"
    versionISO="#{buildJSON['enm_iso_version']}"
    clusterID="#{buildJSON['TE_SUT_CLUSTER_ID'.downcase]}"
    if "#{buildJSON['TE_ALLURE_LOG_URL'.downcase]}" == ""
        allureReportURL="No Report Available"
    else
        allureReportURL="<a href=\"#{buildJSON["TE_ALLURE_LOG_URL".downcase]}\">Allure</a>"
    end


    if curTable==nil
        tableHead=["RA", "Suite Name", "Team Name"]
        tableHead.push("<p>#{versionISO}</p><p>#{clusterID}</p><p>#{dateTimeStamp}</p><p>#{allureReportURL}</p>")
        return tableHead
    else
        curTable[0].insert(3, "<p>#{versionISO}</p><p>#{clusterID}</p><p>#{dateTimeStamp}</p><p>#{allureReportURL}</p>")

        return curTable
    end
end

def formatConfluencePage(columnData)
    colorColumn=""
    if columnData == "FAILURE"
        colorColumn.to_s.concat("<td bgcolor=\"#d95250\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</td>")
        return colorColumn
    end
    if columnData == "SUCCESS"
        colorColumn.to_s.concat("<td bgcolor=\"#5cb85c\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</td>")
        return colorColumn
    end
    if columnData == "Not Executed"
        colorColumn.to_s.concat("<td bgcolor=\"#f0ad4f\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</td>")
        return colorColumn
    end
    if columnData == "ABORTED"
        colorColumn.to_s.concat("<td bgcolor=\"#b3b300\">")
        colorColumn.to_s.concat(columnData.to_s)
        colorColumn.to_s.concat("</td>")
        return colorColumn
    end

    colorColumn.to_s.concat("<td>")
    colorColumn.to_s.concat(columnData.to_s)
    colorColumn.to_s.concat("</td>")
    return colorColumn

end


def createConfluencePage(confluenceData, runType)

    properties=loadProperties()

    user=properties['general']['userName']
    pass=properties['general']['userPass']

    htmlTable="<table><tbody>"
    confluenceData.each_with_index do |row, i|
        rowWithRA = raAdd(row)
        p rowWithRA
        htmlTable.to_s.concat("<tr>")
        if i!=0
            rowWithRA.each do |column|
                htmlTable.concat(formatConfluencePage(column))
            end
        else
            rowWithRA.each do |column|
                htmlTable.to_s.concat("<th>")
                htmlTable.to_s.concat(column.to_s)
                htmlTable.to_s.concat("</th>")
            end
        end
        htmlTable.to_s.concat("</tr>")
    end

    htmlTable.to_s.concat("</tbody></table>")


    jsonResult=loadConfluencePage(runType)
    confluencePageURI=jsonResult['_links']['self']

    jsonResult['body']['storage']['value']=htmlTable
    jsonResult['version']['number']+=1
    File.open("jsonOutput", "w") do |f|
        f.write(JSON.generate(jsonResult))
    end
    system("curl -u '#{user}:#{pass}' -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d @jsonOutput  #{confluencePageURI} ")

    return htmlTable
end

def cullData(data)
    properties=loadProperties

    notExecutedCounter=0
    indexCounters=Array.new()

    data.each_with_index do |row, i|
        #p row
        notExecutedCounter=0
        while(row.length > (properties['general']['buildsToMonitor']+3))
            row.pop
        end
        row.each_with_index do |column, index|
            if column=="Not Executed"
                notExecutedCounter+=1
            end
        end
        if notExecutedCounter==(properties['general']['buildsToMonitor'])
            indexCounters.push(i)
            notExecutedCounter=0
        end

    end

    indexCounters.each do |index|
        data.delete_at(index)
    end

end

def mergeNewData(newData, runType, buildJSON)

    currentData=parseConfluencePage(runType, buildJSON)
    currentData.drop(1).each do |default|
        default.insert(3, "Not Executed")
    end

    newData.each do |data|
        data.insert(0, "N/A")
        isJenkinsDataUsed=0
        if data.size==4
            currentData.each_with_index do |value, i|
                if i!=0
                    if (data[1] == value[1] and data[2] == value[2])
                        currentData[i].delete_at(3)
                        currentData[i].insert(3, data[3])
                        isJenkinsDataUsed=1
                        break
                    end
                end
            end
            if isJenkinsDataUsed==0
                currentData.push(data)
            end
        end

    end

    return currentData

end

def loadConfluencePage(runType)

    properties=loadProperties()
    user=properties['general']['userName']
    pass=properties['general']['userPass']
    confluenceID=properties['builds'][runType]['buildConfluenceID']

    uri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{confluenceID}?expand=body.storage,version")

    Net::HTTP.start(uri.host, uri.port,
        :use_ssl => uri.scheme == 'https',
    :verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|

        request = Net::HTTP::Get.new uri.request_uri
        request.basic_auth "#{user}", "#{pass}"

        response = http.request(request)
        jsonResult=JSON.parse(response.body)
        return jsonResult
    end
end

def parseConfluencePage(runType, buildJSON)

    jsonResult=loadConfluencePage(runType)
    jsonTable=jsonResult['body']['storage']['value']

    if(jsonTable=="")
        puts "Load Confluence: Table does not exist!"
        createTableHeader(nil, buildJSON)
        newTable=Array.new()
        newTable.push(createTableHeader(nil, buildJSON))
        return newTable
    end

    html=Nokogiri::HTML(jsonTable)

    tableRows=html.search('table')
    header=tableRows.search('tr').map do |rows, i|
        rows.css('th').map(&:inner_html)
    end

    content=tableRows.search('tr').map do |rows, i|
        rows.css('td').map(&:inner_html)
    end

    content.delete_at(0)

    fullTable=content.insert(0, header[0])

    puts "Confluence Load: Success!"

    return createTableHeader(fullTable, buildJSON)
end

def load_confluence_file(runType)

    teamSuites=""
    File.open("globalTeamsSuites") do |file|
        teamSuites = JSON.parse(file.read)['#{runType}']
    end
    return teamSuites

end

def save_confluence_file(confluenceArray, runType)
    confluence= Hash.new
    confluence.merge!("#{runType}": confluenceArray)
    File.open("globalTeamsSuites", "w") do |f|
        f.write(confluence.to_json)
    end

end
