#!/bin/bash

# helper script for generating random IP

generate_ip(){
    local IP=$1
    if [[ -z "$IP" ]]; then
        OCT1=$((RANDOM % 256))
        OCT2=$((RANDOM % 256))
        OCT3=$((RANDOM % 256))
        OCT4=$((RANDOM % 256))
        IP="$OCT1.$OCT2.$OCT3.$OCT4"
    fi
    echo "$IP"
}