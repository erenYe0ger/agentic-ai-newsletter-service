from sentence_transformers import SentenceTransformer
import numpy as np


class RankingService:
    """
    Service responsible for computing semantic similarity
    between article content and a predefined AI research
    reference context.

    Uses sentence-transformers embeddings and cosine similarity.
    """

    def __init__(self):

        # Lightweight embedding model (~90MB)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Reference context representing the type of articles we prefer
        self.reference_text = """
        Important developments in artificial intelligence including
        foundation models, large language models, machine learning research,
        neural networks, transformers, training techniques, model architecture,
        benchmarks, datasets, AI agents, and open source AI frameworks.
        """

        # Precompute reference embedding once
        self.reference_embedding = self.model.encode(self.reference_text)

    def similarity(self, text: str) -> float:
        """
        Compute cosine similarity between the article
        text embedding and the reference embedding.
        """

        # Encode article text
        emb = self.model.encode(text)

        # Cosine similarity
        score = np.dot(self.reference_embedding, emb) / (
            np.linalg.norm(self.reference_embedding) * np.linalg.norm(emb)
        )

        return float(score)