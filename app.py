from flask import Flask, render_template_string
import os

app = Flask(__name__)

def load_songs():
    songs = []
    for f in sorted(os.listdir("static")):
        if f.lower().endswith(".mp3"):
            title = os.path.splitext(f)[0]
            songs.append({
                "title": title,
                "artist": "Revivor Records",
                "url": f"/static/{f}"
            })
    return songs

@app.route("/")
def index():
    html = """
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Skelify — Powered by Revivor Records</title>
      <link rel="stylesheet" href="/static/css/styles.css">
      <link rel="icon" href="/static/icons/favicon.png" type="image/png">
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
            <div class="cover">
              <img src="/static/images/{{ song.title }}.jpg" alt="cover art" onerror="this.style.display='none'">
            </div>
            <div class="meta">
              <div class="title">{{ song.title }}</div>
              <div class="artist">{{ song.artist }}</div>
            </div>
            <audio controls preload="metadata">
              <source src="{{ song.url }}" type="audio/mpeg">
            </audio>
          </div>
        {% endfor %}

        <footer class="footer">
          <p>© 2025 Revivor Records • Made with ❤️ on Skelify</p>
        </footer>
      </div>

      <button id="themeToggle" class="toggle">☀️/🌙</button>

      <script>
        // Theme toggle
        const btn = document.getElementById('themeToggle');
        btn.addEventListener('click', () => {
          document.body.classList.toggle('light');
        });

        // Fade-in animation
        document.addEventListener("DOMContentLoaded", () => {
          document.body.classList.add('loaded');
        });
      </script>
    </body>
    </html>
    """
    return render_template_string(html, songs=load_songs())

if __name__ == "__main__":
    app.run(debug=True, port=5001)
