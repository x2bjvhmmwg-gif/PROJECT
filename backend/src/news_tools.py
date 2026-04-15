import requests
import json
from settings import settings

def get_latest_news(query: str) -> str:
    """
    네이버 뉴스 API를 통해 최신 뉴스를 검색합니다.
    """
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=3&sort=sim"
    headers = {
        "X-Naver-Client-Id": settings.naver_client_id,
        "X-Naver-Client-Secret": settings.naver_client_secret
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        results = []
        for item in items:
            results.append({
                "title": item['title'].replace('<b>', '').replace('</b>', ''),
                "description": item['description'].replace('<b>', '').replace('</b>', ''),
                "link": item['originallink']
            })
        return json.dumps(results, ensure_ascii=False)
    return "뉴스 검색에 실패했습니다."