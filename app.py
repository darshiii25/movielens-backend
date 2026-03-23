from flask import Flask
from flask_cors import CORS

from utils.db import get_db_connection

from routes.auth import auth
from routes.recommendation import recommendation
from routes.review import review
from routes.summary import summary

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(recommendation, url_prefix="/api")
app.register_blueprint(review, url_prefix="/api")
app.register_blueprint(summary, url_prefix="/api")

@app.route("/")
def home():
    return {"message": "Backend running successfully"}

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True)
