from flask import Flask, render_template, request

import naver_translate as nt
import google_search as gs

app = Flask(__name__)

# ibm translation
ibm_api_key = 'your key' # ibm api key 값
ibm_api_url = 'https://api.kr-seo.language-translator.watson.cloud.ibm.com/instances/5d1803ac-0d6e-431d-9d70-ce28b26c0822'

# naver translation
naver_api_id = 'your id' # 개발자센터에서 발급받은 Client ID 값
naver_api_secret = 'your secret' # 개발자센터에서 발급받은 Client Secret 값

# google search
google_api_host = "google-search3.p.rapidapi.com"
google_api_key  = "your key" # RAPIDAPI key 값

@app.route('/')
def index():
    return render_template('krInput.html')

@app.route('/kr_input', methods=['POST'])
def kr_input():

    kr_text = request.form['kr_text'] # 한국어 검색어

    sourceLang = 'ko'
    targetLang = 'en'
    #model_id = 'en-ko' # ibm 번역에서 사용, 영어->한국어
    en_text = nt.naver_translation(kr_text, sourceLang, targetLang, naver_api_id, naver_api_secret) # 번역된 검색어

    kr_result = gs.gSearch(kr_text, google_api_key, google_api_host) # 한국어 검색 결과
    en_result = gs.gSearch(en_text, google_api_key, google_api_host) # 영어 검색 결과

    results = {}

    if kr_result is not None:
        results[kr_text] = kr_result
    
    if en_result is not None:
        results[en_text] = en_result
    
    finalResult = ''
    for key, value in results.items():
        finalResult = finalResult + '<h1 class="text-center">%s에 대한 검색 결과</h1></br>%s</br>' %(key, value)

    if len(finalResult) <= 0:
        finalResult = '검색 결과가 없습니다.'
    
    finalResult = finalResult + '<a href="/">Back home</a>'

    return finalResult

if __name__ == '__main__':
    app.run()

    
