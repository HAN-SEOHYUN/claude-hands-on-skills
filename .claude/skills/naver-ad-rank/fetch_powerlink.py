# -*- coding: utf-8 -*-
"""
네이버 파워링크 광고 목록 수집 스크립트
사용법: python fetch_powerlink.py "검색키워드"
"""
import sys
import io
import json

# Windows 콘솔 UTF-8 출력 강제
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import re
import urllib.request
import urllib.parse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.naver.com/",
}


PAGE_SIZE = 25


def fetch_html(keyword: str, paging_index: int = 1) -> str:
    encoded = urllib.parse.quote(keyword)
    url = (
        f"https://ad.search.naver.com/search.naver?where=ad&query={encoded}"
        f"&x=0&y=0&pagingIndex={paging_index}"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8")


def parse_powerlinks(html: str, rank_offset: int = 0) -> list[dict]:
    """파워링크 광고 목록 파싱 — BeautifulSoup 없이 정규식으로 처리."""
    ads = []

    # ol.lst_type 섹션 추출
    ol_match = re.search(r'<ol class="lst_type">(.*?)</ol>', html, re.DOTALL)
    if not ol_match:
        return ads

    ol_content = ol_match.group(1)

    # data-index 기준으로 최상위 li 항목 분리
    items = re.split(r'(?=<li data-index=)', ol_content)
    items = [i for i in items if i.strip().startswith("<li data-index=")]

    for i, item in enumerate(items, start=1):
        # 광고 제목: lnk_tit span이 여러 개(메인+부제목)일 수 있으므로 모두 합침
        title_parts = re.findall(r'class="lnk_tit"[^>]*>(.*?)</span>', item, re.DOTALL)
        title = " ".join(re.sub(r"<[^>]+>", "", p).strip() for p in title_parts).strip()

        # 표시 URL: url 클래스 a 태그
        url_match = re.search(r'class="url"[^>]*>(.*?)</a>', item, re.DOTALL)
        display_url = re.sub(r"<[^>]+>", "", url_match.group(1)).strip() if url_match else ""

        # 사이트명(브랜드명): site 클래스
        site_match = re.search(r'class="site"[^>]*>(.*?)</(?:span|a|div)', item, re.DOTALL)
        site = re.sub(r"<[^>]+>", "", site_match.group(1)).strip() if site_match else ""

        if title:
            ads.append({
                "rank": rank_offset + i,
                "title": title,
                "site": site,
                "display_url": display_url,
            })

    return ads


def fetch_all_ads(keyword: str) -> list[dict]:
    """빈 페이지가 나올 때까지 전체 파워링크 광고 수집."""
    all_ads = []
    paging_index = 1
    while True:
        html = fetch_html(keyword, paging_index=paging_index)
        ads = parse_powerlinks(html, rank_offset=(paging_index - 1) * PAGE_SIZE)
        if not ads:
            break
        all_ads.extend(ads)
        if len(ads) < PAGE_SIZE:
            break
        paging_index += 1
    return all_ads


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "키워드를 인자로 전달해주세요."}, ensure_ascii=False))
        sys.exit(1)

    keyword = sys.argv[1]

    try:
        ads = fetch_all_ads(keyword)
        print(json.dumps({"keyword": keyword, "ads": ads}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
