from flask import Flask, render_template, jsonify, request
import sqlite3
import os

# Set the template and static folders to be in the lochan directory
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

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
        VALUES (1, 'Lochan', 'Software Developer & Student', 
                'Passionate about technology and learning new things. Currently working on exciting projects and always eager to explore new challenges in the world of programming.',
                'Python, JavaScript, HTML/CSS, Flask, React, Git',
                'Coding, Gaming, Music, Photography, Hiking',
                'lochan@example.com')
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/lochan')
def lochan_page():
    return render_template('lochan.html')

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
    app.run(debug=True, port=5001, host='127.0.0.1')
