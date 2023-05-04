#!/bin/bash

program=$(cat platforms/hackerone.json|jq '.[].attributes.name'|grep -w "$1")
if [[ "$program" == "\"$1\"" ]];then
    wget https://github.com/Osb0rn3/bugbounty-targets/raw/main/programs/hackerone.json -q -P platforms -O platforms/hackerone.json
    index0=$(cat platforms/hackerone.json|jq '.[].attributes.name'|grep -nw "$1"|awk 'BEGIN { FS = ":" } ; { print $1 }')
    index=$(expr $index0 - 1)
    echo -n "$index,hackerone"
fi
program=$(cat platforms/bugcrowd.json|jq '.[].name'|grep -w "$1")
if [[ "$program"  == "\"$1\"" ]];then
    wget https://github.com/Osb0rn3/bugbounty-targets/raw/main/programs/bugcrowd.json -q -P platforms -O platforms/bugcrowd.json
    index0=$(cat platforms/bugcrowd.json|jq '.[].name'|grep -nw "$1"|awk 'BEGIN { FS = ":" } ; { print $1 }')
    index=$(expr $index0 - 1)
    echo -n "$index,bugcrowd"

fi
program=$(cat platforms/intigriti.json|jq '.[].name'|grep -w "$1")
if [[ $program == "\"$1\"" ]];then
    wget https://github.com/Osb0rn3/bugbounty-targets/raw/main/programs/intigriti.json -q -P platforms -O platforms/intigriti.json
    index0=$(cat platforms/intigriti.json|jq '.[].name'|grep -nw "$1"|awk 'BEGIN { FS = ":" } ; { print $1 }')
    index=$(expr $index0 - 1)
    echo -n "$index,intigriti"
fi
program=$(cat platforms/yeswehack.json|jq '.[].title'|grep -w "$1")
if [[ "$program" == "\"$1\"" ]];then
    wget https://github.com/Osb0rn3/bugbounty-targets/raw/main/programs/yeswehack.json -q -P platforms -O platforms/yeswehack.json
    index0=$(cat platforms/yeswehack.json|jq '.[].title'|grep -nw "$1"|awk 'BEGIN { FS = ":" } ; { print $1 }')
    index=$(expr $index0 - 1)
    echo -n "$index,yeswehack"
fi
