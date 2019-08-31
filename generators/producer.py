from tail import follow
from parser import apache_log
from sendto import sendto

lines = open('www/access-log')
lines = follow(lines)
log = apache_log(lines)
sendto(log, ("", 15000))
