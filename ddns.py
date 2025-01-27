#!/bin/python3

import subprocess
import re

domain = 'cam-davis.com'
subdomain = 'ops'

records = subprocess.run(['doctl', 'compute', 'domain', 'records', 'list', domain], capture_output=True, text=True)
records = records.stdout

records_split = records.split('\n')

domain_record = [ record for record in records_split if subdomain in record ]
domain_record = domain_record[0]

record_id = re.match(r"[0-9]+", domain_record).group()

ip_response = subprocess.run(['curl', '-4', 'icanhazip.com'], capture_output=True, text=True)
public_ip = ip_response.stdout.strip()

update = subprocess.run(['doctl', 'compute', 'domain', 'records', 'update', domain, '--record-id', record_id, '--record-name', subdomain, '--record-type', 'A', '--record-data', public_ip, '--record-ttl', '3600'], capture_output=True, text=True)
