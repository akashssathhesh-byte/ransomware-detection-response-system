from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "system": "RDRS",
        "status": "Online",
        "threats": 0,
        "alerts": 0
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
