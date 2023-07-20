# Import Module
import ftplib

# Fill Required Information
HOSTNAME = "vh312.timeweb.ru"
USERNAME = "cw64765"
PASSWORD = "x7ORTZ8MSrNO"

# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# force UTF-8 encoding
ftp_server.encoding = "utf-8"

# Enter File Name with Extension
filename = "user_user.png"

# Read file in binary mode
with open(filename, "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {filename}", file)