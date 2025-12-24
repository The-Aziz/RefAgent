"""
Groq LLM wrapper - uses Groq API for fast, cost-effective LLM inference.
"""

class GroqLLM:
    def __init__(self, api_key, prompt=None):
        """Initialize the Groq LLM wrapper.

        Args:
            api_key (str): Groq API key.
            prompt (str|None): Optional system prompt to set once at initialization.
        """
        self.api_key = api_key
        self.message_history = []
        self.prompt = None
        self.base_url = "https://api.groq.com/openai/v1"
        
        if prompt is not None:
            self.prompt = prompt
            self.message_history.append({"role": "system", "content": prompt})

    def query_llm(self, prompt, query, model="llama-3.1-8b-instant", max_tokens=4096):
        """Query the Groq LLM.

        Args:
            prompt (str): System prompt / context.
            query (str | list[str]): Either a single user query string or a list of user query strings.
            model (str): Groq model name (default: llama-3.1-8b-instant - FASTEST).
                       Other options:
                       - gemma-7b-it (most compact)
                       - mixtral-8x7b-32768 (larger but slower)
                       - llama-3.1-70b-versatile (largest)
            max_tokens (int): Maximum tokens for the response (reduced for RPM).

        Returns:
            str: Assistant reply or an error message.
        """
        try:
            from groq import Groq
            
            # Initialize Groq client
            client = Groq(api_key=self.api_key)
            
            # Accept either a single string or a list of strings for queries
            queries = query
            if isinstance(queries, str):
                queries = [queries]
            elif queries is None:
                queries = []
            elif not isinstance(queries, list):
                raise TypeError("`query` must be a string or list of strings")

            # Build messages: append system prompt only if not already set in history
            if prompt is not None and not any(m.get("role") == "system" for m in self.message_history):
                self.prompt = prompt
                self.message_history.insert(0, {"role": "system", "content": prompt})

            for q in queries:
                self.message_history.append({"role": "user", "content": q})

            # Fallback: if no user messages provided, keep at least the system prompt
            if not self.message_history:
                raise ValueError("No prompt or queries provided to send to the LLM")

            # Call Groq API
            response = client.chat.completions.create(
                model=model,
                messages=self.message_history,
                max_tokens=max_tokens,
                temperature=0.7,
            )

            # Extract response text
            reply = response.choices[0].message.content.strip()
            self.message_history.append({"role": "assistant", "content": reply})
            return reply

        except ImportError:
            return "Error: groq package not installed. Install with: pip install groq"
        except Exception as e:
            return f"An error occurred: {str(e)}"
