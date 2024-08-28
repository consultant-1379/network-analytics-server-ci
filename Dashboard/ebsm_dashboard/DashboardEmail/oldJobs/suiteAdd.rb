post '/AddSuite/' do
    ra = params[:ra]
    suite = params[:suite]
	team = params[:team]
	run = params[:run]

	puts "#{ra} #{suite} #{team} #{run}"
	addSuiteConfluence($globalMTRFA250TeamStatus, ra, suite, team, run, 197034522)

end


