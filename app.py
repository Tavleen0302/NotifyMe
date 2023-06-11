from flask import Flask, redirect, render_template, request, session
from flask_mail import Message, Mail

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # change if u want

app.config['MAIL_SERVER'] = 'smtp.gmail.com' # depending on your mail server like outlook is different then gmail, which I am using
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'email' # the email that will send you the info of the clients
app.config['MAIL_PASSWORD'] = 'apppassword' #setup app password for easier access on this account
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def home():
    if 'form_submitted' in session:
        return redirect('/already-submit')
    return render_template('sendpage.html')

@app.route('/thanks', methods=['POST'])
def emailthanks():
    if 'form_submitted' in session:
        return redirect('/already-submit')

    name = request.form['name']
    email = request.form['email']
    phone = request.form['number']
    message = request.form['message']

    msg = Message('New Contact!', sender='email that the recipent will be getting the data from ', recipients=['email that the sender will send too'])#your email where u want all the info to go is the recipents whereas the sender is the collector of the info
    msg.body = "Name: " + name + "\nEmail: " + email + "\nPhone number: " + phone + "\nMessage: " + message
    mail.send(msg)

    session['form_submitted'] = True

    return redirect('/thank-you')

@app.route('/already-submit')
def already():
    return render_template('already_submitted.html')

@app.route('/thank-you')
def thank_you():
    if 'form_submitted' not in session:
        return redirect('/')

    return render_template('messagesent.html')
