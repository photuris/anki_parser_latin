#!/usr/bin/env python


import re


def extract_gutenberg_body(file_path: str) -> str:
    """
    Extract the body of the text from a Project Gutenberg
    plain text book.

    Args:
        file_path (str): Path to input file.

    Returns:
        str: A string containing the extracted text.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    start_marker = re.search(r"\*{3} START OF", content)
    end_marker = re.search(r"\*{3} END OF", content)

    if start_marker and end_marker:
        # Find the next newline character after the start marker
        start = content.find("\n", start_marker.end())

        # Find the next newline character after "Produced by"
        if produced_by := re.search(r"Produced by", content[start:]):
            start = content.find("\n\n", start + produced_by.end())

        # Find the previous newline character before the end marker
        end = content.rfind("\n", 0, end_marker.start())

        # Find the previous newline character before the
        # "End of (the) Project Gutenberg" line
        if end_of_project_marker := re.search(
            r"End of (the )?Project Gutenberg", content[:end]
        ):
            end = content.rfind("\n", 0, end_of_project_marker.start())

        body = content[start:end]

        return body.strip()

    else:
        return content.strip()


def load_paragraphs(file_path: str, start: int = 1, num: int = None) -> str:
    """
    Reads a plain text file and loads a specified number of paragraphs
    into a memory string, starting at a specified paragraph number.

    Args:
        file_path (str): Path to the input file.
        start (int): The index of the first paragraph to load (starting from 1).
        num (int, optional): The number of paragraphs to load. If not provided,
                             all paragraphs after the start will be loaded.

    Returns:
        str: A string containing the loaded paragraphs.
    """
    if start < 1 or (num is not None and num < 1):
        raise ValueError(
            (
                "Both 'start' and 'num' must be greater than or equal to 1, "
                "or 'num' must be None."
            )
        )

    if text := extract_gutenberg_body(file_path):
        paragraphs = re.split(r"\n{2,}", text)
        start_idx = max(0, start - 1)
        end_idx = start_idx + num if num is not None else None
        selected_paragraphs = paragraphs[start_idx:end_idx]

    return "\n\n".join(selected_paragraphs)
