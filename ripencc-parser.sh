#!/usr/bin/env bash

WORKDIR="$(readlink -f $(dirname "$0"))"
OUTFILE="${WORKDIR}/delegated-ripencc-extended-latest"
ALLOCS="${WORKDIR}/alloclist.txt"

cd ${WORKDIR}

### FETCH FILE FROM RIPE
wget -O ${OUTFILE} ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest
wget -O ${ALLOCS} ftp://ftp.ripe.net/pub/stats/ripencc/membership/alloclist.txt

### REMOVE OLD LISTS
rm ${WORKDIR}/*ipv4.txt
rm ${WORKDIR}/*ipv6.txt
rm ${WORKDIR}/index*

### PARSE FILE AND CREATE cc-inetfamily.txt FILES
cat ${OUTFILE} | ${WORKDIR}/parse-delegated.py 
cat ${ALLOCS} | ${WORKDIR}/parse-allocs.py 

### CREATE PACKAGE
tar cvzf ${WORKDIR}/package.tar.gz --exclude="package.tar.gz" --exclude="*log" --exclude="*.txt" --exclude-vcs -C ${WORKDIR} .
