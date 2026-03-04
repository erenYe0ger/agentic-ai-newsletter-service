from app.services.ranking_service import RankingService


class RankingAgent:
    """
    Agent responsible for computing ranking score
    for each article using semantic similarity.
    """

    def __init__(self):
        self.rank_service = RankingService()

    def score(self, article: dict) -> float:
        """
        Compute ranking score for a given article.
        Uses title + summary as semantic input.
        """

        text = f"{article['title']} {article['summary']}"

        return self.rank_service.similarity(text)