from flask import Flask, render_template, request

app = Flask(__name__)

def diagnose(a):
    if a["power"] == "no":
        return "Check the router power cable and switch it on."
    if a["wifi"] == "no":
        return "Turn on Wi-Fi on your device."
    if a["other"] == "yes":
        return "The issue is probably with your device. Restart it and reconnect."
    if a["internet"] == "no":
        return "Restart your router and check your internet service."
    return "Check your network settings or contact your internet service provider."

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        result = diagnose({
            "power": request.form["power"],
            "wifi": request.form["wifi"],
            "other": request.form["other"],
            "internet": request.form["internet"]
        })
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
