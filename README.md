# Time Complexity Visualizer

A Flask server that times an algorithm on growing input sizes, draws the graph, saves it as a PNG, and returns it as a base64 string inside JSON.

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

## Save an analysis to the database

    curl -X POST "http://localhost:8000/save_analysis?algo=linear_search&step=10&n_max=1000"

Runs the same analysis as `/analyze`, then saves the algorithm, step, n_max, and the saved image path to a SQLite database (`analysis.db`), using the `Analysis` model in `models.py`. No raw SQL is used anywhere, only SQLAlchemy.

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
| `queue_enqueue_dequeue` | O(n²) |
| `stack_balanced_parens` | O(n) |
| `queue_deque_enqueue_dequeue` | O(n) |

The last four use a `Stack` and a `Queue` built from scratch (see
`structures.py`). `queue_enqueue_dequeue` and `queue_deque_enqueue_dequeue` do the exact same job, enqueue n items then dequeue n items, but with two different underlying implementations. Comparing their graphs shows why one is O(n²) (a list, where removing from the front shifts everything else) and the other is O(n) (`collections.deque`, where removing from the front doesn't).

## Response

JSON with `algo`, `step`, `n_max`, `sizes`, `times` (seconds), `saved_image` (where the PNG was saved) and `image_base64` (the same PNG as a base64 string).

`/save_analysis` returns `{"message": "Analysis saved successfully"}` and
writes a row to `analysis.db` instead.

## Files

- `app.py`: the Flask server
- `visualizer.py`: the visualizer function from class, plus the algorithms
- `structures.py`: the `Stack` and `Queue` classes, with `test_structures.py` as their test suite
- `models.py`: the `Analysis` database model (SQLAlchemy, no raw SQL)
- `snapshots/`: saved graphs

## Choices

- **Graph is saved, not shown.** The class version opened a live window. A server has  no screen, so this uses matplotlib's `Agg` backend, which draws to a file.
- **Only the algorithm is timed.** The input is built first and only the run is timed.  Otherwise binary search would look like O(n) because of building the list.
- **Worst-case inputs.** Searches look for a value that is not in the list, and sorts get a list in reverse order, so each graph matches its textbook growth.
- **Each size is timed once.** This keeps the code close to the class version. Very fast algorithms (`binary_search`, `constant_time`) look noisy. The shape is what matters.
- **Forgiving input.** `algo='linear_search'` and `n_max=10,000` both work, because the assignment's example URL is written that way.
- **Sample graphs are committed** so they can be seen on GitHub without running anything.
- **`analysis.db` is not committed.** It's local data, not code. Running the server recreates it automatically (`db.create_all()`), same as the `snapshots/` folder.

## Sample graphs

One example graph per algorithm is in the `snapshots/` folder, named `sample_<algorithm>.png`.
