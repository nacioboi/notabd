#!/bin/bash 

PROC_IDS=()
DIRS_TO_CLEAN=()

rsync_proc() {
	while true; do
		# The -avz flag is a combination of flags that preserves the permissions, timestamps, and owner of the files,
		#   and compresses the data as it is transferred.
		rsync -avz $1 $2 >/dev/null &
		sleep 0.2
	done
}

start_rsync() {
	echo "Syncing $1 to $3..."
	rsync_proc $1 $2 &
	PROC_IDS+=($!)
	DIRS_TO_CLEAN+=($3)
}

# For the chat_app example.
start_rsync ../src/supersocket ../example/chat_app/ ../example/chat_app/supersocket
start_rsync ../src/outvar ../example/chat_app/ ../example/chat_app/outvar
start_rsync ../src/pls ../example/chat_app/ ../example/chat_app/pls

# For the injecting exmaple.
start_rsync ../src/pls ../example/injecting/ ../example/injecting/pls

# IPC for the kill script.
for PID in "${PROC_IDS[@]}"; do
	echo $PID >> _rsync_for_examples_state_pids.txt
done
for DIR in "${DIRS_TO_CLEAN[@]}"; do
	echo $DIR >> _rsync_for_examples_state_dirs.txt
done
