@echo off

REM TODO: INSTEAD OF DIRECTLY PUTTING COMMANDS IN THE `proj_tester.py` FILE, WE CAN PUT THEM IN A SEPARATE FILE AND THEN CALL THAT FILE FROM THE `proj_tester.py` FILE. THIS WILL MAKE THE `proj_tester.py` FILE CLEANER AND EASIER TO READ.
REM also, i have been running into issues with the `proj_tester.py` file, so i will try to use a separate file to run the commands and see if that works better.

set path_of_chat_app_subroutines=%1%
set path_of_launch_ps1=\launch_client.ps1
set path_of_launch_ps1=%path_of_chat_app_subroutines%%path_of_launch_ps1%

set path_of_proj_in_wsl=%2%
set path_of_proj_in_windows=%3%
set args_for_ps1=%path_of_proj_in_wsl% %path_of_proj_in_windows%

set path_of_ps=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe


%path_of_ps% -NoProfile -ExecutionPolicy Bypass -Command "& %path_of_launch_ps1% %args_for_ps1% ; exit"