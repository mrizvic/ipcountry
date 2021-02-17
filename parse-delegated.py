#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import os

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

allocs = {}
asnv4 = {}
asnv6 = {}
asnext = {}

for line in sys.stdin.readlines():
	line = line.rstrip()

	### FOR EACH ipv4
	### ripencc|UA|ipv4|213.110.96.0|8192|20090716|assigned|0bc6186a-9d14-46e9-a624-f09ebd01df38

	if line[13:15] == 'v4':
                line = line.rstrip()
                try: (registry,cc,addr_family,netaddr,num,date,status,extension) = line.split('|')
		except Exception as e:
			print(e, line[16], line)
			continue
                cidr = float(num)
		key = "{0}/ipv4".format(cc)
		value = "%s/%d" % (netaddr,(32-math.log(cidr,2)))
		allocs.setdefault(key, []).append(value)
		asnv4.setdefault(extension, []).append(value)
		continue

	### FOR EACH ipv6
	### ripencc|NL|ipv6|2001:610::|29|19990819|allocated|df7485ff-b735-44f3-a51f-0606fde4527b

	if line[13:15] == 'v6':
                (registry,cc,addr_family,netaddr,cidr,date,status,extension) = line.split('|')
		key = "{0}/ipv6".format(cc)
		value = "{0}/{1}".format(netaddr, cidr)
		allocs.setdefault(key, []).append(value)
		asnv6.setdefault(extension, []).append(value)
		continue

	### FOR EACH asn
	### ripencc|EU|asn|251|1|19930901|allocated|935422fc-24cc-4ad9-b447-32e3c258614a
        if line[11:14] == 'asn':
		(registry,cc,rtype,asn,value,date,status,extension) = line.split('|')
		asnext.setdefault(asn, extension)
		continue
		
### CREATE FILE FOR EACH asn.family
for asn in sorted(asnext):
	ext = asnext[asn]

	fname = "asn/{0}/ipv4.txt".format(asn)
	dirname = os.path.dirname(fname)

        if not os.path.exists(dirname):
                os.makedirs(dirname)

	#print(fname)
	with open(fname, 'w') as fd:
		try:
			for pool in asnv4[ext]:
				fd.write("{0}\n".format(pool))
		except Exception as exc:
				continue
				print("EXCEPT4: {0}".format(exc))

	fname = "asn/{0}/ipv6.txt".format(asn)

        if not os.path.exists(dirname):
                os.makedirs(dirname)

	#print(fname)
	with open(fname, 'w') as fd:
		try:
			for pool in asnv6[ext]:
				fd.write("{0}\n".format(pool))
		except Exception as exc:
				continue
				print("EXCEPT6: {0}".format(exc))

### CREATE FILE FOR EACH KEY
for key in sorted(allocs):
	fname = "{0}.txt".format(key)
        dirname = os.path.dirname(fname)
        if not os.path.exists(dirname):
                os.makedirs(dirname)
	with open(fname, 'w') as fd:
		for item in allocs[key]:
			fd.write("{0}\n".format(item))

### GENERATE index.html
fname = "country-addressfamily.html".format(key)
print(fname)
with open(fname, 'w') as fd:
	for key in sorted(allocs):
		line = '<A HREF="{0}.txt">{0}</A><BR>\n'.format(key)
		fd.write(line)

