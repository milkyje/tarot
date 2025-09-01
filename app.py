import streamlit as st
import random
import google.generativeai as genai
import json

# Streamlit의 Secrets 기능을 사용하여 API 키를 안전하게 불러옵니다.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API 키가 설정되지 않았습니다. 사이드바의 'Manage App' -> 'Secrets' 메뉴에서 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# 타로 카드 덱 리스트입니다.
# 전체 78장
tarot_deck = [
    "0. The Fool", "1. The Magician", "2. The High Priestess", "3. The Empress", "4. The Emperor", "5. The Hierophant", "6. The Lovers", "7. The Chariot", "8. Strength", "9. The Hermit", "10. Wheel of Fortune", "11. Justice", "12. The Hanged Man", "13. Death", "14. Temperance", "15. The Devil", "16. The Tower", "17. The Star", "18. The Moon", "19. The Sun", "20. Judgement", "21. The World",
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands", "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands", "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups", "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups", "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords", "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords", "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles", "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles", "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]

# 집시의 십자 스프레드용 메이저 아르카나 카드 15장
gypsy_major_arcana_deck = [
    "0. The Fool", "1. The Magician", "2. The High Priestess", "3. The Empress", "4. The Emperor",
    "5. The Hierophant", "6. The Lovers", "7. The Chariot", "8. Strength", "9. The Hermit",
    "10. Wheel of Fortune", "11. Justice", "12. The Hanged Man", "13. Death", "14. Temperance"
]

# 스프레드에 따라 다른 덱에서 카드를 뽑는 함수
def draw_cards(num_cards, spread_name):
    if spread_name == "집시의 십자":
        random.shuffle(gypsy_major_arcana_deck)
        return random.sample(gypsy_major_arcana_deck, num_cards)
    else:
        random.shuffle(tarot_deck)
        return random.sample(tarot_deck, num_cards)

# JSON 파일에서 프롬프트와 스프레드 데이터를 불러옵니다.
def load_data():
    try:
        with open('prompts.json', 'r', encoding='utf-8') as f:
            prompts_data = json.load(f)
        with open('spreads.json', 'r', encoding='utf-8') as f:
            spreads_data = json.load(f)
        return prompts_data, spreads_data
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'prompts.json'과 'spreads.json' 파일이 프로젝트 루트에 있는지 확인해주세요.")
        st.stop()
    except json.JSONDecodeError:
        st.error("JSON 파일 형식이 올바르지 않습니다. 파일을 확인해주세요.")
        st.stop()

prompts_data, spreads_data = load_data()

# 스프레드 모양을 시각적으로 표시하는 함수
def display_spread_layout(spread_name, cards, spreads_data):
    st.markdown("---")
    st.subheader("뽑은 카드")
    positions = spreads_data.get(spread_name, {}).get("positions", [])

    if spread_name == "쓰리 카드 스프레드(3)":
        cols = st.columns(3)
        for i, card in enumerate(cards):
            with cols[i]:
                st.markdown(f"**{positions[i]}**")
                st.write(card)
    elif spread_name == "집시의 십자 스프레드(5)":
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"**{positions[3]}**")
        st.write(cards[3])
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(3)
        with cols[0]:
            st.markdown(f"**{positions[0]}**")
            st.write(cards[0])
        with cols[1]:
            st.markdown(f"**{positions[1]}**")
            st.write(cards[1])
        with cols[2]:
            st.markdown(f"**{positions[2]}**")
            st.write(cards[2])
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"**{positions[4]}**")
        st.write(cards[4])
        st.markdown("</div>", unsafe_allow_html=True)

    elif spread_name == "켈틱 크로스(10)":
        st.markdown("<div style='display: flex; justify-content: center; align-items: center;'>", unsafe_allow_html=True)
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>", unsafe_allow_html=True)
        for i in range(9, 5, -1):
            st.markdown(f"**{positions[i]}**")
            st.write(cards[i])
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center; justify-content: center; margin-left: 20px;'>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        top_row = st.columns([1,1,1])
        with top_row[1]:
            st.markdown(f"**{positions[5]}**")
            st.write(cards[5])
        
        mid_row = st.columns([1,1,1])
        with mid_row[0]:
            st.markdown(f"**{positions[3]}**")
            st.write(cards[3])
        with mid_row[1]:
            st.markdown(f"**{positions[1]}**")
            st.write(cards[1])
            st.markdown(f"**{positions[0]}**")
            st.write(cards[0])
        with mid_row[2]:
            st.markdown(f"**{positions[2]}**")
            st.write(cards[2])

        bottom_row = st.columns([1,1,1])
        with bottom_row[1]:
            st.markdown(f"**{positions[4]}**")
            st.write(cards[4])
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif spread_name.startswith("다중선택 스프레드"):
        st.markdown(f"**{positions[0]}**")
        st.write(cards[0])
        
        for i in range(1, len(cards), 2):
            st.markdown("---")
            st.markdown(f"**선택지 {int((i+1)/2)}**")
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"**{positions[1]}**")
                st.write(cards[i])
            with cols[1]:
                st.markdown(f"**{positions[2]}**")
                st.write(cards[i+1])

    else:
        for i, card in enumerate(cards):
            st.markdown(f"**{i+1}. {positions[i]}**")
            st.write(card)

# Gemini API를 호출하여 AI의 타로 리딩을 가져오는 함수
def get_ai_reading(category, user_prompt, spread_name, cards):
    current_category = prompts_data.get(category, {})
    prompt_template = current_category.get("templates", {}).get(spread_name)
    
    if not prompt_template:
        st.warning(f"'{category}'에 대한 '{spread_name}' 템플릿이 아직 준비되지 않았습니다. 기본 프롬프트를 사용합니다.")
        return "죄송합니다. 아직 해당 카테고리에 대한 리딩을 준비하지 못했습니다."

    prompt = prompt_template.format(category=category, user_prompt=user_prompt, cards=', '.join(cards))
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# 앱의 메인 화면입니다.
st.title("asTarot - 내가 쓰려고 만든 AI 타로")
st.header("당신의 고민을 이야기해주세요.")

# 1. 상위 고민 범주를 선택하는 드롭다운 메뉴를 만듭니다.
main_category = st.selectbox(
    "고민 범주를 선택하세요:",
    ("해당 카테고리에 맞는 질문을 골라주세요", "관계", "성공", "결정", "탐색")
)

# 2. 하위 카테고리 및 질문 입력 필드 동적 생성
sub_category = main_category
user_input_label = "고민을 구체적으로 입력하세요:"
choice_input_visible = False

if main_category == "관계":
    sub_category_options = ["연애", "대인관계", "기타"]
    sub_category = st.radio("어떤 관계에 대한 고민인가요?", sub_category_options)
    if sub_category == "연애":
        user_input_label = "연애 상대방과의 관계와 구체적인 상황을 입력하세요:"
    elif sub_category == "대인관계":
        user_input_label = "가족, 친구, 동료, 온라인/익명 관계 등 상대방과의 구체적인 상황을 입력하세요:"
    elif sub_category == "기타":
        user_input_label = "반려동물, 식물 등 생명체 또는 덕질 대상, 사물과의 관계에 대한 구체적인 상황을 입력하세요:"
elif main_category == "성공":
    sub_category_options = ["금전운", "직업운", "학업운"]
    sub_category = st.radio("어떤 성공에 대한 고민인가요?", sub_category_options)
    if sub_category == "금전운":
        user_input_label = "금전 흐름, 투자, 사업, 재테크, 복권 등 돈과 관련된 모든 고민을 구체적으로 입력하세요:"
    elif sub_category == "직업운":
        user_input_label = "취업, 이직, 승진, 사업 등 직업과 관련된 구체적인 고민을 입력하세요:"
    elif sub_category == "학업운":
        user_input_label = "시험, 전공, 진학 등 학업과 관련된 구체적인 고민을 입력하세요:"
elif main_category == "결정":
    sub_category_options = ["다중 선택", "우선순위 결정", "타이밍 결정", "포기 여부 결정", "접근 방식 결정", "가치 판단 및 윤리적 결정"]
    sub_category = st.radio("어떤 종류의 결정에 대한 고민인가요?", sub_category_options)
    if sub_category == "다중 선택":
        choice_input_visible = True
        user_input_label = "여러 선택지 중 가장 적합한 것을 고르기 위한 상황을 구체적으로 입력하세요:"
    elif sub_category == "우선순위 결정":
        user_input_label = "여러 가지를 모두 할 수 없을 때, 어떤 순서로 진행할지 고민하는 상황을 입력하세요:"
    elif sub_category == "타이밍 결정":
        user_input_label = "무엇을 할지는 정했지만 '언제' 할지 고민하는 상황을 구체적으로 입력하세요:"
    elif sub_category == "포기 여부 결정":
        user_input_label = "어떤 상황을 계속할지, 아니면 멈춰야 할지 고민하는 상황을 입력하세요:"
    elif sub_category == "접근 방식 결정":
        user_input_label = "목표는 같지만 '어떻게' 할지, 방법이나 방향을 선택하는 상황을 입력하세요:"
    elif sub_category == "가치 판단 및 윤리적 결정":
        user_input_label = "어떤 가치에 따라 결정을 내릴지 고민하고 있는 윤리적/가치적 문제를 입력하세요:"
elif main_category == "탐색":
    sub_category = "탐색"
    user_input_label = "삶의 의미, 내면 탐구, 영성, 운명 등 근원적인 고민에 대해 자유롭게 입력하세요:"

if main_category == "해당 카테고리에 맞는 질문을 골라주세요":
    st.markdown("---")
    st.write("고민 범주를 선택하면 맞춤형 질문이 나타납니다.")
else:
    user_input = st.text_area(user_input_label, height=150)
    
    if choice_input_visible:
        choice_input = st.text_area("선택지들을 한 줄에 하나씩 입력하세요 (최대 5개):", height=150)
        choices = [c.strip() for c in choice_input.split('\n') if c.strip()]
        if len(choices) > 5:
            st.warning("선택지는 최대 5개까지 입력할 수 있습니다.")
            st.stop()
    else:
        choices = []

    # 스프레드 목록을 동적으로 필터링
    filtered_spreads = []
    spread_name_map = {}
    for name, data in spreads_data.items():
        if 'categories' in data:
            if sub_category in data['categories']:
                display_name = f"{name}({data['num_cards']})"
                filtered_spreads.append(display_name)
                spread_name_map[display_name] = name

    # 다중선택 스프레드 로직
    if sub_category == "다중 선택":
        if choices:
            num_cards = 1 + len(choices) * 2
            display_name = f"다중선택 스프레드({num_cards})"
            filtered_spreads = [display_name]
            spread_name_map[display_name] = "다중선택 스프레드"
        else:
            st.warning("선택지를 입력해주세요.")
            st.stop()

    spread_name_with_count = st.selectbox(
        "사용할 스프레드를 선택하세요:",
        options=filtered_spreads,
        help="스프레드를 선택하면 리딩에 사용되는 카드 수와 위치별 의미가 달라집니다."
    )
    
    spread_name = spread_name_map.get(spread_name_with_count)

    if st.button("리딩 시작"):
        if not user_input:
            st.warning("고민을 입력해주세요.")
        elif sub_category == "다중 선택" and not choices:
            st.warning("선택지를 입력해주세요.")
        else:
            with st.spinner('카드를 뽑고 있어요...'):
                num_cards = spreads_data.get(spread_name, {}).get("num_cards", 0)
                if spread_name == "다중선택 스프레드":
                    num_cards = 1 + len(choices) * 2
                
                cards = draw_cards(num_cards, spread_name)

            display_spread_layout(spread_name_with_count, cards, spreads_data)
            
            st.markdown("---")
            st.subheader("타로 리딩 결과")
            ai_response = get_ai_reading(sub_category, user_input, spread_name, cards)
            st.write(ai_response)
            
            # 결과 화면에 버튼 추가
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("추가 질문하기"):
                    st.info("이 기능은 추후 추가될 예정입니다.")
            with col2:
                if st.button("새로운 질문하기"):
                    st.experimental_rerun()
