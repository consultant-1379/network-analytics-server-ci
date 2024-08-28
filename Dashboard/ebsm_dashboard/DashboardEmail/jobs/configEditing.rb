post '/AddSuite/' do
    puts "hello"

end

post '/AddBuild/' do
  buildName = params[:buildName]
  buildJenkinsURL = params[:buildJenkinsURL]
  buildConfluenceID = params[:buildConfluenceID]
  buildLastProcessedBuildNumber = 0
  buildTag = params[:buildTag]

  addBuild(buildName, buildJenkinsURL, buildConfluenceID, buildLastProcessedBuildNumber, buildTag)
end
