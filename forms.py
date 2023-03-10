from flask_wtf import FlaskForm
from wtforms import Form, RadioField, StringField, SubmitField, validators

class GenerationForm(FlaskForm):
    """Form for getting info from user to generate powerpoint from."""
    doc_type = RadioField('Document Type:',
                          choices=[('proposal', 'Proposal Powerpoint'),
                                   ('other', 'Other Type (Not Yet Implemented)')])
    client_type = StringField('Client:', validators=[validators.input_required()])
    firm_type = StringField('Firm:', validators=[validators.input_required()])
    subject = StringField('What is the proposal about?', validators=[validators.input_required()])
    submit = SubmitField()

class ResultsForm(FlaskForm):
    """Form in the results page to ask if user is satisfied."""
    user_satisfaction = RadioField('Are you satisfied with these results?',
                                   choices=[('y', 'Yes'), ('n', 'No')])
    submit = SubmitField()
