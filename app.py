from flask import Flask, render_template, request
app = Flask(__name__)

crimes = {
    "randola": {"pena": 0, "multa": 200000, "sem_fianca": True},
    "zaraglion": {"pena": 0, "multa": 200000, "sem_fianca": True},
    "corrupcao": {"pena": 500, "multa": 50000, "sem_fianca": True, "sem_reducao": True},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    tipo_reu = request.form.get('tipo_reu')
    advogado = request.form.get('advogado') == 'sim'
    artigos = request.form.getlist('artigos')

    total_pena = 0
    total_multa = 0
    detalhes = []

    for art in artigos:
        crime = crimes.get(art.lower())
        if not crime:
            detalhes.append(f"- {art}: ❌ Não encontrado")
            continue

        pena = crime["pena"]
        multa = crime["multa"]
        sem_fianca = crime.get("sem_fianca", False)
        sem_reducao = crime.get("sem_reducao", False)

        if not sem_reducao:
            if tipo_reu == "réu primário":
                pena = int(pena * 0.9)
            elif tipo_reu == "réu confesso":
                pena = int(pena * 0.8)
            elif tipo_reu == "réu reincidente":
                pena = int(pena * 1.2)

            if advogado:
                if sem_fianca:
                    pena = int(pena * 0.5)
                else:
                    pena = int(pena * 0.9)

        total_pena += pena
        total_multa += multa
        detalhes.append(f"- {art.replace('_', ' ').capitalize()}: {pena} meses + R${multa:,}")

    return render_template('resultado.html', detalhes=detalhes, total_pena=total_pena, total_multa=total_multa)

if __name__ == '__main__':
    app.run(debug=True)
