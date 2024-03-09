# Run this file in order to test the project using our custom `proj_tester` suite of tools.

# Windows just needs for the libs to be globally installed via pip...
$out = pip show pyqt5

if ($out -eq "") {
    pip install pyqt5
}

Set-Location proj_tester
python ./proj_tester.py
