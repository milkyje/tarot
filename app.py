import streamlit as st
import google.generativeai as genai
import random
import json

# 1. AI 설정
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Streamlit Secrets에 API 키가 설정되지 않았습니다.")
    st.stop()

# 2. 데이터 통합 관리 (예전 파일들에 있던 정보를 여기 다 모았습니다)
@st.cache_data
def load_resources():
    # [자산 1] 프롬프트 데이터 불러오기
    try:
        with open('prompts.json', 'r', encoding='utf-8') as f:
            p_data = json.load(f)
    except FileNotFoundError:
        st.error("prompts.json 파일이 없습니다. 파일명을 확인해주세요.")
        st.stop()

    # [자산 2] 스프레드별 카드 장수 설정 (예전 spreads.json 기능 흡수)
    s_counts = {
        "원 카드": 1, "투 카드 스프레드": 2, "쓰리 카드 스프레드": 3,
        "켈틱 크로스": 10, "집시의 십자": 5, "아스타로트 스프레드": 12, "아스타로드 스프레드": 12,
        "다중선택 스프레드": 4
    }

    # [자산 3] 타로 카드 78장 리스트 (예전 뽑기 로직 기능 흡수)
    t_deck = [
        "0. 바보", "1. 마법사", "2. 여사제", "3. 여황제", "4. 황제", "5. 교황", "6. 연인", "7. 전차",
        "8. 힘", "9. 은둔자", "10. 운명의 수레바퀴", "11. 정의", "12. 매달린 사람", "13. 죽음",
        "14. 절제", "15. 악마", "16. 탑", "17. 별", "18. 달", "19. 태양", "20. 심판", "21. 세계",
        "완드 에이스", "완드 2", "완드 3", "완드 4", "완드 5", "완드 6", "완드 7", "완드 8", "완드 9", "완드 10",
        "완드 시종", "완드 기사", "완드 퀸", "완드 킹", "컵 에이스", "컵 2", "컵 3", "컵 4", "컵 5", "컵 6",
        "컵 7", "컵 8", "컵 9", "컵 10", "컵 시종", "컵 기사", "컵 퀸", "컵 킹", "검 에이스", "검 2", "검 3",
        "검 4", "검 5", "검 6", "검 7", "검 8", "검 9", "검 10", "검 시종", "검 기사", "검 퀸", "검 킹",
        "펜타클 에이스", "펜타클 2", "펜타클 3", "펜타클 4", "펜타클 5", "펜타클 6", "펜타클 7", "펜타클 8",
        "펜타클 9", "펜타클 10", "펜타클 시종", "펜타클 기사", "펜타클 퀸", "펜타클 킹"
    ]
    
    # [자산 4] 덱별 실제 특징
    d_info = {
        "유니버설 웨이트": "보편적 상징과 직관적 이미지 중심",
        "켈틱드래곤": "드래곤의 원소적 에너지와 고대 켈틱 신화 중심",
        "미스틱 드리밍": "꿈과 무의식, 몽환적 심리 탐색 중심",
        "노움 카드": "현실적 결실과 노동, 흙의 지혜 중심"
    }
    
    return p_data, s_counts, t_deck, d_info

PROMPTS, SPREAD_COUNTS, TAROT_DECK, DECK_INFO = load_resources()

# 3. UI 구성
st.title("🔮 asTarot 마스터 리딩")

# 카테고리 선택
main_cat = st.selectbox("대분류", list(PROMPTS.keys()))
sub_cats = [k for k in PROMPTS[main_cat].keys() if k != "templates"]
sub_cat = st.selectbox("중분류", sub_cats) if sub_cats else None

# 스프레드 및 덱 선택
target_templates = PROMPTS[main_cat][sub_cat]["templates"] if sub_cat else PROMPTS[main_cat]["templates"]
selected_spread = st.selectbox("스프레드", list(target_templates.keys()))
selected_deck = st.selectbox("타로 덱 선택", list(DECK_INFO.keys()))

user_prompt = st.text_area("고민 내용을 입력하세요", placeholder="상황을 자세히 적을수록 정확한 리딩이 가능합니다.")

# 4. 리딩 실행
if st.button("운명의 카드 뽑기"):
    if not user_prompt:
        st.warning("고민을 먼저 적어주세요.")
    else:
        with st.spinner(f"{selected_deck}으로 리딩 중..."):
            # 카드 무작위 뽑기
            count = SPREAD_COUNTS.get(selected_spread, 1)
            drawn = random.sample(TAROT_DECK, count)
            cards_text = ", ".join(drawn)
            
            # 템플릿 가져오기
            template = target_templates[selected_spread]
            
            # 덱 지식 추가
            deck_guide = f"\n(참고: 이 리딩은 '{selected_deck}' 덱의 특징인 {DECK_INFO[selected_deck]}를 바탕으로 해석하세요.)\n"
            
            # 프롬프트 완성
            # JSON의 오타(아스타로드)와 정상(아스타로트) 모두 대응하기 위해 try-except 처리
            try:
                final_prompt = template.format(
                    user_prompt=user_prompt,
                    cards=cards_text,
                    relationship_type=sub_cat if sub_cat else "일반"
                )
            except KeyError:
                # 가끔 JSON에 변수가 부족할 경우를 대비한 안전장치
                final_prompt = template.replace("{user_prompt}", user_prompt).replace("{cards}", cards_text)

            # AI 생성
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(deck_guide + final_prompt)
            
            st.divider()
            st.markdown(response.text)
            
            with st.expander("배열된 카드 확인"):
                st.write(f"선택된 카드: {cards_text}")

if st.button("다시 하기"):
    st.rerun()
