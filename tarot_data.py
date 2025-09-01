import json
import random

# JSON 파일에서 스프레드 데이터를 불러오는 함수
def load_spreads_data():
    try:
        with open("spreads.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# JSON 파일에서 프롬프트 데이터를 불러오는 함수
def load_prompts_data():
    try:
        with open("prompts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# 카드 덱에서 무작위로 카드를 뽑는 함수
def draw_cards(deck, num_cards, spread_name):
    if spread_name == "집시의 십자":
        # 집시의 십자 스프레드 로직: 메이저 아르카나 22장 중 15장을 뽑아 그 중 5장을 선택
        major_arcana_deck = [card for card in deck if "of" not in card]
        selected_15 = random.sample(major_arcana_deck, 15)
        return random.sample(selected_15, num_cards)
    else:
        # 그 외 스프레드 로직: 전체 덱에서 무작위로 카드를 뽑습니다.
        return random.sample(deck, num_cards)

