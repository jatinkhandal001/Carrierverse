import gradio as gr
import random
import time
import threading
from typing import List, Dict, Tuple
import pandas as pd

# Decorator to call a function periodically every X seconds
def periodic_call(interval_sec=600):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def loop():
                while True:
                    try:
                        func(*args, **kwargs)
                    except Exception as e:
                        print(f"[Periodic Error] {e}")
                    time.sleep(interval_sec)
            t = threading.Thread(target=loop, daemon=True)
            t.start()
        return wrapper
    return decorator

# ---------------------------------------------
# Define the AI Class (CareerVerseAI)
# ---------------------------------------------
class CareerVerseAI:
    def __init__(self):
        # Your existing data setup (career_database, skills_database, etc.)
        self.career_database = {
            "Full Stack Developer": {
                "salary": "$75,000 - $120,000",
                "description": "Build end-to-end web applications using modern technologies",
                "required_skills": ["JavaScript", "React", "Node.js", "SQL", "HTML/CSS"],
                "roadmap": [
                    "Master JavaScript fundamentals",
                    "Learn React and state management",
                    "Build backend APIs with Node.js",
                    "Deploy applications to cloud platforms"
                ],
                "match_keywords": ["javascript", "react", "web", "frontend", "backend", "fullstack"]
            },
            # Add remaining roles...
        }

        self.skills_database = [
            "JavaScript", "Python", "React", "Node.js", "SQL", "HTML/CSS",
            "Git", "AWS", "Docker", "MongoDB", "TypeScript", "Vue.js",
            "Java", "C++", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin",
            "Machine Learning", "Data Analysis", "Statistics", "Pandas",
            "TensorFlow", "PyTorch", "Scikit-learn", "Tableau", "Power BI",
            "Figma", "Adobe Photoshop", "Adobe Illustrator", "Sketch",
            "Kubernetes", "Jenkins", "Terraform", "Ansible", "Linux",
            "Network Security", "Ethical Hacking", "Penetration Testing"
        ]

        self.personality_questions = [
            {
                "question": "What type of work environment do you prefer?",
                "options": [
                    "Collaborative team environment",
                    "Independent work with minimal supervision",
                    "Fast-paced startup atmosphere",
                    "Structured corporate setting"
                ]
            },
            # Add more questions...
        ]

    def analyze_skills_and_interests(self, skills: List[str], interests: List[str]) -> List[Dict]:
        # Same logic as before
        recommendations = []
        for career, details in self.career_database.items():
            skill_matches = len(set([s.lower() for s in skills]) & set([s.lower() for s in details["required_skills"]]))
            skill_score = (skill_matches / len(details["required_skills"])) * 60
            interest_matches = sum(1 for interest in interests if any(k in interest.lower() for k in details["match_keywords"]))
            interest_score = (interest_matches / len(interests) if interests else 0) * 40
            match_score = min(95, max(65, skill_score + interest_score + random.randint(5, 15)))
            recommendations.append({
                "title": career,
                "match": int(match_score),
                "salary": details["salary"],
                "description": details["description"],
                "skills": details["required_skills"],
                "roadmap": details["roadmap"]
            })
        recommendations.sort(key=lambda x: x["match"], reverse=True)
        return recommendations[:3]

    def analyze_resume(self, resume_text: str) -> Dict:
        if not resume_text:
            return {"error": "Please provide resume text"}
        word_count = len(resume_text.split())
        sections = ["experience", "education", "skills", "projects"]
        section_score = sum(20 for s in sections if s in resume_text.lower())
        numbers = len([w for w in resume_text.split() if any(c.isdigit() for c in w)])
        achievement_score = min(25, numbers * 2)
        overall_score = min(95, max(60, section_score + achievement_score + random.randint(10, 20)))
        ats_score = min(95, max(70, overall_score + random.randint(-10, 10)))
        keyword_score = min(90, max(60, len(set(resume_text.lower().split()) & set([skill.lower() for skill in self.skills_database])) * 3))
        format_score = random.randint(85, 95)
        suggestions = [
            "Add more quantifiable achievements with specific numbers and percentages",
            "Include relevant keywords for your target role and industry",
            "Optimize section headings for ATS systems (Experience, Education, Skills)",
            "Add a professional summary section at the top"
        ]
        return {
            "overall": overall_score,
            "ats": ats_score,
            "keywords": keyword_score,
            "format": format_score,
            "suggestions": random.sample(suggestions, 4)
        }

    def get_ai_career_advice(self, question: str) -> str:
        lower = question.lower()
        if "interview" in lower:
            return "Practice STAR method and review job descriptions before interviews."
        elif "skill" in lower:
            return "Focus on one deep skill and showcase it through projects."
        return "Stay focused and network consistently — that’s key to career success."

    def get_dummy_trigger(self):
        """Used by periodic trigger to wake up app"""
        print("[Trigger] App is awake 🚀")

career_ai = CareerVerseAI()

# Decorator to wake functions periodically
@periodic_call(600)
def trigger_awake():
    career_ai.get_dummy_trigger()

# Start the periodic thread
trigger_awake()

# ---------------------------------------------
# Gradio Interface Functions
# ---------------------------------------------
def get_career_recommendations(skills_input, interests_input):
    if not skills_input or not interests_input:
        return "Please enter both skills and interests."
    skills = [s.strip() for s in skills_input.split(",")]
    interests = [s.strip() for s in interests_input.split(",")]
    recommendations = career_ai.analyze_skills_and_interests(skills, interests)
    result = "## 🚀 Your Career Recommendations\n"
    for rec in recommendations:
        result += f"### {rec['title']} ({rec['match']}% match)\n"
        result += f"💰 Salary: {rec['salary']}\n📝 {rec['description']}\n"
        result += f"**Skills:** {', '.join(rec['skills'])}\n"
        result += "**Roadmap:**\n" + "\n".join([f"- {step}" for step in rec['roadmap']]) + "\n\n"
    return result

def analyze_resume_text(resume_text):
    analysis = career_ai.analyze_resume(resume_text)
    if "error" in analysis:
        return analysis["error"]
    result = f"""📄 **Resume Score**
- Overall: {analysis['overall']}/100
- ATS Compatibility: {analysis['ats']}/100
- Keywords: {analysis['keywords']}/100
- Format: {analysis['format']}/100

💡 Suggestions:
""" + "\n".join([f"- {s}" for s in analysis['suggestions']])
    return result

def chat_with_ai(message, history):
    response = career_ai.get_ai_career_advice(message)
    history.append([message, response])
    return "", history

def take_personality_quiz():
    out = "### 🧠 Career Personality Assessment\n"
    for i, q in enumerate(career_ai.personality_questions, 1):
        out += f"**Q{i}. {q['question']}**\n" + "\n".join([f"- {opt}" for opt in q['options']]) + "\n\n"
    return out

# ---------------------------------------------
# Gradio App Layout
# ---------------------------------------------
def create_interface():
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink", neutral_hue="slate"),
        title="CareerVerse",
        css="""
        .gradio-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        .gr-button-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 12px;
            font-weight: 600;
        }
        .gr-panel {
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        """
    ) as app:
        gr.Markdown("## CareerVerse AI - Unlock Your Career Potential 💼")

        with gr.Tabs():
            with gr.Tab("🎯 Career Recommendations"):
                s = gr.Textbox(label="Your Skills (comma-separated)")
                i = gr.Textbox(label="Your Interests (comma-separated)")
                o = gr.Markdown()
                btn = gr.Button("Get Career Recommendations")
                btn.click(get_career_recommendations, [s, i], o)

            with gr.Tab("📄 Resume Analyzer"):
                r = gr.Textbox(label="Paste Your Resume Text", lines=10)
                ro = gr.Markdown()
                abtn = gr.Button("Analyze Resume")
                abtn.click(analyze_resume_text, r, ro)

            with gr.Tab("🤖 AI Career Mentor"):
                c = gr.Chatbot(label="Chat with Mentor")
                ci = gr.Textbox(label="Your Question")
                cbtn = gr.Button("Send")
                cbtn.click(chat_with_ai, [ci, c], [ci, c])
                ci.submit(chat_with_ai, [ci, c], [ci, c])

            with gr.Tab("🛠️ Skill Gap Analysis"):
                gr.Markdown("Coming soon...")

            with gr.Tab("🧠 Personality Quiz"):
                qb = gr.Button("Start Quiz")
                qo = gr.Markdown()
                qb.click(take_personality_quiz, outputs=qo)

        return app

# Launch App
if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, share=True)
