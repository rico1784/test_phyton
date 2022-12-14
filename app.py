from flask import Flask, render_template
from flask import request
from mysql import connector
import os
from Model import users

app = Flask(__name__)
# Gestion des images:
IMG_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER


# Définition des routes
@app.route('/')
def routeAccueil():
    entreeSite_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'entree.jpg')
    return render_template("index.html", user_image=entreeSite_Logo)



@app.route('/login', methods=['POST', 'GET'])
def routeLogin():
    if request.method == 'POST':
        postemail = request.form['postEmail']
        password = request.form['postPassword']
        mail = [postemail, password]
        checkmail= users.processUser.checkUser(mail)
        message = checkmail
        if not postemail and not password:
            return render_template('login.html', message='remplir formulaire')
        elif not postemail and password:
            return render_template('login.html', message='remplir email')
        elif postemail and password:
            if postemail == checkmail[0][1] and password == checkmail[0][2]:
                return render_template('login.html',
                                       message='login OK',
                                       is_connected=True)

            else:
                return render_template('login.html', message='login NOT OK')

    return render_template('login.html')







@app.route('/signup', methods=['POST', 'GET'])
def routeSignup():
    if request.method == "POST":
        message = ''
        addEmail = request.form['addEmail']
        password = request.form['addPassword']
        addCheckPassword = request.form['addCheckPassword']
        if password == addCheckPassword:
            add_user = users.processUser.insertUser(addEmail, password)
            if add_user:
                message = 'Votre compte a été créer'
                return render_template('signup.html', message=message)
        elif password != addCheckPassword:
            message = 'Les mots de passe me correspondent pas'
            return render_template('signup.html', message=message)


    return render_template('signup.html')

