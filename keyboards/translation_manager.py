import os
from google.cloud import translate_v2 as translate
import localization
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:/Users/vikaz/OneDrive/Рабочий стол/Work/Project/red_repo/translater-bot-intern-b9dec3a171bd.json'
# project_id = 'translater-bot-intern'
parent = f"projects/{project_id}"

def translate_messages(target_language: str):
    translate_client = translate.Client()

    for message_key in localization.messages["en"]:
        source_text = localization.messages["en"][message_key]
        result = translate_client.translate(source_text, target_language=target_language)
        translated_text = result["translatedText"]
        localization.messages[target_language][message_key] = translated_text
