import os
import json
import hashlib
from dataclasses import dataclass
from typing import List, Callable
import tiktoken

@dataclass
class SummarizationParameters:
    model_context_size: int
    target_summary_size: int
    summary_input_size: int

def summarization_token_parameters(
    model_context_size: int,
    target_summary_size: int
) -> SummarizationParameters:
    summary_input_size = model_context_size - target_summary_size - 1000
    return SummarizationParameters(
        model_context_size=model_context_size,
        target_summary_size=target_summary_size,
        summary_input_size=summary_input_size
    )

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message has a structural cost
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens -= 1
    num_tokens += 2  # priming
    return num_tokens

def split_text_into_sections(text: str, max_tokens: int, separator: str, model: str) -> List[str]:
    paragraphs = text.split(separator)
    sections = []
    current_section = ""
    encoding = tiktoken.get_encoding("cl100k_base")

    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        tentative_section = current_section + separator + paragraph if current_section else paragraph
        tokens = len(encoding.encode(tentative_section))
        if tokens > max_tokens:
            if current_section:
                sections.append(current_section.strip())
                current_section = paragraph
            else:
                sections.append(paragraph.strip())
                current_section = ""
        else:
            current_section = tentative_section

    if current_section:
        sections.append(current_section.strip())

    return sections
def summarization_prompt_messages(content: str, target_summary_size: int) -> List[dict]:
    return [
        {
            "role": "system",
            "content": f"You are a helpful assistant. Summarize the following short story in detail, preserving key events, emotions, and character arcs. Aim for a 200–300 word summary.",
        },
        {
            "role": "user",
            "content": content,
        },
    ]


def memoize_to_file(file_path: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapped(*args):
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                cache = {}

            hash_input = json.dumps(args, sort_keys=True)
            hash_key = hashlib.sha256(hash_input.encode()).hexdigest()

            if hash_key in cache:
                return cache[hash_key]

            result = func(*args)
            cache[hash_key] = result

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)

            return result
        return wrapped
    return decorator
  
