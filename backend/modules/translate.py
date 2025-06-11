from transformers import pipeline

# Using HuggingFace model for translation
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ROMANCE")

def translate_text(text: str, target_lang: str):
    translation = translator(text, tgt_lang=target_lang)
    return translation[0]['translation_text']

