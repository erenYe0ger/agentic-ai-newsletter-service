from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticRankingService:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.reference_text = """
        Important developments in artificial intelligence including
        foundation models, large language models, machine learning research,
        neural networks, transformers, training techniques, model architecture,
        benchmarks, datasets, AI agents, and open source AI frameworks.
        """

        self.reference_embedding = self.model.encode(self.reference_text)

    def similarity(self, text: str):

        emb = self.model.encode(text)

        score = np.dot(self.reference_embedding, emb) / (
            np.linalg.norm(self.reference_embedding) * np.linalg.norm(emb)
        )

        return float(score)