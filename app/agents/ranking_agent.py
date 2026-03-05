from app.services.ranking_service import RankingService


class RankingAgent:
    """
    Agent responsible for computing ranking score
    for each article using semantic similarity.
    """

    def __init__(self) -> None:
        self.rank_service: RankingService = RankingService()

    def score(self, article: dict[str, str]) -> float:
        """
        Compute ranking score for a given article.
        Uses title + summary as semantic input.
        """

        text: str = f"{article['title']} {article['summary']}"

        return self.rank_service.similarity(text)