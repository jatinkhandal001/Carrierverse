import gradio as gr
import random
import json
import time
from typing import List, Dict, Tuple
import pandas as pd

class CareerVerseAI:
    def __init__(self):
        # Sample data for career recommendations
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
            "Data Scientist": {
                "salary": "$80,000 - $130,000", 
                "description": "Analyze complex data to drive business decisions",
                "required_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas"],
                "roadmap": [
                    "Learn Python and data libraries",
                    "Master SQL and database design",
                    "Study machine learning algorithms", 
                    "Build portfolio projects"
                ],
                "match_keywords": ["python", "data", "analytics", "machine learning", "statistics"]
            },
            "DevOps Engineer": {
                "salary": "$85,000 - $140,000",
                "description": "Streamline development and deployment processes", 
                "required_skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux"],
                "roadmap": [
                    "Learn cloud platforms (AWS/Azure)",
                    "Master containerization with Docker",
                    "Implement CI/CD pipelines",
                    "Study infrastructure as code"
                ],
                "match_keywords": ["aws", "docker", "devops", "cloud", "kubernetes"]
            },
            "UI/UX Designer": {
                "salary": "$60,000 - $100,000",
                "description": "Design intuitive and beautiful user experiences",
                "required_skills": ["Figma", "Adobe Creative Suite", "User Research", "Prototyping"],
                "roadmap": [
                    "Learn design principles and theory",
                    "Master design tools like Figma",
                    "Study user research methods",
                    "Build a strong design portfolio"
                ],
                "match_keywords": ["design", "ui", "ux", "figma", "creative", "user experience"]
            },
            "Cybersecurity Analyst": {
                "salary": "$70,000 - $120,000",
                "description": "Protect organizations from cyber threats and vulnerabilities",
                "required_skills": ["Network Security", "Ethical Hacking", "Risk Assessment", "Compliance"],
                "roadmap": [
                    "Learn networking fundamentals",
                    "Study cybersecurity frameworks",
                    "Get security certifications",
                    "Practice ethical hacking"
                ],
                "match_keywords": ["security", "cybersecurity", "hacking", "network", "compliance"]
            },
            "Mobile App Developer": {
                "salary": "$70,000 - $115,000",
                "description": "Create mobile applications for iOS and Android platforms",
                "required_skills": ["Swift", "Kotlin", "React Native", "Flutter", "Mobile UI"],
                "roadmap": [
                    "Choose a platform (iOS/Android)",
                    "Learn platform-specific languages",
                    "Study mobile UI/UX principles",
                    "Publish apps to app stores"
                ],
                "match_keywords": ["mobile", "ios", "android", "swift", "kotlin", "react native"]
            }
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
            {
                "question": "How do you prefer to solve problems?",
                "options": [
                    "Through creative brainstorming",
                    "Using data and analytics",
                    "Following established procedures", 
                    "Experimenting with new approaches"
                ]
            },
            {
                "question": "What motivates you most in your career?",
                "options": [
                    "Making a positive impact on society",
                    "Financial success and stability",
                    "Learning and personal growth",
                    "Recognition and leadership opportunities"
                ]
            },
            {
                "question": "Which work style suits you best?",
                "options": [
                    "Detailed planning and organization",
                    "Flexible and adaptable approach",
                    "Results-driven and goal-oriented",
                    "Creative and innovative thinking"
                ]
            },
            {
                "question": "What type of challenges excite you?",
                "options": [
                    "Technical and analytical problems",
                    "Creative and design challenges", 
                    "People and communication issues",
                    "Strategic and business problems"
                ]
            }
        ]

    def analyze_skills_and_interests(self, skills: List[str], interests: List[str]) -> List[Dict]:
        """Analyze user skills and interests to recommend careers"""
        recommendations = []
        
        for career, details in self.career_database.items():
            match_score = 0
            
            # Calculate skill match
            skill_matches = len(set([s.lower() for s in skills]) & 
                               set([s.lower() for s in details["required_skills"]]))
            skill_score = (skill_matches / len(details["required_skills"])) * 60
            
            # Calculate interest match  
            interest_matches = sum(1 for interest in interests 
                                 if any(keyword in interest.lower() 
                                       for keyword in details["match_keywords"]))
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
        
        # Sort by match score and return top 3
        recommendations.sort(key=lambda x: x["match"], reverse=True)
        return recommendations[:3]

    def analyze_resume(self, resume_text: str) -> Dict:
        """Analyze resume and provide scoring"""
        if not resume_text:
            return {"error": "Please provide resume text"}
        
        # Simple resume analysis
        word_count = len(resume_text.split())
        
        # Check for key sections
        sections = ["experience", "education", "skills", "projects"]
        section_score = sum(20 for section in sections if section in resume_text.lower())
        
        # Check for quantifiable achievements
        numbers = len([word for word in resume_text.split() if any(char.isdigit() for char in word)])
        achievement_score = min(25, numbers * 2)
        
        # Calculate scores
        overall_score = min(95, max(60, section_score + achievement_score + random.randint(10, 20)))
        ats_score = min(95, max(70, overall_score + random.randint(-10, 10)))
        keyword_score = min(90, max(60, len(set(resume_text.lower().split()) & 
                                        set([skill.lower() for skill in self.skills_database])) * 3))
        format_score = random.randint(85, 95)
        
        suggestions = [
            "Add more quantifiable achievements with specific numbers and percentages",
            "Include relevant keywords for your target role and industry", 
            "Optimize section headings for ATS systems (Experience, Education, Skills)",
            "Add a professional summary section at the top",
            "Use action verbs to start bullet points (Developed, Managed, Implemented)",
            "Keep formatting consistent throughout the document"
        ]
        
        return {
            "overall": overall_score,
            "ats": ats_score, 
            "keywords": keyword_score,
            "format": format_score,
            "suggestions": random.sample(suggestions, 4)
        }

    def get_ai_career_advice(self, question: str) -> str:
        """Provide AI career advice based on question"""
        question_lower = question.lower()
        
        advice_responses = {
            "interview": [
                "For interview preparation, practice the STAR method (Situation, Task, Action, Result) for behavioral questions. Research the company thoroughly and prepare specific examples that demonstrate your skills.",
                "Practice coding challenges on platforms like LeetCode, HackerRank, or Codewars. Focus on understanding the problem-solving process rather than memorizing solutions.",
                "Prepare thoughtful questions to ask the interviewer about the role, team culture, and growth opportunities. This shows genuine interest and engagement."
            ],
            "skill": [
                "Focus on learning one technology deeply rather than many superficially. Depth shows expertise to employers and builds confidence.",
                "Build projects that showcase your skills. A strong portfolio with 3-5 well-documented projects is more valuable than certificates alone.",
                "Consider getting certified in cloud platforms like AWS, Azure, or Google Cloud - they're highly valued in today's job market."
            ],
            "salary": [
                "Research salary ranges for your role and location using sites like Glassdoor, PayScale, and levels.fyi. Know your market value before negotiating.",
                "When negotiating, focus on your value proposition. Highlight specific achievements and how you've contributed to previous employers' success.",
                "Consider the total compensation package, not just base salary. Benefits, stock options, and professional development opportunities add significant value."
            ],
            "career": [
                "Networking is crucial for career growth. Join professional communities, attend meetups, and connect with people in your field on LinkedIn.",
                "Set clear career goals and create a roadmap. Break down long-term objectives into smaller, actionable steps you can take each month.",
                "Seek mentorship from experienced professionals in your field. Their guidance can help you avoid common pitfalls and accelerate your growth."
            ],
            "change": [
                "Career transitions take time and planning. Start by identifying transferable skills from your current role that apply to your target field.",
                "Consider taking on side projects or freelance work in your desired field to build experience and test your interest.",
                "Network with professionals in your target industry to learn about the field and discover opportunities."
            ]
        }
        
        # Find matching advice category
        for category, responses in advice_responses.items():
            if category in question_lower:
                return random.choice(responses)
        
        # Default responses for general questions
        general_responses = [
            "That's a great question! Focus on continuous learning and building a strong professional network. These two factors are crucial for long-term career success.",
            "Consider your long-term goals and work backwards to create a plan. Break down big objectives into smaller, manageable steps you can take consistently.",
            "Remember that career growth is a marathon, not a sprint. Stay patient, persistent, and always be open to learning new things.",
            "Building strong relationships and maintaining a positive reputation in your industry will open doors to opportunities you might not even know exist.",
            "Don't be afraid to take calculated risks in your career. Sometimes the biggest growth comes from stepping outside your comfort zone."
        ]
        
        return random.choice(general_responses)

# Initialize the AI system
career_ai = CareerVerseAI()

# Gradio Interface Functions
def get_career_recommendations(skills_input: str, interests_input: str) -> str:
    """Get career recommendations based on skills and interests"""
    if not skills_input.strip() or not interests_input.strip():
        return "Please enter both your skills and interests to get personalized recommendations."
    
    skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
    interests = [interest.strip() for interest in interests_input.split(',') if interest.strip()]
    
    recommendations = career_ai.analyze_skills_and_interests(skills, interests)
    
    result = "🚀 **Your Personalized Career Recommendations** 🚀\n\n"
    
    for i, rec in enumerate(recommendations, 1):
        result += f"## {i}. {rec['title']} ({rec['match']}% Match)\n"
        result += f"💰 **Salary Range:** {rec['salary']}\n"
        result += f"📝 **Description:** {rec['description']}\n\n"
        result += f"🛠️ **Required Skills:**\n"
        for skill in rec['skills']:
            result += f"• {skill}\n"
        result += f"\n📚 **Learning Roadmap:**\n"
        for step in rec['roadmap']:
            result += f"• {step}\n"
        result += "\n" + "="*50 + "\n\n"
    
    return result

def analyze_resume_text(resume_text: str) -> str:
    """Analyze resume and provide feedback"""
    if not resume_text.strip():
        return "Please paste your resume text for analysis."
    
    analysis = career_ai.analyze_resume(resume_text)
    
    if "error" in analysis:
        return analysis["error"]
    
    result = "📊 **Resume Analysis Results** 📊\n\n"
    result += f"🎯 **Overall Score:** {analysis['overall']}/100\n"
    result += f"🤖 **ATS Compatibility:** {analysis['ats']}/100\n" 
    result += f"🔑 **Keyword Optimization:** {analysis['keywords']}/100\n"
    result += f"📄 **Format Quality:** {analysis['format']}/100\n\n"
    
    result += "💡 **Improvement Suggestions:**\n"
    for suggestion in analysis['suggestions']:
        result += f"• {suggestion}\n"
    
    return result

def chat_with_ai(message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
    """Chat with AI career mentor"""
    if not message.strip():
        return "", history
    
    response = career_ai.get_ai_career_advice(message)
    history.append([message, response])
    
    return "", history

def take_personality_quiz() -> str:
    """Display personality quiz questions"""
    result = "🧠 **Career Personality Assessment** 🧠\n\n"
    result += "Answer these questions to discover careers that match your personality:\n\n"
    
    for i, q in enumerate(career_ai.personality_questions, 1):
        result += f"**Question {i}:** {q['question']}\n"
        for j, option in enumerate(q['options'], 1):
            result += f"{j}. {option}\n"
        result += "\n"
    
    result += "💡 **Instructions:** Think about each question carefully and note your preferred answers. "
    result += "This will help you understand what type of work environment and career path suits you best!\n\n"
    result += "🎯 **Career Matching Tips:**\n"
    result += "• If you prefer collaborative environments → Consider team-based roles\n"
    result += "• If you like data and analytics → Explore data science or business analysis\n"
    result += "• If you enjoy creative problem-solving → Look into design or product roles\n"
    result += "• If you want to make an impact → Consider non-profit or social impact careers\n"
    
    return result

def get_skill_recommendations(current_role: str, target_role: str) -> str:
    """Get skill gap analysis and recommendations"""
    if not current_role.strip() or not target_role.strip():
        return "Please enter both your current role and target role for skill analysis."
    
    result = f"🎯 **Skill Gap Analysis: {current_role} → {target_role}** 🎯\n\n"
    
    # Sample skill recommendations based on common career transitions
    skill_maps = {
        "data scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Pandas", "TensorFlow"],
        "web developer": ["JavaScript", "React", "Node.js", "HTML/CSS", "Git", "MongoDB"],
        "devops engineer": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Terraform"],
        "ui/ux designer": ["Figma", "Adobe Creative Suite", "User Research", "Prototyping", "Wireframing"],
        "cybersecurity": ["Network Security", "Ethical Hacking", "Risk Assessment", "Compliance", "Penetration Testing"],
        "mobile developer": ["Swift", "Kotlin", "React Native", "Flutter", "Mobile UI", "App Store Optimization"]
    }
    
    target_skills = []
    for role, skills in skill_maps.items():
        if role in target_role.lower():
            target_skills = skills
            break
    
    if not target_skills:
        target_skills = ["Communication", "Problem Solving", "Project Management", "Leadership", "Technical Writing"]
    
    result += f"🛠️ **Key Skills Needed for {target_role}:**\n"
    for skill in target_skills:
        result += f"• {skill}\n"
    
    result += f"\n📚 **Learning Resources:**\n"
    result += "• **Online Courses:** Coursera, Udemy, edX, Pluralsight\n"
    result += "• **Practice Platforms:** GitHub, Kaggle, LeetCode, HackerRank\n"
    result += "• **Documentation:** Official docs, MDN, Stack Overflow\n"
    result += "• **Communities:** Reddit, Discord, LinkedIn groups\n"
    
    result += f"\n⏱️ **Estimated Timeline:** 3-6 months of consistent learning\n"
    result += f"🎯 **Next Steps:**\n"
    result += "1. Choose 2-3 priority skills to focus on first\n"
    result += "2. Set up a daily learning schedule (1-2 hours)\n"
    result += "3. Build projects to practice new skills\n"
    result += "4. Join communities and network with professionals\n"
    result += "5. Update your resume and LinkedIn profile\n"
    
    return result

# Create Gradio Interface
def create_interface():
    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="pink",
            neutral_hue="slate"
        ),
        title="CareerVerse - AI Career Advisor",
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
        
        gr.Markdown("""
        # 🚀 CareerVerse - AI-Powered Career Advisor
        
        ### Discover your dream career with personalized AI recommendations!
        
        Welcome to CareerVerse, your intelligent career companion. Get personalized career recommendations, 
        resume analysis, skill gap insights, and chat with our AI career mentor.
        """)
        
        with gr.Tabs():
            # Career Recommendations Tab
            with gr.Tab("🎯 Career Recommendations"):
                gr.Markdown("### Get Personalized Career Matches")
                gr.Markdown("Enter your skills and interests to discover careers that match your profile!")
                
                with gr.Row():
                    with gr.Column():
                        skills_input = gr.Textbox(
                            label="Your Skills (comma-separated)",
                            placeholder="e.g., Python, JavaScript, SQL, Project Management, Communication",
                            lines=3
                        )
                        interests_input = gr.Textbox(
                            label="Your Interests (comma-separated)", 
                            placeholder="e.g., Web Development, Data Analysis, Machine Learning, Design",
                            lines=3
                        )
                        recommend_btn = gr.Button("Get Career Recommendations 🚀", variant="primary")
                    
                    with gr.Column():
                        recommendations_output = gr.Markdown(label="Your Career Recommendations")
                
                recommend_btn.click(
                    get_career_recommendations,
                    inputs=[skills_input, interests_input],
                    outputs=recommendations_output
                )
            
            # Resume Analysis Tab  
            with gr.Tab("📄 Resume Analyzer"):
                gr.Markdown("### AI-Powered Resume Analysis")
                gr.Markdown("Paste your resume text below to get instant feedback and improvement suggestions!")
                
                with gr.Row():
                    with gr.Column():
                        resume_input = gr.Textbox(
                            label="Paste Your Resume Text Here",
                            placeholder="Copy and paste your resume content here...",
                            lines=10
                        )
                        analyze_btn = gr.Button("Analyze Resume 📊", variant="primary")
                    
                    with gr.Column():
                        resume_output = gr.Markdown(label="Resume Analysis Results")
                
                analyze_btn.click(
                    analyze_resume_text,
                    inputs=resume_input,
                    outputs=resume_output
                )
            
            # AI Career Mentor Chat Tab
            with gr.Tab("🤖 AI Career Mentor"):
                gr.Markdown("### Chat with Your AI Career Coach")
                gr.Markdown("Ask questions about career advice, interview preparation, skill development, and more!")
                
                chatbot = gr.Chatbot(
                    label="Career Mentor Chat",
                    height=400,
                    placeholder="Hi! I'm your AI Career Mentor. Ask me anything about your career journey!"
                )
                
                with gr.Row():
                    chat_input = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask about interviews, skills, career changes, salary negotiation...",
                        scale=4
                    )
                    chat_btn = gr.Button("Send 💬", variant="primary", scale=1)
                
                # Sample questions for quick start
                gr.Markdown("**Quick Start Questions:**")
                with gr.Row():
                    gr.Button("How to prepare for interviews?").click(
                        lambda: ("How to prepare for interviews?", []), 
                        outputs=[chat_input, chatbot]
                    )
                    gr.Button("What skills should I learn?").click(
                        lambda: ("What skills should I learn next?", []),
                        outputs=[chat_input, chatbot]
                    )
                    gr.Button("Career change advice?").click(
                        lambda: ("I want to change careers, any advice?", []),
                        outputs=[chat_input, chatbot]
                    )
                
                chat_btn.click(
                    chat_with_ai,
                    inputs=[chat_input, chatbot],
                    outputs=[chat_input, chatbot]
                )
                
                chat_input.submit(
                    chat_with_ai,
                    inputs=[chat_input, chatbot], 
                    outputs=[chat_input, chatbot]
                )
            
            # Skill Gap Analysis Tab
            with gr.Tab("🛠️ Skill Gap Analysis"):
                gr.Markdown("### Identify Skills You Need to Learn")
                gr.Markdown("Compare your current role with your target role to identify skill gaps!")
                
                with gr.Row():
                    with gr.Column():
                        current_role = gr.Textbox(
                            label="Current Role",
                            placeholder="e.g., Marketing Coordinator, Student, Sales Representative"
                        )
                        target_role = gr.Textbox(
                            label="Target Role", 
                            placeholder="e.g., Data Scientist, Web Developer, Product Manager"
                        )
                        skill_btn = gr.Button("Analyze Skill Gap 🎯", variant="primary")
                    
                    with gr.Column():
                        skill_output = gr.Markdown(label="Skill Gap Analysis")
                
                skill_btn.click(
                    get_skill_recommendations,
                    inputs=[current_role, target_role],
                    outputs=skill_output
                )
            
            # Personality Quiz Tab
            with gr.Tab("🧠 Personality Quiz"):
                gr.Markdown("### Career Personality Assessment")
                gr.Markdown("Discover what type of careers match your personality and work style!")
                
                quiz_btn = gr.Button("Take Personality Quiz 🧠", variant="primary")
                quiz_output = gr.Markdown(label="Personality Quiz")
                
                quiz_btn.click(
                    take_personality_quiz,
                    outputs=quiz_output
                )
        
        # Footer
        gr.Markdown("""
        ---
        ### 🌟 About CareerVerse
        
        CareerVerse is your AI-powered career companion, designed to help you:
        - **Discover** careers that match your skills and interests
        - **Analyze** your resume for ATS optimization  
        - **Learn** what skills you need for your dream job
        - **Chat** with an AI mentor for personalized advice
        - **Assess** your personality for career matching
        
        **Built with ❤️ using Python and Gradio**
        
        *Start your career transformation journey today!*
        """)
    
    return app

# Launch the application
if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True,
        debug=True
    )