from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'namma_chennai_secret_key'

# --- Database Management ---
import os # <--- Make sure this is imported at the top

# --- Database Management ---
def get_db_connection():
    # This finds the correct path on Vercel's cloud computers
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Table Schema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            nearby_hotels TEXT NOT NULL,
            image_url TEXT,      
            thumbnail_url TEXT,  
            map_url TEXT,
            latitude REAL,       
            longitude REAL       
        )
    ''')
    
    cur = conn.execute('SELECT count(*) FROM spots')
    if cur.fetchone()[0] == 0:
        initial_spots = [
            # 1. Santhome Cathedral (FIXED MAP URL)
            ("Santhome Cathedral Basilica", 
             "A historic minor basilica built over the tomb of Thomas the Apostle. The structure, which was built in the 16th century by Portuguese explorers, is known for its neo-Gothic style.", 
             "Le Royal Méridien, Grand Chennai", 
             "/static/images/san2.jpg",  
             "/static/images/santhome_bg.jpg", 
             "https://maps.google.com/?cid=11621782029321344222&g_mp=Cidnb29nbGUubWFwcy5wbGFjZXMudjEuUGxhY2VzLlNlYXJjaFRleHQ", # <-- UPDATED & FIXED LINK
             13.0335, 80.2785), 
             
            # 2. Snow Kingdom
            ("Snow Kingdom", 
             "India's largest indoor snow theme park. It offers snow sliding, snow dancing, and a play area, maintaining a temperature of -8°C all year round.", 
             "ibis Chennai OMR, Novotel", 
             "/static/images/Media (1).jpg", 
             "/static/images/Media.jpg",     
             "https://www.google.com/maps/place/?q=place_id:ChIJoeVgAZdcUjoRU8iNNuLYHW4",
             12.9099, 80.2486),
             
            # 3. Fort St. George Museum
            ("Fort St. George Museum", 
             "The first English fortress in India, founded in 1644. The museum houses relics from the colonial era, including weapons, coins, medals, and uniforms.", 
             "Taj Coromandel, The Park", 
             "/static/images/Media (3).jpg", 
             "/static/images/Media (2).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJlVHnD61oUjoR_ZKcRDdK_0w",
             13.0796, 80.2875),
             
            # 4. Guindy National Park
            ("Guindy National Park", 
             "The 8th smallest National Park of India and one of the very few national parks situated inside a city. It is home to blackbucks, spotted deer, and jackals.", 
             "ITC Grand Chola, Hilton Chennai", 
             "/static/images/Media (5).jpg", 
             "/static/images/Media (4).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJ82Efv3lnUjoRjSaF7VXwq-o",
             13.0067, 80.2206),
             
            # 5. Vivekananda House
            ("Vivekananda House", 
             "A shrine and pilgrimage center for the admirers of Swami Vivekananda. He stayed here for nine days after his return from the West in 1897.", 
             "Marina Inn, Hotel President", 
             "/static/images/Media (7).jpg", 
             "/static/images/Media (6).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJ3WSdxJxoUjoRMZCq-sm2iAQ",
             13.0494, 80.2803),
             
            # 6. T. Nagar
            ("T. Nagar", 
             "The shopping hub of Chennai. It is the busiest shopping district in India, famous for Kanchipuram silk sarees and heavy gold jewelry.", 
             "Residency Towers, Accord Metropolitan", 
             "/static/images/Media (9).jpg", 
             "/static/images/Media (8).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJcSPapVVmUjoR8ErwQ5f0VEk",
             13.0418, 80.2341),
             
            # 7. Semmozhi Poonga
            ("Semmozhi Poonga", 
             "A botanical garden set up by the horticulture department. It houses over 500 species of plants and features an artificial duck pond.", 
             "Hyatt Regency, The Raintree", 
             "/static/images/Media (11).jpg", 
             "/static/images/Media (10).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJcVcO_UZmUjoR21emTXt0U4k",
             13.0454, 80.2530),
             
            # 8. Madras War Cemetery
            ("Madras War Cemetery", 
             "A tribute to the men and women who sacrificed their lives in WWII. It is maintained by the Commonwealth War Graves Commission.", 
             "Trident, Radisson Blu", 
             "/static/images/Media (13).jpg", 
             "/static/images/Media (12).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJESn9jDZnUjoR8WqBv91TpMw",
             13.0206, 80.1932),
             
            # 9. Mahabalipuram
            ("Mahabalipuram", 
             "A UNESCO World Heritage site known for its 7th- and 8th-century Hindu Group of Monuments. Famous for the Shore Temple and Pancha Rathas.", 
             "InterContinental, Radisson Blu Resort", 
             "/static/images/Media (15).jpg", 
             "/static/images/Media (14).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJ18Mm3rGsUzoRA-Th_AECHmw",
             12.6208, 80.1945),
             
            # 10. VGP Marine Kingdom
            ("VGP Marine Kingdom", 
             "India's first walk-through underground tunnel aquarium. It showcases marine life from five different zones including rainforest and gorge.", 
             "VGP Golden Beach Resort, Fairfield by Marriott", 
             "/static/images/Media (17).jpg", 
             "/static/images/Media (16).jpg", 
             "https://www.google.com/maps/place/?q=place_id:ChIJhXkj8yRdUjoRi529_y783i8",
             12.9080, 80.2492)
        ]
        conn.executemany('INSERT INTO spots (name, description, nearby_hotels, image_url, thumbnail_url, map_url, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', initial_spots)
        conn.commit()
        print("Initialized Database with Fixed Santhome Map Link.")
    
    conn.close()

# --- Routes (Same as before) ---

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login_page')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    email = request.form['email']
    
    if role == 'admin':
        if email.strip() == "admin@nammachennai.com":
            session['user'] = email
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Email!")
            return redirect(url_for('login_page'))
    else:
        if email:
            session['user'] = email
            session['role'] = 'user'
            return redirect(url_for('user_home'))
        else:
            flash("Please enter a valid email.")
            return redirect(url_for('login_page'))

@app.route('/home')
def user_home():
    if session.get('role') != 'user': 
        return redirect(url_for('landing'))
    conn = get_db_connection()
    spots = conn.execute('SELECT * FROM spots').fetchall()
    conn.close()
    return render_template('home.html', spots=spots, user=session['user'])

@app.route('/spot/<int:spot_id>')
def spot_detail(spot_id):
    if session.get('role') != 'user': 
        return redirect(url_for('landing'))
    conn = get_db_connection()
    spot = conn.execute('SELECT * FROM spots WHERE id = ?', (spot_id,)).fetchone()
    conn.close()
    if spot is None: 
        return "Spot not found", 404
    return render_template('detail.html', spot=spot)

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin': 
        return redirect(url_for('landing'))
    conn = get_db_connection()
    spots = conn.execute('SELECT * FROM spots').fetchall()
    conn.close()
    return render_template('admin.html', spots=spots)

@app.route('/add_spot', methods=['POST'])
def add_spot():
    if session.get('role') == 'admin':
        name = request.form['name']
        desc = request.form['desc']
        hotels = request.form['hotels']
        img_url = "https://via.placeholder.com/1200x600" 
        thumb_url = "https://via.placeholder.com/300x200"
        map_url = "https://www.google.com/maps/search/?api=1&query=" + name.replace(" ", "+") + "+Chennai"
        lat, lng = 13.0827, 80.2707
        
        conn = get_db_connection()
        conn.execute('INSERT INTO spots (name, description, nearby_hotels, image_url, thumbnail_url, map_url, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name, desc, hotels, img_url, thumb_url, map_url, lat, lng))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_spot/<int:id>')
def delete_spot(id):
    if session.get('role') == 'admin':
        conn = get_db_connection()
        conn.execute('DELETE FROM spots WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    init_db()

    app.run(debug=True)
