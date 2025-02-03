from flask import Flask, render_template

# Create a new Flask app
app = Flask(__name__, template_folder="template", static_folder="static")


@app.route("/")
def index():
    """Serve the main webpage"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)  # Runs on port 8000
