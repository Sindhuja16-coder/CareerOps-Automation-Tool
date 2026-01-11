from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('careerops.db')
    c = conn.cursor()
    # Create table to store jobs if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'Applied',
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database immediately when app starts
init_db()

# --- ROUTES ---

# 1. Home Page: Loads the Dashboard
@app.route('/')
def index():
    return render_template('index.html')

# 2. API: Get all jobs (sends JSON data to frontend)
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = sqlite3.connect('careerops.db')
    c = conn.cursor()
    c.execute("SELECT * FROM applications ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    # Convert database rows to a list of dictionaries
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "company": row[1],
            "role": row[2],
            "status": row[3],
            "date": row[4]
        })
    return jsonify(jobs)

# 3. API: Add a new job
@app.route('/api/jobs', methods=['POST'])
def add_job():
    data = request.json
    conn = sqlite3.connect('careerops.db')
    c = conn.cursor()
    c.execute("INSERT INTO applications (company, role, status) VALUES (?, ?, ?)", 
              (data['company'], data['role'], 'Applied'))
    conn.commit()
    conn.close()
    return jsonify({"message": "Job added successfully!"})

# 4. API: Update Status (e.g., Applied -> Interview)
@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    conn = sqlite3.connect('careerops.db')
    c = conn.cursor()
    c.execute("UPDATE applications SET status = ? WHERE id = ?", (data['status'], job_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated!"})

# 5. API: Delete a job
@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = sqlite3.connect('careerops.db')
    c = conn.cursor()
    c.execute("DELETE FROM applications WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Job deleted!"})

if __name__ == '__main__':
    # 'host=0.0.0.0' allows you to view this on your phone if on same Wi-Fi
    app.run(debug=True, host='0.0.0.0', port=5000)