import streamlit as st
import random
import openai
# 아래 코드는 AI 프롬프트를 사용하는 가상의 함수입니다.
# 실제로는 여기에 Google Gemini API를 호출하는 코드가 들어갑니다.
def get_ai_reading(category, user_prompt, cards):
    # 이제 category 정보를 사용하여 프롬프트를 다르게 구성할 수 있습니다.
    # 예시를 위해 간단한 문자열을 반환합니다.
    return f"뽑은 카드: {', '.join(cards)}\n\n카테고리: {category}\n사용자 질문: {user_prompt}\n\nAI가 해석한 결과가 여기에 나타납니다."

# 타로 카드 덱 리스트 (이전에 만든 리스트를 여기에 붙여넣으세요)
tarot_deck = [
    "0. The Fool", "1. The Magician", "2. The High Priestess", "3. The Empress", "4. The Emperor", "5. The Hierophant", "6. The Lovers", "7. The Chariot", "8. Strength", "9. The Hermit", "10. Wheel of Fortune", "11. Justice", "12. The Hanged Man", "13. Death", "14. Temperance", "15. The Devil", "16. The Tower", "17. The Star", "18. The Moon", "19. The Sun", "20. Judgement", "21. The World",
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands", "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands", "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups", "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups", "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords", "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords", "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles", "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles", "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]

def draw_cards(num_cards):
    random.shuffle(tarot_deck)
    drawn_cards = random.sample(tarot_deck, num_cards)
    return drawn_cards

st.title("Astarot - 나만의 AI 타로 리더")
st.header("당신의 고민을 이야기해주세요.")

# 1. 상위 고민 범주를 선택하는 드롭다운 메뉴를 만듭니다.
main_category = st.selectbox(
    "고민 범주를 선택하세요:",
    ("선택", "관계", "성공", "선택", "탐색")
)

# 2. '관계'와 '성공' 범주에 하위 카테고리를 추가합니다.
sub_category = ""
if main_category == "관계":
    sub_category = st.radio("어떤 관계에 대한 고민인가요?", ("연애", "인간관계"))
elif main_category == "성공":
    sub_category = st.radio("어떤 성공에 대한 고민인가요?", ("금전운", "직업운", "학업운"))

# 3. 카테고리에 따라 다른 질문을 표시합니다.
user_input = ""
if main_category == "관계":
    if sub_category == "연애":
        user_input = st.text_area("연애 상대방과의 관계와 구체적인 상황을 입력하세요:", height=150)
    elif sub_category == "인간관계":
        user_input = st.text_area("고민이 되는 상대방과의 관계와 구체적인 상황을 입력하세요:", height=150)
elif main_category == "성공":
    if sub_category == "금전운":
        user_input = st.text_area("투자, 사업, 재테크 등 금전과 관련된 고민을 구체적으로 입력하세요:", height=150)
    elif sub_category == "직업운":
        user_input = st.text_area("취업, 이직, 승진, 사업 등 직업과 관련된 고민을 구체적으로 입력하세요:", height=150)
    elif sub_category == "학업운":
        user_input = st.text_area("시험, 전공, 진학 등 학업과 관련된 고민을 구체적으로 입력하세요:", height=150)
elif main_category == "선택":
    user_input = st.text_area("두 가지 선택지 사이에서 고민하고 있는 상황을 구체적으로 입력하세요:", height=150)
elif main_category == "탐색":
    user_input = st.text_area("자신의 내면, 미래, 운명 등과 관련된 고민을 구체적으로 입력하세요:", height=150)
elif main_category == "선택":
    st.markdown("---")
    st.write("고민 범주를 선택하면 맞춤형 질문이 나타납니다.")

# 4. '리딩 시작' 버튼을 만들고, 유효한 카테고리가 선택되었을 때만 작동하게 합니다.
if st.button("리딩 시작"):
    if main_category == "선택":
        st.warning("먼저 고민 범주를 선택해주세요.")
    elif user_input:
        with st.spinner('카드를 뽑고 있어요...'):
            cards = draw_cards(12)
            
            # 최종 카테고리명을 결정합니다.
            final_category = sub_category if sub_category else main_category
            
            ai_response = get_ai_reading(final_category, user_input, cards)
        
        st.markdown("---")
        st.subheader("타로 리딩 결과")
        st.write(ai_response)
    else:
        st.warning("고민을 입력해주세요.")