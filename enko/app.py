from flask import Flask, render_template, request

import naver_translate as nt
import google_search as gs
import report

app = Flask(__name__)

# ibm translation
ibm_api_key = 'piprDDbxjW3UAH4cX5XhKLrXRbyn0ymQIk5nblaji8Pf' # ibm api key 값
ibm_api_url = 'https://api.kr-seo.language-translator.watson.cloud.ibm.com/instances/5d1803ac-0d6e-431d-9d70-ce28b26c0822'

# naver translation
naver_api_id = 'k78Y1KgZUNHXRkkM_VzF' # 개발자센터에서 발급받은 Client ID 값
naver_api_secret = 'WgmJw72QSr' # 개발자센터에서 발급받은 Client Secret 값

# google search
google_api_host = "google-search3.p.rapidapi.com"
google_api_key  = "7367b7df89mshcd92f1e431d8258p17ce0fjsn140a51aa3b55" # RAPIDAPI key 값

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kr_input', methods=['POST'])
def kr_input():

    kr_text = request.form['kr_text'] # 한국어 검색어

    if len(kr_text)<1:
        return '검색어를 입력해주십시오.' + '<a href="/">Back home</a>'

    if len(kr_text) > 25: # 검색어가 너무 길면 자른다.
        kr_text = kr_text[:26]

    sourceLang = 'ko'
    targetLang = 'en'
    #model_id = 'en-ko' # ibm 번역에서 사용, 영어->한국어
    en_text = nt.naver_translation(kr_text, sourceLang, targetLang, naver_api_id, naver_api_secret) # 번역된 검색어

    kr_result = report.reports(gs.gSearch(kr_text, google_api_key, google_api_host)) # 한국어 검색 결과
    en_result = report.reports(gs.gSearch(en_text, google_api_key, google_api_host)) # 영어 검색 결과

    results = {}

    if kr_result is not None:
        results[kr_text] = kr_result
    else:
        results[kr_text] = '검색 결과가 없습니다.'
    
    if en_result is not None:
        results[en_text] = en_result
    else:
        results[en_text] = '검색 결과가 없습니다.'
    
    result1 = '<div class="result-area1"><div class="result-item"><h2 class="search-lang">%s에 대한 검색 결과</h2></br>%s</br></div><div><a class="furtherlink-kr" href="https://www.google.com/search?q=%s">구글에서 더 보기</a></div></div>' %(kr_text, results[kr_text],kr_text)
    result2 = '<div class="result-area2"><div class="result-item"><h2 class="search-lang">%s에 대한 검색 결과</h2></br>%s</br></div><div><a class="furtherlink-en" href="https://www.google.com/search?q=%s">구글에서 더 보기</a></div></div>' %(en_text, results[en_text],en_text)

    finalResult = '<div class="result-container">' + result1 + result2 + '</div><div><a class="go-home" href="/">clear</a></div>'

    return render_template('index.html', data=finalResult)

if __name__ == '__main__':
    app.run()