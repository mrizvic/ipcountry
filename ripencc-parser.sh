#!/usr/bin/env bash

WORKDIR="$(readlink -f $(dirname "$0"))"
OUTFILE="${WORKDIR}/delegated-ripencc-extended-latest"
ALLOCS="${WORKDIR}/alloclist.txt"
die() { echo "$*" 1>&2 ; exit 1; }

which wget > /dev/null && DLAGENT="wget"
which curl > /dev/null && DLAGENT="curl"
[ -z "$DLAGENT" ] && die 'ERROR: please install curl or wget and make sure they are in $PATH'

cd ${WORKDIR}

### FETCH FILE FROM RIPE

if [ "$DLAGENT" == "wget" ]; then
  wget -qO ${OUTFILE} ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest
  wget -qO  ${ALLOCS} ftp://ftp.ripe.net/pub/stats/ripencc/membership/alloclist.txt
elif [ "$DLAGENT" == "curl" ]; then
  curl -qSs -o ${OUTFILE} ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest
  curl -qSs -o  ${ALLOCS} ftp://ftp.ripe.net/pub/stats/ripencc/membership/alloclist.txt
fi


### REMOVE OLD LISTS
find ${WORKDIR} -maxdepth 1 -name '*ipv4.txt' -delete
find ${WORKDIR} -maxdepth 1 -name '*ipv6.txt' -delete
find ${WORKDIR} -maxdepth 1 -name 'country*.html' -delete

### PARSE FILE AND CREATE cc-inetfamily.txt FILES
cat ${OUTFILE} | ${WORKDIR}/parse-delegated.py 
cat ${ALLOCS} | ${WORKDIR}/parse-allocs.py 

### CREATE PACKAGE
tar cvzf ${WORKDIR}/package.tar.gz --exclude="package.tar.gz" --exclude="*log" --exclude="*.txt" --exclude-vcs -C ${WORKDIR} .
