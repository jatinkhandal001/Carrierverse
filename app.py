import gradio as gr
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

# Get the Gemini API key from environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment. Please set it in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_file(file_obj):
    import os
    ext = os.path.splitext(file_obj.name)[-1].lower()
    if ext == ".pdf":
        import fitz  # PyMuPDF
        with fitz.open(file_obj.name) as doc:
            return "\n".join(page.get_text() for page in doc)
    elif ext in [".docx"]:
        import docx
        doc = docx.Document(file_obj.name)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext in [".txt"]:
        with open(file_obj.name, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Unsupported file type. Please upload a PDF, DOCX, or TXT file."

# 1
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

# 2
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

# 3
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

# 4
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

# 5
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

# 6
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

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
.gradio-container {
    background: linear-gradient(135deg, #0a2342 0%, #19376d 100%);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    color: #e3eafc;
    transition: background 0.6s;
}
#header {
    animation: logoPop 1s cubic-bezier(.68,-0.55,.27,1.55);
}
@keyframes logoPop {
    0% { transform: scale(0.7) rotate(-10deg); opacity: 0; }
    80% { transform: scale(1.05) rotate(2deg); opacity: 1; }
    100% { transform: scale(1) rotate(0deg); }
}
.gr-button-primary {
    background: linear-gradient(90deg, #2563eb 0%, #19376d 100%);
    border: none;
    border-radius: 12px;
    font-weight: 700;
    color: #e3eafc;
    box-shadow: 0 2px 16px rgba(25,55,109,0.18);
    transition: transform 0.13s, box-shadow 0.13s, background 0.25s;
    padding: 0.8em 2.2em;
    font-size: 1.07em;
    letter-spacing: 0.01em;
}
.gr-button-primary:hover, .gr-button-primary:focus {
    background: linear-gradient(90deg, #19376d 0%, #2563eb 100%);
    transform: scale(1.05);
    box-shadow: 0 4px 22px rgba(25,55,109,0.28);
}
.gr-panel, .gr-box, .gr-block, .gr-group {
    border-radius: 16px !important;
    background: rgba(25, 55, 109, 0.92) !important;
    border: 1px solid #233a5e !important;
    box-shadow: 0 4px 24px rgba(10,35,66,0.18);
    color: #e3eafc;
    animation: fadeInPanel 0.8s;
}
@keyframes fadeInPanel {
    from { opacity: 0; transform: translateY(24px);}
    to { opacity: 1; transform: none;}
}
.gr-tab {
    font-weight: 700;
    color: #e3eafc !important;
    background: transparent !important;
    transition: background 0.2s, color 0.2s;
    border-radius: 10px 10px 0 0 !important;
    margin-right: 2px;
    padding: 0.7em 1.4em !important;
}
.gr-tab:hover, .gr-tab[aria-selected="true"] {
    background: linear-gradient(90deg, #2563eb44 0%, #19376d44 100%) !important;
    color: #fff !important;
}
.gr-input, .gr-textbox, textarea, input {
    border-radius: 8px !important;
    border: 1.5px solid #233a5e !important;
    background: #13294b !important;
    color: #e3eafc !important;
    padding: 0.7em 1em !important;
    font-size: 1.04em !important;
    transition: border 0.2s;
}
.gr-input:focus, .gr-textbox:focus, textarea:focus, input:focus {
    border: 1.5px solid #2563eb !important;
    box-shadow: 0 0 0 2px #2563eb44;
}
.gr-markdown {
    font-size: 1.06em;
    line-height: 1.7;
    color: #e3eafc;
    animation: fadeInPanel 0.7s;
    background: transparent !important;
}
::-webkit-scrollbar {
    width: 8px;
    background: #233a5e;
}
::-webkit-scrollbar-thumb {
    background: #2563eb;
    border-radius: 8px;
}
"""

with gr.Blocks(
    title="CareerVerse AI (Gemini-powered)",
    css=custom_css
) as app:
    gr.Markdown(
        """
        <div style="display: flex; align-items: center; gap: 16px;" id="header">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="44"/>
            <h1 style="margin: 0; font-weight: 800; font-size: 2.1rem; letter-spacing: -1px; color: #e3eafc;">CareerVerse AI</h1>
        </div>
        <p style="font-size: 1.08rem; color: #e3eafc;">
            <b>Unlock your career potential with Gemini-powered personalized AI guidance!</b>
        </p>
        """
    )

    with gr.Tabs():
        with gr.Tab("🎯 Career Recommendations"):
            s = gr.Textbox(label="Your Skills (comma-separated)")
            i = gr.Textbox(label="Your Interests (comma-separated)")
            o = gr.Markdown()
            btn = gr.Button("Get Career Recommendations", elem_classes="gr-button-primary")
            btn.click(get_career_recommendations, [s, i], o)

        with gr.Tab("📄 Resume Analyzer"):
            resume_file = gr.File(label="Upload Your Resume (PDF, DOCX, or TXT)", file_types=[".pdf", ".docx", ".txt"])
            resume_output = gr.Markdown()
            analyze_btn = gr.Button("Analyze Resume", elem_classes="gr-button-primary")
            analyze_btn.click(analyze_resume_file, resume_file, resume_output)

        with gr.Tab("🤖 AI Career Mentor"):
            c = gr.Chatbot(label="Chat with Mentor", height=320, type="messages")
            ci = gr.Textbox(label="Your Question")
            cbtn = gr.Button("Send", elem_classes="gr-button-primary")
            cbtn.click(chat_with_ai, [ci, c], [ci, c])
            ci.submit(chat_with_ai, [ci, c], [ci, c])

        with gr.Tab("🛠️ Skill Gap Analysis"):
            user_skills = gr.Textbox(label="Your Current Skills (comma-separated)")
            target_job = gr.Textbox(label="Target Job Title or Description")
            gap_output = gr.Markdown()
            gap_btn = gr.Button("Analyze Skill Gap", elem_classes="gr-button-primary")
            gap_btn.click(skill_gap_analysis, [user_skills, target_job], gap_output)

        with gr.Tab("💬 Career Q&A Forum"):
            forum_history = gr.State([])
            q_input = gr.Textbox(label="Ask a Career Question")
            q_output = gr.Markdown()
            ask_btn = gr.Button("Ask", elem_classes="gr-button-primary")

            def handle_forum_question(user_question, qa_history):
                answer = career_qa_forum(user_question, qa_history)
                qa_history = qa_history + [[user_question, answer]]
                forum_md = ""
                for q, a in qa_history[-5:]:
                    forum_md += f"**Q:** {q}\n\n**A:** {a}\n\n---\n"
                return "", qa_history, forum_md

            ask_btn.click(handle_forum_question, [q_input, forum_history], [q_input, forum_history, q_output])
# For Jupyter, just call app.launch(share=True)
app.launch(share=True)
