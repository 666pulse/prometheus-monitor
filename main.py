import json
import requests
from flask import Flask, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge
from prometheus_client.core import GaugeMetricFamily

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

    rapid = round(gasprices[0]['price'], 0)
    fast = round(gasprices[1]['price'], 0)
    standard = round(gasprices[2]['price'], 0)
    slow = round(gasprices[4]['price'], 0)

    rapid_metric = Gauge("gas_rapid", "gas rapid", registry=registry)
    rapid_metric.set(rapid)

    fast_metric = Gauge("gas_fast", "gas fast", registry=registry)
    fast_metric.set(fast)

    standard_metric = Gauge("gas_standard", "gas standard", registry=registry)
    standard_metric.set(standard)

    slow_metric = Gauge("gas_slow", "gas slow", registry=registry)
    slow_metric.set(slow)

    ##### coin #####

    coin_collector = CoinCollector()
    registry.register(coin_collector)

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


class CoinCollector():
    def format_metric_name(self):
        return 'os_memory_'

    def collect(self):
        coin_list = ["btc", "eth", "atom", "dot", "bnb", "ftt", "uni", "aave", "comp"]

        for coin in coin_list:
            label = coin + "_price"
            gauge = GaugeMetricFamily(label, '')
            price = self.get_coin_price(coin)
            gauge.add_metric(labels=[], value=price)
            yield gauge


    def get_coin_price(self, coin):
        # https://www.gate.io/api2#ticker

        headers = {'content-type': 'application/json'}
        url = "https://data.gateapi.io/api2/1/ticker/"+coin+"_usdt"

        resp = requests.request("GET", url).json()
        price = float(resp['last'])
        return price


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
