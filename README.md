# IPCOUNTRY

## Idea
It all started when I landed on this site
http://www-public.imtbs-tsp.eu/~maigron/RIR_Stats/index.html

## Installation
Extract files to /opt/ipcountry for example.

Create cronjob

```
5 0 * * * /opt/ipcountry/ripencc-parser.sh > /dev/null 2>&1
```

Or run manually to fetch file from ftp.ripe.net and create output files

```
/opt/ipcountry/ripencc-parser.sh
```

## IPSET
Create ipsets for desired country and address family
```
/opt/ipcountry/make-ipset.sh /opt/ipcountry/SI-ipv4.txt
/opt/ipcountry/make-ipset.sh /opt/ipcountry/SI-ipv6.txt
```

Update your iptables rules 

```
-A INPUT -p tcp -m set --match-set SI-ipv4 src -m tcp --dport 80 -m conntrack --ctstate NEW -j ACCEPT
-A INPUT -p tcp -m set --match-set SI-ipv4 src -m tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j DROP
-A INPUT -p tcp -m tcp --dport 443 -j DROP
```
