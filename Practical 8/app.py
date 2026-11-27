from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

texts = [
    "I love this product", "This is amazing",
    "Very happy with the service", "Excellent experience",
    "I hate this", "Very bad experience",
    "This is terrible", "I am disappointed",
    "It is okay", "Nothing special",
    "The product is average", "It is normal"
]
labels = [
    "Positive", "Positive", "Positive", "Positive",
    "Negative", "Negative", "Negative", "Negative",
    "Neutral", "Neutral", "Neutral", "Neutral"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_text = request.form["text"].strip()
        if user_text:
            result = model.predict(vectorizer.transform([user_text]))[0]
        else:
            result = "Please enter some text."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
