#!/usr/bin/env python3
"""A native Qt6 launcher for vr-video-player on Linux."""

from __future__ import annotations

import shlex
import shutil
import random
from pathlib import Path

from PySide6.QtCore import QProcess, QSettings, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QButtonGroup, QCheckBox, QComboBox, QDoubleSpinBox,
    QFileDialog, QFormLayout, QFrame, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QRadioButton,
    QVBoxLayout, QWidget,
)


class VrPlayerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings("VR Video Player", "VR Video Player GUI")
        self.player_process = QProcess(self)
        self.player_process.finished.connect(self._on_player_finished)
        self.player_process.errorOccurred.connect(self._on_player_error)
        self.setWindowTitle("VR Video Player")
        self.setMinimumWidth(650)
        self._build_ui()
        self._restore_settings()
        self._update_mode_controls()
        self._update_preview()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel("VR Video Player")
        title_font = title.font()
        title_font.setPointSize(title_font.pointSize() + 6)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        layout.addWidget(QLabel("Video auswaehlen und direkt in VR oeffnen"))

        source_group = QGroupBox("Video-Ordner")
        source_layout = QHBoxLayout(source_group)
        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("Ordner mit Videos auswaehlen")
        self.folder_path.setReadOnly(True)
        source_layout.addWidget(self.folder_path)
        choose_button = QPushButton("Ordner waehlen...")
        choose_button.clicked.connect(self._choose_folder)
        source_layout.addWidget(choose_button)
        layout.addWidget(source_group)

        video_group = QGroupBox("Videos")
        video_layout = QVBoxLayout(video_group)
        self.video_list = QListWidget()
        self.video_list.setMinimumHeight(180)
        self.video_list.setAlternatingRowColors(True)
        self.video_list.currentItemChanged.connect(self._select_video)
        self.video_list.itemDoubleClicked.connect(lambda _item: self._launch())
        video_layout.addWidget(self.video_list)
        self.video_path = QLineEdit()
        self.video_path.setPlaceholderText("Kein Video ausgewaehlt")
        self.video_path.setReadOnly(True)
        self.video_path.textChanged.connect(self._update_preview)
        video_layout.addWidget(self.video_path)
        layout.addWidget(video_group)

        view_group = QGroupBox("Darstellung")
        view_layout = QVBoxLayout(view_group)
        modes_layout = QHBoxLayout()
        self.mode_group = QButtonGroup(self)
        self.mode_buttons: dict[str, QRadioButton] = {}
        for label, mode in (("180 Grad", "sphere"), ("360 Grad", "sphere360"), ("Stereo flach", "flat"), ("Leinwand", "plane")):
            button = QRadioButton(label)
            self.mode_group.addButton(button)
            self.mode_buttons[mode] = button
            modes_layout.addWidget(button)
        self.mode_buttons["sphere"].setChecked(True)
        self.mode_group.buttonClicked.connect(self._update_mode_controls)
        view_layout.addLayout(modes_layout)

        self.stereo_options = QFrame()
        stereo_layout = QHBoxLayout(self.stereo_options)
        stereo_layout.setContentsMargins(0, 0, 0, 0)
        self.left_right = QRadioButton("Links nach rechts")
        self.right_left = QRadioButton("Rechts nach links")
        self.left_right.setChecked(True)
        self.stereo_group = QButtonGroup(self)
        self.stereo_group.addButton(self.left_right)
        self.stereo_group.addButton(self.right_left)
        self.stretch = QCheckBox("Bild strecken")
        self.stretch.setChecked(True)
        stereo_layout.addWidget(self.left_right)
        stereo_layout.addWidget(self.right_left)
        stereo_layout.addStretch()
        stereo_layout.addWidget(self.stretch)
        view_layout.addWidget(self.stereo_options)
        layout.addWidget(view_group)

        options_group = QGroupBox("Optionen")
        options_layout = QFormLayout(options_group)
        self.zoom = self._number_input()
        self.cursor_scale = self._number_input()
        numeric_layout = QHBoxLayout()
        numeric_layout.addWidget(QLabel("Zoom"))
        numeric_layout.addWidget(self.zoom)
        numeric_layout.addSpacing(20)
        numeric_layout.addWidget(QLabel("Cursor-Groesse"))
        numeric_layout.addWidget(self.cursor_scale)
        options_layout.addRow(numeric_layout)
        self.cursor_wrap = QCheckBox("Cursor am Bildrand umschlagen")
        self.free_camera = QCheckBox("Freie Kamera")
        self.reduce_flicker = QCheckBox("Textflackern reduzieren")
        self.use_system_mpv_config = QCheckBox("Systemweite mpv-Konfiguration verwenden")
        for checkbox in (self.cursor_wrap, self.free_camera, self.reduce_flicker, self.use_system_mpv_config):
            options_layout.addRow(checkbox)
        self.mpv_profile = QComboBox()
        self.mpv_profile.addItems(("gpu-hq", "gpu-next", "fast"))
        options_layout.addRow("mpv-Profil:", self.mpv_profile)
        self.autoplay_mode = QComboBox()
        self.autoplay_mode.addItem("Aus", "off")
        self.autoplay_mode.addItem("Naechstes in Reihenfolge", "sequential")
        self.autoplay_mode.addItem("Zufaelliges Video", "random")
        options_layout.addRow("Nach Wiedergabe:", self.autoplay_mode)
        layout.addWidget(options_group)

        layout.addWidget(QLabel("Befehl"))
        self.command_preview = QLineEdit()
        self.command_preview.setReadOnly(True)
        layout.addWidget(self.command_preview)
        launch_layout = QHBoxLayout()
        launch_layout.addStretch()
        self.launch_button = QPushButton("In VR abspielen")
        self.launch_button.setDefault(True)
        self.launch_button.clicked.connect(self._launch)
        launch_layout.addWidget(self.launch_button)
        layout.addLayout(launch_layout)

        for button in (self.left_right, self.right_left, self.stretch):
            button.toggled.connect(self._update_preview)
        for widget in (self.zoom, self.cursor_scale):
            widget.valueChanged.connect(self._update_preview)
        for checkbox in (self.cursor_wrap, self.free_camera, self.reduce_flicker, self.use_system_mpv_config):
            checkbox.toggled.connect(self._update_preview)
        self.mpv_profile.currentTextChanged.connect(self._update_preview)

    @staticmethod
    def _number_input() -> QDoubleSpinBox:
        number_input = QDoubleSpinBox()
        number_input.setRange(0, 100)
        number_input.setDecimals(2)
        number_input.setSingleStep(0.1)
        number_input.setSpecialValueText("Standard")
        return number_input

    def _restore_settings(self) -> None:
        self.resize(self.settings.value("window_size", self.size()))
        self.move(self.settings.value("window_position", self.pos()))
        mode = self.settings.value("view_mode", "sphere")
        self.mode_buttons.get(mode, self.mode_buttons["sphere"]).setChecked(True)
        self.left_right.setChecked(self.settings.value("left_right", True, type=bool))
        self.stretch.setChecked(self.settings.value("stretch", True, type=bool))
        self.zoom.setValue(self.settings.value("zoom", 0.0, type=float))
        self.cursor_scale.setValue(self.settings.value("cursor_scale", 0.0, type=float))
        self.cursor_wrap.setChecked(self.settings.value("cursor_wrap", False, type=bool))
        self.free_camera.setChecked(self.settings.value("free_camera", False, type=bool))
        self.reduce_flicker.setChecked(self.settings.value("reduce_flicker", False, type=bool))
        self.use_system_mpv_config.setChecked(self.settings.value("use_system_mpv_config", False, type=bool))
        profile_index = self.mpv_profile.findText(self.settings.value("mpv_profile", "gpu-hq"))
        if profile_index >= 0:
            self.mpv_profile.setCurrentIndex(profile_index)
        autoplay_index = self.autoplay_mode.findData(self.settings.value("autoplay_mode", "off"))
        if autoplay_index >= 0:
            self.autoplay_mode.setCurrentIndex(autoplay_index)
        folder_path = self.settings.value("last_video_directory", "")
        if folder_path and Path(folder_path).is_dir():
            self._load_video_folder(Path(folder_path))

    def _selected_mode(self) -> str:
        return next(mode for mode, button in self.mode_buttons.items() if button.isChecked())

    def _build_command(self) -> list[str]:
        command = ["vr-video-player", f"--{self._selected_mode()}"]
        if self._selected_mode() == "flat":
            command.append("--left-right" if self.left_right.isChecked() else "--right-left")
            command.append("--stretch" if self.stretch.isChecked() else "--no-stretch")
        if self.zoom.value() > 0:
            command.extend(("--zoom", str(self.zoom.value())))
        if self.cursor_scale.value() > 0:
            command.extend(("--cursor-scale", str(self.cursor_scale.value())))
        if self.cursor_wrap.isChecked():
            command.append("--cursor-wrap")
        if self.free_camera.isChecked():
            command.append("--free-camera")
        if self.reduce_flicker.isChecked():
            command.append("--reduce-flicker")
        if self.use_system_mpv_config.isChecked():
            command.append("--use-system-mpv-config")
        return command + ["--mpv-profile", self.mpv_profile.currentText(), "--video", self.video_path.text().strip()]

    def _update_mode_controls(self) -> None:
        self.stereo_options.setEnabled(self._selected_mode() == "flat")
        self._update_preview()

    def _update_preview(self) -> None:
        self.command_preview.setText(shlex.join(self._build_command()))

    def _choose_folder(self) -> None:
        start_directory = self.settings.value("last_video_directory", str(Path.home()))
        folder_name = QFileDialog.getExistingDirectory(self, "Video-Ordner auswaehlen", start_directory)
        if folder_name:
            self._load_video_folder(Path(folder_name))

    def _load_video_folder(self, folder_path: Path) -> None:
        video_extensions = {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".webm"}
        video_paths = sorted(
            (path for path in folder_path.iterdir() if path.is_file() and path.suffix.lower() in video_extensions),
            key=lambda path: path.name.lower(),
        )
        self.folder_path.setText(str(folder_path))
        self.video_path.clear()
        self.video_list.clear()
        for path in video_paths:
            item = QListWidgetItem(path.name)
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            self.video_list.addItem(item)
        if video_paths:
            self.video_list.setCurrentRow(0)
        else:
            self.video_path.setPlaceholderText("Keine unterstuetzten Videos in diesem Ordner")
        self.settings.setValue("last_video_directory", str(folder_path))

    def _select_video(self, current_item: QListWidgetItem | None, _previous_item: QListWidgetItem | None) -> None:
        if current_item:
            self.video_path.setText(current_item.data(Qt.ItemDataRole.UserRole))

    def _launch(self) -> None:
        if self.player_process.state() != QProcess.ProcessState.NotRunning:
            QMessageBox.information(self, "Wiedergabe aktiv", "Ein Video wird bereits in VR wiedergegeben.")
            return
        video_path = self.video_path.text().strip()
        if not video_path:
            QMessageBox.warning(self, "Kein Video", "Bitte waehle zuerst eine Videodatei aus.")
            return
        if not Path(video_path).is_file():
            QMessageBox.warning(self, "Datei nicht gefunden", f"Die Videodatei existiert nicht:\n{video_path}")
            return
        if not shutil.which("vr-video-player"):
            QMessageBox.critical(self, "Programm nicht gefunden", "vr-video-player wurde nicht im PATH gefunden.")
            return
        self.launch_button.setEnabled(False)
        self.player_process.start("vr-video-player", self._build_command()[1:])

    def _on_player_error(self, _error: QProcess.ProcessError) -> None:
        self.launch_button.setEnabled(True)

    def _on_player_finished(self, _exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        self.launch_button.setEnabled(True)
        if exit_status != QProcess.ExitStatus.NormalExit or self.autoplay_mode.currentData() == "off":
            return
        next_row = self._next_video_row()
        if next_row is not None:
            self.video_list.setCurrentRow(next_row)
            self._launch()

    def _next_video_row(self) -> int | None:
        video_count = self.video_list.count()
        current_row = self.video_list.currentRow()
        if video_count < 2:
            return None
        if self.autoplay_mode.currentData() == "sequential":
            return current_row + 1 if current_row + 1 < video_count else None
        if self.autoplay_mode.currentData() == "random":
            return random.choice([row for row in range(video_count) if row != current_row])
        return None

    def closeEvent(self, event) -> None:
        self.settings.setValue("window_size", self.size())
        self.settings.setValue("window_position", self.pos())
        self.settings.setValue("view_mode", self._selected_mode())
        self.settings.setValue("left_right", self.left_right.isChecked())
        self.settings.setValue("stretch", self.stretch.isChecked())
        self.settings.setValue("zoom", self.zoom.value())
        self.settings.setValue("cursor_scale", self.cursor_scale.value())
        self.settings.setValue("cursor_wrap", self.cursor_wrap.isChecked())
        self.settings.setValue("free_camera", self.free_camera.isChecked())
        self.settings.setValue("reduce_flicker", self.reduce_flicker.isChecked())
        self.settings.setValue("use_system_mpv_config", self.use_system_mpv_config.isChecked())
        self.settings.setValue("mpv_profile", self.mpv_profile.currentText())
        self.settings.setValue("autoplay_mode", self.autoplay_mode.currentData())
        super().closeEvent(event)


if __name__ == "__main__":
    application = QApplication([])
    application.setApplicationName("VR Video Player GUI")
    application.setDesktopFileName("vr-video-player-gui")
    local_icon = Path(__file__).with_name("vr-video-player-gui.svg")
    application.setWindowIcon(QIcon(str(local_icon)) if local_icon.is_file() else QIcon.fromTheme("vr-video-player-gui"))
    window = VrPlayerWindow()
    window.show()
    application.exec()