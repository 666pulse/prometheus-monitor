const express = require("express");
const client = require("prom-client");
const memoryUsage = require("process").memoryUsage;

const PORT = process.env.PORT || 3000;

const app = express();
const metric_label_enum = {
  PATH: "path",
  METHOD: "method",
  STATUS_CODE: "status_code",
};

// * CREATES A NEW CLASS FOR ASSIGNING LABELS TO VARIOUS METRICS
class MetricLabelClass {
  constructor(method, pathname, statusCode) {
    this.method = method;
    this.path = pathname;
    this.status_code = statusCode;
  }
}
// * REGISTERS A NEW PROMETHEUS CLIENT
const register = new client.Registry();

// * The http_response rate histogram for measuring the response rates for each http request
const http_response_rate_histogram = new client.Histogram({
  name: "node_http_duration",
  labelNames: [
    metric_label_enum.PATH,
    metric_label_enum.METHOD,
    metric_label_enum.STATUS_CODE,
  ],
  help: "The duration of HTTP requests in seconds",
  buckets: [
    0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3,
    1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 10,
  ],
});

// * The node_js memory guage for measuring the memory of the application in use
const nodejs_memory = new client.Gauge({
  name: "node_memory_usage_bytes",
  help: "Current memory usage of the Node.js process in bytes",
});

client.collectDefaultMetrics({
  // register: register,
  prefix: "node_", // * Prefixes the default app metrics name with the specified string
});

// register.registerMetric(http_response_rate_histogram);
register.registerMetric(nodejs_memory);

app.use((req, res, next) => {
  const req_url = new URL(req.url, `http://${req.headers.host}`);
  const endTimer = http_response_rate_histogram.startTimer();

  const used_memory_before = memoryUsage().rss;

  const original_res_send_function = res.send;

  const res_send_interceptor = function (body) {
    const timer = endTimer(
      new MetricLabelClass(req.method, req_url.pathname, res.statusCode),
    );

    console.log(`HTTP request took ${timer} seconds to process`);

    const used_memory_after = memoryUsage().rss;

    nodejs_memory.set(used_memory_after - used_memory_before);

    original_res_send_function.call(this, body);
  };

  res.send = res_send_interceptor;
  next();
});

app.get("/metrics", async (req, res, next) => {
  res.setHeader("Content-type", register.contentType);
  res.send(await register.metrics());
  next();
});

app.get("/", (req, res, next) => {
  res.setHeader("Content-type", "text/html");
  res.send(`<a href=' http://localhost:${PORT}/metrics'>metrics</a>`);
  next();
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
