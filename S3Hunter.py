#!/usr/bin/python3

import requests
import optparse
import sys
import os
import concurrent.futures

BLUE='\033[94m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CLEAR='\x1b[0m'

print(BLUE + "S3Hunter[1.0] by ARPSyndicate" + CLEAR)
print(YELLOW + "hunts for unreferenced aws s3 buckets" + CLEAR)

if len(sys.argv)<2:
	print(RED + "[!] ./S3Hunter --help" + CLEAR)
	sys.exit()

else:
	parser = optparse.OptionParser()
	parser.add_option('-l', '--list', action="store", dest="list", help="list of domains to check")
	parser.add_option('-v', '--verbose', action="store_true", dest="verbose", help="enable logging", default=False)
	parser.add_option('-t', '--timeout', action="store", dest="timeout", help="timeout", default=5)
	parser.add_option('-T', '--threads', action="store", dest="threads", help="threads", default=20)
	parser.add_option('-o', '--output', action="store", dest="output", help="output results")
	parser.add_option('-P', '--only-output-permutations', action="store_true", dest="operms", help="just prints out the permutations")
	parser.add_option('--only-direct', action="store_false", dest="permutation", help="runs only direct enum", default=True)
	parser.add_option('--only-permutation', action="store_false", dest="direct", help="runs only permutation enum", default=True)
	parser.add_option('--no-regions', action="store_false", dest="region", help="no regional permutations", default=True)

inputs, args = parser.parse_args()
if not inputs.list:
	parser.error(RED + "[!] list of targets not given" + CLEAR)
list = str(inputs.list)
verbose = inputs.verbose
permutation = inputs.permutation
direct = inputs.direct
operms = inputs.operms
region = inputs.region
output = str(inputs.output)
timeout = int(inputs.timeout)
threads = int(inputs.threads)
result = []
with open(list) as f:
	domains=f.read().splitlines()

def checkResult(res, domain):
	if "ListBucketResult" in str(res):
		result.append(domain)
		print(BLUE + "[+] found "+domain + CLEAR)
        
def directEnum(domain):
	try:
		if verbose:
			print(GREEN + "[VERBOSE] checking for "+domain + CLEAR)
		req = requests.get("http://cloudfront.com", params='', headers={'Host':'%s' % domain}, timeout=timeout)
		res = req.text
		checkResult(res,domain)
		req = requests.get("https://"+domain, timeout=timeout)
		res = req.text
		checkResult(res, domain)
	except:
		pass

def generatePerms(domains):
	perms=[]
	for domain in domains:
		perms.append("https://{0}.s3.amazonaws.com".format(domain))
		perms.append("https://s3.amazonaws.com/{0}".format(domain.replace(".","-")))
		perms.append("https://{0}.s3.amazonaws.com".format(domain.replace(".","-")))
		perms.append("https://s3.amazonaws.com/{0}".format(domain.replace(".","_")))
		perms.append("https://{0}.s3.amazonaws.com".format(domain.replace(".","_")))
		if(region):
			perms.append("https://{0}.s3-us-east-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-us-east-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-us-west-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-us-west-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ca-central-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-eu-central-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-eu-west-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-eu-west-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ap-northeast-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ap-northeast-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-ap-south-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-sa-east-1.amazonaws.com".format(domain))
			perms.append("https://{0}.s3-us-east-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-us-east-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-us-west-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-us-west-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ca-central-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-eu-central-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-eu-west-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-eu-west-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ap-northeast-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ap-northeast-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-ap-south-1.amazonaws.com".format(domain.replace(".","-")))
			perms.append("https://{0}.s3-sa-east-1.amazonaws.com".format(domain.replace(".","-")))		
			perms.append("https://{0}.s3-us-east-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-us-east-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-us-west-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-us-west-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ca-central-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-eu-central-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-eu-west-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-eu-west-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ap-northeast-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ap-northeast-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ap-southeast-2.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-ap-south-1.amazonaws.com".format(domain.replace(".","_")))
			perms.append("https://{0}.s3-sa-east-1.amazonaws.com".format(domain.replace(".","_")))
	return perms

def permEnum(perm):
	try:
		if verbose:
			print(GREEN + "[VERBOSE] checking for "+perm + CLEAR)
		req = requests.get(perm , timeout=timeout)
		res = req.text
		checkResult(res,perm)
	except:
		pass

if not operms:
	if direct:
		print(YELLOW + "[*] starting direct enum"+ CLEAR)
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			try:
				executor.map(directEnum, domains)
			except(KeyboardInterrupt, SystemExit):
				print(RED + "[!] interrupted" + CLEAR)
				executor.shutdown(wait=False)
				sys.exit()

	if permutation:
		print(YELLOW + "[*] starting permutations enum"+ CLEAR)
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			print(YELLOW + "[*] generating permutations"+ CLEAR)
			perms=generatePerms(domains)		
			print(YELLOW + "[*] generated "+str(len(perms))+" permutations"+ CLEAR)
			try:
				executor.map(permEnum, perms)
			except(KeyboardInterrupt, SystemExit):
				print(RED + "[!] interrupted" + CLEAR)
				executor.shutdown(wait=False)
				sys.exit()
	if inputs.output:
		with open(output, 'a') as f:
			f.writelines("%s\n" % line for line in result)
else:
	if inputs.output:
		with open(output, 'a') as f:
			f.writelines("%s\n" % line for line in generatePerms(domains))
	else:
		print(RED + "[!] output file not provided"+ CLEAR)
print(YELLOW+"[*] done"+CLEAR)