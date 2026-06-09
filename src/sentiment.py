from transformers import pipeline

_pipe = None

def _get_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
    return _pipe

def score_posts(posts: list[dict]) -> list[dict]:
    if not posts:
        return []
    pipe = _get_pipe()
    texts = [p["text"][:512] for p in posts]
    results = pipe(texts, truncation=True)
    label_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
    for post, result in zip(posts, results):
        post["score"] = label_map.get(result["label"].lower(), 0.0)
    return posts