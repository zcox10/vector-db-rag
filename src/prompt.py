from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from typing import Any


class Prompter:
    """
    A class for generating code-related prompts and invoking LLM pipelines for code generation.
    """

    def __init__(self) -> None:
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """
        Creates a reusable chat prompt template for code generation.
        """
        return ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=["context", "question"],
                        template=(
                            """You are a coding assistant specializing in software development. Your task is to generate only executable code. Follow these strict rules:

1. Output only functional code.
2. Do not include print statements, comments, explanations, or UI components (e.g., Streamlit).
3. Ensure the code is complete, syntactically correct, and ready to run without modification.

## Task
{question}

## Context (if relevant)
{context}

## Output (Code Only)
"""
                        ),
                    )
                )
            ],
        )

    def generate_response(self, query: str, model: Any, context_text: str) -> str:
        """
        Generates a code response from the LLM based on provided query and context.
        """
        # Define pipeline
        chain = self.prompt_template | model

        # Generate response
        response = chain.invoke({"question": query, "context": context_text})
        cleaned_response = response.strip() if response else "No valid response received."
        print(cleaned_response)
        return cleaned_response
