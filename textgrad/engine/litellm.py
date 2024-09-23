from textgrad.engine.base import CachedEngine
from textgrad.engine.openai import ChatOpenAI    
import platformdirs
try:
    from litellm import completion
except ImportError:
    raise ImportError("If you'd like to use litellm, please install the litellm package by running `pip install litellm`.")
import os
from typing import List, Union
import json

class Litellm(ChatOpenAI):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."
    
    def __init__(
        self,
        model_string: str="litellm/gpt-3.5-turbo-0613",
        system_prompt: str=DEFAULT_SYSTEM_PROMPT,
        is_multimodal: bool=False,
        base_url: str=None,
        **kwargs
    ):
        root = platformdirs.user_cache_dir("textgrad")
        cache_path = os.path.join(root, f"cache_litellm_{model_string}.db")

        CachedEngine.__init__(self, cache_path=cache_path)
        
        self.model_string = "/".join(model_string.split("/")[1:])
        self.system_prompt = system_prompt
        self.is_multimodal = is_multimodal
        self.base_url = base_url
        self.custom_llm_provider = None
        
    
    def _generate_from_single_prompt(
        self, prompt: str, system_prompt: str, temperature=0, max_tokens=2000, top_p=0.99, **kwargs
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt

        cache_or_none = self._check_cache(sys_prompt_arg + prompt)
        
        if cache_or_none:
            return cache_or_none
        
        input_messages = [
            {"role": "system", "content": sys_prompt_arg},
            {"role": "user", "content": prompt},
        ]
        
        response = completion(
            model = self.model_string,
            messages = input_messages,
            temperature = temperature,
            max_tokens = max_tokens,
            top_p = top_p,
            stream=None,
            base_url = self.base_url,
            custom_llm_provider = self.custom_llm_provider,
            **kwargs
        )
        
        response = response["choices"][0].message.content
        
        self._save_cache(sys_prompt_arg + prompt, response)
        
        return response
        
        
    def _generate_from_multiple_input(
        self, content: List[Union[str, bytes]], system_prompt=None, temperature=0, max_tokens=2000, top_p=0.99, **kwargs
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt
        formatted_content = self._format_content(content)

        cache_key = sys_prompt_arg + json.dumps(formatted_content)
        cache_or_none = self._check_cache(cache_key)
        if cache_or_none is not None:
            return cache_or_none

        messages = [
                {"role": "system", "content": sys_prompt_arg},
                {"role": "user", "content": formatted_content},
        ]

        response = completion(
            model=self.model_string,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
            base_url=self.base_url,
            **kwargs #addiional params of completion of litellm
        )
        response_text = response = response["choices"][0]
        self._save_cache(cache_key, response_text)
        return response_text

        
        
        

        
        
    
# class EngineLM(ABC):
#     system_prompt: str = "You are a helpful, creative, and smart assistant."
#     model_string: str
#     @abstractmethod
#     def generate(self, prompt, system_prompt=None, **kwargs):
#         pass

#     def __call__(self, *args, **kwargs):
#         pass