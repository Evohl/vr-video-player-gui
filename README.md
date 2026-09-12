# VR Video Player GUI

Eine kleine native Qt6-GUI fuer `vr-video-player` unter Linux.

Autor: Evohl <evohl@evilneverdies.de>

## Voraussetzungen

- Python 3 mit [PySide6](https://archlinux.org/packages/extra/x86_64/pyside6/)
- [vr-video-player im AUR](https://aur.archlinux.org/packages/vr-video-player)
- Eine funktionierende SteamVR-Installation

Unter Arch Linux kann `vr-video-player` beispielsweise mit einem AUR-Helfer installiert werden:

```bash
yay -S vr-video-player
```

Alternativ kann das AUR-Paket manuell gebaut werden:

```bash
git clone https://aur.archlinux.org/vr-video-player.git
cd vr-video-player
makepkg -si
```

Weitere Informationen zur Einrichtung und Bedienung stehen auf der
[Upstream-Projektseite](https://git.dec05eba.com/vr-video-player/about/).

## Starten

```bash
python3 vrplayer_gui.py
```

Die Anwendung waehlt ein Video aus, erstellt den passenden `vr-video-player`-Befehl und startet ihn. Sie verwendet den Systemstil der installierten Qt-Desktop-Umgebung und speichert die zuletzt verwendeten Optionen. Das Python-Modul `PySide6` muss installiert und `vr-video-player` muss im `PATH` verfuegbar sein.

Die Oberflaeche richtet sich nach der Systemsprache: Deutsch, Englisch, Spanisch und Italienisch werden direkt unterstuetzt; alle anderen Sprachen verwenden Englisch.

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