"""Example of making an API call to the server."""

import json
from typing import Any

import requests
from pydantic import BaseModel


class Requirement(BaseModel):
    description: str
    tags: list[str]


JSON_PROMPT = """Below is a text paired with input that provides further context. Write JSON output that matches the schema to extract information.

### Input:
{}

### Schema:
{}

### Response:
"""


def make_api_call(
    url: str, query: str, hostname: str = "localhost", port: int = "5000"
) -> dict[str, Any]:
    """Make an API call to the specified endpoint.

    Args:
        url (str): The endpoint to make the API call to.
        query (str): The query to send to the endpoint.
        hostname (str): The hostname of the server.
        port (int): The port of the server.

    Returns:
        dict[str, Any]: The JSON response from the server.
    """
    response = requests.post(
        f"http://{hostname}:{port}/{url}",
        json={
            "query": query,
        },
    )

    return response.json()


if __name__ == "__main__":
    prompt = JSON_PROMPT.format(
        "A car is a vehicle that has four wheels and an engine.",
        str(Requirement.model_json_schema()),
    )

    res = make_api_call(url="api/v1/chat/completions", query=prompt)

    # parse the json response
    print(json.dumps(res["response"]))
