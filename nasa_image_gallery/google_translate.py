from google.cloud import translate_v2 as translate
import os

# Establece la ruta al archivo de credenciales JSON
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'dulcet-hulling-427203-s4-92fa254ae49c.json')

def translate_text(text, target_language='en'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
