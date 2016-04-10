# /mnt/sd/arduino/www/vrc/service/servicemail.py
# cd /mnt/sd/arduino/www/vrc/service
# ls-l 
# python /mnt/sd/arduino/www/vrc/service/servicemail.py
# Author:   Michael Gries
# Creation: 2015-03-23
# Modified: 2015-03-24

# Import smtplib for sending an email
import smtplib

# Import the required email modules 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

path = "/mnt/sd/arduino/www/vrc/service/"
data = "vrc_status.txt"
html = "index.htm"
logo = "logo_vaillant.gif"
textfile  = path + data
imagefile = path + logo
htmlfile  = path + html

# Create Html style as first email part
html = """\
<html>
  <head></head>
  <body>
    <p>Showing status of first stored datagram<br>
       after detecting service noitification by VKO unit.<br>
       <br>
       Use homepage <a href="http://www.gries.name/projekte/vrc/vrc.htm">VRC Monitor</a> for decoding.<br>
       <br>
    </p>
  </body>
</html>
"""
part1 = MIMEText(html, 'html')

#Open image as second email part
fi = open(imagefile)
part2 = MIMEImage(fi.read())
fi.close()

# Create common ASCII text as third email part
plaintext = "\n\nDatagram: \n"
part3 = MIMEText(plaintext, 'plain')

# Open a plain text file as fourth email part
# Make sure the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
part4 = MIMEText(fp.read(), 'plain')
fp.close()

# Open a html file as fifth email part
fh = open(htmlfile)
part5 = MIMEText(fh.read(), 'html')
fh.close()

sendSubject = 'Status: Wartungs Anforderung'
sendFrom = "vrc@gries.name" # email address by sending entity
sendTo = "michael@gries.name" # recipient's email address

msg = MIMEMultipart()
msg['Subject'] = sendSubject 
msg['From'] = sendFrom 
msg['To'] = sendTo 

msg.attach(part1)
msg.attach(part2)
msg.attach(part3)
msg.attach(part4)
msg.attach(part5)



# Send the message via our own SMTP server, but don't include the
# envelope header.

try:
  # server = smtplib.SMTP('localhost')
  server = smtplib.SMTP('smtp.1und1.de', 587)
  server.set_debuglevel(0)
  #server.set_debuglevel(1)
  server.login('michael@gries.name', 'nopasswd1')
  server.sendmail(sendFrom, sendTo , msg.as_string())
  print "Sucessfully sent email"
except SMTPException:
  print "SMTP error: email not sent"
finally:
  server.quit()
  print "SMTP service finalized"
