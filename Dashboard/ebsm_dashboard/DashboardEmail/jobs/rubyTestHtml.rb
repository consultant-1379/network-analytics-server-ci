require 'rubygems'
require 'json'
require 'open-uri'
require 'date'
require 'time'
require 'nokogiri'
require 'rubygems'
require "selenium-webdriver"
require 'net/http'
require 'rss/utils'
require 'uri'
require 'csv'
require 'cgi'
require "erb"

def statusUpdate(status)
	miniConID = '209055012'
	miniuri = URI("https://confluence-nam.lmera.ericsson.se:443/rest/api/content/#{miniConID}?expand=body.storage,version")
	
	jsonRes=Hash.new()
	Net::HTTP.start(miniuri.host, miniuri.port, :use_ssl => miniuri.scheme == 'https',:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		request = Net::HTTP::Get.new miniuri.request_uri
		request.basic_auth "assure", "assure"
		response = http.request(request)
		jsonRes = JSON.parse(response.body)
	end
	
	#set colour of the status
	if status=="Fail"
		statColour="#E32219"
	elsif status=="Pass"
		statColour="#89BA17"
	end

	htmlPage="
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: separate;
    border-left: 0;
    border-radius: 4px;
    border-spacing: 0px;
}
th, td {
    padding: 15px;
}
</style>
</head>
#Or colour = 205081
<body>
	<table width=290px>
		<tr>
			<td bgcolor=#0066cc><p style='margin-left:5px'><font color=#FFFFFF>Server Status</font></p></td>
			<td bgcolor=#{statColour}><a href='https://confluence-nam.lmera.ericsson.se/display/TEAM8/Test+Page'><center><font color=#FFFFFF>#{status}</font></center></a></td>
		</tr>
	</table>
</body>
</html>"
	
	jsonRes['body']['storage']['value']=htmlPage
	jsonRes['version']['number']+=1	#increase the version number on the confluence page
	jsonStored = JSON.generate(jsonRes)
	
	request = Net::HTTP::Put.new(miniuri)
	request.basic_auth("assure", "assure")
	request.content_type = "application/json"
	
	request.body = jsonStored
	
	print request.body
	
	response = Net::HTTP.start(miniuri.host, miniuri.port, :use_ssl => miniuri.scheme == 'https',:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		p http.request(request)
		puts "Confluence Load: Success!"
	end
end


statusUpdate("Fail")