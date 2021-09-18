# Gas Monitor

## Prometheus

### config 

```yml
# my global config
global:
  scrape_interval:     20s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 20s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'gas'

    static_configs:
    - targets: ['localhost:8000']
```    

### run 

```shell
prometheus --web.listen-address 0.0.0.0:9090

python3 ./main.py
```

## Grafana

### install

```
wget https://dl.grafana.com/oss/release/grafana_8.1.4_amd64.deb

sudo dpkg -i grafana_8.1.4_amd64.deb
```
### change port

```ini
; /etc/grafana/grafana.ini
[server]
http_port=xxxx
```
### Start the server

```shell
sudo service grafana-server start

sudo service grafana-server status
```

---

Refer:

https://opensource.com/article/19/4/weather-python-prometheus

https://grafana.com/docs/grafana/latest/installation/

https://grafana.com/docs/grafana/latest/administration/configuration/#comments-in-ini-files

<!-- https://api.weather.gov/gridpoints/RAH/73,57/forecast/hourly -->
