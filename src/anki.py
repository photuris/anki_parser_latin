#!/usr/bin/env python

import json
import urllib.request

HOSTNAME = "localhost"
PORT = 8765


def call_anki_connect(action, **params):
    """Call AnkiConnect API."""

    def request(action, **params):
        return {"action": action, "params": params, "version": 6}

    request_json = json.dumps(request(action, **params)).encode("utf-8")

    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request(f"http://{HOSTNAME}:{PORT}", request_json)
        )
    )

    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")

    if response["error"] is not None:
        raise Exception(response["error"])

    return response["result"]


def add_anki_card(deck, model, fields, tags):
    call_anki_connect(
        "addNote",
        note={
            "deckName": deck,
            "modelName": model,
            "fields": fields,
            "tags": tags,
        },
    )


def add_anki_deck(deck):
    call_anki_connect("createDeck", deck=deck)
