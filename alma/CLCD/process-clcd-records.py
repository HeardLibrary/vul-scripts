import pysftp
import hashlib
import os
import shutil
import ftplib
from ftplib import FTP
from pathlib import Path
from funct import *
from smtp import *

#############################################################
## above funct and smtp are files that contain credentials ##
#############################################################

#####################################################
## files generated from Alma - Publishing Profiles ##
## 6 CLCD profiles ran once a month                ##
## submitted to VUIT's AWS SFTP server             ##
## check VUIT's SFTP server for files              ##
## credentials are stored in funct.py              ##
## download files in this directory for process    ##
## then remove files from SFTP server              ##
#####################################################

try:
    conn = pysftp.Connection(host=sftpdomain,port=22,username=sftpuname,password=sftppwd)
    print("connection established successfully")
except:
    print("failed to establish connection to targeted server")

current_dir = conn.pwd
print('our current working directory is: ',current_dir)

with conn.cd('alma/CLCD/'):
    files = conn.listdir()
    for file in files:
        conn.get(file)
        print(file,' downloaded successfully ')
        conn.remove(file)

conn.close()

###################################################
## end downloading files from VUIT's SFTP server ##
###################################################

#######################################################
## process files downloaded                          ##
## these have to be renamed in a specific convention ##
## check https://enterprise.clcd.com/ for details    ##
## once renamed FTP to CLCD                          ##
## 3/13/2025 -- FTP connection failing currently     ##
#######################################################

def md5sum(filename, blocksize=65536):
    hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

custid = '2022100002'
otype = 'UPDATE'
under = '_'
dst = 'Archive/'
pdst = 'Sent/'

fnamelst = [f for f in os.listdir('.') if os.path.isfile(f)]

##ftp = ftplib.FTP(clcddomain)
##ftp.login(clcduname,clcdpwd)
SUBJECT = 'New CLCD files'
BODY_TEXT = f"These CLCD files are ready to be sent to CLCD.{os.linesep}"

for fname in fnamelst:
    if fname.startswith('CLCD'):
        print("File: ",fname,"; Checksum: ",md5sum(fname),"; Timestamp: ",os.path.getctime(fname))
        shutil.copy(fname,dst)
        newfname=custid+under+otype+under+str(md5sum(fname))+under+str(os.path.getctime(fname))+".mrc"
        BODY_TEXT=BODY_TEXT+newfname+f"{os.linesep}"
        os.rename(fname,newfname)
        file_path = Path(newfname)
        file = open(newfname,'rb')
        ##ftp.storbinary(f'STOR {file_path.name}',file)
        shutil.move(newfname,pdst)

##ftp.quit

####################################################################################
## Below sends an email confirmation when files have been received and processed. ##
## RECIPIENT is current set to creator of this script but can be anyone.          ##
## https://www.library.vanderbilt.edu/go.new/px6e                                 ##
####################################################################################

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
##part2 = MIMEText(BODY_HTML, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
##msg.attach(part2)

# Try to send the message.
try:
    with SMTP_SSL(HOST, PORT) as server:
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
        print("Email sent!")

except SMTPException as e:
        print("Error: ", e)
