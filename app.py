import base64
import os
from datetime import datetime
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, Analysis, User
from visualizer import time_complexity_visualizer, ALGORITHMS

app = Flask(__name__)

N_MIN = 0  # minimum is always 0
EXAMPLE_STEP = 100
EXAMPLE_N_MAX = 1000
SNAPSHOT_DIR = "snapshots"
PORT = int(os.environ.get("PORT", 8000))
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'analysis.db')}"
# JWT setup. Set JWT_SECRET_KEY in the environment for anything real;
# the fallback is only so the app runs out of the box for development.
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-only-secret-key-change-me-in-production-0123456789")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# Tokens are read ONLY from the "Authorization: Bearer <token>" header,
# never from the query string.
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Every way a JWT can fail becomes a 401 with a plain message.
# (flask-jwt-extended returns 422 for malformed tokens by default.)
@jwt.unauthorized_loader
def missing_token(reason):
    return jsonify(error="I don't know you", detail=reason), 401


@jwt.invalid_token_loader
def invalid_token(reason):
    return jsonify(error="I don't know you", detail=reason), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify(error="Bye", detail="Token has expired, please log in again"), 401


def clean(value):
    """Accept 'linear_search', ['linear_search'] or plain linear_search."""
    return value.strip().strip("[]'\" ")


def get_int(name):
    """Accept 10000 or 10,000."""
    return int(clean(request.args.get(name, "")).replace(",", ""))


@app.route("/analyze")
def analyze():
    algo = clean(request.args.get("algo", ""))
    if algo not in ALGORITHMS:
        return jsonify(error=f"Unknown algo '{algo}'", available=sorted(ALGORITHMS)), 400

    try:
        step, n_max = get_int("step"), get_int("n_max")
    except ValueError:
        return jsonify(error="step and n_max must be whole numbers"), 400
    if step <= 0 or n_max < N_MIN:
        return jsonify(error="step must be > 0 and n_max must be >= 0"), 400

    save_path = os.path.join(SNAPSHOT_DIR, f"{algo}_{datetime.now():%Y%m%d_%H%M%S}.png")
    sizes, times = time_complexity_visualizer(ALGORITHMS[algo], N_MIN, n_max, step, save_path)

    with open(save_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    return jsonify(algo=algo, step=step, n_max=n_max, sizes=sizes,
                   times=times, saved_image=save_path, image_base64=image_b64)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    if not username or not password:
        return jsonify(error="username and password are required"), 400
    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already taken"), 409

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(username=str(data.get("username", "")).strip()).first()
    if user is None or not user.check_password(str(data.get("password", ""))):
        return jsonify(error="I don't know you"), 401

    # The token's subject must be a string in newer PyJWT versions.
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token, token_type="Bearer")


@app.route("/save_analysis", methods=["POST"])
@jwt_required()
def save_analysis():
    algo = clean(request.args.get("algo", ""))
    if algo not in ALGORITHMS:
        return jsonify(error=f"Unknown algo '{algo}'", available=sorted(ALGORITHMS)), 400

    try:
        step, n_max = get_int("step"), get_int("n_max")
    except ValueError:
        return jsonify(error="step and n_max must be whole numbers"), 400
    if step <= 0 or n_max < N_MIN:
        return jsonify(error="step must be > 0 and n_max must be >= 0"), 400

    save_path = os.path.join(SNAPSHOT_DIR, f"{algo}_{datetime.now():%Y%m%d_%H%M%S}.png")
    time_complexity_visualizer(ALGORITHMS[algo], N_MIN, n_max, step, save_path)

    analysis = Analysis(algorithm=algo, step=step, n_max=n_max, saved_image=save_path)
    db.session.add(analysis)
    db.session.commit()

    return jsonify(message="Analysis saved successfully")


@app.route("/")
def home():
    links = "".join(
        f'<li><a href="/analyze?algo={name}&step={EXAMPLE_STEP}&n_max={EXAMPLE_N_MAX}">{name}</a></li>'
        for name in sorted(ALGORITHMS)
    )
    return (
        "<h2>Time complexity visualizer</h2>"
        "<p>Click an algorithm to run it. You get JSON with the timings "
        "and the plot as a base64 image.</p>"
        f"<ul>{links}</ul>"
        "<p>To use other sizes, change <code>step</code> and <code>n_max</code> "
        "in the address bar.</p>"
    )

if __name__ == "__main__":
    app.run(host="localhost", port=PORT)