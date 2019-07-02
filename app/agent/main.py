import pymongo
import requests
import time
from collections import OrderedDict
from hashlib import sha512

API_URL = 'https://api.coinmarketcap.com/v1/ticker/'


def get_db_connection(uri):
    """Define la conexion a la base de datos"""
    client = pymongo.MongoClient(uri)
    return client.cryptongo
    
def get_cryptocurrencies_from_api():
    """De la API de CoinMarketCap se obtiene los documentos desde una posición inicial."""
    r = requests.get(API_URL)
    if r.status_code == 200:
        result = r.json()
        return result
    raise Exception('Api Error')

def first_element(elements):
    return elements[0]

def get_hash(value):
    return sha512(value.encode('utf-8')).hexdigest()

def get_ticker_hash(ticker_data):
    ticker_data = OrderedDict(sorted(ticker_data.items(), key=first_element))
    
    # Se concatena en un string todos los valores ordenados del diccionario.
    ticker_value = ''
    for _, value in ticker_data.items():
        ticker_value += str(value)
    return get_hash(ticker_value)

def remove_element_dictionary(dictionary, key):
    """
    Un diccionario puede ser dinámico, por lo cuál se utiliza este método para eliminar un elemento del mismo.
    :param dictionary:
    :param key:
    :return: Diccionario con el elemento eliminado.
    """

    r = dict(dictionary)
    #del r[key]
    return r

def check_if_exists(connection, ticker_hash):
    """Verifica si la información ya existe en la BD (por medio de un hash).
    La BD almacenará un historico de las criptomonedas."""

    if connection.tickers.find_one({'ticker_hash': ticker_hash}):
        return True
    return False

def save_ticker(connection, ticker_data=None):
    """Almacena el documento en la BD siempre y cuando no exista.""" 
    #evita operaciones si no existe informacion.
    if not ticker_data:
        return False

    ticker_hash = get_ticker_hash(ticker_data)

    if check_if_exists(connection, ticker_hash):
        return False
        
    #ticker_data['ticker_hash'] = get_ticker_hash(ticker_data)
    ticker_data['ticker_hash'] = ticker_hash

    # Almacena el documento en la BD de Mongo por medio de insertOne()
    connection.tickers.insert_one(ticker_data)
    return True

if __name__ == "__main__":
    while True:
        print("Guardando información en Mongo-Crypto")
        connection = get_db_connection('mongodb://mongo-crypto:27017/')
        tickers = get_cryptocurrencies_from_api()
        #print(tickers)

        for ticker in tickers:
            save_ticker(connection, ticker)
        time.sleep(240)