import os
from google.cloud import translate_v2 as translate
import localization

def translate_messages(target_language: str):
    translate_client = translate.Client()

    for message_key in localization.messages["en"]:
        source_text = localization.messages["en"][message_key]
        result = translate_client.translate(source_text, target_language=target_language)
        translated_text = result["translatedText"]
        localization.messages[target_language][message_key] = translated_text
