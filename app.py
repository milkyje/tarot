import streamlit as st
from config import TAROT_DECK
from tarot_data import load_spreads_data, load_prompts_data, draw_cards
from tarot_ai import get_ai_reading
import json

# 데이터 로딩
spreads_data = load_spreads_data()
prompts_data = load_prompts_data()

st.title("타로 리더")

# 사이드바 메뉴 구성
with st.sidebar:
    st.header("타로 리딩 설정")
    categories = list(prompts_data.keys())
    category = st.selectbox("고민 카테고리:", options=categories)

    # 선택지에 따라 스프레드 목록 필터링
    spread_name_map = {}
    if category == "다중 선택":
        filtered_spreads = ["다중선택 스프레드"]
        spread_name_map["다중선택 스프레드"] = "다중선택 스프레드"
    else:
        filtered_spreads = []
        for spread_display_name, spread_info in spreads_data.items():
            if category in spread_info.get("categories", []):
                display_name = f"{spread_display_name} ({spread_info['num_cards']}장)"
                filtered_spreads.append(display_name)
                spread_name_map[display_name] = spread_display_name

    spread_name_with_count = st.selectbox(
        "사용할 스프레드를 선택하세요:",
        options=filtered_spreads,
        help="스프레드를 선택하면 리딩에 사용되는 카드 수와 위치별 의미가 달라집니다."
    )
    spread_name = spread_name_map.get(spread_name_with_count)

# 메인 화면 UI
user_input = st.text_area(
    "고민을 입력해주세요. 구체적으로 작성할수록 정확한 리딩을 받을 수 있습니다.",
    value="",
    height=150,
    placeholder="예시) 남자친구와 자꾸 싸우는데, 이 관계를 계속 유지하는 게 맞을까요? (고민 카테고리: 연애)\n\n"
)

# '다중 선택' 카테고리일 때만 선택지 입력란 표시
choices = []
if spread_name == "다중선택 스프레드":
    st.subheader("선택지 입력")
    choice1 = st.text_input("선택지 1", placeholder="예시) 헤어진다")
    choice2 = st.text_input("선택지 2", placeholder="예시) 대화를 통해 해결한다")
    choices = [choice1, choice2]
    # 추가 선택지 입력란 필요 시 확장 가능

if st.button("리딩 시작"):
    if not user_input:
        st.warning("고민을 입력해주세요.")
    elif spread_name == "다중선택 스프레드" and not all(choices):
        st.warning("선택지를 모두 입력해주세요.")
    else:
        with st.spinner('카드를 뽑고 있어요...'):
            num_cards = spreads_data.get(spread_name, {}).get("num_cards", 0)
            if spread_name == "다중선택 스프레드":
                num_cards = 1 + len(choices) * 2
            
            cards = draw_cards(TAROT_DECK, num_cards, spread_name)

        st.subheader("뽑은 카드")
        st.write(f"**스프레드:** {spread_name_with_count}")
        st.write(f"**총 {len(cards)}장**")
        st.write(f"**카드 목록:** {', '.join(cards)}")
        
        st.markdown("---")
        st.subheader("타로 리딩 결과")
        ai_response = get_ai_reading(category, user_input, choices, spread_name, cards, prompts_data)
        st.write(ai_response)

