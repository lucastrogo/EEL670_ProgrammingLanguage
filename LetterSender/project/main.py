from flask import Flask, render_template, request, redirect
import os.path
import json
import pandas as pd
from datetime import date
app = Flask(__name__)

#ao rodar a aplicacao devera antes ser feita uma verificacao em respeito se há um arquivo txt contendo username, senha e dre
#caso false sera criado um arquivo "dados.txt" onde será feito um append por meio de open("dados.txt", "r")
#aplicacao terá quatro telas, uma de homepage para seleção de cadastro e login (botoes)
#

data_base = "EEL670_ProgrammingLanguage/LetterSender/project/dados.json"

data_base_infos = {"User":[{
                "UserName": " ",
                "Password": " ",
                "DRE": " "
}]}


def data_search(data_base, nome, senha, dre):
    data_base_infos = {
                "UserName": nome,
                "Password": senha,
                "DRE": dre}
    data_base_json = pd.read_json(data_base)
    for i in range(len(data_base_json.index)):
        if data_base_json["User"][i]["DRE"] == dre:
            print("DRE is already in database, please signin")
            return redirect('/')
    i += 1
    with open(data_base, "r+") as f:
        file_data = json.load(f)
        file_data["User"].append(data_base_infos)
        f.seek(0)
        json.dump(file_data, f, indent=4)
        print("User was created successfully")
        return redirect('/')


def login_validation(nome, senha):
    data_base_json = pd.read_json(data_base)
    for i in range(len(data_base_json.index)):
        print("Essa funcao esta sendo executada")
        if data_base_json["User"][i]["UserName"] == nome and data_base_json["User"][i]["Password"] == senha:
            print("Login was successfully")
            return redirect('/letter')
    i += 1
    print("Incorret username or password")
    return redirect('/')

def save_message(remetente, destinatario, mensagem):
    letter_sender = f"EEL670_ProgrammingLanguage/LetterSender/project/letter{remetente}.txt"
    message = {"Remetente": remetente,
                "Destinatario": destinatario,
                "Mensagem": mensagem,
                "Data": f"{date.today()}"}
    with open(letter_sender, "w") as f:
        f.write(str(message))
    return redirect('/messagesent')
    print("DataBase was successfully created")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/message')
def message_sent():
    return render_template("messagesent.html")

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
        return data_search(data_base, nome, senha, dre)
    return render_template("signup.html")


@app.route("/letter", methods = ['GET', 'POST'])
def letter():
    if request.method == "POST":
        remetente = request.form.get("Remetente")
        destinatario = request.form.get("Destinatario")
        mensagem = request.form.get("Mensagem")
        return save_message(remetente, destinatario, mensagem)
    return render_template("lettersender.html")



if __name__ == '__main__':
    if os.path.isfile(data_base) == True:
        print("DataBase is already loaded")
    else:
        with open(data_base, "w") as f:
            f.write(json.dumps(data_base_infos, indent = 4))
        print("DataBase was successfully created")
    app.run(debug=True)