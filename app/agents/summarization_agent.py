from app.services.summarizer_service import SummarizerService


class SummarizationAgent:
    """
    Agent responsible for generating article summaries.

    Delegates summarization logic to SummarizerService.
    """

    def __init__(self) -> None:
        self.summarizer: SummarizerService = SummarizerService()

    def run(self, text: str) -> str:
        """
        Generate summary for extracted article text.
        """
        print("[SummarizationAgent] Summarizing...")
        return self.summarizer.summarize(text)