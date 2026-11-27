from flask import Flask, render_template, request
import heapq

app = Flask(__name__)
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def neighbors(s):
    i = s.index(0)
    r, c = divmod(i, 3)
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr * 3 + nc
            t = list(s)
            t[i], t[j] = t[j], t[i]
            result.append(tuple(t))
    return result

def heuristic(s, choice):
    if choice == "misplaced":
        return sum(s[i] != 0 and s[i] != GOAL[i] for i in range(9))
    total = 0
    for i, v in enumerate(s):
        if v:
            g = GOAL.index(v)
            total += abs(i//3 - g//3) + abs(i%3 - g%3)
    return total

def solvable(s):
    a = [x for x in s if x]
    inv = sum(a[i] > a[j] for i in range(len(a)) for j in range(i+1,len(a)))
    return inv % 2 == 0

def a_star(start, choice):
    pq = [(heuristic(start, choice), 0, start, [start])]
    best = {start: 0}
    while pq:
        _, cost, state, path = heapq.heappop(pq)
        if state == GOAL:
            return path
        for nxt in neighbors(state):
            nc = cost + 1
            if nc < best.get(nxt, float("inf")):
                best[nxt] = nc
                heapq.heappush(pq, (nc + heuristic(nxt, choice), nc, nxt, path + [nxt]))
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    path = None
    error = None
    if request.method == "POST":
        try:
            start = tuple(int(request.form[f"cell{i}"]) for i in range(9))
            choice = request.form.get("heuristic", "manhattan")
            if sorted(start) != list(range(9)):
                error = "Enter every number from 0 to 8 exactly once."
            elif not solvable(start):
                error = "This puzzle cannot be solved."
            else:
                path = a_star(start, choice)
        except:
            error = "Please enter valid numbers."
    return render_template("index.html", path=path, error=error)

if __name__ == "__main__":
    app.run(debug=True)
