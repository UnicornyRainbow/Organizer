# [Organizer](https://unicornyrainbow.github.io/Organizer)

Thank you for installing Secrets! Currently you can only build it from source, since I haven't published a release yet.<!--There are multiple ways to install it:-->

<!-- ## Graphical
Go to the [latest release](https://github.com/UnicornyRainbow/Organizer/releases/latest) and download the correct file for your cpu architecture (if you are not sure, give organizer.flatpak a try).\
Then open the file in your file manager and double click it, it should open your graphical package manager /software store, then click on install.

## Command Line
Download it with
* `wget https://github.com/UnicornyRainbow/Organizer/releases/latest/download/organizer.flatpak` for x86
* `wget https://github.com/UnicornyRainbow/Organizer/releases/latest/download/organizer_aarch.flatpak` for aarch
then install it
* `sudo flatpak install organizer.flatpak` or
* `sudo flatpak install organizer_aarch.flatpak`
-->
## Build it on your own
<!-- Download the the source code from the [latest release](https://github.com/UnicornyRainbow/Organizer/releases/latest), then unpack it and open a terminal in the folder.\
To always have the most current (maybe not stable) version, run `git clone https://github.com/UnicornyRainbow/Organizer`, then `cd Organizer`.
-->
Now that you have a terminal opened in the folder with source code, make the build script executable `chmod +x flatpak_build.sh`, then run it `./flatpak_build.sh`.
It builds a .flatpak file you can distribute and also installs it on your system.
