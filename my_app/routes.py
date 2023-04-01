from my_app import app
from flask import request, render_template
from flask import redirect, url_for
from flask import g
import random

enigmes = {}
enigmes['id1'] = {'question': 'Quel est le nom du cheval d\'Alexandre ?', 'reponse': 'Bucéphale'}
enigmes['id2'] = {'question': 'Quel est le nom du deuxième homme à avoir marché sur la lune ?', 'reponse': 'Aldrin'}
enigmes['id3'] = {'question': 'Quel est le nom du premier empereur romain ?', 'reponse': 'Auguste'}
enigmes['id4'] = {'question': 'Quel est le nom de l\'auteur qui a décrit les 3 lois de la robotique en S-F ?', 'reponse': 'Asimov'}
enigmes['id5'] = {'question': 'Quelle est la formule chimique de l\'acide sulfurique ?', 'reponse': 'H2SO4'}

id = 6
#print(*enigmes)
key = ''
reponse=''

def toto():
    return 'bonjour'
@app.route("/", methods=['GET'])
def affiche_enigme():
    global key
    # Si la clé est vide, sélectionner une énigme.  Sinon, reproposer la dernière énigme.
   # if request.args.get('reponse'):
       # reponse = request.args.get('reponse')
   #     return redirect(url_for('envoyer_resultat'))
    if not key:
        key = random.choice(list(enigmes))
    enigme = enigmes[key]["question"]
    return render_template("question.html",enigme = enigme)

@app.route("/reponse", methods=['POST'])
def verifier_reponse():
    global reponse
    global key
    reponse = request.form['reponse']
    #if reponse == enigmes[key]["reponse"]:
    #    key = ''
    #    return "Bravo, tu es un chef !"
    #else:
    #    return redirect('/', code=302)
    g.reponse = reponse
    return toto()


def resultat():
    global key
    if g.reponse == enigmes[key]["reponse"]:
        key = ''
        return "Bravo, tu es un chef !"
    else:
        return "bonjour"
        #return redirect('/', code=302)
