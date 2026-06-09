from transformers import pipeline

# module-level singleton so the model is only loaded once per process
_pipe = None

def _get_pipe():
    """Lazily load and cache the sentiment analysis pipeline."""
    global _pipe
    if _pipe is None:
        _pipe = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
    return _pipe

def score_posts(posts: list[dict]) -> list[dict]:
    """
    Score each post's text with the sentiment model.

    Adds a 'score' key to each post dict: 1.0 positive, 0.0 neutral, -1.0 negative.

    Args:
        posts: List of post dicts with at least a 'text' key.

    Returns:
        The same list with 'score' populated on each dict.
    """
    if not posts:
        return []

    pipe = _get_pipe()

    # truncate to 512 chars to stay within model token limits
    texts = [p["text"][:512] for p in posts]
    results = pipe(texts, truncation=True)

    label_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
    for post, result in zip(posts, results):
        post["score"] = label_map.get(result["label"].lower(), 0.0)

    return posts