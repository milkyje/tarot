import google.generativeai as genai
import json
import streamlit as st

# API 키 설정
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API 키가 설정되지 않았습니다. 사이드바의 'Manage App' -> 'Secrets' 메뉴에서 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

# AI 리딩을 생성하는 함수 (프롬프트도 함께 반환)
def get_ai_reading(category, user_input, choices, spread_name, cards, prompts_data):
    try:
        if category == "다중 선택":
            prompt_template = prompts_data.get(category, {}).get("templates", {}).get(spread_name)
            if not prompt_template:
                return "죄송합니다. 해당 스프레드에 대한 프롬프트 템플릿이 없습니다.", ""
            
            prompt = prompt_template.format(
                category=category,
                user_prompt=user_input,
                choices=choices,
                cards=cards
            )
        else:
            prompt_template = prompts_data.get(category, {}).get("templates", {}).get(spread_name)
            if not prompt_template:
                return "죄송합니다. 해당 스프레드에 대한 프롬프트 템플릿이 없습니다.", ""

            prompt = prompt_template.format(
                category=category,
                user_prompt=user_input,
                cards=cards
            )

        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text, prompt

    except Exception as e:
        return f"리딩을 생성하는 중 오류가 발생했습니다: {e}", ""

# 추가 질문에 대한 리딩을 생성하는 함수
def get_follow_up_reading(previous_reading, user_input, cards, follow_up_input):
    try:
        prompt = f"""
        당신은 타로 리딩 전문가입니다. 이전에 제공했던 리딩과 사용자의 추가 질문에 답해주세요.

        - **이전 리딩의 요약:**
          이전 리딩은 '{previous_reading}' 입니다.

        - **사용자의 원래 고민:**
          '{user_input}'

        - **뽑았던 카드:**
          {', '.join(cards)}

        - **추가 질문:**
          '{follow_up_input}'

        위 정보를 바탕으로, 사용자의 추가 질문에 대해 심층적인 리딩과 조언을 제공해주세요.
        """
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"추가 질문에 대한 답변을 생성하는 중 오류가 발생했습니다: {e}"
