from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# ----------------------------------------------------------------------------
# MEMORY MANAGEMENT
# ----------------------------------------------------------------------------
# Store conversation history in memory as a list of dictionaries.
# Format: {"role": "user" or "assistant", "content": "message text"}
# Constraint: Keep only the last 20 messages.
conversation_history = []

# ----------------------------------------------------------------------------
# RESPONSE ENGINE (RULE-BASED AI)
# ----------------------------------------------------------------------------

def get_response(user_input):
    """
    Analyzes the user input and conversation history to generate a context-aware
    response using a large rule-based if-elif-else structure.
    """
    
    # Normalize input to lowercase for easier matching
    input_lower = user_input.lower().strip()
    
    # 1. Basic Greetings
    if any(word in input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        responses = [
            "Hello! I'm Aria. How can I assist you today?",
            "Hi there! Ready to code or chat?",
            "Hey! What's on your mind?"
        ]
        return random.choice(responses)

    elif any(word in input_lower for word in ['good morning', 'good evening', 'good afternoon']):
        period = "morning" if "morning" in input_lower else ("evening" if "evening" in input_lower else "afternoon")
        return f"Good {period}! I hope you're having a productive day."

    # 2. Identity
    elif any(word in input_lower for word in ['who are you', 'what is your name', 'your name']):
        return "I am Aria, your Personal AI Assistant built with Python and Flask. I'm here to help with code, career advice, and general knowledge."

    elif any(word in input_lower for word in ['who made you', 'who created you']):
        return "I was created by a Senior Full-Stack Engineer using pure Python logic and a custom frontend."

    # 3. Conversational Courtesies
    elif 'how are you' in input_lower:
        return "I'm functioning at 100% efficiency, thanks for asking! How are you doing?"
    
    elif 'thank you' in input_lower or 'thanks' in input_lower:
        return "You're welcome! If you have more questions, just ask."

    elif 'bye' in input_lower or 'goodbye' in input_lower:
        return "Goodbye! Have a wonderful day and happy coding!"

    # 4. Time and Date
    elif 'time' in input_lower:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    
    elif 'date' in input_lower:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."

    # 5. Programming & Tech Stack
    elif 'python' in input_lower:
        return "Python is an interpreted, high-level, general-purpose programming language. It's great for Web Dev (Flask/Django), Data Science, and AI."
    
    elif 'flask' in input_lower:
        return "Flask is a micro-framework for Python based on Werkzeug and Jinja2. It's lightweight and perfect for building REST APIs and small web apps."

    elif 'javascript' in input_lower or 'js' in input_lower:
        return "JavaScript is the language of the web. It enables interactive web pages and is an essential part of web applications."

    elif 'html' in input_lower or 'css' in input_lower:
        return "HTML provides the structure of a webpage, while CSS handles the styling and layout. Together with JS, they form the triad of the frontend."

    elif 'react' in input_lower:
        return "React is a JavaScript library for building user interfaces, maintained by Meta. It allows developers to create large web applications that can update and render efficiently."

    elif 'sql' in input_lower:
        return "SQL (Structured Query Language) is the standard language for managing and manipulating relational databases."

    elif 'git' in input_lower or 'github' in input_lower:
        return "Git is a distributed version control system. GitHub is a hosting service for Git repositories, essential for collaborative coding."

    # 6. Full Stack & CS Concepts
    elif 'frontend' in input_lower:
        return "Frontend development involves everything users see and interact with in their browser: HTML, CSS, and JavaScript."
    
    elif 'backend' in input_lower:
        return "Backend development refers to the server-side of an application. It handles database interactions, user authentication, and application logic."

    elif 'database' in input_lower:
        return "A database is an organized collection of structured information, or data, typically stored electronically in a computer system."

    elif 'algorithm' in input_lower:
        return "An algorithm is a finite sequence of well-defined instructions, typically used to solve a class of specific problems or to perform a computation."

    elif 'data structure' in input_lower:
        return "A data structure is a storage that is used to store and organize data. It is a way of arranging data on a computer so that it can be accessed and updated efficiently."

    # 7. AI & Data Science
    elif 'ai' in input_lower or 'artificial intelligence' in input_lower:
        return "Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems."

    elif 'machine learning' in input_lower:
        return "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed."

    elif 'deep learning' in input_lower:
        return "Deep Learning is a subset of machine learning that uses multi-layered neural networks to learn from vast amounts of data."

    elif 'llm' in input_lower or 'large language model' in input_lower:
        return "LLMs are deep learning algorithms that can recognize, summarize, translate, predict, and generate text and other content."

    # 8. Career & Education
    elif 'resume' in input_lower or 'cv' in input_lower:
        return "A good resume should be concise, highlight achievements over duties, and be tailored to the job description. Keep it to 1-2 pages."

    elif 'interview' in input_lower:
        return "For interviews, research the company, practice the STAR method (Situation, Task, Action, Result), and prepare thoughtful questions to ask the interviewer."

    elif 'roadmap' in input_lower:
        return "Roadmaps are great for tracking progress. Break down your big goal into small, achievable milestones."

    # 9. Lifestyle & Fun
    elif 'joke' in input_lower:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "I would tell you a UDP joke, but you might not get it."
        ]
        return random.choice(jokes)

    elif 'motivation' in input_lower or 'motivate' in input_lower:
        return "Code is like humor. When you have to explain it, it’s bad. Keep pushing forward!"

    elif 'weather' in input_lower:
        return "I don't have access to a live weather sensor, but I hope it's sunny wherever you are!"

    elif 'music' in input_lower:
        return "Music can boost productivity. Lo-Fi beats are popular among programmers for focus."

    # 10. Context Awareness (Simple implementation)
    # If user asks "and?" or "what about X?", refer to previous topic
    elif len(input_lower) < 10 and len(conversation_history) > 1:
        last_msg = conversation_history[-1]['content'].lower()
        if "python" in last_msg or "flask" in last_msg:
            return "Is there a specific Python framework or library you'd like to know more about?"
        elif "resume" in last_msg or "interview" in last_msg:
            return "Do you need help writing a specific section of your resume?"

    # 11. Fallback
    else:
        fallbacks = [
            "I'm not sure I understand. Could you rephrase that?",
            "That's an interesting topic. Tell me more.",
            "I can help with Python, Flask, career advice, and general tech questions. What do you need?",
            "I'm still learning! Try asking me about 'Python' or 'Resume tips'."
        ]
        return random.choice(fallbacks)

# ----------------------------------------------------------------------------
# ROUTES
# ----------------------------------------------------------------------------

@app.route('/')
def home():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages:
    1. Get JSON data.
    2. Update history (User).
    3. Generate AI response.
    4. Update history (Assistant).
    5. Trim history to last 20 messages.
    6. Return JSON response.
    """
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"response": "Please say something!"})

    # 1. Add User Message to History
    conversation_history.append({"role": "user", "content": user_message})

    # 2. Generate Response
    ai_response = get_response(user_message)

    # 3. Add AI Response to History
    conversation_history.append({"role": "assistant", "content": ai_response})

    # 4. Trim Memory (Keep only last 20 messages)
    # This ensures the list doesn't grow infinitely in server memory
    if len(conversation_history) > 20:
        # Remove the oldest message (index 0)
        conversation_history.pop(0)

    return jsonify({"response": ai_response})

# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    # Debug mode is True for development
    app.run(debug=True, port=5000) 
