from typing import Dict, Any
from langchain_huggingface.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, Pipeline


class LlmModel:
    """
    A class to initialize and manage an LLM pipeline for text generation.
    """

    def __init__(self, model_kwargs: Dict[str, Any]) -> None:
        self.model_kwargs = self._prepare_model_kwargs(model_kwargs)
        self.pipeline = self._create_pipeline()
        self.model = HuggingFacePipeline(pipeline=self.pipeline)

    def _prepare_model_kwargs(self, model_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepares model and tokenizer kwargs with proper padding.
        """
        # Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_kwargs["model_id"])
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token = tokenizer.eos_token
        model_kwargs["tokenizer"] = tokenizer

        # LLM
        model_kwargs["model"] = AutoModelForCausalLM.from_pretrained(model_kwargs["model_id"])
        return model_kwargs

    def _create_pipeline(self) -> Pipeline:
        """
        Creates the Huggingface pipeline for the LLM.
        """
        # Create pipeline without model_id to avoid conflicts
        pipeline_kwargs = {k: v for k, v in self.model_kwargs.items() if k != "model_id"}
        return pipeline(**pipeline_kwargs)
