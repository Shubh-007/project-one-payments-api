from flask import Flask, request, jsonify
from flask_cors import CORS
from src.fees import interchange_fee, InvalidAmountError
from src.settlement.rules import settlement_window
from src.legacy.settlement_core import settle

app = Flask(__name__)
CORS(app)


@app.route("/api/fees/interchange", methods=["POST"])
def api_interchange_fee():
    """Calculate interchange fee for a given amount."""
    try:
        data = request.get_json()
        if not data or "amount" not in data:
            return jsonify({"error": "Missing 'amount' field"}), 400

        amount = data["amount"]
        fee = interchange_fee(amount)
        return jsonify({"amount": amount, "fee": fee})
    except InvalidAmountError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/api/settlement/window", methods=["GET"])
def api_settlement_window():
    """Get settlement window (T+1 or T+2) for a region."""
    try:
        region = request.args.get("region", "")
        if not region:
            return jsonify({"error": "Missing 'region' query parameter"}), 400

        window = settlement_window(region)
        return jsonify({"region": region, "window": window})
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/api/settlement/settle", methods=["POST"])
def api_settle():
    """Execute settlement on a batch of transactions."""
    try:
        data = request.get_json()
        if not data or "batch" not in data:
            return jsonify({"error": "Missing 'batch' field"}), 400

        batch = data["batch"]
        result = settle(batch)
        return jsonify({"result": result, "count": len(batch)})
    except Exception as e:
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
