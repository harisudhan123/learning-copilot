from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import os
from datetime import datetime
import requests
import random

app = Flask(__name__)
app.secret_key = "hackathon2025"

# ==== REPLACE WITH YOUR MONGODB ATLAS STRING ====
client = MongoClient("mongodb+srv://Harisudhank:harisudhan478@hari.croxrix.mongodb.net/")
db = client.learning_copilot
users = db.users

# Mock topics (you can expand)
TOPICS = ["Calculus", "Linear Algebra", "Thermodynamics", "Probability", "Differential Equations"]

# Simple mock AI generator (in real hackathon you can call Grok API / OpenAI)
def generate_30_day_plan(topic, knowledge_level, learning_style, pace):
    days = []
    difficulty = ["Easy", "Medium", "Hard"]
    
    for day in range(1, 31):
        diff_idx = min(day // 10, 2)
        days.append({
            "day": day,
            "title": f"Day {day}: Advanced {topic} Concepts",
            "content": [
                f"https://www.youtube.com/results?search_query={topic}+day+{day}",
                f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            ],
            "practice": f"{difficulty[diff_idx]} Practice Problems on {topic}",
            "explanation": "Detailed step-by-step solutions provided after submission",
            "revision": "Revise yesterday's concepts in 15 mins"
        })
    return days

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['topic'] = request.form['topic']
        session['knowledge'] = request.form['knowledge']
        session['style'] = request.form['style']
        session['pace'] = request.form['pace']
        return redirect(url_for('loading'))
    return render_template('quiz.html', topics=TOPICS)

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/generate_plan')
def generate_plan():
    plan = generate_30_day_plan(
        session['topic'],
        session['knowledge'],
        session['style'],
        session['pace']
    )
    
    user_data = {
        "name": session['name'],
        "topic": session['topic'],
        "knowledge_level": session['knowledge'],
        "learning_style": session['style'],
        "pace": session['pace'],
        "plan": plan,
        "created_at": datetime.now()
    }
    users.update_one(
        {"name": session['name'], "topic": session['topic']},
        {"$set": user_data},
        upsert=True
    )
    return render_template('plan.html', plan=plan, user=session)

if __name__ == '__main__':
    app.run(debug=True)