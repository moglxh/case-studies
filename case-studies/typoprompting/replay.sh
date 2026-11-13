#!/bin/bash
# usage: bash replay.sh <name>
name="$1"
echo "1) DNS lookup for $name.lab.test"
ip=$(dig @127.0.0.1 "$name.lab.test" +short)
if [ -z "$ip" ]; then
    echo "   no answer (NXDOMAIN) - the victim never connects"
    exit 0
fi
echo "   answer: $ip"
echo "2) Connect and request the page"
curl -sL -H "Host: $name.lab.test" "http://$ip:8080/"
