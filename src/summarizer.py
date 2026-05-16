from src.factory import AIClientFactory

class HistorySummarizer:
    def __init__(self):
        self.llm = AIClientFactory.get_llm(model_name="llama-3.1-8b-instant", temperature=0)

    def summarize_history(self, messages: list) -> str:
        if not messages:
            return ""
        
        history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        
        prompt = f"""
        Summarize the following agricultural conversation history concisely.
        
        CRITICAL REQUIREMENT: 
        1. Preserve the user's name (if mentioned) and any personal context they shared.
        2. Preserve all key agricultural facts, crop names, symptoms, and advice given.
        3. Maintain a summary that allows the assistant to remember WHO they are talking to.
        
        History:
        {history_text}
        
        Summary:
        """
        try:
            summary = self.llm.invoke(prompt).content.strip()
            return summary
        except Exception as e:
            print(f"Summarization error: {e}")
            return history_text[:2000] # Fallback to truncation


summarizer = HistorySummarizer()
