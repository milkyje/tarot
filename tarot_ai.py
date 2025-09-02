import google.generativeai as genai
import json
import streamlit as st

# API 키 설정은 config.py로 이동했으므로 삭제

# AI 리딩을 생성하는 함수 (프롬프트도 함께 반환)
def get_ai_reading(category, user_input, choices, spread_name, cards, prompts_data):
    try:
        # prompts.json에서 해당 카테고리와 스프레드에 맞는 템플릿을 찾음
        if category in prompts_data and "templates" in prompts_data[category] and spread_name in prompts_data[category]["templates"]:
            prompt_template = prompts_data[category]["templates"][spread_name]
        elif category in prompts_data.get("관계", {}) and "templates" in prompts_data["관계"].get(category, {}) and spread_name in prompts_data["관계"][category]["templates"]:
            prompt_template = prompts_data["관계"][category]["templates"][spread_name]
        elif category in prompts_data.get("성공", {}) and "templates" in prompts_data["성공"].get(category, {}) and spread_name in prompts_data["성공"][category]["templates"]:
            prompt_template = prompts_data["성공"][category]["templates"][spread_name]
        elif category in prompts_data.get("결정", {}) and "templates" in prompts_data["결정"].get(category, {}) and spread_name in prompts_data["결정"][category]["templates"]:
            prompt_template = prompts_data["결정"][category]["templates"][spread_name]
        elif category == "탐색" and "templates" in prompts_data["탐색"] and spread_name in prompts_data["탐색"]["templates"]:
            prompt_template = prompts_data["탐색"]["templates"][spread_name]
        elif category == "다중 선택" and "templates" in prompts_data["다중 선택"] and spread_name in prompts_data["다중 선택"]["templates"]:
            prompt_template = prompts_data["다중 선택"]["templates"][spread_name]
        else:
            return "죄송합니다. 해당 카테고리 또는 스프레드에 대한 프롬프트 템플릿을 찾을 수 없습니다.", ""

        # 프롬프트에 동적 데이터 포매팅
        if spread_name == "다중선택 스프레드":
            prompt = prompt_template.format(
                category=category,
                user_prompt=user_input,
                choices=choices,
                cards=cards
            )
        else:
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
        return f"리딩을 생성하는 중 오류가 발생했습니다: {e}"