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

    rapid = gasprices['rapid']
    fast = gasprices['fast']
    standard = gasprices['standard']
    slow = gasprices['slow']

    rapid_metric = Gauge("gas_rapid", "gas rapid", registry=registry)
    rapid_metric.set(rapid)

    fast_metric = Gauge("gas_fast", "gas fast", registry=registry)
    fast_metric.set(fast)

    standard_metric = Gauge("gas_standard", "gas standard", registry=registry)
    standard_metric.set(standard)

    slow_metric = Gauge("gas_slow", "gas slow", registry=registry)
    slow_metric.set(slow)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
