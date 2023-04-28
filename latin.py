#!/usr/bin/env python

import re
from pywords.matchfilter import MatchFilter
import pywords.utils as pwutils
from typing import Optional, Dict, Any


class LatinParser:
    vocab = {
        "all": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "X"],
        "beginner": ["A", "B", "C"],
        "common": ["C", "D"],
        "intermediate": ["D", "E"],
        "advanced": ["F", "G", "H", "I", "X"],
    }

    def __init__(self, corpus: str = "", frequency: str = "all") -> None:
        self.corpus = corpus
        self.frequency = frequency.lower().strip()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    def verbs(self) -> list[Dict[str, str]]:
        def split_verb(verb_string: str) -> Dict[str, str]:
            """
            Splits a verb string into its components:
            word, conjugation, transitivity, and definitions.
            """
            regex_verb = r"(.+?)\s*\[(\d+|\w+)]\s*(vi|tr|vt|irreg)?\s*(.+)"

            if (match := re.match(regex_verb, verb_string)) is not None:
                definitions = match.group(4).strip()
                definitions = (
                    definitions[:-1]
                    if definitions.endswith(";")
                    else definitions
                )

                return {
                    "word": match.group(1).strip(),
                    "conjugation": match.group(2).strip(),
                    "transitivity": (match.group(3) or "irreg").strip(),
                    "definitions": "".join(
                        (f"{d.strip()}\r\n" for d in definitions.split(";"))
                    ),
                }

            raise ValueError(f"Invalid verb string: {verb_string}")

        verbs, _ = pwutils.get_vocab_list(
            self.corpus,
            filt=MatchFilter(
                parts_of_speech=["V"], frequencies=self.vocab[self.frequency]
            ),
        )

        return [split_verb(v) for v in verbs]

    def nouns(self) -> list[Optional[Dict[str, Any]]]:
        def split_noun(word: str) -> Optional[Dict[str, Any]]:
            """
            Splits a noun entry into its components:
            word, gender, & definitions.
            """
            noun = re.split("(neut.|masc.|fem.)", word)

            if len(noun) != 3:
                return None

            return {
                "word": noun[0],
                "gender": noun[1],
                "definitions": "".join(
                    f"{d.strip()}\r\n" for d in noun[2].split(";")
                ),
            }

        nouns, _ = pwutils.get_vocab_list(
            self.corpus,
            filt=MatchFilter(
                parts_of_speech=["N"], frequencies=self.vocab[self.frequency]
            ),
        )

        return [split_noun(n) for n in nouns]
