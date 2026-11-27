from flask import Flask, render_template

app = Flask(__name__)

ROWS = COLS = 4
GOAL = (3, 3)
OBSTACLE = (1, 1)
GAMMA = 0.9
ACTIONS = {
    "↑": (-1, 0), "↓": (1, 0),
    "←": (0, -1), "→": (0, 1)
}

def move(state, action):
    r, c = state
    dr, dc = ACTIONS[action]
    nr, nc = r + dr, c + dc
    if not (0 <= nr < ROWS and 0 <= nc < COLS) or (nr, nc) == OBSTACLE:
        return state
    return nr, nc

def value_iteration():
    values = {(r, c): 0.0 for r in range(ROWS) for c in range(COLS)}
    values[OBSTACLE] = 0.0

    for _ in range(500):
        new_values = values.copy()
        delta = 0
        for state in values:
            if state == GOAL or state == OBSTACLE:
                continue
            options = [
                -1 + GAMMA * values[move(state, action)]
                for action in ACTIONS
            ]
            new_values[state] = max(options)
            delta = max(delta, abs(new_values[state] - values[state]))
        values = new_values
        if delta < 0.001:
            break

    policy = {}
    for state in values:
        if state in (GOAL, OBSTACLE):
            policy[state] = "G" if state == GOAL else "■"
        else:
            action = max(
                ACTIONS,
                key=lambda a: -1 + GAMMA * values[move(state, a)]
            )
            policy[state] = action
    return values, policy

@app.route("/")
def index():
    values, policy = value_iteration()
    grid = [
        [(r, c, round(values[(r, c)], 2), policy[(r, c)])
         for c in range(COLS)]
        for r in range(ROWS)
    ]
    return render_template("index.html", grid=grid)

if __name__ == "__main__":
    app.run(debug=True)
