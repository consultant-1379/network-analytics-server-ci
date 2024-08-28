#!/usr/bin/env ruby
#Encoding: UTF-8
require 'date'
require 'time'


def sendStatusMail (loopType, parameterHashmap,teamStatus)

	properties=load_properties()
	
		sendFailureEmailsTo=""	
		
		formattedDateOfExecution = parameterHashmap["Date/Time Started"]

		fullHtmlFileName="./htmlEmails/#{loopType}_#{parameterHashmap["EPOCH"]}.html"
		sendMailName="./htmlEmails/#{loopType}_#{parameterHashmap["EPOCH"]}.sendMail"

		#Table Header
		system("echo '\<table style=\"vertical-align: top;\" border=\"1\" cellspacing=\"0\" cellpadding=\"0\" width=\"400\"\>'>>#{fullHtmlFileName}")
		system("echo '	\<tr bgcolor=\"#ffff99\"\>'>>#{fullHtmlFileName}")
		system("echo '    	\<th\>Attribute\</th\>'>>#{fullHtmlFileName}")
		system("echo '    	\<th\>Value\</th\>'>>#{fullHtmlFileName}")
		system("echo ' 	\<\/tr\>'>>#{fullHtmlFileName}")

		# Use for-loop on keys.
		for key in parameterHashmap.keys()

		#print key, "/", parameterHashmap[key], "\n"
			system("echo '	\<tr\>'>>#{fullHtmlFileName}")
			system("echo '    	\<td\>#{key}\</td\>'>>#{fullHtmlFileName}")
			system("echo '    	\<td\>#{parameterHashmap[key]}\</td\>'>>#{fullHtmlFileName}")
			system("echo ' 	\<\/tr\>'>>#{fullHtmlFileName}")
		end
		
		
		#Table Footer
		system("echo '\<\/table\>'>>#{fullHtmlFileName}")
		
		#------------------------------------------------------------------- STATUS -----------------------------------------------------------------
		system("echo ' 	\<hr>'>>#{fullHtmlFileName}")
		
		# Use for-loop on keys.
		#for key in teamStatus.keys()
		#	print key, "/", teamStatus[key], "\n"
		#end
		
		#Table Header
		system("echo '\<table style=\"vertical-align: top;\" border=\"1\" cellspacing=\"0\" cellpadding=\"0\" width=\"400\"\>'>>#{fullHtmlFileName}")
		system("echo '	\<tr bgcolor=\"#ffff99\"\>'>>#{fullHtmlFileName}")
		system("echo '    	\<th\>Test Suite\</th\>'>>#{fullHtmlFileName}")
		system("echo '    	\<th\>Team Name\</th\>'>>#{fullHtmlFileName}")
		system("echo '    	\<th\>Status\</th\>'>>#{fullHtmlFileName}")
		system("echo ' 	\<\/tr\>'>>#{fullHtmlFileName}")

		# Use for-loop on keys.
		for key in teamStatus.keys()

		data =key.split("$")
		teamName=data[1]
		
		
		#print key, "/", parameterHashmap[key], "\n"
		if teamStatus[key].downcase().strip() == "failure"
			system("echo '	\<tr bgcolor=\"#ff4d4d\"\>'>>#{fullHtmlFileName}")
			#teamName=data[1].strip
			#estepdu
			#------------------------------------------
			
			if teamName.downcase() =~ /_/
				muiltipeTeams=teamName.split("_")
				for index in 0 ... muiltipeTeams.size
					teamsEMail=properties[muiltipeTeams[index].downcase()]
					if ( teamsEMail )
						sendFailureEmailsTo.concat("#{teamsEMail} ")
					end
				end
			else
				if ( properties[teamName.downcase()] )
					sendFailureEmailsTo.concat("#{properties[teamName.downcase()]} ")
				end
			end
			#------------------------------------------
		elsif teamStatus[key].downcase().strip() == "success"
			system("echo '	\<tr bgcolor=\"#80ffaa\"\>'>>#{fullHtmlFileName}")
		else
			system("echo '	\<tr bgcolor=\"##f1c40f\"\>'>>#{fullHtmlFileName}")
		end		
			system("echo '    	\<td\>#{data[0].strip}\</td\>'>>#{fullHtmlFileName}")
			
			#Links Awakening again!!!!! f*%king "'" single quote
			replacements = [ ["'", ""] ]
			replacements.each {|replacement| teamName.gsub!(replacement[0], replacement[1])}
			
			system("echo '    	\<td\>#{teamName.strip}\</td\>'>>#{fullHtmlFileName}")
			system("echo '    	\<td\>#{teamStatus[key]}\</td\>'>>#{fullHtmlFileName}")
			system("echo ' 	\<\/tr\>'>>#{fullHtmlFileName}")
		end
		
	
		#Table Footer
		system("echo '\<\/table\>'>>#{fullHtmlFileName}")
		
		system("echo ' 	\<hr>'>>#{fullHtmlFileName}")
		
		system("echo '<p><b>Please Note:<\/b> Consistent failing longloop test cases will be reported on the following page <a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=132006563\">Long Loop Trend Analysis<\/a> <\/p>'>>#{fullHtmlFileName}")
		system("echo '<p>If you have failing testware please update page with the reason(s)!<\/p>'>>#{fullHtmlFileName}")
		system("echo '<p>'>>#{fullHtmlFileName}")
		system("echo '<ul>'>>#{fullHtmlFileName}")
		system("echo '<li><a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=162418846\">ENM RFA 250<\/a><\/li>'>>#{fullHtmlFileName}")
		system("echo '<li><a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=162418848\">ENM RFA 250 Staging<\/a><\/li>'>>#{fullHtmlFileName}")
		system("echo '<li><a href=\"http://confluence-nam.lmera.ericsson.se/pages/viewpage.action?pageId=162418850\">ENM Longloop<\/a><\/li>'>>#{fullHtmlFileName}")
		system("echo '<\/ul>'>>#{fullHtmlFileName}")
		system("echo '<\/p>'>>#{fullHtmlFileName}")

		
		############### Finally E-Mail ############################	
		#Send mail
		#Remove duplicate emails addresses
		sendFailureEmailsTo=sendFailureEmailsTo.split.reverse.uniq.reverse.join(' ')
		#Create a html mail
		system "( echo To: '#{sendFailureEmailsTo}' > #{sendMailName})"
		system "( echo cc: '#{properties["#{loopType}emailsCc"]}' >> #{sendMailName})" 
		system "( echo bcc: '#{properties["emailsBcc"]}' >> #{sendMailName})" 
		system "( echo 'From: No-Reply@Maintrack.Status' >> #{sendMailName})" 
		system "( echo 'Content-Type: text/html; ' >> #{sendMailName})" 
		system "( echo Subject: Maintrack #{loopType}  '#{formattedDateOfExecution}' >> #{sendMailName})"
		system "( cat #{fullHtmlFileName} >> #{sendMailName})"
		#All mail information created so send the mail
		system("cat #{sendMailName} | /usr/sbin/sendmail -t")
		system("rm #{fullHtmlFileName}")
		system("rm #{sendMailName}")


end





