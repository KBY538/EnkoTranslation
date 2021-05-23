from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import urllib3
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings()

def ibm_translation(text, sourceLang, targetLang, api_key, api_url):

    authenticator = IAMAuthenticator(api_key)

    language_translator = LanguageTranslatorV3( # 2020년 5월 6일 기준 최신 버전
        version='2018-05-01',
        authenticator=authenticator
    )

    try:
        language_translator.set_service_url(api_url)

        language_translator.set_disable_ssl_verification(True)
    
        model_id = sourceLang+'-'+targetLang

        translation = language_translator.translate(text=text, model_id=model_id).get_result()
        translatedText = translation['translations'][0]['translation']
        
        return translatedText

    except ApiException as ex:
        print ("Method failed with status code " + str(ex.code) + ": " + ex.message)