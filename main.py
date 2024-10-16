from pyexpat.errors import messages

from flask import Flask, session, redirect, render_template, request

app = Flask(__name__)
app.secret_key = 'jrfasefasefgj'
a = []


@app.route('/')
def index():
    if session.get('auth', False) == True:
        return render_template('youraccount.html', a=a, login=session['login'])
    else:
        session.get('auth', False)
        return render_template("mainpage.html")


@app.route('/reg')
def reg():
    log = ' '
    password = ' '
    return render_template("registration.html", log=log, password=password)


@app.route('/save', methods=['POST'])
def save():
    log = request.form['login']
    session.get('login', log)
    password = request.form['password']
    if not log:
        return render_template('registration.html', message='Empty login')

    if not password:
        return render_template('registration.html', log=log, message='Empty password')
    x = {'login': log, 'password': password, 't': []}
    a.insert(0, x)
    session['auth'] = True
    session['login'] = log
    return redirect('/')


@app.route('/login')
def login():
    log = ''
    password = ''
    return render_template('login.html', log=log, password=password)


@app.route('/auth', methods=['POST'])
def auth():
    log = request.form.get('login', False)
    password = request.form.get('password', False)

    print(log)

    if not log:
        return render_template('emptyregistration.html', title='REGISTRATION',
                               message='Укажите логин', password=password)

    if not password:
        return render_template('emptyregistration.html', title='REGISTRATION',
                               message='Укажите пароль', log=log)
    session.get('login', log)

    for i in a:
        if i['login'] == log and i['password'] == password:
            session['auth'] = True
            session['login'] = log
            return redirect('/')
        return render_template('loginerror.html', log=log, password=password)

    for i in a:
        if i['login'] == log and i['password'] == password:
            session['auth'] = True
            session['login'] = log
            return redirect('/')
    return render_template('loginerror.html', log=log, password=password)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/text')
def text():
    return render_template("text.html")


@app.route('/write', methods=["POST"])
def write():
    t = request.form.get('text', False)
    name = request.form.get('name', False)
    if not name:
        return render_template('emptynote.html', title='Добавление заметки',
                               message='Укажите название заметки', text=text)

    if not t:
        return render_template('emptynote.html', title='Добавление заметки',
                               message='Укажите текст заметки', name=name)
    c = {'name': name, 'text': t}
    for i in a:
        if i['login'] == session['login']:
            i['t'].insert(0, c)

    return redirect('/')


@app.route('/<int:id>/red')
def red(id):
    return render_template("edit.html", id=id, a=a, login=session['login'])


@app.route('/<int:id>/save', methods=["POST"])
def sav(id):
    t = request.form.get('text')
    name = request.form.get('name')
    for i in a:
        if i['login'] == session['login']:
            i['t'][id]['text'] = t
            i['t'][id]['name'] = name

    return redirect('/')


@app.route('/<int:id>/del')
def delite(id):
    for i in a:
        if i['login'] == session['login']:
            del i['t'][id]
    return redirect('/')


app.run(debug=True)
