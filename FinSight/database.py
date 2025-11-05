import sqlite3 

def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        interest REAL,
        gdp REAL,
        prediction TEXT      
    )
    """)
    
    conn.commit()
    conn.close()

def insert_prediction(interest, inflation, gdp, prediction):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO predictions (interest, inflation, gdp, prediction)
    VALUES (?, ?, ?, ?)
    """, (interest, inflation, gdp, prediction))
    conn.commit()
    conn.close()

def get_all_predictions():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()
    return data