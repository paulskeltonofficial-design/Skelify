
from flask import Flask, render_template_string

app = Flask(__name__)

# Your song list (you can add more later)
songs = [
    {"title": "I wanna hold you", "artist": "Paul Skelton", "url": "/static/Paul Skelton - I wanna hold you.mp3"}
]

@app.route('/')
def index():
    html = """
    <html>
    <head>
      <title>My Label</title>
    </head>
    <body style="font-family:sans-serif; background:#111; color:white; text-align:center;">
      <h1>🎶 My Label Streaming App 🎶</h1>
      {% for song in songs %}
        <div style="margin:20px;">
          <h2>{{song.title}} - {{song.artist}}</h2>
          <audio controls>
            <source src="{{song.url}}" type="audio/mpeg">
          </audio>
        </div>
      {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, songs=songs)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
