from flask import Flask, render_template_string, request, jsonify
import os, sqlite3

app = Flask(__name__)

DB_PATH = "plays.db"

# ---------- Database setup ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS plays (title TEXT PRIMARY KEY, count INTEGER DEFAULT 0)"
        )

def get_play_count(title):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT count FROM plays WHERE title=?", (title,))
        row = cur.fetchone()
        return row[0] if row else 0

def add_play(title):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO plays (title, count) VALUES (?,1) "
            "ON CONFLICT(title) DO UPDATE SET count=count+1;",
            (title,),
        )
        conn.commit()

# ---------- Song loader ----------
def load_songs():
    songs = []
    for f in sorted(os.listdir("static")):
        if f.lower().endswith(".mp3"):
            title = os.path.splitext(f)[0]
            songs.append({
                "title": title,
                "artist": "Revivor Records",
                "url": f"/static/{f}",
                "plays": get_play_count(title)
            })
    return songs

# ---------- Routes ----------
@app.route("/")
def index():
    html = """
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Skelify — Powered by Revivor Records</title>
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
              <div class="title">{{ song.title }}</div>
              <div class="artist">{{ song.artist }}</div>
              <div class="plays">▶️ {{ song.plays }} plays</div>
            </div>
            <audio controls preload="metadata" onplay="countPlay('{{ song.title }}')">
              <source src="{{ song.url }}" type="audio/mpeg">
            </audio>
          </div>
        {% endfor %}

        <footer class="footer">
          <p>© 2025 Revivor Records • Made with ❤️ on Skelify</p>
        </footer>
      </div>

      <script>
        async function countPlay(title){
          await fetch("/play/" + encodeURIComponent(title), {method:"POST"});
        }
      </script>
    </body>
    </html>
    """
    return render_template_string(html, songs=load_songs())

@app.route("/play/<title>", methods=["POST"])
def play(title):
    add_play(title)
    return jsonify(success=True, plays=get_play_count(title))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))







