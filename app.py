from flask import Flask, render_template, request, session, redirect, url_for

import openai
from pptx import Presentation

openai.api_key = "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"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")


def generate(docType, clientType, firmType):
    prompt = "Document Type: " + docType + "Client Type: " + clientType + "Firm Type: " + firmType

    promptPres = prompt + "Given this context, generate a title for my presentation. No quotation marks"

    promptExecSummary = prompt + "Given this context, generate an executive summary for my presentation"

    promptAgenda = prompt + "Given this context, generate an agenda outline for my presentation"

    session["titlePres"] = \
        openai.Completion.create(prompt=promptPres, model='text-davinci-003', temperature=0.5, max_tokens=100)[
            'choices'][
            0]['text']
    session["execSummary"] = \
        openai.Completion.create(prompt=promptExecSummary, model='text-davinci-003', temperature=0.5, max_tokens=100)[
            'choices'][0]['text']
    session["agenda"] = \
        openai.Completion.create(prompt=promptAgenda, model='text-davinci-003', temperature=0.5, max_tokens=100)[
            'choices'][
            0]['text']
    return redirect(url_for("results_page"))
    # with the provided text, we can now create a slides with the title presentation, executive summary, and agenda


@app.route("/results_page", methods=["GET", "POST"])
def results_page():
    if request.method == "GET":
        # there's a better way to do this... but that's for later.
        if "titlePres" in session and "execSummary" in session and "agenda" in session:
            titlePres = session["titlePres"]
            execSummary = session["execSummary"]
            agenda = session["agenda"]
            #TODO: render results page
        else:
            #TODO: how did we get here?
    elif request.method == "POST":
        #TODO: handle request from form
        userSatisfaction = input("\n User, are you satisfied with the initial template? Y/N")

        if userSatisfaction.lower() == "y":
            SLD_LAYOUT_TITLE_AND_CONTENT = 1

            prs = Presentation()
            slide_layout = prs.slide_layouts[SLD_LAYOUT_TITLE_AND_CONTENT]
            slide = prs.slides.add_slide(slide_layout)

            title_placeholder = slide.shapes.title
            title_placeholder.text = 'Agenda Example'
            slide.add_paragraph("Whatever you want to say here.")

            prs.save("userui.pptx")


@app.route("/form", methods=["GET", "POST"])
def interactiveUI():
    if request.method == "GET":
        # we should have the options in the form be sent to the template instead of hard coded, but we can do that later
        return render_template("presentation_form.html")
    elif request.method == "POST":
        docType = request.form["docType"]
        clientType = request.form["clientType"]
        firmType = request.form["firmType"]

        if docType == "":
            docType = request.form["docTypeOther"].lower()

        return generate(docType, clientType, firmType)
    else:
        return "INVALID REQUEST"
