
import time

from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Application version
APP_VERSION = "1.1.0"

# Temporary in-memory product data
products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Keyboard", "price": 1500},
    {"id": 3, "name": "Mouse", "price": 700},
]

# 1. Count HTTP requests
REQUEST_COUNT = Counter(
    "shopsphere_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

# 2. Measure HTTP request duration
REQUEST_LATENCY = Histogram(
    "shopsphere_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

# 3. Count failed HTTP responses
ERROR_COUNT = Counter(
    "shopsphere_http_errors_total",
    "Total number of HTTP error responses",
    ["method", "endpoint", "status"],
)


@app.before_request
def start_timer():
    # Do not count Prometheus scraping its own metrics endpoint
    if request.path != "/metrics":
        request.start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        endpoint = (
            request.url_rule.rule
            if request.url_rule
            else "unmatched"
        )

        method = request.method
        status = str(response.status_code)

        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status,
        ).inc()

        duration = time.perf_counter() - request.start_time

        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)

        if response.status_code >= 400:
            ERROR_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=status,
            ).inc()

    return response


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/products")
def get_products():
    return jsonify(products), 200


@app.get("/products/<int:product_id>")
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product), 200

    return jsonify({"error": "Product not found"}), 404


@app.get("/version")
def get_version():
    return jsonify({
        "application": "ShopSphere",
        "version": APP_VERSION
    }), 200


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
