from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = 'leaderboard.db'

AKTBOB_TIME = 5.5

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Ensure the leaderboard table and Aktbob entry exist
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            time FLOAT,
            timestamp DATETIME,
            email TEXT
        )
    ''')
    conn.execute('''
        INSERT INTO leaderboard (id, name, time, timestamp, email)
        VALUES (1, 'Aktbob', ?, datetime('now', 'localtime'), 'aktbob@example.com')
        ON CONFLICT(id) DO UPDATE SET 
            time = ?,
            timestamp = datetime('now', 'localtime')
    ''', (AKTBOB_TIME, AKTBOB_TIME))

    conn.commit()


@app.route('/')
def index():
    return render_template('index.html')
    


@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, time, strftime('%d.%m.%Y, %H.%M', timestamp) as ftimestamp FROM leaderboard ORDER BY time ASC").fetchall()
    conn.close()

    leaderboard = [{"id": row["id"], "name": row["name"], "time": f'{row["time"]:.2f}', "timestamp": row["ftimestamp"]} for row in rows]
    benchmark = next((row for row in leaderboard if row["id"] == 1), None)
    benchmark_time = benchmark["time"] if benchmark else "N/A"

    return jsonify({"rows": leaderboard, "benchmark_time": benchmark_time})


@app.route('/add_result', methods=['POST'])
def add_result():
    data = request.json
    name = data['name']
    time = float(data['time'])
    email = data.get('email', '')
    contestant_id = data.get('id')

    conn = get_db_connection()
    
    if contestant_id:
        existing = conn.execute('SELECT time FROM leaderboard WHERE id = ?', (contestant_id,)).fetchone()
        if existing and time < existing['time']:
            conn.execute(
                '''
                UPDATE leaderboard 
                SET time = ?, timestamp = datetime('now', 'localtime'), email = ? 
                WHERE id = ?
                ''',
                (time, email, contestant_id)
            )
            conn.commit()
            conn.close()
            return jsonify({"status": "updated", "id": contestant_id})
    else:
        cursor = conn.execute(
            '''
            INSERT INTO leaderboard (name, time, timestamp, email) 
            VALUES (?, ?, datetime('now', 'localtime'), ?)
            ''',
            (name, time, email)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"status": "inserted", "id": new_id})




if __name__ == '__main__':
    app.run(debug=True)
