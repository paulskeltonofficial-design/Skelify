from flask import Flask, render_template_string, request
import os, sqlite3

app = Flask(__name__)

# --- database setup for play counter ---
DB_PATH = "plays.db"
if not os.path.exists(DB_PATH):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE plays (title TEXT PRIMARY KEY, count INTEGER DEFAULT 0)")

def get_plays(title):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT count FROM plays WHERE title=?", (title,))
        row = cur.fetchone()
        return row[0] if row else 0

def add_play(title):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO plays (title, count)
            VALUES (?, 1)
            ON CONFLICT(title) DO UPDATE SET count = count + 1
        """, (title,))
        conn.commit()

# --- load songs dynamically from static folder ---
def load_songs():
    songs = []
    for f in sorted(os.listdir("static")):
        if f.lower().endswith(".mp3"):
            title = os.path.splitext(f)[0]
            plays = get_plays(title)
            songs.append({
                "title": title,
                "artist": "Revivor Records",
                "url": f"/static/{f}",
                "plays": plays
            })
    return songs

# --- routes ---
@app.route("/")
def index():
    html = """
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Skelify — Powered by Revivor</title>
      <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
      <div class="wrap">
        <header class="header">
          <img src="/static/images/skelify-logo.png" alt="Skelify Logo" class="logo">
          <h1>Skelify</h1>
          <p class="subtitle">Powered by Revivor Records</p>
        </header>

        {% for song in songs %}
          <div class="song">
            <div class="meta">
              <h2>{{ song.title }}</h2>
              <p>{{ song.artist }}</p>
              <p class="plays">▶ {{ song.plays }} plays</p>
            </div>
            <audio controls preload="metadata" onplay="fetch('/play/{{song.title}}')">
              <source src="{{ song.url }}" type="audio/mpeg">
            </audio>
          </div>
        {% endfor %}

        <footer>
          <p>© 2025 Revivor Records • Made with ❤️ on Skelify</p>
        </footer>
      </div>
    </body>
    </html>
    """
    return render_template_string(html, songs=load_songs())

@app.route("/play/<title>")
def play(title):
    add_play(title)
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))






