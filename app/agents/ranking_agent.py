from app.services.ranking_service import RankingService

class RankingAgent:
    def __init__(self, interests):
        self.rank = RankingService()
        self.interests = interests

    def score(self, article):
        return self.rank.score(article["summary"], self.interests)