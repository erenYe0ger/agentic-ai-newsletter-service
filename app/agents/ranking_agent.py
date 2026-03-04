from app.services.semantic_ranking_service import SemanticRankingService


class RankingAgent:

    def __init__(self):
        self.rank_service = SemanticRankingService()

    def rank(self, articles):

        ranked = []

        for article in articles:

            text = f"{article['title']}. {article['summary']}"

            score = self.rank_service.similarity(text)

            # DEBUG OUTPUT
            print("\n[Ranking]")
            print("Title:", article["title"])
            print("Similarity score:", round(score, 4))

            ranked.append({
                **article,
                "score": score
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        print("\n[Ranking] Top articles after semantic ranking:\n")

        for a in ranked[:5]:
            print(round(a["score"], 4), "-", a["title"])

        return ranked