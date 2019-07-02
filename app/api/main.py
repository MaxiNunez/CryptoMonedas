import pymongo
from flask import Flask, jsonify, request, render_template, url_for, redirect

def get_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo

app = Flask(__name__)
connection = get_connection('mongodb://mongo-crypto:27017/')

def get_rank_top20():
    params = {}
    name = request.args.get('name', '')

    if name:
        params.update({'name': name})
    cursor = connection.data.find(params, {'_id': 0, 'ticker_hash': 0}).limit(20)
    print(cursor)

    return list(cursor)

def get_documents():
    params = {}
    name = request.args.get('name','')
    limit = int(request.args.get('limit',0))

    if name:
        params.update({'name':name})
    
    cursor = connection.data.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)
    
    return list(cursor)

@app.route("/")
def index():
    tickers = get_documents()
    return render_template("index.html", tickers = tickers)

@app.route('/tickers',methods=['GET'])
def tickers():
    t = get_documents()
    return render_template("tickers.html", t = t)

@app.route('/top20', methods=['GET'])
def top20():
    top = get_rank_top20()
    return render_template("top20.html",top = top)

@app.route('/mostrarDatos')
def mostrarDatos():
    name = request.args.get('name')
    cryptoMoneda = connection.data.find({'name':name}).limit(1)
    return render_template("mostrarDatos.html", cryptoMoneda = cryptoMoneda)

@app.route('/eliminar', methods=['GET'])
def eliminar():
    name = request.args.get('name')
    connection.data.delete_many({'name':name})
    return redirect("/")

if __name__ == "__main__":
    app.run()
