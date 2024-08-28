require 'rubygems'
require 'json'
require 'open-uri'
require 'date'
require 'time'
require 'rubygems'
require 'net/http'
require 'rss/utils'
require 'uri'
require 'csv'
require 'cgi'
require "erb"

def addNewKPI(latestRun,fullTable,dateOfLastRun)	#add the new KPIs to end of the confluence table
	arrayServers = latestRun.keys
	arrayServers.each do |serverNam|	#for every server in the hashmap
		#p serverNam
		featureHash = latestRun[serverNam]
		arrayFeatures = featureHash.keys
		arrayFeatures.each do |featureNam|	#for every feature
			#p featureNam
			kpiHash = latestRun[serverNam][featureNam][dateOfLastRun]	#get hash of all KPIs with the latest date
			arrayKPI = kpiHash.keys
			arrayKPI.each do |kpiNum|
				#p kpiNum	#holds the current kpi number
				kpiStatus = latestRun[serverNam][featureNam][dateOfLastRun][kpiNum]	#holds the current kpi status(pass/fail/empty)
				#p kpiStatus
				fullTable.push([serverNam, featureNam, kpiNum, kpiStatus])
			end
		end
	end
	return fullTable
end