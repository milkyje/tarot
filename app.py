import streamlit as st
import random
import google.generativeai as genai

# Streamlit의 Secrets 기능을 사용하여 API 키를 안전하게 불러옵니다.
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

# 타로 카드 이미지 URL 딕셔너리입니다. (실제 이미지 경로로 대체 필요)
image_map = {card: f"https://placehold.co/100x150/d9f0ff/000000?text={card.replace(' ', '%20')}" for card in tarot_deck}
image_map["Tarot Card Back"] = "https://placehold.co/100x150/d4af37/ffffff?text=Tarot+Card"

def get_tarot_reading(prompt, cards, spread_name):
    """
    제공된 프롬프트와 카드 목록을 기반으로 Gemini 모델에게 타로 리딩을 요청합니다.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-05-20",
        system_instruction=f"당신은 {spread_name} 스프레드를 전문적으로 해석하는 타로 마스터입니다. 사용자의 질문과 선택된 카드들을 바탕으로 깊이 있고 진심이 담긴 조언을 제공해 주세요. 단, 너무 구체적이거나 단정적인 해석보다는 추상적인 의미도 함께 제시하여 사용자가 스스로 해석할 여지를 남겨주세요. 실질적이고 구체적인 적용 방안을 제시하는 것에 초점을 맞춰주세요."
    )
    
    card_list_str = ", ".join(cards)
    full_prompt = f"사용자의 질문: '{prompt}'\n선택된 카드: {card_list_str}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"타로 리딩 중 오류가 발생했습니다: {e}")
        return "죄송합니다, 리딩을 가져오는 데 실패했습니다. 잠시 후 다시 시도해 주세요."

def display_cards(selected_cards):
    """
    선택된 카드들을 UI에 표시합니다.
    """
    cols = st.columns(len(selected_cards))
    for i, card in enumerate(selected_cards):
        with cols[i]:
            st.image(image_map[card], caption=card, use_column_width=True)

st.title("타로 마스터")
st.write("당신의 고민을 이야기하고 타로 카드의 지혜를 얻어보세요.")

# --- 스프레드 선택 로직 ---
st.sidebar.header("고민 범주 선택")
main_category = st.sidebar.radio("주요 고민 범주:", ["연애", "성공", "선택", "인간관계", "탐색"])

spread_options = []
if main_category == "연애":
    spread_options = [
        "쓰리 카드 (3장, 관계의 과거/현재/미래)",
        "집시의 십자 (5장, 관계 심층 분석)",
        "썸/고백운 (3장, 썸의 흐름과 결과)",
        "짝사랑운 (3장, 상대방의 마음과 관계 발전 가능성)",
        "새로운 연애운 (3장, 앞으로 다가올 인연)",
        "관계운 (3장, 관계의 문제점과 해결책)"
    ]
elif main_category == "성공":
    spread_options = [
        "쓰리 카드 (3장, 고민의 흐름과 결과)",
        "금전운 (3장, 재정 상태의 흐름)",
        "직업운 (3장, 직장생활의 방향성과 조언)",
        "학업운 (3장, 학업 성과와 학습 방법)"
    ]
elif main_category == "선택":
    spread_options = [
        "양자택일 (2장, 두 선택지의 결과)",
        "다중선택 (최대 5장, 여러 선택지 비교)",
    ]
elif main_category == "인간관계":
    spread_options = [
        "쓰리 카드 (3장, 고민의 흐름과 결과)",
        "친구 관계 (3장, 관계의 문제점과 조언)",
        "가족 관계 (3장, 가족 내 갈등 해결)",
        "대인 관계 (3장, 대인 관계 개선을 위한 조언)"
    ]
elif main_category == "탐색":
    spread_options = [
        "원 카드 (1장, 간단한 질문에 대한 답)",
        "오늘의 운세 (1장, 오늘의 에너지와 조언)",
        "나의 재능 (3장, 숨겨진 재능과 잠재력)",
        "인생의 의미 (5장, 인생의 방향성 탐색)"
    ]

selected_spread_text = st.sidebar.radio("스프레드 선택:", spread_options)
selected_spread_name = selected_spread_text.split(" (")[0]
st.markdown("---")

# --- 세션 상태 관리 ---
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []
if 'last_spread' not in st.session_state:
    st.session_state.last_spread = selected_spread_name
if 'multi_choices' not in st.session_state:
    st.session_state.multi_choices = [""]
if 'choice_results' not in st.session_state:
    st.session_state.choice_results = {}
if 'last_user_input' not in st.session_state:
    st.session_state.last_user_input = ""

# 스프레드 변경 시 상태 초기화
if st.session_state.last_spread != selected_spread_name:
    st.session_state.show_result = False
    st.session_state.selected_cards = []
    st.session_state.multi_choices = [""]
    st.session_state.choice_results = {}
    st.session_state.last_user_input = ""
    st.session_state.last_spread = selected_spread_name
    st.rerun()

st.header(f"'{selected_spread_name}' 스프레드")
user_input = ""
num_cards = 0

# --- 스프레드별 로직 ---
if selected_spread_name == "다중선택":
    user_input = st.text_area("고민하고 있는 상황을 구체적으로 입력하세요:", height=150, key="multi_user_input")
    
    # + 버튼으로 선택지 추가
    if st.button("+ 선택지 추가", disabled=len(st.session_state.multi_choices) >= 5):
        st.session_state.multi_choices.append("")
        st.rerun()

    for i in range(len(st.session_state.multi_choices)):
        st.session_state.multi_choices[i] = st.text_input(f"선택지 {chr(65+i)}:", value=st.session_state.multi_choices[i], key=f"choice_{i}")

    if st.button("카드를 뽑겠습니다.", use_container_width=True, disabled=not (user_input and all(st.session_state.multi_choices))):
        num_cards = len(st.session_state.multi_choices)
        st.session_state.selected_cards = random.sample(tarot_deck, num_cards)
        st.session_state.show_result = True
        st.session_state.last_user_input = user_input
        st.rerun()

else: # 일반 스프레드
    user_input = st.text_area("고민을 구체적으로 입력하세요:", height=150)
    
    if selected_spread_name == "원 카드":
        num_cards = 1
    elif selected_spread_name in ["양자택일", "오늘의 운세", "금전운", "직업운", "학업운", "친구 관계", "가족 관계", "대인 관계", "썸/고백운", "짝사랑운", "새로운 연애운", "관계운", "쓰리 카드", "나의 재능"]:
        num_cards = 3
    elif selected_spread_name in ["집시의 십자 (관계 심층 분석)", "인생의 의미"]:
        num_cards = 5
    elif selected_spread_name == "양자택일":
        choice_a = st.text_input("선택지 A:")
        choice_b = st.text_input("선택지 B:")
        user_input = f"{user_input}\n선택지 A: {choice_a}\n선택지 B: {choice_b}"
        num_cards = 2

    if st.button("카드를 뽑겠습니다.", use_container_width=True, disabled=not user_input):
        st.session_state.selected_cards = random.sample(tarot_deck, num_cards)
        st.session_state.show_result = True
        st.session_state.last_user_input = user_input
        st.rerun()

# --- 리딩 결과 화면 ---
if st.session_state.show_result:
    st.markdown("---")
    st.subheader("뽑으신 카드")
    display_cards(st.session_state.selected_cards)
    
    st.markdown("---")
    st.subheader("타로 리딩 결과")

    if selected_spread_name == "다중선택":
        for i, choice in enumerate(st.session_state.multi_choices):
            card = st.session_state.selected_cards[i]
            if choice not in st.session_state.choice_results:
                with st.spinner(f"'{choice}'에 대한 리딩을 가져오고 있습니다..."):
                    prompt = f"질문: '{st.session_state.last_user_input}'의 상황에서 '{choice}'를 선택했을 때의 결과는 무엇인가요? 선택된 카드: {card}"
                    reading = get_tarot_reading(prompt, [card], "다중선택")
                    st.session_state.choice_results[choice] = reading
            
            st.markdown(f"**선택지 {chr(65+i)} ({choice}) 카드:**")
            st.image(image_map[card], caption=card, use_column_width=True)
            st.markdown(f"**리딩:**\n{st.session_state.choice_results[choice]}")
            
            # 모든 리딩에 적용되는 추가 질문 기능
            st.markdown(f"---")
            follow_up_prompt = st.text_input(f"'{choice}'에 대해 더 궁금한 점이 있으신가요?", key=f"follow_up_{i}")
            if st.button("추가 질문하기", key=f"follow_up_btn_{i}", disabled=not follow_up_prompt):
                with st.spinner("타로 마스터가 추가 질문에 답하고 있습니다..."):
                    follow_up_reading = get_tarot_reading(follow_up_prompt, [card], "추가 질문")
                    st.markdown(f"**타로 마스터의 답변:**\n{follow_up_reading}")

    else: # 일반 스프레드
        with st.spinner("타로 마스터가 카드를 해석하고 있습니다..."):
            reading_result = get_tarot_reading(st.session_state.last_user_input, st.session_state.selected_cards, selected_spread_name)
            st.markdown(reading_result)
        
        # 모든 리딩에 적용되는 추가 질문 기능
        st.markdown(f"---")
        follow_up_prompt = st.text_input("리딩 내용에 대해 더 궁금한 점이 있으신가요?", key="main_follow_up")
        if st.button("추가 질문하기", key="main_follow_up_btn", disabled=not follow_up_prompt):
            with st.spinner("타로 마스터가 추가 질문에 답하고 있습니다..."):
                follow_up_reading = get_tarot_reading(follow_up_prompt, st.session_state.selected_cards, "추가 질문")
                st.markdown(f"**타로 마스터의 답변:**\n{follow_up_reading}")


    st.markdown("---")
    if st.button("새로운 질문하기", use_container_width=True):
        st.session_state.show_result = False
        st.session_state.selected_cards = []
        st.session_state.multi_choices = [""]
        st.session_state.choice_results = {}
        st.session_state.last_user_input = ""
        st.rerun()
