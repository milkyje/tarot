import streamlit as st
import json
from tarot_data import draw_cards, load_spreads_data
from tarot_ai import get_ai_reading, generate_prompt_text

# 기본 데이터 로딩
spreads_data = load_spreads_data()

with open('category_settings.json', 'r', encoding='utf-8') as f:
    categories_data = json.load(f)

st.title("asTarot - 내가 쓰려고 만든 ai 타로리딩")

# 1. 카드덱명 입력 + 안내문(기본 유니버설 웨이트)

deck_name = st.text_input("사용할 카드덱 이름을 입력하세요", value="유니버설 웨이트")

if deck_name != "유니버설 웨이트":
    st.warning(
        "입력하신 카드덱은 AI가 학습한 주요 덱일 경우 비교적 정확한 리딩이 가능합니다.\n"
        "하지만 알려지지 않았거나 덱 정보가 부족한 경우, AI가 생성한 리딩은 신뢰도가 낮을 수 있으니 참고용으로만 활용해 주세요."
    )

# 2. 큰 카테고리 선택 및 세부카테고리, 예시 질문 로드

main_categories = list(categories_data.keys())
selected_main = st.selectbox("고민 분야를 선택하세요", options=main_categories)

sub_cats = categories_data[selected_main]["subcategories"]
sub_cat_names = [c["name"] for c in sub_cats]
selected_sub = st.selectbox("세부 분야를 선택하세요", options=sub_cat_names)
selected_sub_obj = next(c for c in sub_cats if c["name"] == selected_sub)

question_placeholder = selected_sub_obj.get("example", "")
user_question = st.text_area("고민 내용을 구체적으로 입력해 주세요:", height=150, placeholder=question_placeholder)

# 3. 스프레드 목록(세부카테고리 맞춤 필터링)

valid_spreads = selected_sub_obj.get("spreads", [])
spread_sel = st.selectbox("사용할 카드 스프레드를 선택하세요:", options=valid_spreads)

choices = []
if spread_sel == "다중선택 스프레드":
    st.subheader("선택지 입력")
    choice1 = st.text_input("선택지 1")
    choice2 = st.text_input("선택지 2")
    choices = [choice1, choice2]
    for i in range(3, 6):
        choice = st.text_input(f"선택지 {i}", key=f"choice_{i}")
        if choice:
            choices.append(choice)

# 4. 리딩 버튼 및 프롬프트 생성 버튼

col1, col2 = st.columns(2)

with col1:
    if st.button("리딩 시작 (Gemini 1.5 API 사용)"):
        if not user_question:
            st.warning("고민 내용을 입력해주세요.")
        elif spread_sel == "다중선택 스프레드" and not all(choices):
            st.warning("모든 선택지를 입력해 주세요.")
        else:
            if spread_sel == "다중선택 스프레드":
                num_cards = 1 + len(choices)*2
            else:
                num_cards = spreads_data.get(spread_sel, {}).get("num_cards", 0)
            cards = draw_cards(num_cards)
            ai_response = get_ai_reading(selected_main, user_question, spread_sel, cards)
            st.markdown(f"**[Gemini API 1.5 버전 기준 AI 리딩 결과]**")
            st.subheader("뽑은 카드")
            st.write(f"{len(cards)}장: {', '.join(cards)}")
            st.subheader("AI 타로 리딩 결과")
            st.write(ai_response)

with col2:
    if st.button("AI 리딩용 프롬프트 생성 (복사 가능)"):
        if not user_question:
            st.warning("고민 내용을 입력해주세요.")
        else:
            if spread_sel == "다중선택 스프레드":
                # 다중선택 시 choices 활용
                prompt_text = generate_prompt_text(selected_main, user_question, spread_sel, choices=choices)
            else:
                prompt_text = generate_prompt_text(selected_main, user_question, spread_sel)
            st.subheader("생성된 AI 리딩 프롬프트")
            st.text_area("복사해서 AI 챗에 붙여넣으세요", value=prompt_text, height=300)

