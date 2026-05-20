from utils.llm_client import chat

SYSTEM_PROMPT = """You are an expert career advisor and technical recruiter specializing in AI Engineering and Software Engineering roles.
Analyze CVs with the eye of a senior hiring manager at top tech companies.
Always respond in the same language as the CV content. If the CV is in Vietnamese, respond in Vietnamese. If English, respond in English.
Be specific, actionable, and honest."""

ANALYSIS_PROMPT = """Analyze the following CV and provide a comprehensive evaluation.

CV CONTENT:
{cv_text}

TARGET ROLE: {target_role}

Provide your analysis in the following structured format:

## 📊 Overall Score: [X/100]

## ✅ Strengths
List 3-5 specific strengths with brief explanations.

## ⚠️ Weaknesses
List 3-5 specific weaknesses or gaps.

## 🎯 Improvement Suggestions
List 5-7 concrete, actionable improvements ranked by priority.

## 🔑 Keywords Missing
List important keywords/skills missing for the target role that ATS systems look for.

## 💡 Quick Wins
List 2-3 changes that would immediately improve this CV's impact.

## 📈 Match Score for {target_role}: [X%]
Brief explanation of the match score.
"""


def analyze_cv(cv_text: str, target_role: str = "AI Engineer", provider: str = "groq") -> str:
    prompt = ANALYSIS_PROMPT.format(cv_text=cv_text, target_role=target_role)
    return chat(prompt=prompt, system=SYSTEM_PROMPT, provider=provider)
