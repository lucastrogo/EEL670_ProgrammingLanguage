import sqlite3
from flask import redirect


def get_dre():
    conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
    c = conn.cursor()

    c.execute('SELECT dre FROM alunos')

    dre_list = [row[0] for row in c.fetchall()]

    conn.close()

    if dre_list:
        return dre_list
    else:
        print("Nenhum registro encontrado para o DRE")
        return []



def create_db():

    conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
    c = conn.cursor()

    c.execute('''
            CREATE TABLE IF NOT EXISTS alunos
            ([dre] STRING PRIMARY KEY, [nome] STRING, [senha] STRING )''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS grades
            ([dre] STRING, [t1] INTEGER, [t2] INTEGER, [l1] INTEGER, [l2] INTEGER, [l3] INTEGER, [l4] INTEGER, [l5] INTEGER, [np] FLOAT);
            ''')

    conn.commit()

def insert_aluno(dre, nome, senha):

    conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
    c = conn.cursor()

    c.execute('SELECT dre FROM alunos WHERE dre=?', (dre,))
    existing_dre = c.fetchone()

    if existing_dre:
        print(f'O DRE {dre} já está cadastrado.')
    else:
        c.execute('INSERT INTO alunos (dre, nome, senha) VALUES (?, ?, ?)', (dre, nome, senha))
        conn.commit()
        print(f'Aluno {nome} inserido com sucesso!')

    conn.close()

def insert_grade(dre, t1, t2, l1, l2, l3, l4, l5):

    conn = sqlite3.connect('EEL670_ProgrammingLanguage/GradeCalculator/project/grade.db')
    c = conn.cursor()

    c.execute('''
            INSERT INTO grades (dre, t1, t2, l1, l2, l3, l4, l5)
            VALUES (?,?,?,?,?,?,?,?)
            ''', (dre, t1, t2, l1, l2, l3, l4, l5))

    conn.commit()

