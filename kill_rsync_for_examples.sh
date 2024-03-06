#!/bin/bash

PROC_IDS=()
DIRS_TO_CLEAN=()

# Load the process IDs and directories to clean.
for PID in $(cat _rsync_for_examples_state_pids.txt); do
	PROC_IDS+=($PID)
done
for DIR in $(cat _rsync_for_examples_state_dirs.txt); do
	DIRS_TO_CLEAN+=($DIR)
done


# Kill all processes and clean all directories.
for PROC_ID in "${PROC_IDS[@]}"; do
	echo "Killing process $PROC_ID..."
	kill $PROC_ID
done
for DIR_TO_CLEAN in "${DIRS_TO_CLEAN[@]}"; do
	echo "Cleaning directory $DIR_TO_CLEAN..."
	rm -rf $DIR_TO_CLEAN
done
echo "All processes killed and directories cleaned."

rm _rsync_for_examples_pid.txt
rm _rsync_for_examples_state_pids.txt
rm _rsync_for_examples_state_dirs.txt

echo "Cleaned up pid and dir files."