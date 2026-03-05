from sentence_transformers import SentenceTransformer
import numpy as np
import numpy.typing as npt


class RankingService:
    """
    Service responsible for computing semantic similarity
    between article content and an AI-focused reference context.

    Uses sentence-transformers embeddings and cosine similarity
    to prioritize important AI developments.
    """

    def __init__(self) -> None:

        # Lightweight embedding model (~90MB)
        self.model: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")

        # Reference context representing the type of articles we prefer
        self.reference_text: str = """
        Recent breakthroughs and research developments in artificial intelligence,
        including new machine learning models, large language models, multimodal
        models, foundation models, and advances in deep learning architectures.

        Focus on scientific research, technical papers, benchmarks, training
        methods, evaluation techniques, reasoning capabilities, alignment and
        safety research, model efficiency, scaling laws, and AI infrastructure.

        Particular emphasis on publications, technical reports, and research
        announcements from leading AI labs such as OpenAI, Google DeepMind,
        Anthropic, Meta AI, HuggingFace, and major academic or industry
        research groups working on frontier AI systems.
        """

        # Precompute reference embedding once
        self.reference_embedding: npt.NDArray[np.float_] = self.model.encode(self.reference_text)

    def similarity(self, text: str) -> float:
        """
        Compute cosine similarity between the article
        text embedding and the reference embedding.
        """

        emb: npt.NDArray[np.float_] = self.model.encode(text)

        score: float = np.dot(self.reference_embedding, emb) / (
            np.linalg.norm(self.reference_embedding) * np.linalg.norm(emb)
        )

        return float(score)