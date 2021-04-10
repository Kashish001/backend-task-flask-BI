import spacy
from spacy import displacy
import wikipedia
import random
import os
from flask import Flask, redirect, url_for, render_template, request 

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def searchBar():
    if request.method == "POST" :
        query = request.form["query"]
        return redirect(url_for("searchResult", query = query))
    else :
        return render_template("index.html")

@app.route("/<query>")
def searchResult(query):
    try:
        content = wikipedia.page(str(query)).content
    except wikipedia.DisambiguationError as e:
        randPage = random.choice(e.options)
        content  = wikipedia.page(randPage).content
    content = nlp(content)
    annotatedText = displacy.render(content, style='ent')
    annotatedText = f"<h1>{query}</h1>" + annotatedText
    return annotatedText

if __name__ == "__main__":
    app.run()
    