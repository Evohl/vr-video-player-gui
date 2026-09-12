# VR Video Player GUI

A small native Qt6 GUI for `vr-video-player` on Linux.

Author: Evohl <evohl@evilneverdies.de>

The application lets you select videos, builds the appropriate `vr-video-player` command, and starts playback. The interface supports German, English, Spanish, and Italian; English is used for all other system languages.

## Features

- Responsive folder scanning in a background thread, with videos added to the list in batches while the scan is still running
- Asynchronous duration metadata loading through `ffprobe`, so large folders remain usable while durations appear progressively
- Alphabetically sorted video list with the selected file and generated `vr-video-player` command shown in the interface
- 180-degree, 360-degree, flat stereo, and virtual screen viewing modes
- Stereo direction, image stretching, zoom, cursor scale, cursor wrapping, free camera, and flicker-reduction controls
- Selectable mpv profiles and optional use of the system mpv configuration
- Sequential or random autoplay after successful playback
- Start and stop lifecycle handling that prevents another video from being launched before the current player process has exited
- Persistent window position, window size, video folder, and playback settings
- Built-in player log for standard output and error messages

## Installation on Arch Linux

### 1. Install the prerequisites

The `base-devel` package and Git are required to build the package:

```bash
sudo pacman -S --needed base-devel git
```

A working SteamVR installation is also required.

### 2. Install vr-video-player

The GUI uses [vr-video-player](https://aur.archlinux.org/packages/vr-video-player) for VR playback. Install the dependency with an AUR helper such as `yay`:

```bash
yay -S vr-video-player
```

Without an AUR helper, the package can be built and installed manually:

```bash
git clone https://aur.archlinux.org/vr-video-player.git
cd vr-video-player
makepkg -si
cd ..
```

Additional information, particularly about SteamVR, is available on the [upstream project page](https://git.dec05eba.com/vr-video-player/about/).

### 3. Install VR Video Player GUI

Clone the GUI repository and install the included Arch package:

```bash
git clone https://github.com/Evohl/vr-video-player-gui.git
cd vr-video-player-gui
makepkg -si
```

`makepkg` installs the other required packages, including Python, [PySide6](https://archlinux.org/packages/extra/x86_64/pyside6/), and FFmpeg, via `pacman`.

## Launching the application

After installation, launch **VR Video Player GUI** from the application menu or a terminal:

```bash
vr-video-player-gui
```

## Updating

In the cloned project directory, pull the latest changes and rebuild the package:

```bash
git pull
makepkg -si
```

## Running without installation

For development or a quick test, run the GUI directly from the project directory:

```bash
python3 vrplayer_gui.py
```

Alternatively, make the script executable and run it directly:

```bash
chmod +x vrplayer_gui.py
./vrplayer_gui.py
```