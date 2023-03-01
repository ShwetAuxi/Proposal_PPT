from flask import Flask, render_template

import openai
import pptx
from pptx import Presentation

openai.api_key = "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"

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")


def interactiveUI():
    docType = input("User, what type of document do you want? ")
    clientType = input("User, who is the client? ")
    firmType = input("User, who is the client? ")

    if docType.lower() == "proposal":
        pass
        # pass in variables into chat gpt to create 
        # paragraphs for title of presentation, executive
        # summary and Agenda outline
prompt = "Document Type: " + docType + "Client Type: " + clientType + "Firm Type: " + firmType

promptPres = prompt + "Given this context, generate a title for my presentation. No quotation marks"

promptExecSummary = prompt + "Given this context, generate an executive summary for my presentation"

promptAgenda = prompt + "Given this context, generate an agenda outline for my presentation"

titlePres = openai.Completion.create(prompt=promptPres, model='text-davinci-003', temperature=0.5, max_tokens=100)['choices'][0]['text']
execSummary = openai.Completion.create(prompt=promptExecSummary, model='text-davinci-003', temperature=0.5, max_tokens=100)['choices'][0]['text']
agenda = openai.Completion.create(prompt=promptAgenda, model='text-davinci-003', temperature=0.5, max_tokens=100)['choices'][0]['text']
  
    # with the provided text, we can now create a slides with the title presentation, executive summary, and agenda


print(titlePres)
print(execSummary)
print(agenda)
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

