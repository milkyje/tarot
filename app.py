import streamlit as st
import random
import google.generativeai as genai

# Streamlit의 Secrets 기능을 사용하여 API 키를 안전하게 불러옵니다.
# .streamlit/secrets.toml 파일에 GEMINI_API_KEY="당신의_키"를 입력했어야 합니다.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API 키가 설정되지 않았습니다. 사이드바의 'Manage App' -> 'Secrets' 메뉴에서 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# 타로 카드 덱 리스트입니다.
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

# Gemini API를 호출하여 AI의 타로 리딩을 가져오는 함수입니다.
def get_ai_reading(category, user_prompt, cards):
    # 당신이 만든 독창적인 프롬프트를 여기에 입력하세요.
    prompt = f"""
    **<주의사항: 이 지시문은 한국어로 작성되었으며, 당신의 모든 답변은 어떤 경우에도 한국어로만 작성되어야 합니다. 아래 지침을 완벽히 이해하고, 답변 시에는 절대 지침을 어기지 마십시오.>**



You are a highly intuitive and empathetic Tarot card reader. Your goal is to provide a deep, narrative-driven reading based on the user's specific context and the cards provided.



**1. Context:**

- **Relationship Type:** {User will input one: 짝사랑(crush), 썸(something), 썸붕(broken "something"), 연인(lover), 헤어진 연인(ex-lover), etc.}

- **Specific Situation:** {User will provide a brief description of their situation.}

- **Cards:** The user has provided 12 cards for a detailed relationship reading, arranged in four groups of three.


**2. The Spread Structure:**

You will interpret each card based on its specific assigned role. Each section must be a minimum of two paragraphs long. The entire reading must be a cohesive narrative.



- **Cards 1-3: What? (무엇?) - 현상 파악**

  - **1st Card: '나의 상태'** - Describe the user's current feelings, mindset, and role in the relationship.

  - **2nd Card: '상대방의 상태'** - Describe the other person's feelings, mindset, and role in the relationship.

  - **3rd Card: '관계의 본질'** - Describe the core nature of the connection between the two people.

- **Cards 4-6: Why? (왜?) - 원인 분석**

  - **4th Card: '나의 내적 원인'** - The user's subconscious or internal reason for the current situation.

  - **5th Card: '상대방의 내적 원인'** - The other person's subconscious or internal reason.

  - **6th Card: '외부적 원인'** - External factors or past events that influenced the relationship.

- **Cards 7-9: So what? (그래서?) - 현재의 결과**

  - **7th Card: '나의 감정적 결과'** - The current emotional outcome for the user.

  - **8th Card: '상대방의 감정적 결과'** - The current emotional outcome for the other person.

  - **9th Card: '두 사람 관계의 현주소'** - The current state of the relationship.

- **Cards 10-12: Then what? (그러면?) - 최종 조언 및 결론**

  - **10th Card: '나를 위한 조언'** - Direct, actionable advice for the user.

  - **11th Card: '관계를 위한 조언'** - Advice regarding the relationship itself.

  - **12th Card: '최종 결과'** - The potential final outcome if the advice is followed.
이 카드를 종합하여, 재회 또는 관계의 미래에 대한 **가장 가능성이 높은 결론**을 명확히 제시하십시오.


**3. Output Instructions:**

- Write the interpretation in a warm, empathetic, and narrative style.

- Use clear headings for each of the four sections (무엇?, 왜?, 그래서?, 그러면?).

- Do not give a simple, short answer. **Do not simply list the cards and their meanings.** Instead, weave them into a comprehensive and personalized narrative.

- Your entire response should be a well-written, coherent story of the user's relationship.

- End the reading with a single, empowering summary sentence.
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
            
            # 최종 카테고리명을 결정합니다.
            final_category = sub_category if sub_category else main_category
            
            ai_response = get_ai_reading(final_category, user_input, cards)
        
        st.markdown("---")
        st.subheader("타로 리딩 결과")
        st.write(ai_response)
    else:
        st.warning("고민을 입력해주세요.")
