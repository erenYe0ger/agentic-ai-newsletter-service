from app.services.semantic_ranking_service import SemanticRankingService


class RankingAgent:

    def __init__(self):
        self.rank_service = SemanticRankingService()

    def score(self, article):

        text = f"{article['title']} {article['summary']}"

        return self.rank_service.similarity(text)