def reports(gResult):
    
    resultText = ''

    for r in gResult['results']:
        line = '<div><a href='+r['link']+'>'+r['title']+'</a></br>'+r['description']+'</br></div>'
        resultText = resultText + line
    
    return resultText