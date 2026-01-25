#!/bin/bash

run_attack() {
    echo "[*] Running attack: $1"
    ./$1
}

# check if any arguments have been provided
if [ $# -eq 0 ]; then
    echo "[*] No arguments provided, running all attacks..."
    run_attack "attacks/brute_force.sh"
    run_attack "attacks/lfi.sh"
    run_attack "attacks/scan.sh"
    run_attack "attacks/sqli.sh"
else
    # iterating over arguments
    for arg in "$@"; do
        case $arg in
            --brute)
                run_attack "/attacks/brute_force.sh"
                ;;
            --lfi)
                run_attack "attacks/lfi.sh"
                ;;
            --scan)
                run_attack "attacks/scan.sh"
                ;;
            --sqli)
                run_attack "attacks/sqli.sh"
                ;;
            *)
                echo "[!] Unknown flag: $arg"
                echo "[*] Usage: $0 [--brute] [--lfi] [--scan] [--sqli]"
                exit 1
                ;;
        esac
    done
fi


echo "[V] Attack simulation complete."
