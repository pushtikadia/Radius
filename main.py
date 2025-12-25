import sqlite3
import math
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow phone connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static files (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Automatic Redirect: localhost:8000 -> Dashboard
@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")

# --- DATABASE SETUP (Auto-runs on start) ---
def init_db():
    conn = sqlite3.connect('lifeline.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            item TEXT,
            lat REAL,
            lon REAL
        )
    ''')
    # Check if empty, then add dummy data
    c.execute('SELECT count(*) FROM posts')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO posts (type, item, lat, lon) VALUES (?, ?, ?, ?)",
                  ('REQUEST', 'Emergency Water', 40.730610, -73.935242))
        print("Database initialized with dummy data.")
        
    conn.commit()
    conn.close()

init_db()

# --- LOGIC ---
class Post(BaseModel):
    type: str
    item: str
    lat: float
    lon: float

class PostResponse(Post):
    id: int
    distance_km: float = 0.0

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.post("/api/posts")
def create_post(post: Post):
    conn = sqlite3.connect('lifeline.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (type, item, lat, lon) VALUES (?, ?, ?, ?)", 
              (post.type, post.item, post.lat, post.lon))
    conn.commit()
    conn.close()
    return {"message": "Post created"}

@app.get("/api/nearby", response_model=List[PostResponse])
def get_nearby(lat: float, lon: float, radius_km: float = 9999):
    conn = sqlite3.connect('lifeline.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    rows = c.fetchall()
    conn.close()

    results = []
    for row in rows:
        dist = calculate_distance(lat, lon, row[3], row[4])
        if dist <= radius_km:
            results.append({
                "id": row[0],
                "type": row[1],
                "item": row[2],
                "lat": row[3],
                "lon": row[4],
                "distance_km": round(dist, 2)
            })
    
    results.sort(key=lambda x: x['distance_km'])
    return results