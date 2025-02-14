from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

aktbob_time = 10.5  # Define the time for Aktbob

# SQLite setup
conn = sqlite3.connect('leaderboard.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    time FLOAT,
                    timestamp DATETIME,
                    email TEXT
                )''')
conn.commit()

# SQLite setup
aktbob_time = 10.5  # Define the time for Aktbob
conn = sqlite3.connect('leaderboard.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    time FLOAT,
                    timestamp DATETIME,
                    email TEXT
                )''')
conn.commit()

# Insert or update the row with id = 1 for Aktbob
conn.execute('''
    INSERT INTO leaderboard (id, name, time, timestamp, email)
    VALUES (1, 'Aktbob', ?, datetime('now'), 'aktbob@example.com')
    ON CONFLICT(id) DO UPDATE SET 
        name = 'Aktbob',
        time = ?,
        timestamp = datetime('now'),
        email = 'rpamtm001@aarhus.dk'
''', (aktbob_time, aktbob_time))
conn.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    cursor = conn.execute("SELECT id, name, time, timestamp FROM leaderboard ORDER BY time ASC")
    rows = [{"id": row[0], "name": row[1], "time": f'{row[2]:.2f}', "timestamp": row[3][:-3]} for row in cursor.fetchall()]
    
    # Find the benchmark time (id = 1)
    benchmark = next((row for row in rows if row["id"] == 1), None)
    benchmark_time = benchmark["time"] if benchmark else "N/A"
    
    return jsonify({"rows": rows, "benchmark_time": benchmark_time})

@app.route('/add_result', methods=['POST'])
def add_result():
    data = request.json
    conn.execute("INSERT INTO leaderboard (name, time, timestamp, email) VALUES (?, ?, ?, ?)", 
                 (data['name'], data['time'], data['timestamp'], data.get('email')))
    conn.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
