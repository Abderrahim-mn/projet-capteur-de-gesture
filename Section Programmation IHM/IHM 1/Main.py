import sys
import serial
import pyautogui
import sqlite3
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

# Thread pour la lecture des données du capteur
class SensorThread(QThread):
    movement_detected = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True

    def run(self):
        try:
            ser = serial.Serial(self.port, 115200)
            while self.running:
                if ser.in_waiting:
                    data = ser.readline().decode().strip()
                    self.movement_detected.emit(data)
        except serial.SerialException as e:
            print(f"Erreur de connexion au port série : {e}")
        finally:
            ser.close()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

# Application PyQt
class SpotifyControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.default_button_styles = {}  # Initialisation ici
        self.initUI()
        self.initSensor()
        self.initDatabase()

    def initUI(self):
        self.setWindowTitle('Music Control')
        layout = QVBoxLayout()

        self.status_label = QLabel('Waiting for sensor data...', self)
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        self.play_button = self.create_button('▶', self.play_music)
        self.pause_button = self.create_button('⏸', self.pause_music)
        self.next_button = self.create_button('⏭', self.next_track)
        self.prev_button = self.create_button('⏮', self.prev_track)

        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.next_button)

        volume_layout = QHBoxLayout()
        self.vol_up_button = self.create_button('🔊', self.volume_up)
        self.vol_down_button = self.create_button('🔉', self.volume_down)

        volume_layout.addWidget(self.vol_up_button)
        volume_layout.addWidget(self.vol_down_button)

        layout.addLayout(button_layout)
        layout.addLayout(volume_layout)
        self.setLayout(layout)

        # Appliquer la feuille de style
        self.apply_stylesheet()

    def create_button(self, label, func):
        button = QPushButton(label, self)
        button.clicked.connect(func)
        self.default_button_styles[button] = button.styleSheet()
        return button

    def initSensor(self):
        self.sensor_thread = SensorThread('COM3')  # Remplacez par votre port série
        self.sensor_thread.movement_detected.connect(self.handle_movement)
        self.sensor_thread.start()

    def initDatabase(self):
        
        self.conn = sqlite3.connect('movements.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movement TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Supprimez toutes les lignes de la table movements
        self.cursor.execute('DELETE FROM movements')
        self.conn.commit()
        

    def log_movement(self, movement):
        self.cursor.execute('INSERT INTO movements (movement) VALUES (?)', (movement,))
        self.conn.commit()

    def play_music(self):
        pyautogui.press('playpause')

    def pause_music(self):
        pyautogui.press('playpause')

    def next_track(self):
        pyautogui.press('nexttrack')

    def prev_track(self):
        pyautogui.press('prevtrack')

    def volume_up(self):
        self.adjust_volume(0.1)  # Increase volume by 10%

    def volume_down(self):
        self.adjust_volume(-0.1)  # Decrease volume by 10%

    def adjust_volume(self, change):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == "Spotify.exe":
                current_volume = volume.GetMasterVolume()
                new_volume = min(max(current_volume + change, 0.0), 1.0)
                volume.SetMasterVolume(new_volume, None)
                break

    def handle_movement(self, movement):
        self.status_label.setText(f'Movement detected: {movement}')
        self.log_movement(movement)  # Log the movement to the database
        actions = {
            "Backward": (self.play_button, self.play_music),
            "Forward": (self.pause_button, self.pause_music),
            "Left": (self.next_button, self.next_track),
            "Right": (self.prev_button, self.prev_track),
            "Up": (self.vol_up_button, self.volume_up),
            "Down": (self.vol_down_button, self.volume_down)
        }
        action = actions.get(movement)
        if action:
            button, func = action
            func()
            self.change_button_color(button)

    def change_button_color(self, button):
        default_style = self.default_button_styles[button]
        button.setStyleSheet("""QPushButton {
            background-color: #b91d1d;
            border: none;
            color: #FFFFFF;
            font-size: 24px;
            margin: 10px;
            padding: 15px;
            border-radius: 30px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: background-color 0.3s, transform 0.3s;
        }""")
        QTimer.singleShot(500, lambda: button.setStyleSheet(default_style))

    def closeEvent(self, event):
        self.sensor_thread.stop()
        self.conn.close()
        event.accept()

    def apply_stylesheet(self):
        with open("C:/Users/mouno/OneDrive/Desktop/PROJE_EMB/IHM/style.css", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpotifyControlApp()
    ex.show()
    sys.exit(app.exec_())
