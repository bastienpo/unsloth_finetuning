"""Flask app to serve the API endpoints."""

import datetime

from flask import Blueprint, Flask, abort, jsonify, request
from llama_cpp import Llama

app = Flask(__name__)

api_v1 = Blueprint("api_v1", __name__)

llm = Llama.from_pretrained(
    "bastienp/Gemma-2-2B-it-JSON-data-extration",
    filename="*Q4_K_M.gguf",
    verbose=False,
)


@api_v1.route("/health", methods=["GET"])
def ready() -> tuple[dict, int]:
    """GET request to check if the server is ready."""
    return jsonify(
        {
            "status": "OK",
            "lastChecked": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        },
    ), 200


@api_v1.route("/chat/completions", methods=["POST"])
def completions() -> tuple[dict, int]:
    """POST request to get completions for a given prompt."""
    if not request.is_json:
        abort(400, "Request must be JSON in json format")

    # Check if the request is a valid JSON
    try:
        data = request.get_json(silent=True)
    except ValueError as e:
        abort(400, f"Invalid JSON: {e}")

    if "query" not in data:
        abort(400, "Request must contain a query field")

    start = datetime.datetime.now(tz=datetime.UTC)

    res = llm.create_completion(prompt=data["query"], max_tokens=248)

    end = datetime.datetime.now(tz=datetime.UTC)

    return jsonify(
        {
            "response": str.strip(res["choices"][0]["text"]),
            "duration": (end - start).total_seconds(),
            "usage_metadata": res["usage"],
        }
    ), 200


app.register_blueprint(api_v1, url_prefix="/api/v1")
