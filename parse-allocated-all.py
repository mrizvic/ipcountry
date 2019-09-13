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

### HELPER
def addKeyVal (key, value):
	try: allocs[key]
	except KeyError: allocs[key] = list()
	finally: allocs[key].append(value)
	return

for line in sys.stdin.readlines():

	### FOR EACH allocated ipv4
        if line.find("|ipv4") > -1 and line.find("allocated",35) > 0:
                line = line.rstrip()
                (ripe,cc,addr_family,netaddr,num,date,status,id) = line.split('|')
                cidr = numcidr4[num]
		key = "{0}-ipv4".format(cc)
		value = "{0}/{1}".format(netaddr, cidr)
		addKeyVal(key, value)
		continue

	### FOR EACH allocated ipv6
        if line.find("|ipv6") > -1 and line.find("allocated",35) > 0:
                (ripe,cc,addr_family,netaddr,cidr,date,status,id) = line.split('|')
		key = "{0}-ipv6".format(cc)
		value = "{0}/{1}".format(netaddr, cidr)
		addKeyVal(key, value)
		continue

### CREATE FILE FOR EACH KEY
for key in sorted(allocs):
	fname = "{0}.txt".format(key)
	fd = open(fname, 'w')
	for item in allocs[key]:
		fd.write("{0}\n".format(item))
	fd.close()

### GENERATE index.html
fname = "index.html".format(key)
fd = open(fname, 'w')
for key in sorted(allocs):
	line = '<A HREF="{0}.txt">{0}</A><BR>\n'.format(key)
	fd.write(line)
fd.close()

