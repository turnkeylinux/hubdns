#!/bin/bash -e

# random sleep (max 5 min) to prevent clients from hitting the hub at the same time
SLEEP=$[ ($RANDOM % 3600) ] && sleep $SLEEP

hubdns-update --quiet
