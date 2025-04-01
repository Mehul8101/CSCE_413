from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'users.db'

TEMPLATE = '''<!DOCTYPE html><html><head><title>User Search</title><style>body { font-family: Arial, sans-serif; margin: 40px; }.query { background: #f0f0f0; padding: 10px; margin: 10px 0; }</style></head><body><h1>Search Users</h1><form method="get"><input type="text" name="name" placeholder="Enter name to search"><input type="submit" value="Search"></form>{% if query %}<div class="query"><strong>SQL Query:</strong> {{ query }}</div>{% endif %}{% if users %}<h2>Results:</h2><ul>{% for user in users %}<li>{{ user[1] }}</li>{% endfor %}</ul>{% endif %}</body>
</html>
'''

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)""")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Mehul",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Charlie",))
    conn.commit()
    conn.close()

@app.route('/')
def search():
    name = request.args.get('name', '')
    users = []
    query = ''
    if name:
        query = f"SELECT * FROM users WHERE name LIKE '{name}'"
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()
    
    return render_template_string(TEMPLATE, users=users, query=query)

if __name__ == '__main__':
    if os.path.exists(DATABASE):
        os.remove(DATABASE)    
    init_db()
    app.run(debug=True)

#Used parts of the code displayed in class