import sqlite3


def start_db():
    # Δημιουργία σύνδεσης με τη βάση δεδομένων mydb.db
    conn = sqlite3.connect('mydb.db')

    # Δημιουργία cursor object για να εκτελέσεις εντολές SQL
    cursor = conn.cursor()

    # Δημιουργία πίνακα leaderboard αν δεν υπάρχει ήδη
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score_athens REAL,
            score_knossos REAL,
            score_sparta REAL
        )
    ''')

    # Αποθήκευση των αλλαγών
    conn.commit()

    # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
    conn.close()

    print("Η βάση δεδομένων δημιουργήθηκε ή ήδη υπάρχει με τον πίνακα leaderboard.")


def clear_leaderboard():
    start_db()
    # Δημιουργία σύνδεσης με τη βάση δεδομένων mydb.db
    conn = sqlite3.connect('mydb.db')

    # Δημιουργία cursor object για να εκτελέσεις εντολές SQL
    cursor = conn.cursor()

    # Διαγραφή όλων των εγγραφών από τον πίνακα leaderboard
    cursor.execute('DELETE FROM leaderboard')

    # Αποθήκευση των αλλαγών
    conn.commit()

    # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
    conn.close()

    print("Όλες οι εγγραφές διαγράφηκαν από τον πίνακα leaderboard.")


def add_leaderboard_entry(username, score_athens, score_knossos, score_sparta):
    start_db()
    # Δημιουργία σύνδεσης με τη βάση δεδομένων mydb.db
    conn = sqlite3.connect('mydb.db')

    # Δημιουργία cursor object για να εκτελέσεις εντολές SQL
    cursor = conn.cursor()

    # Εισαγωγή νέας εγγραφής στον πίνακα leaderboard
    cursor.execute('''
        INSERT INTO leaderboard (username, score_athens, score_knossos, score_sparta)
        VALUES (?, ?, ?, ?)
    ''', (username, score_athens, score_knossos, score_sparta))

    # Αποθήκευση των αλλαγών
    conn.commit()

    # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
    conn.close()

    print(f"Η εγγραφή για τον χρήστη {username} προστέθηκε επιτυχώς στη βάση δεδομένων.")
    print(f"Oi xronoi tou paikti einai {score_athens} {score_knossos} {score_sparta}")


# Παράδειγμα χρήσης της μεθόδου
# add_leaderboard_entry('player2', 120.5, 98.7, 110.3)
def format_time(seconds):
    seconds = float(seconds)  # Μετατροπή σε αριθμητική τιμή (αν είναι string)
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def get_top_5_players():
    # Δημιουργία σύνδεσης με τη βάση δεδομένων mydb.db
    conn = sqlite3.connect('mydb.db')

    # Δημιουργία cursor object για να εκτελέσεις εντολές SQL
    cursor = conn.cursor()

    # Ανάκτηση των top 5 παικτών με τον καλύτερο συνολικό χρόνο
    cursor.execute('''
        SELECT username, score_athens, score_knossos, score_sparta,
               (score_athens + score_knossos + score_sparta) AS total_score
        FROM leaderboard
        ORDER BY total_score ASC
        LIMIT 5
    ''')

    # Ανάγνωση των αποτελεσμάτων
    top_5_players = cursor.fetchall()

    # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
    conn.close()

    # Μορφοποίηση των αποτελεσμάτων
    # for player in top_5_players:
    #     username, athens, knossos, sparta, total = player
    #     print(f"Παίκτης: {username}, Αθήνα: {format_time(athens)}, Κνωσός: {format_time(knossos)}, Σπάρτη: {format_time(sparta)}, Σύνολο: {format_time(total)}")

    return top_5_players


# def get_top_5_players():
#     # Δημιουργία σύνδεσης με τη βάση δεδομένων mydb.db
#     conn = sqlite3.connect('mydb.db')
#
#     # Δημιουργία cursor object για να εκτελέσεις εντολές SQL
#     cursor = conn.cursor()
#
#     # Ανάκτηση των top 5 παικτών με τον καλύτερο συνολικό χρόνο
#     cursor.execute('''
#         SELECT username, score_athens, score_knossos, score_sparta,
#                (score_athens + score_knossos + score_sparta) AS total_score
#         FROM leaderboard
#         ORDER BY total_score ASC
#         LIMIT 5
#     ''')
#
#     # Ανάγνωση των αποτελεσμάτων
#     top_5_players = cursor.fetchall()
#
#     # Κλείσιμο της σύνδεσης με τη βάση δεδομένων
#     conn.close()
#
#     return top_5_players
#
clear_leaderboard()  # Διαγραφή όλων των εγγραφών


#Παράδειγμα χρήσης της μεθόδου
# top_5 = get_top_5_players()

# for player in top_5:
#     username, athens, knossos, sparta, total = player
#     print(
#         f"Παίκτης: {player[0]}, Αθήνα: {format_time(player[1])}, Κνωσός: {format_time(player[2])}, Σπάρτη: {format_time(player[3])}, Σύνολο: {format_time(player[4])}")
# for player in top_5:
#     print(
#         f"Username: {player[0]}, Score Athens: {player[1]}, Score Knossos: {player[2]}, Score Sparta: {player[3]}, Total Score: {player[4]}")


