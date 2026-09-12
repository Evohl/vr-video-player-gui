# VR Video Player GUI

Eine kleine native Qt6-GUI fuer `vr-video-player` unter Linux.

Autor: Evohl <evohl@evilneverdies.de>

Die Anwendung waehlt Videos aus, erstellt den passenden `vr-video-player`-Befehl und startet die Wiedergabe. Die Oberflaeche unterstuetzt Deutsch, Englisch, Spanisch und Italienisch; bei anderen Systemsprachen wird Englisch verwendet.

## Installation unter Arch Linux

### 1. Voraussetzungen installieren

Zum Bauen des Pakets werden `base-devel` und Git benoetigt:

```bash
sudo pacman -S --needed base-devel git
```

Ausserdem muss eine funktionierende SteamVR-Installation vorhanden sein.

### 2. vr-video-player installieren

Die GUI verwendet [vr-video-player](https://aur.archlinux.org/packages/vr-video-player) fuer die eigentliche VR-Wiedergabe. Mit einem AUR-Helfer wie `yay` wird die Abhaengigkeit so installiert:

```bash
yay -S vr-video-player
```

Ohne AUR-Helfer kann das Paket manuell gebaut und installiert werden:

```bash
git clone https://aur.archlinux.org/vr-video-player.git
cd vr-video-player
makepkg -si
cd ..
```

Weitere Hinweise, insbesondere zu SteamVR, stehen auf der [Upstream-Projektseite](https://git.dec05eba.com/vr-video-player/about/).

### 3. VR Video Player GUI installieren

Das Repository der GUI klonen und das enthaltene Arch-Paket installieren:

```bash
git clone https://github.com/Evohl/vr-video-player-gui.git
cd vr-video-player-gui
makepkg -si
```

`makepkg` installiert die weiteren benoetigten Pakete wie Python, [PySide6](https://archlinux.org/packages/extra/x86_64/pyside6/) und FFmpeg ueber `pacman`.

## Anwendung starten

Nach der Installation kann **VR Video Player GUI** ueber das Anwendungsmenue oder im Terminal gestartet werden:

```bash
vr-video-player-gui
```

## Aktualisieren

Im geklonten Projektverzeichnis die neuesten Aenderungen laden und das Paket neu bauen:

```bash
git pull
makepkg -si
```

## Ohne Installation ausfuehren

Fuer Entwicklung oder einen kurzen Test kann die GUI direkt aus dem Projektverzeichnis gestartet werden:

```bash
python3 vrplayer_gui.py
```

Alternativ ist das Skript direkt ausfuehrbar:

```bash
chmod +x vrplayer_gui.py
./vrplayer_gui.py
```