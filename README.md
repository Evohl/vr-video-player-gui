# VR Video Player GUI

Eine kleine native Qt6-GUI fuer `vr-video-player` unter Linux.

Autor: Evohl <evohl@evilneverdies.de>

## Starten

```bash
python3 vrplayer_gui.py
```

Die Anwendung waehlt ein Video aus, erstellt den passenden `vr-video-player`-Befehl und startet ihn. Sie verwendet den Systemstil der installierten Qt-Desktop-Umgebung und speichert die zuletzt verwendeten Optionen. `PySide6` sowie `vr-video-player` muessen im `PATH` installiert sein.

## Arch Linux und Startmenue

Ein Arch-Paketrezept (`PKGBUILD`) und ein Startmenueeintrag (`vr-video-player-gui.desktop`) liegen im Projektstamm. Fuer eine lokale Installation:

```bash
makepkg -si
```

Danach erscheint **VR Video Player GUI** im Anwendungsmenue und ist auch mit folgendem Befehl startbar:

```bash
vr-video-player-gui
```

Fuer eine Veroeffentlichung im AUR wird ein oeffentliches Git-Repository mit diesen Quelldateien benoetigt. Vor dem Upload muss im `PKGBUILD` die `url` durch die Repository-URL ersetzt und `pkgver` bei Releases aktualisiert werden. Anschliessend werden `PKGBUILD`, `vrplayer_gui.py` und `vr-video-player-gui.desktop` in das namensgleiche AUR-Git-Repository gepusht.

## Optionaler Starter

```bash
chmod +x vrplayer_gui.py
./vrplayer_gui.py
```