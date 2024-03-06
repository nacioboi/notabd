# Windows development Instructions and Notes

## Windows must be tested natively sometimes

And this is fine, but only use native windows when absolutely necessary.

---

## Install WSL2

If you do not require to test code on native windows, you can use WSL2 to run a linux environment on your windows machine.

> This eases and simplifies the development process.

### You may enjoy the Windows Terminal

>The Windows Terminal is a modern, fast, efficient, powerful, and productive terminal application for users of command-line tools and shells like Command Prompt, PowerShell, and WSL.

If you would like to install you can find it in the Microsoft Store.

### Actually installing WSL2

Using the following command in a powershell terminal:

```powershell
wsl --install
```

After this you must reboot your machine.

### Install a Linux Distribution

You can install a linux distribution from the Microsoft Store.

I like Arch Linux, but you can choose any distribution you like.
**ALSO NOTE: I will only be covering how to install Visual Studio Code on Arch Linux WSL.**

For e.g.,

- Ubuntu
- Debian
- Kali Linux
- OpenSUSE

and others are to choose from.

---

## Once you have WSL2 installed

You can use a command to launch the WSL2 terminal.

```powershell
wsl
```

Or, for Windows Terminal, you can just click the new tab dropdown and select your linux distribution.

---

## Install the necessary packages

- `rsync` - An extremely handy file synchronization tool.

  - On Ubuntu/Debian/Kali `sudo apt update && sudo apt install -y rsync`.
  - On Arch Linux `sudo pacman -Sy rsync`.

- `git` - The version control system.

  - On Ubuntu/Debian/Kali `sudo apt update && sudo apt install -y git`.
  - On Arch Linux `sudo pacman -Sy git`.

- `python` (version 3.11) - The programming language.

  - On Ubuntu/Debian/Kali `sudo apt update && sudo apt install -y python3.11`.
  - On Arch Linux `sudo pacman -Sy python` (NOTE: May not install 3.11).

---

## Using WSL2 inside Visual Studio Code

Launch vscode **ON NATIVE WINDOWS** and install the `Remote - WSL` extension.

Then you can just open a WSL2 terminal and type any linux command you need.

---

## Syncing sub-projects for the example codes

Make sure your using WSL2 terminal inside vscode.

```bash
chmod +x ./rsync_for_examples.sh ; ./rsync_for_examples.sh
```
