import os

from visualizer import time_complexity_visualizer, ALGORITHMS

N_MIN = 0
N_MAX = 1000   # small so the O(n²) algorithms finish quickly
N_STEP = 100
SNAPSHOT_DIR = "snapshots"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

for name, algo in ALGORITHMS.items():
    path = os.path.join(SNAPSHOT_DIR, f"sample_{name}.png")
    time_complexity_visualizer(algo, N_MIN, N_MAX, N_STEP, path)
    print("saved", path)
