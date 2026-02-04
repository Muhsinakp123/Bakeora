SYNONYMS = {
    "choco": "chocolate",
    "bday": "birthday",
    "biscut": "biscuit",
    "strawbery": "strawberry",
    "vanila": "vanilla",
    "cup cake": "cupcake",
}

def normalize_query(q):
    q = q.lower().strip()

    for wrong, correct in SYNONYMS.items():
        q = q.replace(wrong, correct)

    return q
