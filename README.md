# IPCOUNTRY

## Idea
It all started when I landed on this site
http://www-public.imtbs-tsp.eu/~maigron/RIR_Stats/index.html

So I wrote parser for some files on ftp.ripe.net which extracts data and creates large amount of .txt. Each files contains IP address pools for specific country, operator and ip address family.
There are two variants of output files. Lets see some examples:
```
...
SI-ipv4.txt
DE-ipv4.txt
AT-ipv4.txt
CZ-ipv4.txt
...
SI-ipv6.txt
DE-ipv6.txt
AT-ipv6.txt
CZ-ipv6.txt
...

```
the files above contain IP address space per country code.

The other format contains country code and operator name:
```
...
si.a1.ipv4.txt
si.a1.ipv6.txt
si.arnes.ipv4.txt
si.arnes.ipv6.txt
si.telekom.ipv4.txt
si.telekom.ipv6.txt
si.mobitel.ipv4.txt
si.mobitel.ipv6.txt
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
15 0 * * * /opt/ipcountry/make-ipset.sh /opt/ipcountry/SI-ipv4.txt > /opt/ipcountry/make-ipset.sh.log4 2>&1
15 0 * * * /opt/ipcountry/make-ipset.sh /opt/ipcountry/SI-ipv6.txt > /opt/ipcountry/make-ipset.sh.log6 2>&1
```

You can also fetch files from remote site
```
15 0 * * * /opt/ipcountry/make-ipset.sh https://yourserver/SI-ipv4.txt
15 0 * * * /opt/ipcountry/make-ipset.sh https://yourserver/SI-ipv6.txt
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
