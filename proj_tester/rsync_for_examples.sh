#!/bin/bash

# Only run if we are in the proj_tester directory.
[[ ! -f rsync_for_examples.sh ]] && echo "rsync_for_examples.sh: ERROR: NOT IN THE CORRECT DIR. EXITING..." && exit 1

echo hi

bash -c "cd $(pwd) && ./_rsync_for_examples.sh" &
PID=$!
sleep 2

echo -ne $PID > _rsync_for_examples_pid.txt
