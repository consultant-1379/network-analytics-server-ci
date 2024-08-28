def statusUpdate(status)
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))		#read in yaml file
	miniConID = properties["miniConfluenceID"]
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

	
	htmlPage="<ac:structured-macro ac:macro-id=\"413ad5ed-5fd1-44cf-824b-95982c4e8e17\" ac:name=\"html\" ac:schema-version=\"1\"><ac:plain-text-body><![CDATA[<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;border-collapse: separate;border-left: 0;border-radius: 4px;border-spacing: 0px;}th, td {padding: 15px;}</style></head><body><table width=200px><tr><td bgcolor=#205081><font color=#FFFFFF>Server Status</font></td><td bgcolor=#{statColour}><a href='https://confluence-nam.lmera.ericsson.se/display/TEAM8/KPI+Radiator+Page'><center><font color=#FFFFFF>#{status}</font></center></a></td></tr></table></body></html>]]></ac:plain-text-body></ac:structured-macro>"

	jsonRes['body']['storage']['value']=htmlPage
	jsonRes['version']['number']+=1	#increase the version number on the confluence page
	jsonStored = JSON.generate(jsonRes)
	
	request = Net::HTTP::Put.new(miniuri)
	request.basic_auth("assure", "assure")
	request.content_type = "application/json"
	
	request.body = jsonStored
	
	response = Net::HTTP.start(miniuri.host, miniuri.port, :use_ssl => miniuri.scheme == 'https',:verify_mode => OpenSSL::SSL::VERIFY_NONE) do |http|
		p http.request(request)
		puts "Confluence Load: Success!"
	end
end