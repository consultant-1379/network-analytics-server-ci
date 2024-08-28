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

def dashboardCreator(buildData, jenkinsBuildJson, confluenceData)

    reqArea=Hash.new() {|h,k| h[k]=[]}

    confluenceData.drop(1).each do |row|
        row.each_with_index do |column, i|
            if (i==0 && column!="N/A")
                ra = ("#{CGI::unescapeHTML(column)}")
                reqArea["#{ra}"].push(row)
                next
            end
        end
    end
    reqArea.each_pair do |key, value|
        #p key
        File.open("./dashboards/#{CGI::unescapeHTML(key).gsub(/[^0-9A-Za-z]/, '').downcase}-mt-#{buildData[1]['buildName'].to_s.downcase.split.join('')}.erb", "w") do |f|
            f.write(htmlCreation(buildData, value))
            eventSender(value)
        end
    end
end

def htmlCreation(buildData, dashboardData)

    dashboardSize=dashboardData.size
    htmlPage=String.new()
    htmlPage.concat("<!DOCTYPE html>
    <html lang=\"en\">
    <head>
      <meta charset=\"utf-8\"/>
      <meta name=\"description\" content=\"\">
      <meta name=\"viewport\" content=\"width=device-width\">
      <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\">

      <title><%= yield_content(:title) %></title>

      <!-- The javascript and css are managed by sprockets. The files can be found in the /assets folder-->
      <script type=\"text/javascript\" src=\"/assets/application.js\"></script>
      <link rel=\"stylesheet\" href=\"/assets/application.css\">

      <link href='//fonts.googleapis.com/css?family=Open+Sans:300,400,600,700' rel='stylesheet' type='text/css'>
      <link rel=\"icon\" href=\"/assets/favicon.ico\"></head>")
    htmlPage.concat("<script type='text/javascript'>
      $(function() {
        var width =  ($( window ).width() / 5);
        var height = ($( window ).height() / #{(((dashboardSize/5)+1).ceil)});
        Dashing.widget_base_dimensions = [width,height]

      });
    </script>")
    htmlPage.concat("<div><h1 style=\"font-size:60px\">#{CGI::unescapeHTML(dashboardData[0][0])} Maintrack #{buildData[1]['buildName']} Dashboard</h1></div>")
    htmlPage.concat("<div class=\"gridster\">")
    htmlPage.concat("<ul>")

    dashboardData.each do |row|
        #puts "hello"
        #p row[1]
        htmlPage.concat("<li data-switcher-interval=\"10000\" data-row=\"1\" data-col=\"1\" data-sizex=\"1\" data-sizey=\"1\">")
        htmlPage.concat("<div data-id=\"#{row[1]}_#{row[2]}\" data-view=\"RFAMaintrack\" data-unordered=\"true\" data-title=\"#{row[2]}\" data-moreinfo=\"\"></div>")
    end
    htmlPage.concat("</ul>")
    htmlPage.concat("<div data-id=\"ticker\" data-view=\"Ticker\" data-scroll_orientation=\"horizontal\" style=\"display: none;\"></div>")
    htmlPage.concat("</div>")
    #p htmlPage
    return htmlPage
end

def eventSender(dashboardData)
    dashboardData.each do |row|
        items = []
        items << { label: "Test Suite:", value: "#{row[1]}" }
        items << { label: "Status:", value: "#{row[3]}"}
        #puts getStatus("#{row[3]}")
        send_event("#{row[1]}_#{row[2]}", { status: getStatus("#{row[3]}"), items: items })
    end

end

def getStatus (testResults)
    #puts testResults
    if testResults.downcase().strip() == "failure"
        #puts "w"
        return 'warning'
    elsif testResults.downcase().strip() == "success"
        return 'ok'
    end
    return 'danger'
end
