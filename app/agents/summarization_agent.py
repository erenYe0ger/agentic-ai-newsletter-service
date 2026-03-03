from app.services.summarizer_service import SummarizerService

class SummarizationAgent:
    def __init__(self):
        self.s = SummarizerService()

    def run(self, text: str):
        print("[SummarizationAgent] Summarizing...")
        return self.s.summarize(text)