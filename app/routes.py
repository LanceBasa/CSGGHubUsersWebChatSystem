from app import app
from flask import render_template, request, session, redirect, url_for
from pydantic import BaseModel, validator, ValidationError
import secrets

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chatbox/')
def chat():
    return render_template('chatbox.html')


@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/registerLogin/', methods=["GET","POST"])
def registerLogin():
    if request.method == 'POST':
        if 'login' in request.form:
            return render_template('profile.html')

        elif 'register' in request.form:
            return render_template('chatbox.html')

            
    return render_template('registerLogin.html')
    




if __name__ =='__main__':
    app.run(debug=True)