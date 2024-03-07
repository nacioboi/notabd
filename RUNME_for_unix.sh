# Run this file in order to test the project using our custom `proj_tester` suite of tools.

# Make sure that the venv exists
ensure_venv() {
	if [ ! -d "venv" ]; then
		echo "Creating virtual environment..."
		python3 -m venv venv
		bash -c "source venv/bin/activate && pip install pyqt5"
	else
		echo "Virtual environment already exists."
		echo "Would you like to reinstall? (y/N)"
		read -n 1
		if [[ $REPLY =~ ^[Yy]$ ]]; then
			echo "Reinstalling virtual environment..."
			rm -rf venv
			ensure_venv
		else
			echo "Skipping virtual environment reinstallation."
		fi
	fi
}

ensure_venv

# Run the `__project_runner.py`
echo -e "\n\n\n"
echo "In order to use pyqt5 on unix, you should select the platform plugin you would like to use with pyqt5."
echo
echo "Available platform plugins are:"
echo "[0] NONE - Let pyqt5 decide the platform plugin to use. [Default],"
echo "[1] eglfs,"
echo "[2] linuxfb,"
echo "[3] minimal,"
echo "[4] minimalegl,"
echo "[5] offscreen,"
echo "[6] vnc,"
echo "[7] wayland-egl,"
echo "[8] wayland,"
echo "[9] wayland-xcomposite-egl,"
echo "[10] wayland-xcomposite-glx,"
echo "[11] webglxcb."

read -p "Enter the number of the graphics environment you would like to use: " env_num
platform=""

case $env_num in
	0)
		platform="NONE"
		;;
	1)
		platform="eglfs"
		;;
	2)
		platform="linuxfb"
		;;
	3)
		platform="minimal"
		;;
	4)
		platform="minimalegl"
		;;
	5)
		platform="offscreen"
		;;
	6)
		platform="vnc"
		;;
	7)
		platform="wayland-egl"
		;;
	8)
		platform="wayland"
		;;
	9)
		platform="wayland-xcomposite-egl"
		;;
	10)
		platform="wayland-xcomposite-glx"
		;;
	11)
		platform="webglxcb"
		;;
	*)
		platform="NONE"
		;;
esac

cmd="source venv/bin/activate && cd proj_tester && python ./proj_tester.py"

if [[ $platform != "NONE" ]]; then
	echo "Selected platform: $platform..."
	cmd="$cmd -platform $platform"
fi
	
bash -c "$cmd"

