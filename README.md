# Time Complexity Visualizer

A Flask server that times an algorithm on growing input sizes, draws the graph,
saves it as a PNG, and returns it as a base64 string inside JSON.

## Run

    pip install -r requirements.txt
    python3 app.py

Then open http://localhost:8000. The home page has one link per algorithm.

## Use

    http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000

| Parameter | Meaning |
|-----------|---------|
| `algo`    | Algorithm to time (see list below) |
| `step`    | Difference between one input size and the next |
| `n_max`   | Largest input size. The smallest is always 0. |

The O(n²) algorithms get slow for large sizes. Use something like `step=100&n_max=2000` for them.

## Algorithms

| Name | Expected growth |
|------|-----------------|
| `linear_search` | O(n) |
| `binary_search` | O(log n) |
| `bubble_sort` | O(n²) |
| `nested_loops` | O(n²) |
| `selection_sort` | O(n²) |
| `insertion_sort` | O(n²) |
| `merge_sort` | O(n log n) |
| `constant_time` | O(1) |

The first four are the required ones. The other four are extras.

## Response

JSON with `algo`, `step`, `n_max`, `sizes`, `times` (seconds), `saved_image`
(where the PNG was saved) and `image_base64` (the same PNG as a base64 string).

## Files

- `app.py`: the Flask server
- `visualizer.py`: the visualizer function from class, plus the algorithms
- `snapshots/`: saved graphs

## Choices

- **Graph is saved, not shown.** The class version opened a live window. A server has
  no screen, so this uses matplotlib's `Agg` backend, which draws to a file.
- **Only the algorithm is timed.** The input is built first and only the run is timed.
  Otherwise binary search would look like O(n) because of building the list.
- **Worst-case inputs.** Searches look for a value that is not in the list, and sorts
  get a list in reverse order, so each graph matches its textbook growth.
- **Each size is timed once.** This keeps the code close to the class version. Very fast
  algorithms (`binary_search`, `constant_time`) look noisy. The shape is what matters.
- **Forgiving input.** `algo='linear_search'` and `n_max=10,000` both work, because the
  assignment's example URL is written that way.
- **Sample graphs are committed** so they can be seen on GitHub without running anything.

## Sample graphs

One example graph per algorithm is in the `snapshots/` folder, named `sample_<algorithm>.png`.
