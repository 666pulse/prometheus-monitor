import json
import requests
from flask import Flask, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge

app = Flask(__name__)

@app.route('/')
def home():
    return Response('prometheus server\n', mimetype='text/plain')

@app.route('/metrics')
def metrics():
    registry = get_metrics()
    return Response(generate_latest(registry), mimetype='text/plain')

def get_metrics():
    registry = CollectorRegistry()

    ##### gas #####

    gasprices = get_gasprices()

    rapid = round(gasprices[0]['maxFeePerGas'], 0)
    fast = round(gasprices[1]['maxFeePerGas'], 0)
    standard = round(gasprices[2]['maxFeePerGas'], 0)
    slow = round(gasprices[4]['maxFeePerGas'], 0)

    rapid_metric = Gauge("gas_rapid", "gas rapid", registry=registry)
    rapid_metric.set(rapid)

    fast_metric = Gauge("gas_fast", "gas fast", registry=registry)
    fast_metric.set(fast)

    standard_metric = Gauge("gas_standard", "gas standard", registry=registry)
    standard_metric.set(standard)

    slow_metric = Gauge("gas_slow", "gas slow", registry=registry)
    slow_metric.set(slow)

    ##### coin #####

    btc_price = get_btc_price()
    btc_price_metric = Gauge("btc_price", "btc price", registry=registry)
    btc_price_metric.set(btc_price)

    eth_price = get_eth_price()
    eth_price_metric = Gauge("eth_price", "eth price", registry=registry)
    eth_price_metric.set(eth_price)

    atom_price = get_atom_price()
    atom_price_metric = Gauge("atom_price", "atom price", registry=registry)
    atom_price_metric.set(atom_price)

    dot_price = get_dot_price()
    dot_price_metric = Gauge("dot_price", "dot price", registry=registry)
    dot_price_metric.set(dot_price)

    ##### exchange #####

    bnb_price = get_bnb_price()
    bnb_price_metric = Gauge("bnb_price", "bnb price", registry=registry)
    bnb_price_metric.set(bnb_price)

    ftt_price = get_ftt_price()
    ftt_price_metric = Gauge("ftt_price", "ftt price", registry=registry)
    ftt_price_metric.set(ftt_price)

    ##### defi #####

    uni_price = get_uni_price()
    uni_price_metric = Gauge("uni_price", "uni price", registry=registry)
    uni_price_metric.set(uni_price)

    aave_price = get_aave_price()
    aave_price_metric = Gauge("aave_price", "aave price", registry=registry)
    aave_price_metric.set(aave_price)

    comp_price = get_comp_price()
    comp_price_metric = Gauge("comp_price", "comp price", registry=registry)
    comp_price_metric.set(comp_price)

    return registry

def get_gasprices():
    # https://docs.ethgas.watch/api
    # https://eth-converter.com/
    # https://doc.upvest.co/reference
    # https://fees.upvest.co/estimate_eth_fees

    headers = {'content-type': 'application/json'}
    url = "https://api.blocknative.com/gasprices/blockprices?chainid=1"

    payload = None
    resp = requests.request("GET", url, headers=headers, data=payload).json()
    gasprices = resp['blockPrices'][0]['estimatedPrices']
    return gasprices

def get_coin_price(coin):
    # https://www.gate.io/api2#ticker

    headers = {'content-type': 'application/json'}
    url = "https://data.gateapi.io/api2/1/ticker/"+coin+"_usdt"

    resp = requests.request("GET", url).json()
    price = float(resp['last'])
    return price

def get_btc_price():
    price = get_coin_price("btc")
    return price

def get_eth_price():
    price = get_coin_price("eth")
    return price

def get_dot_price():
    price = get_coin_price("dot")
    return price

def get_atom_price():
    price = get_coin_price("atom")
    return price

def get_bnb_price():
    price = get_coin_price("bnb")
    return price

def get_ftt_price():
    price = get_coin_price("ftt")
    return price

def get_uni_price():
    price = get_coin_price("uni")
    return price

def get_aave_price():
    price = get_coin_price("aave")
    return price

def get_comp_price():
    price = get_coin_price("comp")
    return price

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
