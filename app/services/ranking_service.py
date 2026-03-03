class RankingService:
    def score(self, article_text: str, interests: list[str]):
        score = 0
        for interest in interests:
            if interest.lower() in article_text.lower():
                score += 1
        return score