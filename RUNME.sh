# Make sure that the venv exists
ensure_venv() {
	if [ ! -d "venv" ]; then
		echo "Creating virtual environment..."
		python3 -m venv venv
		bash -c "source venv/bin/activate && pip install -r requirements.txt"
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
bash -c "source venv/bin/activate && python __project_runner.py -platform wayland"
