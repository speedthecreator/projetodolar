import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='./templates')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/calculate", methods=['POST'])
def calculate():
    product_value = float(request.form['product_value'])
    freight_value = float(request.form['freight_value'])
    service_value = float(request.form['service_value'])
    valor_brasil = float(request.form['valor_brasil'])
    icms_value = float(request.form['icms_value'])
    valor_caixa = float(request.form['valor_caixa'])

    def taxaFrete(freight_value):
        if freight_value <= 45:
            taxa = 3.99 + freight_value
        elif freight_value <= 110:
            taxa = 7.99 + freight_value
        else:
            taxa = 12.99 + freight_value
        return taxa

    taxa_frete = taxaFrete(freight_value) + valor_caixa
    total_value = product_value + \
        taxaFrete(freight_value) + service_value + icms_value + valor_caixa
    tax = product_value * 0.6
    valor_junto = tax + total_value
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=BRL&from=USD&amount={valor_junto}"

    headers = {"apikey": "TgXUckEKo83Eu3OIqartNeMODXkaFF8S"}

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        exchange_rate = response.json()['result']
        tax = round(tax, 2)
        icms_value = round(icms_value, 2)
        service_value = round(service_value, 2)
        product_value = round(product_value, 2)
        taxa_frete = round(taxa_frete, 2)
        valor_brasil = round(valor_brasil, 2)
        valor_junto = round(valor_junto, 2)
        final_value = round(exchange_rate, 2)
        dolar = round(final_value / valor_junto, 2)
        diferenca = round(final_value - valor_brasil, 2)
        return render_template('result.html', final_value=final_value, valor_junto=valor_junto, dolar=dolar, valor_brasil=valor_brasil, diferenca=diferenca, taxa_frete=taxa_frete, product_value=product_value, service_value=service_value, tax=tax, icms_value=icms_value)
    else:
        return "Erro ao obter a cotação do dólar"


if __name__ == '__main__':
    app.run(debug=False)