# IPCOUNTRY

## What is it?
Block or allow IP ranges from specific country and never deal with updating ACL manually :)

Scripts will create `ipset` / `iptables` access lists based on country, ipv4/ipv6 or asn. ACL is periodically updated with `cronjob`. See examples below.

## Idea
It all started when I landed on this site
http://www-public.imtbs-tsp.eu/~maigron/RIR_Stats/index.html

So I wrote parser for some files on ftp.ripe.net which extracts data and creates large amount of .txt. Each files contains IP address pools for specific country, operator and ip address family.
There are three variants of output files. Lets see some examples:
```
...
SI/ipv4.txt
DE/ipv4.txt
AT/ipv4.txt
CZ/ipv4.txt
...
SI/ipv6.txt
DE/ipv6.txt
AT/ipv6.txt
CZ/ipv6.txt
...

```
the files above contain IP address space per country code.

The second format contains country code and operator name:
```
...
SI/a1/ipv4.txt
SI/a1/ipv6.txt
SI/arnes/ipv4.txt
SI/arnes/ipv6.txt
SI/telekom/ipv4.txt
SI/telekom/ipv6.txt
SI/mobitel/ipv4.txt
SI/mobitel/ipv6.txt
...

```

Third variant are ASN files:
```
...
asn/5603/ipv4.txt
asn/5603/ipv6.txt
asn/29276/ipv4.txt
asn/29276/ipv6.txt
...
```

## Installation
Extract files to /opt/ipcountry for example.

Create cronjob

```
5 0 * * * /opt/ipcountry/ripencc-parser.sh > /dev/null 2>&1
```

Or run manually to fetch files from ftp.ripe.net and create output files

```
/opt/ipcountry/ripencc-parser.sh
```

## ipset cronjob
Create ipset for desired country and address family
```
15 0 * * * /opt/ipcountry/make-ipset.sh /opt/ipcountry/SI/ipv4.txt SI-ipv4 > /opt/ipcountry/make-ipset.sh.log4 2>&1
15 0 * * * /opt/ipcountry/make-ipset.sh /opt/ipcountry/SI/ipv6.txt SI-ipv6 > /opt/ipcountry/make-ipset.sh.log6 2>&1
```

You can also fetch files from remote site
```
15 0 * * * /opt/ipcountry/make-ipset.sh https://yourserver/SI/ipv4.txt SI-ipv4
15 0 * * * /opt/ipcountry/make-ipset.sh https://yourserver/SI/ipv6.txt SI-ipv6
```

## iptables

Update your iptables rules 

```
-A INPUT -p tcp -m set --match-set SI-ipv4 src -m tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
-A INPUT -p tcp -m set --match-set SI-ipv4 src -m tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j DROP
-A INPUT -p tcp -m tcp --dport 443 -j DROP
```

## Disclaimer
Use at your own risk.

## Coffee
If you find this useful you can buy me a coffee :) https://ko-fi.com/markor
