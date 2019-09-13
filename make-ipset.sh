#!/usr/bin/env bash

die() { echo "$*" 1>&2 ; exit 1; }

which aggregate > /dev/null || die "ERROR: missing aggregate"
which ipset     > /dev/null || die "ERROR: missing ipset"

if [ "$EUID" -ne 0 ]; then
  die "ERROR: run as root"
fi

ME=$(basename "$0")
WORKDIR="$(readlink -f $(dirname "$0"))"
FILE=$1

if [ -z "$FILE" ]; then
  die "USAGE: $ME <ipv4-networks-file>"
fi

LFILE=$(readlink -f $FILE)
BFILE=$(basename "$FILE")


### IF LOCAL FILE DOESNT EXIST FETCH FROM REMOTE SITE
if [ ! -f "$LFILE" ]; then
  echo "###: WGET $BFILE"
  wget -O - "http://ipcountry.ts.si/$BFILE" | aggregate > $LFILE
fi

if [ ! -f "$LFILE" ]; then
  die "ERROR: $LFILE DOESNT EXIST"
fi


### FLUSH EXISTING IPSET OR CREATE NEW IF DOESNT EXIST
SETNAME=$(basename "$FILE" | cut -d '.' -f1) 
echo "###: IPSET FLUSH || CREATE $SETNAME"
if [[ $SETNAME =~ "ipv4" ]]; then
  ipset flush $SETNAME || ipset create $SETNAME hash:net family inet hashsize 8192 maxelem 8192
elif [[ $SETNAME =~ "ipv6" ]]; then
  ipset flush $SETNAME || ipset create $SETNAME hash:net family inet6 hashsize 8192 maxelem 8192
else
  die "ERROR: ipv4 OR ipv6 STRING MISSING FROM FILENAME"
fi

echo "###: IPSET POPULATE $SETNAME"
### ADD NEW NETWORKS
for i in $(cat $FILE); do
  ipset add $SETNAME $i
done 


echo "###: IPSET SAVE $SETNAME"
### SAVE FOR REBOOT
ipset save > /etc/ipset.conf 

