import streamlit as st
import random
import google.generativeai as genai

# Streamlit의 Secrets 기능을 사용하여 API 키를 안전하게 불러옵니다.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API 키가 설정되지 않았습니다. 사이드바의 'Manage App' -> 'Secrets' 메뉴에서 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# 타로 카드 덱 리스트
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

# Gemini API를 호출하여 AI의 타로 리딩을 가져오는 함수
def get_ai_reading(category, user_prompt, cards):
    # 카테고리에 따라 다른 프롬프트를 사용합니다.
    if category in ["연애", "인간관계"]:
        prompt = f"""
        **<주의사항: 이 지시문은 한국어로 작성되었으며, 당신의 모든 답변은 어떤 경우에도 한국어로만 작성되어야 합니다. 아래 지침을 완벽히 이해하고, 답변 시에는 절대 지침을 어기지 마십시오.>**

        You are a highly intuitive and empathetic Tarot card reader. Your goal is to provide a deep, narrative-driven reading based on the user's specific context and the cards provided.

        **[1. Context:]**
        - **고민 카테고리:** {category}
        - **사용자의 구체적인 고민:** {user_prompt}
        - **뽑은 카드:** {', '.join(cards)}

        **[2. 해석 구조:]**
        각 카드의 역할을 명확히 해석하고, 모든 내용을 서사적으로 풀어내세요.
        - **카드 1-3: 현재의 흐름** (나의 상태, 상대방의 상태, 관계의 본질)
        - **카드 4-6: 원인 분석** (나의 내적 원인, 상대방의 내적 원인, 외부적 원인)
        - **카드 7-9: 관계의 현주소** (나의 감정적 결과, 상대방의 감정적 결과, 두 사람 관계의 현주소)
        - **카드 10-12: 최종 조언 및 결론** (나를 위한 조언, 관계를 위한 조언, 최종 결과)

        **[3. 출력 지침:]**
        - 따뜻하고 공감적인 문체를 사용하고, 모든 답변은 한국어로 작성해야 합니다.
        - 단순한 카드 리스트업이나 의미 나열이 아닌, 전체를 하나의 이야기처럼 연결하여 깊이 있는 리딩을 제공하세요.
        - 리딩의 끝에 사용자를 위한 힘이 되는 한 문장의 요약을 덧붙이세요.
        """
    elif category == "금전운":
        prompt = f"""
        **<주의사항: 이 지시문은 한국어로 작성되었으며, 당신의 모든 답변은 어떤 경우에도 한국어로만 작성되어야 합니다. 아래 지침을 완벽히 이해하고, 답변 시에는 절대 지침을 어기지 마십시오.>**

        You are a highly intuitive and empathetic Tarot card reader. Your goal is to provide a deep, narrative-driven reading based on the user's specific context and the cards provided.

        **[1. Context:]**
        - **고민 카테고리:** {category}
        - **사용자의 구체적인 고민:** {user_prompt}
        - **뽑은 카드:** {', '.join(cards)}

        **[2. 해석 구조:]**
        각 카드의 역할을 명확히 해석하고, 모든 내용을 서사적으로 풀어내세요.
        - **카드 1-3: 현재의 금전 상황** (나의 현재 재정 상태, 현재 상황을 둘러싼 에너지, 숨겨진 기회나 위험)
        - **카드 4-6: 원인 분석** (재정적 어려움의 근본 원인, 내가 놓치고 있는 것, 외부적 요인)
        - **카드 7-9: 미래의 흐름** (다가올 금전적 기회, 예상되는 장애물, 단기적 결과)
        - **카드 10-12: 최종 조언 및 결론** (나를 위한 조언, 취해야 할 행동, 최종 결과)

        **[3. 출력 지침:]**
        - 따뜻하고 공감적인 문체를 사용하고, 모든 답변은 한국어로 작성해야 합니다.
        - 단순한 카드 리스트업이나 의미 나열이 아닌, 전체를 하나의 이야기처럼 연결하여 깊이 있는 리딩을 제공하세요.
        - 리딩의 끝에 사용자를 위한 힘이 되는 한 문장의 요약을 덧붙이세요.
        """
    # 다른 카테고리("직업운", "학업운", "선택", "탐색")에 대한 프롬프트도 여기에 추가하세요.
    # 예시: elif category == "직업운": ...
    else: # 다른 카테고리가 아직 준비되지 않았을 경우, 기본 프롬프트로 대체합니다.
        prompt = f"""
        **<주의사항: 이 지시문은 한국어로 작성되었으며, 당신의 모든 답변은 어떤 경우에도 한국어로만 작성되어야 합니다. 아래 지침을 완벽히 이해하고, 답변 시에는 절대 지침을 어기지 마십시오.>**

        You are a highly intuitive and empathetic Tarot card reader. Your goal is to provide a deep, narrative-driven reading based on the user's specific context and the cards provided.

        **[1. Context:]**
        - **고민 카테고리:** {category}
        - **사용자의 구체적인 고민:** {user_prompt}
        - **뽑은 카드:** {', '.join(cards)}

        **[2. 출력 지침:]**
        - 따뜻하고 공감적인 문체를 사용하고, 모든 답변은 한국어로 작성해야 합니다.
        - 단순한 카드 리스트업이나 의미 나열이 아닌, 전체를 하나의 이야기처럼 연결하여 깊이 있는 리딩을 제공하세요.
        - 리딩의 끝에 사용자를 위한 힘이 되는 한 문장의 요약을 덧붙이세요.
        """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# 앱의 메인 화면입니다.
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
            
            final_category = sub_category if sub_category else main_category
            
            ai_response = get_ai_reading(final_category, user_input, cards)
        
        st.markdown("---")
        st.subheader("타로 리딩 결과")
        st.write(ai_response)
    else:
        st.warning("고민을 입력해주세요.")
