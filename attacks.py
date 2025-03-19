import argparse
import random
import socket
import sys
import time
from datetime import datetime

SSH_PAYLOADS = [
    "SSH-2.0-OPenSSH_7.9\r\nroot:x:0:root:/root/bin/bash\r\n",
    "SSH-2.0-PuTTY_Release_0.70\rnadmin:admin123\r\n",
    "SSH=2.0-JSCH-0.1.54\r\nssh-connection\r\n"
]

FTP_PAYLOADS = [
    "USER anonymous\r\nPASS anonymous@example.com\r\n",
    "USER admin\r\nPASS admin123\r\n",
    "SITE EXEC ../../../bin/sh\r\n"
]

TELNET_PAYLOADS = [
    "login: admin\r\npasswrod: password123\r\n",
    "login: root\r\npassword: toor\r\n",
    "\xff\xfb\x01\xff\xfb\x03\xff\xfd\x03\xff\xfe\x01\r\n"
]

HTTP_PAYLOADS = [
    "GET /wp-admin/admin-ajax.php HTTP/1.1\r\nHost: target\r\n\r\n",
    "POST /cgi-bin/../../../../bin/sh HTTP/1.1\r\nHost: target\r\n\r\n",
    "GET /?page=../../../etc/passwd HTTP/1.1\r\nHost: target\r\nUser-Agent: sqlmap/1.3.11#dev\r\n\r\n"
    
    
]

HTTPS_PAYLOADS = [
    "POST /api/login HTTP/1.1\r\nHost: target\r\nContent-Type: application/json\r\n\r\n{\"username\":\"admin\", \"password\":\"admin123\"}",
    "GET /phpmyadmin/ HTTP/1.1\r\nHost: target\r\nUser-Agent: Nmap\r\n\r\n",
    "GET/solr/admin/ HTTP/1.1\r\nHost: target\r\n\r\n"
]

MYSQL_PAYLOADS = [
    "\x03select version",
    "\x03SHOW DATABASES"
]

PORT_PAYLOADS = {
    21: SSH_PAYLOADS,
    22: FTP_PAYLOADS,
    23: TELNET_PAYLOADS,
    80: HTTP_PAYLOADS,
    443: HTTPS_PAYLOADS,
    3306: MYSQL_PAYLOADS
}


def simulate_attack(host, port, intensity, payload=None):
    # Instead of making real connections, just return success
    return True

