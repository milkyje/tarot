import streamlit as st
import google.generativeai as genai
import random
import json

# 1. 페이지 설정
st.set_page_config(page_title="asTarot 마스터", page_icon="🔮")

# 2. 데이터 로드
try:
    with open('prompts.json', 'r', encoding='utf-8') as f:
        PROMPTS = json.load(f)
except Exception as e:
    st.error(f"prompts.json 파일을 읽을 수 없습니다: {e}")
    st.stop()

SPREAD_COUNTS = {
    "원 카드": 1, "투 카드 스프레드": 2, "쓰리 카드 스프레드": 3,
    "켈틱 크로스": 10, "집시의 십자": 5, "아스타로트 스프레드": 12,
    "다중선택 스프레드": 4
}

TAROT_DECK = [
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

# 3. AI 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 API 키를 등록해주세요.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 4. UI 구성
st.title("🔮 asTarot 마스터 리딩")

main_cat = st.selectbox("대분류", list(PROMPTS.keys()))
sub_cats = [k for k in PROMPTS[main_cat].keys() if k != "templates"]
sub_cat = st.selectbox("중분류", sub_cats) if sub_cats else None

# 템플릿 선택 및 예외 처리
try:
    target_templates = PROMPTS[main_cat][sub_cat]["templates"] if sub_cat else PROMPTS[main_cat]["templates"]
    selected_spread = st.selectbox("스프레드", list(target_templates.keys()))
except KeyError:
    st.error("선택한 카테고리에 맞는 템플릿을 찾을 수 없습니다.")
    st.stop()

user_prompt = st.text_area("고민 내용을 입력하세요")

# 5. 리딩 실행
if st.button("운명의 카드 뽑기"):
    if not user_prompt:
        st.warning("고민 내용을 먼저 입력해주세요.")
    else:
        with st.spinner("마스터 아스타로트가 통찰을 얻는 중..."):
            # 카드 샘플링
            count = SPREAD_COUNTS.get(selected_spread, 1)
            drawn_cards = random.sample(TAROT_DECK, count)
            cards_text = ", ".join(drawn_cards)
            
            template = target_templates[selected_spread]
            
            # AI 모델 호출 (가장 안정적인 모델 명칭 사용)
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 프롬프트 구성
                instruction = "당신은 타로 마스터 아스타로트입니다. 가성비와 현실적 조언을 중심으로 리딩하세요.\n\n"
                final_prompt = template.format(
                    user_prompt=user_prompt,
                    cards=cards_text,
                    relationship_type=sub_cat if sub_cat else "일반"
                )
                
                response = model.generate_content(instruction + final_prompt)
                
                # 결과 출력
                st.divider()
                result_text = response.text
                st.markdown(result_text)
                
                # 📋 프롬프트/결과 복사 기능 추가
                st.subheader("📍 리딩 결과 관리")
                st.copy_to_clipboard(result_text)
                st.success("리딩 내용이 클립보드에 복사되었습니다!")
                
                with st.expander("배열된 카드 확인"):
                    st.write(f"카드: {cards_text}")
                    
            except Exception as e:
                st.error(f"리딩 중 오류가 발생했습니다: {e}")
                st.info("Reboot App을 실행하거나 잠시 후 다시 시도해 보세요.")

if st.button("새로 시작하기"):
    st.rerun()
