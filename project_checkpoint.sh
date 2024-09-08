#!/bin/bash

while true; do
  # Get the current timestamp
  timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  
  # Add and commit changes with the timestamp in the commit message
  git add .
  git commit -m "Automated project checkpoint commit at $timestamp"
  git push
  
  # Echo a message with the timestamp
  echo "### ### ### ### ### ### ### ### ### ### ### ###   Checkpoint finished at $timestamp   ### ### ### ### ### ### ### ### ### ### ### ###"
  
  # Wait for 10 minutes (600 seconds) before repeating
  sleep 600
done