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

    gasprices = get_gasprices()

    # https://eth-converter.com/
    gwei = 1000000000
    rapid = gasprices['rapid']/gwei
    fast = gasprices['fast']/gwei
    standard = gasprices['standard']/gwei
    slow = gasprices['slow']/gwei

    rapid_metric = Gauge("gas_rapid", "gas rapid", registry=registry)
    rapid_metric.set(rapid)

    fast_metric = Gauge("gas_fast", "gas fast", registry=registry)
    fast_metric.set(fast)

    standard_metric = Gauge("gas_standard", "gas standard", registry=registry)
    standard_metric.set(standard)

    slow_metric = Gauge("gas_slow", "gas slow", registry=registry)
    slow_metric.set(slow)

    btc_price = get_btc_price()
    btc_price_metric = Gauge("btc_price", "btc price", registry=registry)
    btc_price_metric.set(btc_price)

    eth_price = get_eth_price()
    eth_price_metric = Gauge("eth_price", "eth price", registry=registry)
    eth_price_metric.set(eth_price)

    icp_price = get_icp_price()
    icp_price_metric = Gauge("icp_price", "icp price", registry=registry)
    icp_price_metric.set(icp_price)

    ftm_price = get_ftm_price()
    ftm_price_metric = Gauge("ftm_price", "ftm price", registry=registry)
    ftm_price_metric.set(ftm_price)

    sol_price = get_sol_price()
    sol_price_metric = Gauge("sol_price", "sol price", registry=registry)
    sol_price_metric.set(sol_price)

    avax_price = get_avax_price()
    avax_price_metric = Gauge("avax_price", "avax price", registry=registry)
    avax_price_metric.set(avax_price)

    atom_price = get_atom_price()
    atom_price_metric = Gauge("atom_price", "atom price", registry=registry)
    atom_price_metric.set(atom_price)

    dot_price = get_dot_price()
    dot_price_metric = Gauge("dot_price", "dot price", registry=registry)
    dot_price_metric.set(dot_price)

    dydx_price = get_dydx_price()
    dydx_price_metric = Gauge("dydx_price", "dydx price", registry=registry)
    dydx_price_metric.set(dydx_price)

    # ksm_price = get_ksm_price()
    # ksm_price_metric = Gauge("ksm_price", "ksm price", registry=registry)
    # ksm_price_metric.set(ksm_price)

    return registry

def get_gasprices():
    '''
      {
        "code": 200,
        "data": {
            "rapid": 49000000000,
            "fast": 39512143433,
            "standard": 38512143433,
            "slow": 38512143433,
            "timestamp": 1631956024923
        }
      }
    '''

    headers = {'content-type': 'application/json'}
    url = "https://www.gasnow.org/api/v3/gas/price"

    payload = None
    resp = requests.request("GET", url, headers=headers, data=payload).json()

    gasprices = resp['data']

    return gasprices

def get_coin_price(coin):
    # https://www.gate.io/api2#ticker

    headers = {'content-type': 'application/json'}
    url = "https://data.gateapi.io/api2/1/ticker/"+coin+"_usdt"

    resp = requests.request("GET", url).json()
    price = float(resp['last'])
    return price

def get_dot_price():
    price = get_coin_price("dot")
    return price

def get_atom_price():
    price = get_coin_price("atom")
    return price

def get_avax_price():
    price = get_coin_price("avax")
    return price

def get_ftt_price():
    price = get_coin_price("ftt")
    return price

def get_sol_price():
    price = get_coin_price("sol")
    return price

# def get_ksm_price():
#     price = get_coin_price("ksm")
#     return price

# def get_srm_price():
#     price = get_coin_price("srm")
#     return price

# def get_ray_price():
#     price = get_coin_price("ray")
#     return price

def get_dydx_price():
    price = get_coin_price("dydx")
    return price

def get_ftm_price():
    price = get_coin_price("ftm")
    return price

def get_btc_price():
    price = get_coin_price("btc")
    return price

def get_eth_price():
    price = get_coin_price("eth")
    return price

def get_icp_price():
    price = get_coin_price("icp")
    return price

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
