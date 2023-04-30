#!/usr/bin/env python

import argparse
from typing import Optional, Dict, Any
from src.anki import add_anki_card, add_anki_deck
from src.plainbook import load_paragraphs, extract_gutenberg_body
from src.latin_parser import LatinParser


def main() -> None:
    """
    Main routine.
        - Load paragraphs from specified source text.
        - Extract words from source text.
        - Build Anki cards and save them to specified deck.
    """
    # Load text by number of specified paragraphs
    # - TODO: properly parse Project Gutenberg texts without modification
    if paragraphs := load_paragraphs(DOCUMENT, start=START, num=COUNT):

        # Parse Latin text into parts of speech, by frequency,
        # and add words to Anki deck
        # - TODO: finish the remaining parts of speech
        with LatinParser(corpus=paragraphs, frequency=FREQ) as parser:
            verbs = parser.verbs()
            nouns = parser.nouns()

            if verbs or nouns:
                add_anki_deck(TITLE)

            if verbs:
                for v in verbs:
                    if v:
                        fields = {"Front": v["definitions"], "Back": v["word"]}
                        add_anki_card(
                            TITLE, "Basic", fields, v["transitivity"]
                        )

            if nouns:
                for n in nouns:
                    if n:
                        fields = {"Front": n["definitions"], "Back": n["word"]}
                        add_anki_card(TITLE, "Basic", fields, n["gender"])


def _parse_args() -> Dict[str, bool]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--document", help="Load document to parse.")
    parser.add_argument("-t", "--title", help="Title for Anki deck.")
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        help="Starting paragraph index (starting from 1).",
        default=1,
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="Number of paragraphs to parse.",
        default=None,
    )
    parser.add_argument(
        "-f",
        "--frequency",
        choices=["all", "beginner", "common", "intermediate", "advanced"],
        help="Specify the frequency level of words to filter.",
        default="beginner",
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = _parse_args()

    DOCUMENT = args.pop("document")
    TITLE = args.pop("title")
    FREQ = args.pop("frequency")
    START = args.pop("start")
    COUNT = args.pop("count")

    main()
