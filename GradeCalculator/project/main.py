from flask import Flask, render_template, request, redirect, session
import os.path
import json
import pandas as pd
from datetime import date
import sqlite3
from db_manipulation import create_db, insert_aluno, insert_grade

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def login_validation(nome, senha):

    conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM alunos WHERE nome = ? AND senha = ?''', (nome, senha))
    user = c.fetchall()

    if user:
        print("Redirecting to grades page")
        return redirect('/grades')
    print("Incorret username or password")
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        nome = request.form.get('UserName')
        senha = request.form.get('Password')
        return login_validation(nome, senha)
    return render_template("signin.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        nome = request.form.get("UserName")
        dre = request.form.get("DRE")
        senha = request.form.get("Password")
        insert_aluno(dre, nome, senha)
        return redirect('/signin')
    return render_template("signup.html")

@app.route("/grades", methods = ['GET', 'POST'])
def grades():
    dre = session.get('dre', None)
    if request.method == "POST":
        t1 = request.form.get("Trabalho1")
        t2 = request.form.get("Trabalho2")
        l1 = request.form.get("Lista1")
        l2 = request.form.get("Lista2")
        l3 = request.form.get("Lista3")
        l4 = request.form.get("Lista4")
        l5 = request.form.get("Lista5")
        insert_grade(dre, t1, t2, l1, l2, l3, l4, l5)
        conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
        c = conn.cursor()
        c.execute('SELECT t1, t2, l1, l2, l3, l4, l5 FROM grades')
        r = c.fetchall()
        if r:
            t1, t2, l1, l2, l3, l4, l5 = r[0]
            print(t1, t2, l1, l2, l3, l4, l5)
            grade = ((t1 + t2) / 2 * 0.8) + (((l1 + l2 + l3 + l4 + l5) / 5) * 0.2)
            if grade >= 7:
                print(f"Parabéns, você foi aprovado com média {grade}")
                c.execute('INSERT INTO grades (np) VALUES (?)', (grade,))
            elif 3 <= grade < 7:
                print(f"Você está de pf com média {grade}")
                c.execute('INSERT INTO grades (np) VALUES (?)', (grade,))
            else:
                print(f"Você foi reprovado com média {grade}")
                c.execute('INSERT INTO grades (np) VALUES (?)', (grade,))
        else:
            print(f"Nenhum registro encontrado para o DRE {dre}")
    return render_template("grades.html")



if __name__ == '__main__':
    create_db()
    app.run(debug=True)