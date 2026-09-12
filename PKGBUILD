# Maintainer: Evohl <evohl@evilneverdies.de>

pkgname=vr-video-player-gui
pkgver=0.1.0
pkgrel=3
pkgdesc="Native Qt6 launcher for vr-video-player"
arch=('any')
url="https://github.com/Evohl/vr-video-player-gui"
license=('MIT')
depends=('python' 'pyside6' 'vr-video-player')
source=('vrplayer_gui.py'
        'vr-video-player-gui.desktop'
    'vr-video-player-gui.svg'
        'LICENSE')
sha256sums=('SKIP'
            'SKIP'
        'SKIP'
            'SKIP')

package() {
    install -Dm755 "${srcdir}/vrplayer_gui.py" "${pkgdir}/usr/bin/${pkgname}"
    install -Dm644 "${srcdir}/${pkgname}.desktop" "${pkgdir}/usr/share/applications/${pkgname}.desktop"
    install -Dm644 "${srcdir}/${pkgname}.svg" "${pkgdir}/usr/share/icons/hicolor/scalable/apps/${pkgname}.svg"
    install -Dm644 "${srcdir}/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}