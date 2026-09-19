import base64
import os
from datetime import datetime

from flask import Flask, jsonify, request


from visualizer import time_complexity_visualizer, ALGORITHMS

app = Flask(__name__)

N_MIN = 0  # minimum is always 0
EXAMPLE_STEP = 100
EXAMPLE_N_MAX = 1000
SNAPSHOT_DIR = "snapshots"
PORT = int(os.environ.get("PORT", 8000))
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


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
