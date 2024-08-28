
def add_feature(server,feature)
	properties = YAML.load(File.open('./dateLookUp.yaml', "r+"))
	content = '2000-01-01 10_30_00'	#placeholder date... will be updated by the end of the run
	
	if properties == nil
		#print "Failed to open file"
		return
	end

	#Check if server exists
	server_exists = false
	properties.each do |x|
		if x.include? server
			server_exists = true
		end
	end

	#Add server if it is not found
	if server_exists == false
		#print "Server does not exist. Adding #{server}"
		properties[server] = {}
	end

	#Check if feature exists
	for index,val in properties[server]
		if index == feature
			#print "Feature (#{feature}) already exists in #{server}."
			return
		end
	end

	properties[server][feature]= content
	output = YAML.dump properties
	File.write("./dateLookUp.yaml", output)
end