
from flask import Flask, jsonify

app = Flask(__name__)

# Temporary in-memory product data.
# We will introduce a database in a later phase.
products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Keyboard", "price": 1500},
    {"id": 3, "name": "Mouse", "price": 700},
]


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
