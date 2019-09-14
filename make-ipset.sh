#!/usr/bin/env bash

PATH=$PATH:/usr/bin:/usr/sbin:/bin:/sbin
ME=$(basename "$0")

die() { echo "$*" 1>&2 ; exit 1; }

which ipset > /dev/null || die "ERROR: missing ipset"
[ "$EUID" -ne 0 ] && die "ERROR: run as root"
[ -z "$1" ] && die "USAGE: $ME <ipv4-or-ipv6-cidr-networks-file>"

FILE=$1
WORKDIR="$(readlink -f $(dirname "$0"))"
LFILE=$(readlink -f $FILE)
BFILE=$(basename "$FILE")

### FETCH FROM REMOTE SITE
if [[ $FILE =~ ://.*\.txt ]]; then
  cd $WORKDIR
  FILE=$BFILE
  echo "###: WGET $FILE"
  wget -O "$FILE" "http://ipcountry.ts.si/$FILE"
fi

[ ! -f "$FILE" ] && die "ERROR: $FILE DOESNT EXIST"

### FLUSH EXISTING IPSET OR CREATE NEW IF DOESNT EXIST
SETNAME="${FILE%.*}"
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
for pool in $(cat $FILE); do
  ipset add $SETNAME $pool
done 


echo "###: IPSET SAVE $SETNAME"
### SAVE FOR REBOOT
ipset save > /etc/ipset.conf 

