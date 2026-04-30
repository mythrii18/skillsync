import json
import re
import os

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset = os.path.join(current_dir, "cyclone_dataset.json")

with open(dataset, "r", encoding="utf-8") as f:
    DATA = json.load(f)


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Greeting patterns
greeting_triggers = [
    "hi", "hello", "hey", "good morning", "good afternoon",
    "good evening", "howdy", "what's up", "whats up", "sup",
    "namaste", "hii", "helo", "greetings"
]

# Question complexity keywords
simple_keywords = [
    "how many", "what is", "where is", "when", "which",
    "salary", "stipend", "location", "office", "deadline",
    "bond", "cgpa", "fresher", "experience", "apply",
    "contact", "email", "perks", "benefits", "laptop",
    "macbook", "remote", "hybrid", "vacancies", "openings"
]

medium_keywords = [
    "hiring process", "interview process", "role", "describe",
    "skills required", "what skills", "assessment", "test",
    "technical", "culture fit", "preparation", "tips",
    "team structure", "work mode", "eligibility"
]

big_keywords = [
    "tell me about", "about company", "about cyclone",
    "full job description", "complete hiring", "detailed",
    "eligibility criteria", "salary details", "benefits",
    "company values", "career growth", "why join",
    "internship program", "work life balance", "diversity"
]


def get_question_level(text):
    """
    Determine the response level based on question pattern:
    - small: 2-4 lines (simple factual questions)
    - medium: 4-7 lines (descriptive questions)
    - big: 7+ lines (detailed/comprehensive questions)
    """
    text_lower = text.lower()
    
    # Check for big/complex questions first
    for keyword in big_keywords:
        if keyword in text_lower:
            return "big"
    
    # Check for medium questions
    for keyword in medium_keywords:
        if keyword in text_lower:
            return "medium"
    
    # Check for simple questions
    for keyword in simple_keywords:
        if keyword in text_lower:
            return "small"
    
    # Default based on question length and complexity
    words = text.split()
    question_words = ["what", "how", "why", "where", "when", "tell", "describe", "explain"]
    has_question = any(w in question_words for w in words)
    
    if has_question:
        if len(words) > 8:
            return "medium"
        elif len(words) > 4:
            return "small"
    
    return "small"


def match_pattern(text, patterns):
    """Check if any pattern matches the user input"""
    text_lower = text.lower()
    for pattern in patterns:
        if pattern in text_lower:
            return True
    return False


def search_qa_dataset(text, level):
    """
    Search the Q&A dataset based on question pattern and return
    appropriate response based on level
    """
    qa_data = DATA.get("qa_dataset", {})
    
    # Search in the appropriate level dataset
    for size in ["small", "medium", "big"]:
        dataset = qa_data.get(size, [])
        for item in dataset:
            patterns = item.get("patterns", [])
            if match_pattern(text, patterns):
                response = item.get("response", "")
                
                # Adjust response based on requested level
                if level == "small":
                    # Return short version (first 2-3 lines)
                    lines = response.split("\n")
                    return "\n".join(lines[:2]) if len(lines) > 2 else response
                elif level == "medium":
                    # Return medium version (first 4-6 lines)
                    lines = response.split("\n")
                    return "\n".join(lines[:4]) if len(lines) > 4 else response
                else:  # big
                    # Return full response
                    return response
    
    return None


def fallback_response(text, level):
    """Fallback responses when no pattern matches"""
    text_lower = text.lower()
    
    # Salary/Stipend related
    if any(w in text_lower for w in ["salary", "pay", "ctc", "lpa", "package", "money", "compensation"]):
        if level == "small":
            return "Salary ranges from ₹4.5-13 LPA based on role. Internship: ₹15-20K/month."
        return f"Full-time: ₹4.5-13 LPA (varies by role). Internship: ₹15,000-20,000/month. Final offer depends on interview performance."

    # Location related
    if any(w in text_lower for w in ["location", "office", "address", "where", "city", "bangalore"]):
        if level == "small":
            return "Bangalore - Prestige Tech Park, Marathahalli"
        return f"Office: Cyclone HQ, 4th Floor, Prestige Tech Park, Marathahalli, Bangalore – 560037. Work Mode: Hybrid (Tue-Thu office, Mon-Fri remote)"

    # Work mode related
    if any(w in text_lower for w in ["work mode", "remote", "wfh", "hybrid", "work from home"]):
        if level == "small":
            return "Hybrid: Tue, Wed, Thu in-office. Mon & Fri remote."
        return "Hybrid model: Tuesday, Wednesday, Thursday in-office at Marathahalli. Monday & Friday remote. Core hours: 11am-4pm."

    # Deadline related
    if any(w in text_lower for w in ["deadline", "last date", "close", "when apply"]):
        if level == "small":
            return "Rolling basis - apply soon!"
        return f"Application Deadline: {DATA['application']['deadline']}. Apply at: {DATA['application']['apply_link']}"

    # Bond/Contract related
    if any(w in text_lower for w in ["bond", "service agreement", "lock in", "contract"]):
        return "No bond, no service agreement, no lock-in. We believe good work and good culture retain people — not contracts."

    # CGPA related
    if any(w in text_lower for w in ["cgpa", "percentage", "academic", "marks"]):
        if level == "small":
            return "No minimum CGPA - we care about skills, not scores."
        return "No minimum CGPA requirement. We care about skills, not scores. Active backlogs not preferred, but past cleared backlogs are fine."

    # Fresher related
    if any(w in text_lower for w in ["fresher", "fresh graduate", "new graduate", "no experience", "0 experience", "entry level"]):
        if level == "small":
            return "Yes! Freshers welcome for Junior App Developer role."
        return "Yes! Freshers with strong projects are welcome for Junior App Developer role (0-2 years). A degree alone won't get you in — but great portfolio will!"

    # Experience related
    if any(w in text_lower for w in ["experience required", "years needed", "eligibility"]):
        if level == "small":
            return "Experience varies: Junior App Dev 0-2 yrs, Data Analyst 1-3 yrs, others 1-5 yrs."
        return "Experience by role: Junior App Dev 0-2 yrs, Data Analyst 1-3 yrs, Frontend 1-3 yrs, Backend 1-4 yrs, DevOps 2-5 yrs, QA 1-3 yrs, UI/UX 1-3 yrs, PM 2-5 yrs."

    # Apply related
    if any(w in text_lower for w in ["apply", "how to apply", "application", "send resume"]):
        if level == "small":
            return "Apply at: https://cyclone.io/careers/apply"
        return f"Apply at: {DATA['application']['apply_link']}. Submit resume + link to at least one project (GitHub, Play Store, App Store, or portfolio)."

    # Contact related
    if any(w in text_lower for w in ["contact", "email", "reach", "whom to contact"]):
        if level == "small":
            return "Contact: careers@cyclone.io"
        return f"Contact: {DATA['application']['contact_email']}. For referrals, ask your referrer to email hr@cyclone.io."

    # Perks/Benefits related
    if any(w in text_lower for w in ["perks", "benefits", "allowances", "advantages"]):
        if level == "small":
            return "MacBook Pro, ₹10K learning budget, health insurance, flexible hours, ESOPs."
        return f"Perks: {', '.join(DATA['perks'])}"

    # Tech stack related
    if any(w in text_lower for w in ["tech stack", "technologies", "tools", "frameworks", "tech"]):
        if level == "small":
            return "Flutter, React, Node.js, Python, AWS, Docker, PostgreSQL"
        return "Mobile: Flutter, React Native. Web: React, TypeScript. Backend: Node.js, Python. Cloud: AWS, GCP. DevOps: Docker, Kubernetes."

    # Roles/Jobs related
    if any(w in text_lower for w in ["jobs", "roles", "positions", "openings", "vacancies", "hiring"]):
        if level == "small":
            return "8 open positions: Junior App Dev, Data Analyst, Frontend, Backend, DevOps, QA, UI/UX, PM"
        roles_list = [f"{r['title']} ({r.get('salary', 'Competitive')})" for r in DATA.get("roles", [])]
        return "Open Positions:\n" + "\n".join([f"• {r}" for r in roles_list])

    # Company about related
    if any(w in text_lower for w in ["about company", "what is cyclone", "company overview", "cyclone info"]):
        if level == "small":
            return "Cyclone - product-first app dev company, 120+ team, 85+ products, 4M users"
        return f"{DATA['company']['description']}"

    # Culture related
    if any(w in text_lower for w in ["culture", "values", "work environment", "environment"]):
        if level == "small":
            return "Ownership over blame, Ship fast iterate faster, Radical transparency"
        return f"Values: {', '.join(DATA['culture']['values'])}. Work Style: {DATA['culture']['work_style']}. Growth: {DATA['culture']['growth']}"

    # Default fallback
    if level == "small":
        return "For more details, contact careers@cyclone.io or visit https://cyclone.io/careers/apply"
    return f"For detailed information, please contact our HR team at {DATA['application']['contact_email']} or visit {DATA['application']['apply_link']}"


def generate_greeting_response():
    return """👋 Hello! I'm Cyclone's Hiring Assistant!

I can help you with:
• Job vacancies and roles
• Salary and stipend details
• Hiring process and interview prep
• Company culture and benefits
• How to apply

Just ask me anything! Example:
• "What jobs are available?"
• "What is the salary?"
• "How do I apply?"
• "Tell me about the company"

💼 We're hiring for 8 roles in Bangalore!
Apply now at: https://cyclone.io/careers/apply"""


def classify_intent(text):
    """Classify user intent"""
    words = text.split()
    
    # Check for greetings
    for t in greeting_triggers:
        if t in words:
            return "greeting"
    
    # Check for skill evaluation
    skill_indicators = ["i know", "i have", "my skills", "i can", "i work with", 
                       "i use", "proficient", "experience", "skills"]
    for indicator in skill_indicators:
        if indicator in text:
            return "resume"
    
    return "faq"


def chatbot_response(user_input):
    """
    Main chatbot function - Swiggy/Zomato style for job applicants
    """
    if not user_input.strip():
        return "Please ask a question! I can help with jobs, salary, hiring process, and more."

    text = preprocess_text(user_input)
    level = get_question_level(text)
    intent = classify_intent(text)

    # Handle greetings
    if intent == "greeting":
        return generate_greeting_response()

    # Handle FAQ questions
    if intent == "faq":
        # First try to match from Q&A dataset
        response = search_qa_dataset(text, level)
        
        if response:
            return response
        
        # Fallback to keyword-based responses
        return fallback_response(text, level)

    # Default response
    return fallback_response(text, level)


# CLI for testing
def clear():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    clear()
    print("""
╔══════════════════════════════════════════════════╗
   🌀  CYCLONE  |  Hiring Assistant
   Your Bridge to the Right Job!
╚══════════════════════════════════════════════════╝
   Type 'quit' to exit.
   Ask me about jobs, salary, process, and more!
══════════════════════════════════════════════════
""")

    while True:
        try:
            user_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Bot: Thanks for your interest in Cyclone. Good luck! 🚀\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye"):
            print("\n  Bot: Thanks for your interest in Cyclone. Good luck! 🚀\n")
            break

        response = chatbot_response(user_input)
        print(f"\n  Bot: {response}\n")