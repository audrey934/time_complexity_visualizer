from visualizer import time_complexity_visualizer, ALGORITHMS

N_MIN, N_MAX, N_STEP = 0, 500, 50  # small so the O(n²) ones stay fast

for name, algo in ALGORITHMS.items():
    sizes, times = time_complexity_visualizer(algo, N_MIN, N_MAX, N_STEP, f"test_{name}.png")
    print(f"{name}: {len(sizes)} points, last time = {times[-1]:.6f}s")