from flask import Flask, render_template, request, redirect
import os.path
import json
import pandas as pd

app = Flask(__name__)

#ao rodar a aplicacao devera antes ser feita uma verificacao em respeito se há um arquivo txt contendo username, senha e dre
#caso false sera criado um arquivo "dados.txt" onde será feito um append por meio de open("dados.txt", "r")
#aplicacao terá quatro telas, uma de homepage para seleção de cadastro e login (botoes)
#

data_base = "EEL670_ProgrammingLanguage/LetterSender/project/dados.json"
letter_sender = "EEL670_ProgrammingLanguage/LetterSender/project/letter.txt"

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
    with open(data_base, "r+") as f:
        for i in range(len(data_base_json.index)):
            if data_base_json["User"][i]["DRE"] == dre:
                print("User already exists")
                return render_template("singin.html")
            else:
                file_data = json.load(f)
                file_data["User"].append(data_base_infos)
                f.seek(0)
                json.dump(file_data, f, indent=4)
                print("User was created successfully")
                return render_template("singin.html")
        i += 1


@app.route('/signup', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        nome = request.form.get("UserName")
        dre = request.form.get("DRE")
        senha = request.form.get("Password")
        return data_search(data_base, nome, senha, dre)
    return render_template("singup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        nome = request.form.get('username')
        senha = request.form.get('password')
        return data_search(data_base, nome, senha)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        nome = request.form.get("UserName")
        dre = request.form.get("DRE")
        senha = request.form.get("Password")
        return data_search(data_base, nome, senha, dre)
        return redirect('/')
    return render_template("singup.html")


if __name__ == '__main__':
    if os.path.isfile(data_base) == True:
        print("DataBase is already loaded")
    else:
        with open(data_base, "w") as f:
            f.write(json.dumps(data_base_infos, indent = 4))
        print("DataBase was successfully created")
    app.run(debug=True)