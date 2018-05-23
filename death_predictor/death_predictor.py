# coding=utf-8


# Death Predictor
# By Juan Negrier <juannegrier@gmail.com>
#
# Simple skill to predict how when the user will die

import logging
from datetime import datetime
from random import randint
from flask import Flask, json, render_template
from flask_ask import Ask, request, statement, question, session
from predictions import stories


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
    welcome_msg = render_template('welcome')
    session.attributes['last_question'] = 'welcome'
    ask_again = render_template('continue')

    return question(welcome_msg).reprompt(ask_again)


@ask.intent("AMAZON.YesIntent")
def next_round():
    _question = render_template('name')
    session.attributes['last_question'] = 'name'

    return question(_question).reprompt(_question)

@ask.intent("AMAZON.NoIntent")
def next_round():
    msg = render_template('negative')
    return statement(msg)

@ask.intent("nameIntent")
def next_round():
    msg = render_template('thanks')
    _question = render_template('dob')
    session.attributes['last_question'] = 'dob'

    return question(msg + _question).reprompt(_question)

@ask.intent("dobIntent")
def next_round():
    msg = render_template('msg_before_prediction')
    prediction = render_template('prediction', story=stories[randint(0, 3)])

    return statement(msg + prediction)

@ask.intent('AMAZON.StopIntent')
def handle_stop():
    farewell_text = render_template('stop_bye')
    return statement(farewell_text)

@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    farewell_text = render_template('cancel_bye')
    return statement(farewell_text)

@ask.intent('AMAZON.HelpIntent')
def handle_help():
    help_text = render_template('help_text')
    return question(help_text)

@ask.intent('AMAZON.StartOverIntent')
def handle_start_over():
    start_over = render_template('welcome')
    return question(start_over)

@ask.intent('AMAZON.FallbackIntent')
def handle_fallback():
    last_question = render_template(session.attributes['last_question'])
    return question(last_question)

if __name__ == '__main__':
    app.run(debug=True)
