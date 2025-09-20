from flask import Flask, render_template, jsonify, request
import sqlite3
import os

# Set the template and static folders to be in the lochan directory
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Serve static files from the main project directory
from flask import send_from_directory
import os

@app.route('/home/<path:filename>')
def serve_home_static(filename):
    return send_from_directory('../home', filename)

@app.route('/emily/<path:filename>')
def serve_emily_static(filename):
    return send_from_directory('../emily', filename)

@app.route('/kennedy/<path:filename>')
def serve_kennedy_static(filename):
    return send_from_directory('../kennedy', filename)

@app.route('/naisha/<path:filename>')
def serve_naisha_static(filename):
    return send_from_directory('../naisha', filename)

@app.route('/tony/<path:filename>')
def serve_tony_static(filename):
    return send_from_directory('../tony', filename)

# Database setup
def init_db():
    conn = sqlite3.connect('lochan_data.db')
    cursor = conn.cursor()
    
    # Create table for personal information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT,
            bio TEXT,
            skills TEXT,
            interests TEXT,
            contact_email TEXT
        )
    ''')
    
    # Insert sample data
    cursor.execute('''
        INSERT OR REPLACE INTO personal_info 
        (id, name, title, bio, skills, interests, contact_email)
        VALUES (1, 'Lochan', 'Freshman studying Data Science', 
                'A deep dive into one of history''s most controversial events: the assassination of President John F. Kennedy. This page explores the facts, theories, and my personal analysis of what happened on November 22, 1963.',
                'Historical Research, Critical Analysis, Data Science, Python, JavaScript',
                'JFK Assassination, Conspiracy Theories, American History, Cold War Politics',
                'lochan@example.com')
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home/')
def home_redirect():
    return render_template('home.html')

@app.route('/home/index.html')
def home_index():
    return render_template('home.html')

@app.route('/lochan')
def lochan_page():
    return render_template('lochan.html')

@app.route('/lochan/lochan.html')
def lochan_original():
    return render_template('lochan.html')

# Serve other team member pages
@app.route('/emily/emily.html')
def emily_page():
    return send_from_directory('../emily', 'emily.html')

@app.route('/kennedy/kennedy.html')
def kennedy_page():
    return send_from_directory('../kennedy', 'kennedy.html')

@app.route('/naisha/naisha.html')
def naisha_page():
    return send_from_directory('../naisha', 'naisha.html')

@app.route('/tony/tony.html')
def tony_page():
    return send_from_directory('../tony', 'tony.html')

@app.route('/api/lochan/info')
def get_lochan_info():
    conn = sqlite3.connect('lochan_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM personal_info WHERE id = 1')
    info = cursor.fetchone()
    
    conn.close()
    
    if info:
        return jsonify({
            'name': info[1],
            'title': info[2],
            'bio': info[3],
            'skills': info[4],
            'interests': info[5],
            'contact_email': info[6]
        })
    else:
        return jsonify({'error': 'No data found'}), 404

@app.route('/api/lochan/update', methods=['POST'])
def update_lochan_info():
    data = request.get_json()
    
    conn = sqlite3.connect('lochan_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE personal_info 
        SET name = ?, title = ?, bio = ?, skills = ?, interests = ?, contact_email = ?
        WHERE id = 1
    ''', (
        data.get('name', ''),
        data.get('title', ''),
        data.get('bio', ''),
        data.get('skills', ''),
        data.get('interests', ''),
        data.get('contact_email', '')
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Information updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='127.0.0.1')
