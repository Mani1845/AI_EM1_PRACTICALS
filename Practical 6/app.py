from flask import Flask, render_template, request

app = Flask(__name__)

graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}
colors = ["Red", "Green", "Blue"]

def solve(assignment):
    if len(assignment) == len(graph):
        return assignment
    node = next(n for n in graph if n not in assignment)
    for color in colors:
        if all(assignment.get(neighbor) != color for neighbor in graph[node]):
            assignment[node] = color
            result = solve(assignment)
            if result:
                return result
            del assignment[node]
    return None

@app.route("/")
def index():
    solution = solve({})
    return render_template("index.html", solution=solution)

if __name__ == "__main__":
    app.run(debug=True)
