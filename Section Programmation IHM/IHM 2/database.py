import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('gestures.db')
c = conn.cursor()

# Supprimer la table si elle existe déjà
c.execute('DROP TABLE IF EXISTS gesture_commands')

# Création de la table pour stocker les séquences de gestes et commandes
c.execute('''
CREATE TABLE IF NOT EXISTS gesture_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gesture1 TEXT NOT NULL,
    gesture2 TEXT NOT NULL,
    gesture3 TEXT NOT NULL,
    command TEXT NOT NULL
)
''')

# Exemple d'insertion de données dans la table
c.executemany('''
INSERT INTO gesture_commands (gesture1, gesture2, gesture3, command)
VALUES (?, ?, ?, ?)
''', [
    ('Up', 'Down', 'Left', 'open_edge'),
    ('Right', 'Up', 'Down', 'open_notepad'),
    ('Down', 'Left', 'Right', 'open_firefox'),
    ('Left', 'Right', 'Up', 'open_explorer'),
    ('Right', 'Left', 'Right', 'open_vscode'),
    ('Up', 'Up', 'Up', 'open_taskmanager'),
    ('Clockwise', 'Clockwise', 'Clockwise', 'open_horloge')
])

# Sauvegarder (commit) les changements et fermer la connexion
conn.commit()
conn.close()
