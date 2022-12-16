from flask import Flask, redirect, url_for, render_template
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
    return render_template("index.html",
                           user_image=entreeSite_Logo)



@app.route('/login', methods=['POST', 'GET'])
def routeLogin():

    if request.method == 'POST':
        postemail = request.form['postEmail']
        password = request.form['postPassword']
        mail = [postemail,password]
        if not postemail:
            return render_template('login.html', message='merci de compléter le formulaire')
        elif not password and postemail:
            return render_template('login.html', message='manque le mot de passe')
        else:
            checkmail= users.processUser.checkUser(mail)
            passuser = checkmail[0][2]
            test= users.processUser.logOK()
            status = test.self.isOk(True)
            if passuser == password:
                return redirect(url_for('routeAccueil', name=status))
            elif passuser != password:
                return render_template('login.html', message='Connexion échouée')

            return render_template('login.html', message='Connexion échouée')
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
                return render_template('login.html', message=message)
        elif password != addCheckPassword:
            message = 'Les mots de passe me correspondent pas'
            return render_template('signup.html', message=message)


    return render_template('signup.html')

