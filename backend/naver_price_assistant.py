import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

################################################################################
# 1) 크롤링 함수: 네이버 쇼핑 검색결과 (노트북 등)
################################################################################
def crawl_naver_shopping(query: str, max_count: int = 20):
    """
    네이버 쇼핑에서 'query'로 검색해,
    상품명, 가격, 평점, 판매사, 리뷰 수 등을 추출하여
    파이썬 리스트[dict,...] 형태로 반환.
    
    max_count: 가져올 최대 상품 개수 (기본 20개)
    """
    # 크롬 옵션 설정 (브라우저 창을 띄우지 않는 headless 모드 예시)
    chrome_options = Options()
    # 필요에 따라 주석 처리/해제
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    # 크롬드라이버 경로 설정(환경에 맞게 수정)
    service = Service("C:\Users\USER\Desktop\chromedriver-win64\chromedriver.exe")  # 예: "./chromedriver" or "C:/path/chromedriver.exe"
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 네이버 쇼핑 검색 URL
    base_url = "https://search.shopping.naver.com/search/all"
    driver.get(f"{base_url}?query={query}")

    time.sleep(2)  # 페이지 로딩 대기 (필요 시 늘릴 수 있음)

    # 스크롤/더보기 등을 통해 더 많은 상품을 로드할 수도 있음
    # 여기서는 예시로, 첫 페이지의 일정 부분만 가져온다

    products = []

    # items: 상품 리스트 요소들(2023년 기준)
    # 실제 클래스명/구조는 수시로 바뀔 수 있음
    item_selector = "li.basicList_item__2XT81"
    items = driver.find_elements(By.CSS_SELECTOR, item_selector)

    for idx, item in enumerate(items):
        if idx >= max_count:
            break

        try:
            # 상품명
            name_elem = item.find_element(By.CSS_SELECTOR, "a.basicList_link__1MaTN")
            name = name_elem.text.strip()
            link = name_elem.get_attribute("href")

            # 가격
            # ex) <span class="price_num__2WUXn">1,234,567원</span>
            price_elem = item.find_element(By.CSS_SELECTOR, "span.price_num__2WUXn")
            price_text = price_elem.text.strip()
            # 숫자만 추출
            price_value = int(re.sub(r'[^0-9]', '', price_text))

            # 평점 (없을 수도 있으니 try-except)
            rating_value = 0.0
            try:
                rating_elem = item.find_element(By.CSS_SELECTOR, "span.basicList_star__3NkBn > em")
                rating_value = float(rating_elem.text.strip())
            except:
                pass

            # 판매사
            # ex) <span class="basicList_mall_name__1XaKA">11번가</span>
            seller = ""
            try:
                seller_elem = item.find_element(By.CSS_SELECTOR, "span.basicList_mall_name__1XaKA")
                seller = seller_elem.text.strip()
            except:
                pass

            # 리뷰 수
            # ex) <em class="basicList_num__1yXM9">1,234</em>
            review_count = 0
            try:
                review_elem = item.find_element(By.CSS_SELECTOR, "em.basicList_num__1yXM9")
                review_text = review_elem.text.strip().replace(',', '')
                review_count = int(review_text)
            except:
                pass

            product_info = {
                "name": name,
                "price": price_value,
                "rating": rating_value,
                "seller": seller,
                "review_count": review_count,
                "link": link
            }
            products.append(product_info)

        except Exception as e:
            print("Error parsing item:", e)
            continue

    driver.quit()
    return products

################################################################################
# 2) 간단한 가격비서 로직: 예산 이하 상품만 추천, 평점 높은 순 정렬
################################################################################
def recommend_by_budget(products, budget, top_k=5):
    """
    주어진 products(리스트[dict]) 중 예산 이하인 상품만 골라,
    간단히 '평점'이 높은 순으로 정렬 후 상위 top_k개를 반환.
    """
    # 1) 예산 이하 필터링
    filtered = [p for p in products if p["price"] <= budget]

    # 2) 평점 순 정렬 (평점이 같다면 리뷰 수가 많은 순)
    filtered.sort(key=lambda x: (x["rating"], x["review_count"]), reverse=True)

    # 상위 top_k개만
    return filtered[:top_k]

################################################################################
# 3) AI 가격비서 함수
#    (실제로는 LangChain or CrewAI Agent와 연동 가능 - 여기서는 간단 예시)
################################################################################
def ai_price_assistant(query, budget):
    """
    - 네이버 쇼핑에서 'query'로 크롤링
    - 예산 'budget' 이하 상품 중 평점 높은 순으로 추천
    - 요약된 결과 메시지(자연어) 반환
    """
    # 1. 네이버 쇼핑 크롤링
    products = crawl_naver_shopping(query=query, max_count=30)

    if not products:
        return "상품을 찾지 못했습니다."

    # 2. 예산 내 추천
    recommended = recommend_by_budget(products, budget=budget, top_k=5)
    if not recommended:
        return f"예산 {budget}원 이하로 구매 가능한 '{query}' 상품이 없습니다."

    # 3. 메시지 구성
    message = f"'{query}'에 대한 예산 {budget}원 이하 추천 상품 TOP {len(recommended)}:\n"
    for i, r in enumerate(recommended, start=1):
        message += (
            f"{i}. {r['name']} / 가격: {r['price']}원 / 평점: {r['rating']} / "
            f"판매사: {r['seller']} / 리뷰: {r['review_count']}건\n"
            f"   링크: {r['link']}\n"
        )
    return message

################################################################################
# 4) 실제 동작 테스트 (메인 실행)
################################################################################
if __name__ == "__main__":
    # 예) "노트북" 키워드, 예산 1,000,000원 (100만원)
    keyword = "노트북"
    budget = 1000000  # 100만원

    result_message = ai_price_assistant(keyword, budget)
    print("=== AI 가격비서 추천 결과 ===")
    print(result_message)
