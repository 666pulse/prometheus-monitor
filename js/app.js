const express = require("express");
const client = require("prom-client");

const PORT = process.env.PORT || 3000;

const app = express();

function getRandomInt(min, max) {
  const minCeiled = Math.ceil(min);
  const maxFloored = Math.floor(max);
  return Math.floor(Math.random() * (maxFloored - minCeiled) + minCeiled);
}

const register = new client.Registry();

// * The node_js memory guage for measuring the memory of the application in use
const nodejs_memory = new client.Gauge({
  name: "node_memory_usage_bytes",
  help: "Current memory usage of the Node.js process in bytes",
});

client.collectDefaultMetrics({
  // register: register,
  prefix: "node_",
});

register.registerMetric(nodejs_memory);

app.use((req, res, next) => {
  nodejs_memory.set(getRandomInt(10, 1000));
  next();
});

app.get("/metrics", async (req, res, next) => {
  res.setHeader("Content-type", register.contentType);
  res.send(await register.metrics());
  next();
});

app.get("/", (req, res, next) => {
  res.setHeader("Content-type", "text/html");
  res.send(`<a href='http://localhost:${PORT}/metrics'>metrics</a>`);
  next();
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});
