import math
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/factorial")
def factorial():
    raw = request.args.get("number")
    if raw is None:
        return jsonify(error="Query parameter 'number' is required"), 400
    try:
        number = int(raw)
    except ValueError:
        return jsonify(error="'number' must be an integer"), 400
    if not 0 <= number <= 200:
        return jsonify(error="'number' must be between 0 and 200"), 400
    return jsonify(number=number, factorial=math.factorial(number))


@app.get("/health")
def health():
    return jsonify(status="ok")
