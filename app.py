from flask import Flask, render_template, request
import sqlite3 as sql3

app = Flask(__name__)

def get_db_conn():
    conn = sql3.connect('data/database/project.db')
    conn.row_factory = sql3.Row
    return conn

def close_db_conn(conn):
    conn.close()

def init_db():
    conn = get_db_conn()
    conn.execute('CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY, title TEXT, description TEXT, date TEXT)')
    conn.close()

@app.before_request
def before_request():
    init_db()

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/project_meneger', methods=['POST', 'GET'])
def pj():
    if request.method == 'POST':
        tit = request.form['title']
        des = request.form['des']
        date = request.form['date']
        conn = get_db_conn()

        conn.execute('INSERT INTO projects(title, description, date) VALUES (?, ?, ?)', (tit, des, date)).fetchall()
        conn.commit()
    
    conn = get_db_conn()
    proj = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    
    return render_template('pj.html', proj=proj)

@app.route('/project_meneger/delete', methods=['POST', 'GET'])
def del_pj():
    if request.method == 'POST':
        iddel = request.form['id']
        conn = get_db_conn()

        conn.execute('DELETE FROM projects WHERE id=?', (iddel,))
        conn.commit()

    return render_template('del_pj.html')

if __name__ == "__main__":
    app.run(debug=True)