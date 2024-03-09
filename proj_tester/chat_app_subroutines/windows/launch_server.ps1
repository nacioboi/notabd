# TODO: INSTEAD OF DIRECTLY PUTTING COMMANDS IN THE `proj_tester.py` FILE, WE CAN PUT THEM IN A SEPARATE FILE AND THEN CALL THAT FILE FROM THE `proj_tester.py` FILE. THIS WILL MAKE THE `proj_tester.py` FILE CLEANER AND EASIER TO READ.
# also, i have been running into issues with the `proj_tester.py` file, so i will try to use a separate file to run the commands and see if that works better.

param (
	[string]$PathOfProjInWSL,
	[string]$PathOfProjInWindows
)

$PathOfWSL = (Get-Command wsl).Source
$PathOfPython = (Get-Command python).Source

function Start-Command {
	param (
		$Prog,
		$Arguments
	)
	Start-Process -NoNewWindow -Wait -FilePath $Prog -ArgumentList $Arguments
}

Start-Command -Prog $PathOfWSL -Arguments "-d Arch bash -c 'cd $PathOfProjInWSL && ./rsync_for_examples.sh'"
Start-Command -Prog $PathOfPython -Arguments "$PathOfProjInWindows\\example\\chat_app\\server.py"
Start-Command -Prog $PathOfWSL -Arguments "-d Arch bash -c 'cd $PathOfProjInWSL && ./kill_rsync_for_examples.sh'"
	