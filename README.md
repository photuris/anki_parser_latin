# Latin Parser for Anki
Parses Latin text and creates Anki flashcards

## Usage

Parses `De Bello Gallico` and generates Anki cards from the entire corpus:

```bash
(.env) $ python ./parse.py -t "Caesar Words" -d de_bello_gallico.txt 
```

Parses 5 paragraphs of `De Bello Gallico`, starting at the 5th paragraph,
and generates Anki cards for words found in Latin at an "intermediate"
learner’s level (excluding the most common words, and very rare or
highly specialized vocabulary).

```bash
(.env) $ python ./parse.py -t "Caesar Words" \
    -d de_bello_gallico.txt \
    -s 5 \
    -c 5 \
    -f intermediate
```