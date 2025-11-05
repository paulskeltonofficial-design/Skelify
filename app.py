from flask import Flask, render_template_string, request, jsonify
import os, sqlite3

app = Flask(__name__)

DB_PATH = "plays.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS stats (
                    title TEXT PRIMARY KEY,
                    plays INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0
                )""")
    conn.commit()
    conn.close()

def get_stat(title, field):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT {field} FROM stats WHERE title=?", (title,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def update_stat(title, field):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO stats (title) VALUES (?)", (title,))
    c.execute(f"UPDATE stats SET {field} = {field} + 1 WHERE title=?", (title,))
    conn.commit()
    conn.close()

def load_songs():
    songs = []
    for f in sorted(os.listdir("static")):
        if f.lower().endswith(".mp3"):
            title = os.path.splitext(f)[0]
            songs.append({
                "title": title,
                "artist": "Revivor Records",
                "url": f"/static/{f}",
                "plays": get_stat(title, "plays"),
                "likes": get_stat(title, "likes")
            })
    return songs

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Skelify — Powered by Revivor Records</title>
      <style>
        body{background:#111;color:#fff;font-family:sans-serif;text-align:center;margin:0;padding:20px;}
        .song{margin:25px auto;padding:15px;border:1px solid #333;border-radius:12px;width:90%;max-width:500px;background:#1c1c1c;}
        .title{font-size:1.3em;margin-bottom:5px;}
        .artist{color:#999;margin-bottom:10px;}
        .stats{margin-top:5px;color:#aaa;}
        button.like{background:none;border:none;color:#f55;font-size:1.2em;cursor:pointer;}
      </style>
    </head>
    <body>
      <img src="/static/icons/skelify-logo.png" style="height:80px;">
      <h1>Skelify</h1>
      <p>Powered by Revivor Records</p>

      {% for song in songs %}
        <div class="song" data-title="{{ song.title }}">
          <div class="title">{{ song.title }}</div>
          <div class="artist">{{ song.artist }}</div>
          <audio controls preload="metadata">
            <source src="{{ song.url }}" type="audio/mpeg">
          </audio>
          <div class="stats">
            ▶️ <span class="plays">{{ song.plays }}</span> plays &nbsp; ❤️ <span class="likes">{{ song.likes }}</span>
            <button class="like">❤️</button>
          </div>
        </div>
      {% endfor %}

      <footer style="margin-top:30px;color:#666;">© 2025 Revivor Records • Made with ❤️ on Skelify</footer>

      <script>
      document.querySelectorAll("audio").forEach(player=>{
        player.addEventListener("play",()=>{
          const title=player.closest(".song").dataset.title;
          fetch("/play/"+encodeURIComponent(title),{method:"POST"})
          .then(()=>{const el=player.closest(".song").querySelector(".plays");el.textContent=parseInt(el.textContent)+1;});
        });
      });
      document.querySelectorAll("button.like").forEach(btn=>{
        btn.addEventListener("click",()=>{
          const song=btn.closest(".song");
          const title=song.dataset.title;
          fetch("/like/"+encodeURIComponent(title),{method:"POST"})
          .then(()=>{const el=song.querySelector(".likes");el.textContent=parseInt(el.textContent)+1;});
        });
      });
      </script>
    </body>
    </html>
    """
    return render_template_string(html, songs=load_songs())

@app.route("/play/<title>", methods=["POST"])
def play(title):
    update_stat(title, "plays")
    return ("", 204)

@app.route("/like/<title>", methods=["POST"])
def like(title):
    update_stat(title, "likes")
    return ("", 204)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)



