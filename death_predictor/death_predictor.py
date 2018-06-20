# coding=utf-8


# Death Predictor
# By Juan Negrier <juannegrier@gmail.com>
#
# Simple skill to joke predicting when the user will die

import logging
from datetime import datetime
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, request, statement, question, session
from predictions import language_stories
from dialogs import language_string


__author__ = 'Juan Negrier'
__email__ = 'juannegrier@gmail.com'


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.on_session_started
def start_session():
    logging.debug("Session started at {}".format(datetime.now().isoformat()))

@ask.launch
def new_game():
    welcome_msg = render_template('welcome', welcome_msg=language_string[request.locale]['translation']['WELCOME_MSG'])
    session.attributes['last_question'] = 'welcome'
    ask_again = render_template('continue', continue_msg=language_string[request.locale]['translation']['CONTINUE_MSG'])

    return question(welcome_msg).reprompt(ask_again)

@ask.intent("AMAZON.YesIntent")
def next_round():
    _question = render_template('name', name_msg=language_string[request.locale]['translation']['NAME_MSG'])
    session.attributes['last_question'] = 'name'

    return question(_question).reprompt(_question)

@ask.intent("AMAZON.NoIntent")
def goodbye():
    msg = render_template('negative', negative_msg=language_string[request.locale]['translation']['NEGATIVE_MSG'])
    return statement(msg)

@ask.intent("nameIntent")
def name_question():
    msg = render_template('thanks', thanks_msg=language_string[request.locale]['translation']['THANKS_MSG'])
    _question = render_template('dob', dob_msg=language_string[request.locale]['translation']['DOB_MSG'])
    session.attributes['last_question'] = 'dob'

    return question(msg + _question).reprompt(_question)

@ask.intent("dobIntent")
def dob_question():
    msg = render_template('msg_before_prediction', before_msg=language_string[request.locale]['translation']['BEFORE_PREDICTION_MSG'])
    prediction = render_template('prediction', prediction_msg=language_stories[request.locale]['translation'][randint(0, 15)])

    return statement(msg + prediction)

@ask.intent('AMAZON.StopIntent')
def handle_stop():
    farewell_text = render_template('stop_bye', stop_msg=language_string[request.locale]['translation']['STOP_BYE_MSG'])
    return statement(farewell_text)

@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    farewell_text = render_template('cancel_bye', cancel_msg=language_string[request.locale]['translation']['CANCEL_BYE_MSG'])
    return statement(farewell_text)

@ask.intent('AMAZON.HelpIntent')
def handle_help():
    help_text = render_template('help_text', help_msg=language_string[request.locale]['translation']['HELP_MSG'])
    return question(help_text)

@ask.intent('AMAZON.StartOverIntent')
def handle_start_over():
    start_over = render_template('welcome', welcome_msg=language_string[request.locale]['translation']['WELCOME_MSG'])
    return question(start_over)

@ask.intent('AMAZON.FallbackIntent')
def handle_fallback():
    last_question = render_template(session.attributes['last_question'])
    return question(last_question)

if __name__ == '__main__':
    app.run(debug=True)
