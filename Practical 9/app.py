from flask import Flask, render_template, request

app = Flask(__name__)

def plan_blocks(initial, goal):
    current = initial[:]
    steps = ["Initial state: " + " ".join(current)]
    for i, block in enumerate(goal):
        if i < len(current) and current[i] == block:
            continue
        if block in current:
            current.remove(block)
        current.insert(i, block)
        steps.append("Move " + block + " to position " + str(i + 1))
        steps.append("Current state: " + " ".join(current))
    return steps

@app.route("/", methods=["GET", "POST"])
def index():
    steps = None
    error = None
    if request.method == "POST":
        initial = request.form["initial"].upper().split()
        goal = request.form["goal"].upper().split()
        if not initial or not goal or sorted(initial) != sorted(goal) or len(set(initial)) != len(initial):
            error = "Enter the same unique blocks in both fields."
        else:
            steps = plan_blocks(initial, goal)
    return render_template("index.html", steps=steps, error=error)

if __name__ == "__main__":
    app.run(debug=True)
