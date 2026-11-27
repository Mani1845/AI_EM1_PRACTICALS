from flask import Flask, render_template, request

app = Flask(__name__)

RULES = [
    (["rain"], "wet_ground"),
    (["sprinkler_on"], "wet_ground"),
    (["rain"], "carry_umbrella"),
    (["cloudy", "rain"], "possible_rain"),
    (["wet_ground", "traffic_busy"], "drive_slowly"),
    (["possible_rain"], "carry_umbrella")
]

def forward_chaining(facts):
    facts = set(facts)
    steps = []
    changed = True
    while changed:
        changed = False
        for conditions, conclusion in RULES:
            if all(c in facts for c in conditions) and conclusion not in facts:
                facts.add(conclusion)
                steps.append(" → ".join(conditions) + " ⇒ " + conclusion)
                changed = True
    return sorted(facts), steps

@app.route("/", methods=["GET", "POST"])
def index():
    facts = []
    steps = []
    if request.method == "POST":
        initial = request.form.getlist("facts")
        facts, steps = forward_chaining(initial)
    return render_template("index.html", facts=facts, steps=steps)

if __name__ == "__main__":
    app.run(debug=True)
