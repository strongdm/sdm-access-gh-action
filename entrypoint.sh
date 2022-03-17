#!/bin/bash

echo "Checking pending requests..."
git checkout main
git pull
git diff --name-only HEAD HEAD^ | while read line; do 
    resource_name=$(echo $line | awk '/^resources/ { gsub("resources/", "", $0); print $0 }')
    if [ "$resource_name" != "" ]; then
        raw_user_email=$(git log -p -- $line | grep Author | head -1)
        user_email=$(echo $raw_user_email | awk 'match($0, /<.*>/) { print substr($0, RSTART+1, RLENGTH-2) }')
        echo "About to grant temporary access to $user_email on $resource_name"
        python3 main.py $resource_name $user_email
    fi
done
