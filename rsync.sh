echo -e "This shell script will rsync from \`src/{infoinject,outvar,ptysocker,supersocket}\` to \`src/examples/*\`.\n\n"

# First, make sure we in the right directory.
ls | grep -q src || { echo "You must run this script from the root of the repository"; exit 1; }

# Then make a backup of the root of the repository.
echo "] Making a backup of the root of the repository..."
cp -r . ../backup

# Then make the dirs.
mkdir -p ../examples/*/{infoinject,outvar,ptysocker,supersocket}


ask_rm() {
	echo "Can I remove $1? (y/n)"
	read -r
	[[ $REPLY == [yY] ]] && rm -rf "$1"
}

on_exit() {
	# Make sure we in the right directory.
	ls | grep -q src || { echo "You must run this script from the root of the repository"; exit 1; }

	# Then remove the dirs.
	echo "Removing the dirs"

	ask_rm ../examples/*/infoinject/
	ask_rm ../examples/*/outvar/
	ask_rm ../examples/*/ptysocker/
	ask_rm ../examples/*/supersocket/
}

trap "on_exit" EXIT
# Then rsync the files.
echo "Rsyncing the files"
rsync -av src/infoinject/ ../examples/*/infoinject/
rsync -av src/outvar/ ../examples/*/outvar/
rsync -av src/ptysocker/ ../examples/*/ptysocker/
rsync -av src/supersocket/ ../examples/*/supersocket/

# Then make sure we set a trap to remove the dirs.
echo "Setting a trap to remove the dirs"