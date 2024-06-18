import spacy
import ollama
from modules.ddg_search import DDGSearch

class SimpleContextAssembler:
    """
    A class to assemble context for a language model.

    This class maintains a stack of the last three names mentioned in the prompts
    and uses the most recent name to replace pronouns like "he". It also performs
    DuckDuckGo searches based on the prompt and adds the search results to the
    context.
    """
    def __init__(self):
        """
        Initializes the ContextAssembler with a spaCy model for NLP, an empty
        name stack, and a maximum stack size of 3.
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.name_stack = []  # Initialize name stack
        self.max_stack_size = 3
        self.ddg_search = DDGSearch()

    def extract_name(self, text):
        """
        Extracts the first person name from the given text using spaCy's named
        entity recognition.

        Args:
            text (str): The text to extract the name from.

        Returns:
            str: The first person name found, or None if no name is found.
        """
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def resolve_pronoun(self, prompt):
        """
        Resolves the pronoun "he" in the prompt by replacing it with the most
        recent name from the name stack.

        Args:
            prompt (str): The prompt to resolve pronouns in.

        Returns:
            str: The prompt with the pronoun replaced, or the original prompt if
                no name is stored.
        """
        doc = self.nlp(prompt)
        resolved_prompt = prompt  # Start with the original prompt
        for token in doc:
            if token.pos_ == "PRON" and token.text.lower() == "he":
                if self.name_stack:
                    last_name = self.name_stack[-1]  # Get the most recent name
                    resolved_prompt = resolved_prompt.replace(token.text, last_name)  # Replace ALL instances
        return resolved_prompt

    def assemble_context(self, prompt):
        """
        Assembles context for the given prompt by performing a DuckDuckGo search.

        This method extracts names from the prompt, updates the name stack,
        resolves pronouns, and generates a search query based on the prompt.
        The search results are then returned as context.

        Args:
            prompt (str): The prompt to assemble context for.

        Returns:
            list: A list of search results from DuckDuckGo, which serves as
                the context.
        """
        # Extract name, if any
        name = self.extract_name(prompt)

        # Update name stack 
        if name:
            self.name_stack.append(name)
            # Keep only the last max_stack_size names
            if len(self.name_stack) > self.max_stack_size:
                self.name_stack.pop(0)  # Remove the oldest name

        # Resolve pronouns in the prompt (only if a name is stored)
        if self.name_stack:
            prompt = self.resolve_pronoun(prompt)  # Replace pronoun in the prompt itself

        search_results = self.ddg_search.run_search(prompt)
        print("Search results:", search_results)

        # Add search results to context (optional)
        context = search_results
        return context

    def expand_prompt(self, prompt, context):
        """
        Expands the prompt by appending the assembled context to it.

        Args:
            prompt (str): The original prompt.
            context (list): The assembled context (search results).

        Returns:
            str: The expanded prompt with the context appended.
        """
        expanded_prompt = f"{prompt}\n\nContext: {', '.join(context)}"
        print("Expanded prompt:", expanded_prompt)
        return expanded_prompt
