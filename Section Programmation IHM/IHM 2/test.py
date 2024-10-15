import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

# Fonction pour lancer Firefox
def launch_firefox():
    subprocess.Popen(['test.py'])
    print("Firefox lancé")

# Configuration de l'application PyQt
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Lanceur de Firefox")

# Configuration du layout et du bouton
layout = QVBoxLayout()
launch_button = QPushButton("Lancer Firefox")
launch_button.clicked.connect(launch_firefox)
layout.addWidget(launch_button)

window.setLayout(layout)

# Afficher la fenêtre
window.show()
sys.exit(app.exec_())



