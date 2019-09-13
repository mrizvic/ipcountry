#!/usr/bin/env bash

WORKDIR="$(readlink -f $(dirname "$0"))"
OUTFILE="${WORKDIR}/delegated-ripencc-extended-latest"

cd ${WORKDIR}

### FETCH FILE FROM RIPE
wget -O ${OUTFILE} ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest

### REMOVE OLD LISTS
rm ${WORKDIR}/*-ipv4.txt
rm ${WORKDIR}/*-ipv6.txt
rm ${WORKDIR}/index.html

### PARSE FILE AND CREATE cc-inetfamily.txt FILES
cat ${OUTFILE} | ${WORKDIR}/parse-allocated-all.py 

### CREATE PACKAGE
tar cvzf ${WORKDIR}/package.tar.gz --exclude="package.tar.gz" --exclude="*log" --exclude="*.txt" --exclude="index.html" -C ${WORKDIR} .
