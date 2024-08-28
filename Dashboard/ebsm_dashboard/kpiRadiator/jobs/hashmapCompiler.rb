require 'yaml'
require 'nokogiri'
require 'date'

def kpiStatus(folderServer,folderFeature,folderDate)
	#Put inside a function
	#Call that function passing the server, feature and date (concatinate the doc variable to match the path)
	#This will loop though all the KPI's for that feature
	#As it is looping add the status (pass/fail to the hashmap)

	kpiHash = Hash.new()

	##Parsing the data from the html results table
	doc =  Nokogiri::HTML(File.open("AutomatedKPI_checker/Results/#{folderServer.to_s}/#{folderFeature.to_s}/#{folderDate.to_s}/Summary.html"))	#using relitive path
	tableRows=doc.search('table')
	content=tableRows.search('tr').map do |rows, i|
		rows.css('td').map(&:inner_html)
	end

	content = content.reject do |e|
		e.empty?
	end

	content.each do |kpi|		#for row in	#loop through the number of kpis in the results table
		status = kpi[0]
		kpiNoko = Nokogiri::HTML(kpi[1].to_s)
		kpiDetails = kpiNoko.css('a').map(&:text)
		kpiSpecifics = kpiDetails[0].split(",")
		
		kpiHash[kpiSpecifics[0]] = status
	end
	return kpiHash	#holds the status of each kpi in the feature
end

def updateYAML(properties)	#write to YAML with new date
	File.open('./dateLookUp.yaml', 'w') {|f| f.write properties.to_yaml } #Store
	#puts 'YAML updated'
end

def hashedStatus()	#will return a hashmap of all results found in the results directory
	properties = YAML.load(File.open("./dateLookUp.yaml", "r"))		#read in yaml file

	finalHash = Hash.new()
	Dir.glob('AutomatedKPI_checker/Results/*') do |server|	##get data from html Results file
		if File.directory?(server)
			Dir.glob("#{server}/*") do |feature|
				if File.directory?(feature)
					Dir.glob("#{feature}/*") do |date|
						folderSplit = date.split('/')
						folderServer = folderSplit[2]	#current server name
						folderFeature = folderSplit[3]	#current feature name
						folderDate = folderSplit[4]	#current date
						
						if !(finalHash.has_key?(folderServer)) 	#if does not finalHash has a key matching folderServer
							finalHash[folderServer]=Hash.new()	#add this to the hash (hashmap is used later to add missing servers to confluence)
						end
						if !(finalHash[folderServer].has_key?(folderFeature)) 
							finalHash[folderServer][folderFeature]=Hash.new()
						end
						if !(finalHash[folderServer][folderFeature].has_key?(folderServer)) 
							finalHash[folderServer][folderFeature][folderDate]=Hash.new()
						end
						
						add_feature(folderServer, folderFeature)	#this function checks if the feature is in the yaml file, if not it will add it
						
						begin	#try to parse the date
							formatDate = DateTime.parse(folderDate.gsub("_", ":"))	#folder date time in DateTime format
							
							#Do comparison action with yaml file
							yamlDate = DateTime.parse(properties[folderServer][folderFeature].gsub("_", ":"))	#yaml date time in DateTime format

							if yamlDate<formatDate	#if new date in html...update and add to confluence
								##Parsing the data from the html results table
								finalHash[folderServer][folderFeature][folderDate] = kpiStatus(folderServer,folderFeature,folderDate)
								properties['newestDate']=folderDate
								properties[folderServer][folderFeature]=folderDate
								
								updateYAML(properties)
							end
							
						rescue Exception => e	#if the file is not a date do nothing(uncomment to debug)
							#puts e.message
							#puts e.backtrace.inspect
						end
					end
				end
			end
		end
	end
	return finalHash
end



