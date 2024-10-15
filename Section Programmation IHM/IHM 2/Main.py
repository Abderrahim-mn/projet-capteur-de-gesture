import serial
import time
import sqlite3
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

# Configurer le port série
ser = serial.Serial('COM3', 115200)  # Remplacez 'COM3' par le port série correct pour votre capteur

# Dictionnaire des commandes et des programmes correspondants avec les icônes
command_program_map = {
    'open_firefox': {'path': ['C:\\Program Files\\Mozilla Firefox\\firefox.exe'], 'icon': 'C:\\Users\\mouno\\OneDrive\\Desktop\\PROJE_EMB\\sequence de mouvement\\icons\\firefox.png'},
    'open_notepad': {'path': ['notepad.exe'], 'icon': 'icons\\notepad.png'},
    'open_edge': {'path': ['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'], 'icon': 'C:\\Users\\mouno\\OneDrive\\Desktop\\PROJE_EMB\\sequence de mouvement\\icons\\edge.png'},
    'open_explorer': {'path': ['explorer.exe'], 'icon': 'icons\\explorer.png'},
    'open_vscode': {'path': [r'C:\\Users\\mouno\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'], 'icon': 'C:\\Users\\mouno\\OneDrive\\Desktop\\PROJE_EMB\\sequence de mouvement\\icons\\vscode.png'},
    'open_taskmanager': {'path': [r'C:\\Windows\\System32\\Taskmgr.exe'], 'icon': 'C:\\Users\\mouno\\OneDrive\\Desktop\\PROJE_EMB\\sequence de mouvement\\icons\\taskmanager.png'},
     'open_horloge': {'path': ['control.exe'], 'icon': 'C:\\Users\\mouno\\OneDrive\\Desktop\\PROJE_EMB\\sequence de mouvement\\icons\\horloge.png'},
    # Ajoutez d'autres commandes et programmes ici
}

# Fonction pour exécuter la commande
def execute_command(command):
    command_label.setText(f"Commande exécutée: {command}")
    print(f"Exécution de la commande: {command}")
    
    # Exécuter le programme correspondant à la commande
    if command in command_program_map:
        try:
            subprocess.Popen(command_program_map[command]['path'], shell=True)
            print(f"{command_program_map[command]['path'][0]} lancé")
            
            # Afficher l'icône de l'application exécutée
            icon_path = command_program_map[command]['icon']
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                app_icon.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                app_icon.setToolTip(command)
                print(f"Affichage de l'icône: {icon_path}")
            else:
                print(f"Erreur: Icône non trouvée à l'emplacement: {icon_path}")
        except Exception as e:
            print(f"Erreur lors de l'exécution de la commande {command}: {e}")
    else:
        print(f"Commande non reconnue: {command}")

# Fonction pour obtenir la commande basée sur la séquence de gestes
def get_command_from_db(gesture_sequence):
    conn = sqlite3.connect('gestures.db')
    c = conn.cursor()
    
    # Construire et exécuter la requête SQL
    c.execute('''
    SELECT command FROM gesture_commands
    WHERE gesture1 = ? AND gesture2 = ? AND gesture3 = ?
    ''', gesture_sequence)

    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# Fonction de la boucle principale
def main_loop():
    global gesture_sequence

    if ser.in_waiting > 0:
        # Lire le geste actuel depuis le capteur
        gesture = ser.readline().decode('utf-8').strip()
        print(f"Geste détecté : {gesture}")

        # Mettre à jour l'affichage des gestes détectés
        gesture_list_widget.addItem(gesture)
        gesture_list_widget.scrollToBottom()

        # Ajouter le geste à la séquence
        gesture_sequence.append(gesture)

        # Garder uniquement les trois derniers gestes dans la séquence
        if len(gesture_sequence) > 3:
            gesture_sequence.pop(0)

        # Vérifier si la séquence de trois gestes correspond à une commande
        if len(gesture_sequence) == 3:
            command = get_command_from_db(tuple(gesture_sequence))
            if command:
                execute_command(command)
                gesture_sequence = []  # Réinitialiser la séquence après l'exécution de la commande

# Initialiser la séquence de gestes
gesture_sequence = []

# Configurer l'application PyQt
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Détection de Gestes")
window.resize(800, 600)  # Ajuster la taille de la fenêtre

# Appliquer des styles
app.setStyleSheet("""
    QWidget {
        background-color: #2E3440;
        color: #D8DEE9;
        font-family: Arial, sans-serif;
    }
    QLabel {
        font-size: 18pt;
        color: #88C0D0;
        padding: 10px;
        border: 1px solid #4C566A;
        border-radius: 5px;
        background-color: #3B4252;
    }
    QListWidget {
        font-size: 14pt;
        color: #ECEFF4;
        background-color: #4C566A;
        border: 1px solid #4C566A;
        padding: 5px;
        border-radius: 5px;
    }
    QListWidget::item {
        padding: 10px;
        margin: 5px;
    }
""")

layout = QVBoxLayout()

gesture_label = QLabel("Gestes détectés:")
layout.addWidget(gesture_label)

gesture_list_widget = QListWidget()
layout.addWidget(gesture_list_widget)

command_label = QLabel("Commande exécutée: ")
layout.addWidget(command_label)

# Ajouter une zone pour afficher l'icône de l'application exécutée
icon_layout = QHBoxLayout()
app_icon = QLabel()
icon_layout.addWidget(app_icon)
layout.addLayout(icon_layout)

window.setLayout(layout)

# Configurer le timer pour la boucle principale
timer = QTimer()
timer.timeout.connect(main_loop)
timer.start(100)  # Exécuter la boucle toutes les 100 ms

window.show()
sys.exit(app.exec_())
