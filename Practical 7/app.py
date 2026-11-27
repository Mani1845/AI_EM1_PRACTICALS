from flask import Flask, render_template, request
from sklearn.naive_bayes import GaussianNB

app = Flask(__name__)

X = [
    [2, 50, 40], [3, 60, 45], [4, 65, 50],
    [5, 70, 55], [6, 75, 65], [7, 80, 70],
    [8, 85, 80], [9, 90, 90], [1, 30, 25],
    [2, 40, 35], [7, 95, 85], [5, 55, 60]
]
y = [
    "Needs Improvement", "Needs Improvement",
    "Needs Improvement", "Needs Improvement",
    "Good Performance", "Good Performance",
    "Good Performance", "Good Performance",
    "Needs Improvement", "Needs Improvement",
    "Good Performance", "Good Performance"
]

model = GaussianNB()
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])
            if not (0 <= hours <= 24 and 0 <= attendance <= 100 and 0 <= marks <= 100):
                raise ValueError
            result = model.predict([[hours, attendance, marks]])[0]
        except ValueError:
            result = "Please enter valid values within the given ranges."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
