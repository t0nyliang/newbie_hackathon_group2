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

@app.route('/style.css')
def serve_home_css():
    return send_from_directory('../home', 'style.css')

@app.route('/group2.jpg')
def serve_home_image():
    return send_from_directory('../home', 'group2.jpg')

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
    
    # Create table for JFK case information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jfk_case_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            basic_info TEXT,
            stated_suspect TEXT,
            issues_controversies TEXT,
            what_i_believe TEXT
        )
    ''')
    
    # Insert comprehensive JFK case data with proper formatting
    cursor.execute('''
        INSERT OR REPLACE INTO jfk_case_info 
        (id, basic_info, stated_suspect, issues_controversies, what_i_believe)
        VALUES (1, 
                '<h3>The Event</h3><p>On November 22, 1963, at 12:30 PM CST, President John F. Kennedy was assassinated while riding in a motorcade through Dealey Plaza in Dallas, Texas. The motorcade was traveling from Love Field airport to the Dallas Trade Mart, where Kennedy was scheduled to speak.</p><h3>Key Details</h3><ul><li><strong>Time:</strong> 12:30 PM CST</li><li><strong>Location:</strong> Dealey Plaza, Dallas, Texas</li><li><strong>Vehicle:</strong> 1961 Lincoln Continental convertible</li><li><strong>Route:</strong> Main Street to Houston Street to Elm Street</li><li><strong>Witnesses:</strong> Hundreds of people in the plaza</li></ul>',
                
                '<h3>Lee Harvey Oswald</h3><p>According to the official Warren Commission Report, Lee Harvey Oswald was identified as the lone gunman responsible for Kennedy''s assassination.</p><h3>Oswald''s Background</h3><ul><li><strong>Born:</strong> October 18, 1939, in New Orleans</li><li><strong>Military Service:</strong> U.S. Marine Corps (1956-1959)</li><li><strong>Defection:</strong> Moved to Soviet Union in 1959, returned in 1962</li><li><strong>Employment:</strong> Worked at the Texas School Book Depository</li><li><strong>Arrest:</strong> November 22, 1963, at 1:50 PM</li><li><strong>Death:</strong> November 24, 1963, shot by Jack Ruby</li></ul><h3>Evidence Against Oswald</h3><ul><li>Rifle found on 6th floor of Texas School Book Depository</li><li>Fingerprints on the rifle and boxes</li><li>Witnesses placed him on the 6th floor</li><li>Photographic evidence of him with the rifle</li></ul>',
                
                '<h3>Ballistics Questions</h3><ul><li><strong>Magic Bullet Theory:</strong> Single bullet causing 7 wounds in Kennedy and Connally</li><li><strong>Timing:</strong> Oswald''s ability to fire 3 shots in 5.6 seconds</li><li><strong>Trajectory:</strong> Downward angle from 6th floor window</li><li><strong>Bullet Fragments:</strong> Inconsistent with single shooter theory</li></ul><h3>Witness Testimony</h3><ul><li>Multiple witnesses reported shots from different locations</li><li>Grassy knoll witnesses claimed shots from the front</li><li>Inconsistent descriptions of the shooter</li><li>Many witnesses changed their stories over time</li></ul><h3>Government Investigation Concerns</h3><ul><li>Warren Commission''s limited scope and time constraints</li><li>Classified documents still unreleased</li><li>FBI and CIA withholding information</li><li>Evidence mishandling and chain of custody issues</li></ul>',
                
                '<h3>My Analysis</h3><p>LBJ was the mastermind, with help from the CIA.</p><h3>Key Points Supporting Conspiracy Theory</h3><ul><li><strong>Multiple Shooters:</strong> The trajectory and timing of shots suggest more than one gunman</li><li><strong>Oswald''s Capabilities:</strong> His marksmanship skills were questionable for such precise shots</li><li><strong>Government Cover-up:</strong> Too many classified documents and suspicious behavior</li><li><strong>Ruby''s Motive:</strong> Jack Ruby''s murder of Oswald prevented a proper trial</li><li><strong>Witness Intimidation:</strong> Many witnesses died under suspicious circumstances</li></ul><h3>Most Likely Scenario</h3><p>Other people that could have been involved:</p><ul><li>Anti-Castro Cuban exiles</li><li>Organized crime figures</li><li>Military-industrial complex interests</li><li>Intelligence agency operatives</li></ul>')
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    return send_from_directory('../home', 'index.html')

@app.route('/home/')
def home_redirect():
    return send_from_directory('../home', 'index.html')

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
    
    cursor.execute('SELECT * FROM jfk_case_info WHERE id = 1')
    info = cursor.fetchone()
    
    conn.close()
    
    if info:
        return jsonify({
            'basic_info': info[1],
            'stated_suspect': info[2],
            'issues_controversies': info[3],
            'what_i_believe': info[4]
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
