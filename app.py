# careerverse_app.py
import gradio as gr
import google.generativeai as genai
import os
import threading
import time
import functools

# Only needed for local development with .env
if os.environ.get("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

# Get Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment. Please set it in Render or .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Periodic Call Decorator ------------------
def periodic_call(interval_sec=720):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            if not hasattr(wrapper, "_thread_started"):
                def loop():
                    while True:
                        try:
                            print(f"⏰ Running scheduled function: {func.__name__}")
                            func()
                        except Exception as e:
                            print(f"❌ Error in scheduled function {func.__name__}: {e}")
                        time.sleep(interval_sec)
                threading.Thread(target=loop, daemon=True).start()
                wrapper._thread_started = True
            func()  # Run once immediately
        return wrapper
    return decorator

# ------------------ Core Functions ------------------
def extract_text_from_file(file_obj):
    import os
    ext = os.path.splitext(file_obj.name)[-1].lower()
    if ext == ".pdf":
        import fitz
        with fitz.open(file_obj.name) as doc:
            return "\n".join(page.get_text() for page in doc)
    elif ext == ".docx":
        import docx
        doc = docx.Document(file_obj.name)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(file_obj.name, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Unsupported file type. Please upload a PDF, DOCX, or TXT file."

def get_career_recommendations(skills, interests):
    if not skills or not interests:
        return "Please enter both skills and interests."
    prompt = (
        f"You are a career advisor. The user has these skills: {skills}.\n"
        f"Their interests are: {interests}.\n"
        "Suggest the top 3 career paths with:\n"
        "- Career name\n"
        "- Why it's a good fit\n"
        "- Estimated salary range (USD)\n"
        "- 5-step roadmap\n"
        "- Best learning platforms\n"
        "Format in clean Markdown."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def analyze_resume_file(file_obj):
    if file_obj is None:
        return "Please upload your resume file."
    text = extract_text_from_file(file_obj)
    if text.startswith("Unsupported"):
        return text
    prompt = (
        "You are an expert resume reviewer. Analyze the following resume text for:\n"
        "- Overall score (out of 100)\n"
        "- ATS compatibility (out of 100)\n"
        "- Keyword match (out of 100)\n"
        "- Format (out of 100)\n"
        "- 3 improvement suggestions\n"
        "Resume:\n"
        f"{text}\n"
        "Respond in Markdown."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def chat_with_ai(message, history):
    chat_history = ""
    for m in history:
        if m["role"] == "user":
            chat_history += f"User: {m['content']}\n"
        elif m["role"] == "assistant":
            chat_history += f"Assistant: {m['content']}\n"
    prompt = (
        "You are a helpful AI career mentor. Use the chat history and respond helpfully.\n"
        f"{chat_history}User: {message}\nAssistant:"
    )
    try:
        response = model.generate_content(prompt)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response.text})
        return "", history
    except Exception as e:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"Error: {e}"})
        return "", history

def take_personality_quiz():
    prompt = (
        "Generate a 5-question multiple-choice career personality quiz. "
        "Each question should have 4 options. Format as Markdown."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def skill_gap_analysis(user_skills, target_role):
    if not user_skills or not target_role:
        return "Please enter both your skills and a target job."
    prompt = (
        f"You are a career advisor. The user has these skills: {user_skills}.\n"
        f"Their target job is: {target_role}.\n"
        "1. List the key skills required for this job.\n"
        "2. Identify which required skills the user is missing.\n"
        "3. Suggest resources or courses to learn those missing skills.\n"
        "Format the answer in Markdown with clear sections."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def career_qa_forum(user_question, qa_history=[]):
    history_text = ""
    for q, a in qa_history:
        history_text += f"Q: {q}\nA: {a}\n"
    prompt = (
        "You are a helpful career advisor. Answer the user's question clearly and with practical advice.\n"
        f"{history_text}Q: {user_question}\nA:"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ------------------ Scheduled Calls ------------------
@periodic_call()
def scheduled_recommendations():
    get_career_recommendations("python, ml", "data science, ai")

@periodic_call()
def scheduled_chat():
    chat_with_ai("How can I grow in my AI career?", [])

@periodic_call()
def scheduled_quiz():
    take_personality_quiz()

@periodic_call()
def scheduled_gap_analysis():
    skill_gap_analysis("python, communication", "AI Product Manager")

@periodic_call()
def scheduled_qa():
    career_qa_forum("What soft skills matter most in tech careers?", [])

custom_css = """
body, .gradio-container {
    background-color: #87ceeb !important;  /* skyblue background */
    color: #000000 !important;             /* black text for full visibility */
}

.gradio-markdown {
    color: #000000 !important;             /* markdown text black */
}

.gr-button {
    background-color: #1e90ff !important; /* dodger blue buttons */
    color: white !important;
    border: none !important;
}

.gr-input, .gr-textbox textarea {
    background-color: #e0f0ff !important;  /* very light blue inputs */
    color: #000000 !important;
    border: 1px solid #1e90ff !important;
}

.gr-chatbot-message {
    color: #000000 !important;
}

"""

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="blue",
        neutral_hue="sky"  # keep neutral light so CSS bg works nicely
    ),
    css=custom_css,
    title="CareerVerse AI (Gemini-powered)"
) as app:
    gr.Markdown("""<HEADER_HTML_HERE>""")  # Replace with your original HTML header

    with gr.Tabs():
        with gr.Tab("🌟 Career Recommendations"):
            s = gr.Textbox(label="Your Skills (comma-separated)")
            i = gr.Textbox(label="Your Interests (comma-separated)")
            o = gr.Markdown()
            btn = gr.Button("Get Career Recommendations")
            btn.click(get_career_recommendations, [s, i], o)

        with gr.Tab("📄 Resume Analyzer"):
            resume_file = gr.File(label="Upload Resume", file_types=[".pdf", ".docx", ".txt"])
            resume_output = gr.Markdown()
            analyze_btn = gr.Button("Analyze Resume")
            analyze_btn.click(analyze_resume_file, resume_file, resume_output)

        with gr.Tab("🤖 AI Career Mentor"):
            c = gr.Chatbot(label="Chat with Mentor", height=320, type="messages")
            ci = gr.Textbox(label="Your Question")
            cbtn = gr.Button("Send")
            cbtn.click(chat_with_ai, [ci, c], [ci, c])
            ci.submit(chat_with_ai, [ci, c], [ci, c])

        with gr.Tab("🛠️ Skill Gap Analysis"):
            user_skills = gr.Textbox(label="Your Current Skills")
            target_job = gr.Textbox(label="Target Job")
            gap_output = gr.Markdown()
            gap_btn = gr.Button("Analyze Skill Gap")
            gap_btn.click(skill_gap_analysis, [user_skills, target_job], gap_output)

        with gr.Tab("💬 Career Q&A Forum"):
            forum_history = gr.State([])
            q_input = gr.Textbox(label="Ask a Career Question")
            q_output = gr.Markdown()
            ask_btn = gr.Button("Ask")

            def handle_forum_question(user_question, qa_history):
                answer = career_qa_forum(user_question, qa_history)
                qa_history = qa_history + [[user_question, answer]]
                forum_md = ""
                for q, a in qa_history[-5:]:
                    forum_md += f"**Q:** {q}\n\n**A:** {a}\n\n---\n"
                return "", qa_history, forum_md

            ask_btn.click(handle_forum_question, [q_input, forum_history], [q_input, forum_history, q_output])


# Trigger the decorators once
scheduled_recommendations()
scheduled_chat()
scheduled_quiz()
scheduled_gap_analysis()
scheduled_qa()

app.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
