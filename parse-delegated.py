#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

### for i in range(32,0,-1):    print ("'{0}': '{1}',".format(2**i,i))

numcidr4={

        '1':          '32',
        '2':          '31',
        '4':          '30',
        '8':          '29',
        '16':         '28',
        '32':         '27',
        '64':         '26',
        '128':        '25',
        '256':        '24',
        '512':        '23',
        '1024':       '22',
        '2048':       '21',
        '4096':       '20',
        '8192':       '19',
        '16384':      '18',
        '32768':      '17',
        '65536':      '16',
        '131072':     '15',
        '262144':     '14',
        '524288':     '13',
        '1048576':    '12',
        '2097152':    '11',
        '4194304':    '10',
        '8388608':    '9',
        '16777216':   '8',
        '33554432':   '7',
        '67108864':   '6',
        '134217728':  '5',
        '268435456':  '4',
        '536870912':  '3',
        '1073741824': '2',
        '2147483648': '1',
        '4294967296': '0',

}

allocs = dict()
asnv4 = dict()
asnv6 = dict()
asnext = dict()

### HELPER
def addKeyVal (dictionary, key, value):
	try: dictionary[key]
	except KeyError: dictionary[key] = list()
	finally: dictionary[key].append(value)
	return

for line in sys.stdin.readlines():
	line = line.rstrip()

	### FOR EACH allocated ipv4
        if line.find("|ipv4") > -1 and line.find("allocated",35) > 0:
                line = line.rstrip()
                (registry,cc,addr_family,netaddr,num,date,status,extension) = line.split('|')
                cidr = numcidr4[num]
		key = "{0}-ipv4".format(cc)
		value = "{0}/{1}".format(netaddr, cidr)
		addKeyVal(allocs, key, value)
		addKeyVal(asnv4, extension, value)
		continue

	### FOR EACH allocated ipv6
        if line.find("|ipv6") > -1 and line.find("allocated",35) > 0:
                (registry,cc,addr_family,netaddr,cidr,date,status,extension) = line.split('|')
		key = "{0}-ipv6".format(cc)
		value = "{0}/{1}".format(netaddr, cidr)
		addKeyVal(allocs, key, value)
		addKeyVal(asnv6, extension, value)
		continue

	### FOR EACH allocated ipv6
	### ripencc|EU|asn|251|1|19930901|allocated|935422fc-24cc-4ad9-b447-32e3c258614a
        if line.find("|asn") > -1 and line.find("allocated",25) > 0:
		(registry,cc,rtype,asn,value,date,status,extension) = line.split('|')
		addKeyVal(asnext, asn, extension)
		continue
		
### CREATE FILE FOR EACH asn.family
for asn in sorted(asnext):
	ext = asnext[asn][0]

	fname = "asn{0}.ipv4.txt".format(asn)
	fd = open(fname, 'w')
	try:
		for pool in asnv4[ext]:
			fd.write("{0}\n".format(pool))
	except Exception as e:
			print(e)
	fd.close()

	fname = "asn{0}.ipv6.txt".format(asn)
	fd = open(fname, 'w')
	try:
		for pool in asnv6[ext]:
			fd.write("{0}\n".format(pool))
	except Exception as e:
			print(e)
	fd.close()

### CREATE FILE FOR EACH KEY
for key in sorted(allocs):
	fname = "{0}.txt".format(key)
	fd = open(fname, 'w')
	for item in allocs[key]:
		fd.write("{0}\n".format(item))
	fd.close()

### GENERATE index.html
fname = "country-addressfamily.html".format(key)
fd = open(fname, 'w')
for key in sorted(allocs):
	line = '<A HREF="{0}.txt">{0}</A><BR>\n'.format(key)
	fd.write(line)
fd.close()

