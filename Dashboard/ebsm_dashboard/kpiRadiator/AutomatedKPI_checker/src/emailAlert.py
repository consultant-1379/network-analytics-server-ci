# this is a script used to send an email from an email account (me) to another email account (you)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_alert_email(name, server_num, server_name, kpi_num, date_tag):
    # Name will be the name of the feature reporting a fault
    print '\nFail detected, send an email alert to Ross'
    me = "myemailtest96@gmail.com"
    my_password = "passthebutter"
    you = "ross.daly@ericsson.com"  # change the destination email address here

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Alert"
    msg['From'] = me
    msg['To'] = you

    html = '<html><body><p><h2>%s' \
           ' Fail Logged</h2></p><p>Server %s' \
           ' is reporting a failure after checking the %s' \
           ' feature.<br>The HTML results table can be checked under the %s directory.Link: ' \
           '<a href="http://atclvm571.athtem.eei.ericsson.se:3030/AutomatedKPI_checker' \
           '/Results/%s/%s/%s/%s__%s_Results_%s.html">' \
           'My Little Test Link</a></p></body></html>' \
           % (name, server_name, name, server_num, server_name, name, date_tag, kpi_num, date_tag, name)
     
    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    # Send the message via email server, over SSL - passwords are being sent
    s = smtplib.SMTP_SSL('smtp.gmail.com')

    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()
