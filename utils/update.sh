#!/bin/bash

wget https://github.com/Osb0rn3/bugbounty-targets/raw/main/programs/$1.json -q -P platforms -O platforms/$1.json
