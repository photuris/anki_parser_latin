#!/usr/bin/env python


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

    current_paragraph_idx = 0
    current_paragraph = ""
    selected_paragraphs = []

    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                if current_paragraph_idx >= start - 1:
                    selected_paragraphs.append(current_paragraph.strip())

                current_paragraph_idx += 1
                current_paragraph = ""

                if num is not None and len(selected_paragraphs) == num:
                    break
            else:
                current_paragraph += line

        if current_paragraph_idx >= start - 1 and (
            num is None or len(selected_paragraphs) < num
        ):
            selected_paragraphs.append(current_paragraph.strip())

    return "\n\n".join(selected_paragraphs)
