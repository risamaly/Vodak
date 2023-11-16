from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

registrace_seznam = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('prvni_stranka.html', registrace=registrace_seznam), 200

@app.route('/druha_stranka', methods=['GET', 'POST'])
def druha_stranka():
    return render_template('druha_stranka.html', zprava="Tajná zpráva.."), 200

@app.route('/registrace', methods=['GET', 'POST'])
def registrace():
    if request.method == 'POST':
        je_plavec = request.form.get('je_plavec')
        nick = request.form.get('nick')
        kanoe_kamarad = request.form.get('kanoe_kamarad')

        # Kontrola duplicity nicku
        if any(registrace['nick'] == nick for registrace in registrace_seznam):
            return jsonify({"chyba": "Nick je již používán."}), 400

        # Kontrola platnosti nicku
        if not re.match("^[A-Za-z0-9]{2,20}$", nick):
            return jsonify({"chyba": "Nick je neplatný."}), 400

        # Kontrola plaveckých schopností
        if je_plavec != '1':
            return jsonify({"chyba": "Osoba není plavec."}), 400

        # Kontrola platnosti jména kamaráda
        if kanoe_kamarad and not re.match("^[A-Za-z0-9]{2,20}$", kanoe_kamarad):
            return jsonify({"chyba": "Jméno kamaráda je neplatné."}), 400

        registrace_data = {"nick": nick, "je_plavec": je_plavec, "kanoe_kamarad": kanoe_kamarad}
        registrace_seznam.append(registrace_data)
        return jsonify({"zprava": "Registrace úspěšná.", "data": registrace_data}), 200

    return render_template('registrace.html'), 200

@app.route('/api/check-nickname/<nick>', methods=['GET'])
def check_nickname(nick):
    is_available = not any(registrace['nick'] == nick for registrace in registrace_seznam)
    return jsonify({"isAvailable": is_available})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

