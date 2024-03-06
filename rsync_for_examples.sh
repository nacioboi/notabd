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

stop_all_procs() {
	for PROC_ID in "${PROC_IDS[@]}"; do
		echo "Killing process $PROC_ID..."
		kill $PROC_ID
	done
	for DIR_TO_CLEAN in "${DIRS_TO_CLEAN[@]}"; do
		echo "Cleaning directory $DIR_TO_CLEAN..."
		rm -rf $DIR_TO_CLEAN
	done
	echo "All processes killed and directories cleaned."
}

trap stop_all_procs EXIT

# For the chat_app example.
start_rsync ./src/supersocket ./example/chat_app/ ./example/chat_app/supersocket
start_rsync ./src/outvar ./example/chat_app/ ./example/chat_app/outvar
start_rsync ./src/pls ./example/chat_app/ ./example/chat_app/pls

# For the injecting exmaple.
start_rsync ./src/pls ./example/injecting/ ./example/injecting/pls

echo ""
echo ""
echo "Press any key to stop the rsync processes..."
read -n 1 -s
