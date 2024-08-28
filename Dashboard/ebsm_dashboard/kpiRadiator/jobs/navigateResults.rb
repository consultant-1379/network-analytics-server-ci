#This sends the results from the kpi checker to the confluence when requested
get '/AutomatedKPI_checker/Results/:multi' do |multi|
	send_file "./AutomatedKPI_checker/Results/#{multi}"
end

get '/AutomatedKPI_checker/Results/:serverNam/:featureNam/:date/:sum' do |serverNam,featureNam,date,sum|
	send_file "./AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{date}/#{sum}"
end

get '/AutomatedKPI_checker/Results/:serverNam/:featureNam/:date/:kpiNam/:kpiSum' do |serverNam,featureNam,date,kpiNam,kpiSum|
	send_file "./AutomatedKPI_checker/Results/#{serverNam}/#{featureNam}/#{date}/#{kpiNam}/#{kpiSum}"
end