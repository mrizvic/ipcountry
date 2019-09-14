#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

allocs = dict()

### HELPER
def addKeyVal (key, value):
	try: allocs[key]
	except KeyError: allocs[key] = list()
	finally: allocs[key].append(value)
	return

ln = 0

for line in sys.stdin.readlines():
	if ln == 0:
		(cc,tag) = line.rstrip().split('.')
		ln += 1
		continue
	if ln == 1:
		name = line.rstrip()
		ln += 1
		continue
	if ln == 2:
		ln += 1
		continue
	if ln > 2:
		if len(line) < 3:
			ln = 0
			continue
		dataz = line.rstrip().split('\t')
		network = dataz[1].rstrip()
		family = "ipv4"
		if ":" in network:
			family = "ipv6"
		key = "{0}.{1}.{2}".format(cc, tag, family)
		addKeyVal(key, network)
		continue


### CREATE FILE FOR EACH KEY
for key in sorted(allocs):
	fname = "{0}.txt".format(key)
	fd = open(fname, 'w')
	for item in allocs[key]:
		fd.write("{0}\n".format(item))
	fd.close()

### GENERATE index.html
fname = "country.operator.addressfamily.html".format(key)
fd = open(fname, 'w')
for key in sorted(allocs):
	line = '<A HREF="{0}.txt">{0}</A><BR>\n'.format(key)
	fd.write(line)
fd.close()

