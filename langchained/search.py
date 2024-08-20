"""Very simple keyword search: score each chunk by how many query words it contains."""


def score_chunk(chunk, words):
    text = chunk["text"].lower()
    source = chunk["source"].lower()
    score = 0
    for word in words:
        if word in text:
            score += text.count(word)
        if word in source:
            score += 2
    return score


def search(chunks, query, k=3):
    words = [word.lower() for word in query.split() if len(word) > 2]

    scored = []
    for chunk in chunks:
        score = score_chunk(chunk, words)
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for score, chunk in scored[:k]]
