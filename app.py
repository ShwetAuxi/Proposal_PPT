import os

from flask import Flask, render_template, request, session, redirect, url_for, send_file, flash
from flask_bootstrap import Bootstrap5

import openai
from pptx import Presentation

from forms import ResultsForm, GenerationForm

# insert your openai key here. Don't upload your key to GitHub or it'll get revoked!
openai.api_key = "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"

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config.update(SECRET_KEY=os.urandom(12))

MODEL = "pt-3.5-turbo"

TEMP = 0.5

MAX_TOKENS = 100


@app.route("/")
def hello_world():
    # return render_template("index.html", title="Hello")
    return redirect(url_for("formPage"))


def generate(docType, clientType, firmType, subject=None):
    try:
        prompt = "Document Type: " + docType + "Client Type: " + clientType + "Firm Type: " + firmType

        promptPres = prompt + "Given this context, generate a title for my presentation. No quotation marks:"

        promptExecSummary = prompt + "Given this context, generate an executive summary for my presentation:"

        promptAgenda = prompt + "Given this context, generate an agenda outline for my presentation:"

        session["titlePres"] = \
            openai.Completion.create(prompt=promptPres, model=MODEL, temperature=TEMP, max_tokens=MAX_TOKENS)[
                'choices'][
                0]['text']
        session["execSummary"] = \
            openai.Completion.create(prompt=promptExecSummary, model=MODEL, temperature=TEMP, max_tokens=MAX_TOKENS)[
                'choices'][0]['text']
        session["agenda"] = \
            openai.Completion.create(prompt=promptAgenda, model=MODEL, temperature=TEMP, max_tokens=MAX_TOKENS)[
                'choices'][
                0]['text']
        return redirect(url_for("results_page"))
    except openai.error.AuthenticationError as e:
        return "OPENAI AUTH KEY ERROR"
    # with the provided text, we can now create a slides with the title presentation, executive summary, and agenda


@app.route("/results_page", methods=["GET", "POST"])
def results_page():
    form = ResultsForm(request.form)
    if request.method == "GET":
        # there's a better way to do this... but that's for later.
        if "titlePres" in session and "execSummary" in session and "agenda" in session:
            titlePres = session["titlePres"]
            execSummary = session["execSummary"]
            agenda = session["agenda"]
            return render_template("results_page.html",
                                   titlePres=titlePres,
                                   execSummary=execSummary,
                                   agenda=agenda,
                                   form=form)
        else:
            # TODO: how did we get here?
            return "SESSION DATA INVALID"
    elif request.method == "POST":
        # TODO: handle request from form
        # userSatisfaction = request.form["userSatisfaction"] old ver
        userSatisfaction = form.user_satisfaction.data

        if userSatisfaction.lower() == "y":
            SLD_LAYOUT_TITLE_AND_CONTENT = 1

            prs = Presentation()
            slide_layout = prs.slide_layouts[SLD_LAYOUT_TITLE_AND_CONTENT]
            slide = prs.slides.add_slide(slide_layout)

            title_placeholder = slide.shapes.title
            title_placeholder.text = 'Agenda Example'
            # TODO: fix the following line!!!
            # slide.add_paragraph("Whatever you want to say here.")

            prs.save("generated_template.pptx")
            return send_file('generated_template.pptx')
        else:
            return redirect(url_for("formPage"))


@app.route("/form", methods=["GET", "POST"])
def formPage():
    form = GenerationForm(request.form)
    if request.method == "POST" and form.validate():
        return generate(form.doc_type.data, form.client_type.data, form.firm_type.data, form.subject.data)
    elif request.method == "POST":
        flash('PLEASE FILL IN ALL FIELDS')
    return render_template('presentation_form_page.html', form=form)


@app.route("/form_old", methods=["GET", "POST"])
def interactiveUI():
    """Old UI using hardcoded html form. Consider this deprecated."""
    if request.method == "GET":
        # we should have the options in the form be sent to the template instead of hard coded, but we can do that later
        return render_template("presentation_form_old.html")
    elif request.method == "POST":
        docType = request.form["docType"]
        clientType = request.form["clientType"]
        firmType = request.form["firmType"]

        if docType == "":
            docType = request.form["docTypeOther"].lower()

        return generate(docType, clientType, firmType)
    else:
        return "INVALID REQUEST"


@app.route("/shutdown")
def shutdown():
    # this doesn't work...
    print('shutdown')
    raise RuntimeError("shutdown")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host=('0.0.0.0'), port=port)
