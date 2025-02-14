# **Aktbob Konkurrence Web Application**

This web application is a leaderboard for the **Aktbob 2.0 Competition**, where participants try to beat the benchmark time set by **Aktbob** in identifying and removing sensitive information.

---

## **Features**
- **Live Timer**: Tracks the contestant's time and displays it in real-time.
- **Leaderboard**: Displays the ranking of participants based on their time.
- **Highlighting**:
  - **Gold highlight** for the top performer.
  - **Bright red highlight** for **Aktbob’s benchmark** time.
  - **Blue highlight** for the latest entry.
- **Automatic Timestamping**: Each entry records the current time.
- **Optional Email Field**: Used to contact the winner.

---

## **Setup Instructions**

### **1. Prerequisites**
Ensure you have **Python 3.x** installed. You can check your Python version with:
```bash
python --version
```

### **2. Install Required Libraries**
Install the necessary Python packages using **pip**:
```bash
pip install flask
```

### **3. Database Setup**
The application uses **SQLite** as its database. The `leaderboard` table is created automatically if it does not exist. Additionally, a row for **Aktbob** is inserted or updated with a defined time (`10.5 seconds` by default).

---

## **Running the Application**
1. Clone the repository or copy the files to your local machine.
2. Run the Python Flask server:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## **Project Structure**
```
/static              - Contains static files (e.g., favicon, styles)
templates/index.html - The main HTML file for the user interface
app.py               - The main Flask application
leaderboard.db       - SQLite database for storing participant data
```

---

## **Main Libraries Used**
- **Flask**: Python web framework for serving the application.
- **SQLite**: Lightweight database for storing participant information.
- **Bootstrap**: Frontend framework for styling and responsive design.

---

## **Database Schema**
The database table `leaderboard` has the following columns:
- `id` (INTEGER PRIMARY KEY): Unique identifier for each row.
- `name` (TEXT): Name of the participant.
- `time` (FLOAT): Time taken by the participant (in seconds).
- `timestamp` (DATETIME): When the result was recorded.
- `email` (TEXT): Optional email for contacting the participant.

### **Sample Query to View the Leaderboard**
```sql
SELECT * FROM leaderboard ORDER BY time ASC;
```

---

## **Customization**
You can customize the benchmark time for **Aktbob** in the `app.py`:
```python
aktbob_time = 10.5  # Change this value as needed
```

---

## **Future Enhancements**
- **Export Leaderboard to CSV**
- **Authentication for Admin Access**
- **Real-Time Leaderboard Updates**

---

## **License**
This project is open-source and free to use for educational purposes.
