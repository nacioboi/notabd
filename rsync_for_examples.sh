#!/bin/bash

bash _rsync_for_examples.sh &
PID=$!
sleep 2

echo -ne $PID > _rsync_for_examples_pid.txt
