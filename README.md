# 🤖 LinkedIn Post Generator — Multi-Agent AI Pipeline

An AI system that researches any topic on the live web and writes a polished, ready-to-publish LinkedIn post — using a team of three specialized AI agents working in sequence. Built with CrewAI and Google Gemini.

## ✨ What it does
Give it a topic, and three AI agents take over:
1. **🔍 Researcher** — searches the web for current, credible facts and statistics
2. **✍️ Writer** — drafts an engaging LinkedIn post grounded in that research
3. **🪄 Editor** — polishes the draft: sharpens the hook, cuts hype, tightens the flow

The finished post is saved as a dated draft for you to review and publish — **human-in-the-loop by design.**

## 🧠 How it works
Each agent has its own role, goal, and personality, passing its output to the next via CrewAI's task context.

## 🛠️ Tech stack
- **Python 3.12**
- **CrewAI** — multi-agent orchestration
- **Google Gemini** (`gemini-2.5-flash`) — the reasoning engine
- **Serper** — Google Search API for live research
- **python-dotenv** — secure key management

## 🚀 Setup
1. Clone the repo:
```bash
   git clone https://github.com/saeedengai/linkedin-post-generator.git
   cd linkedin-post-generator
```
2. Create and activate a virtual environment:
```bash
   python -m venv multi_agent_env
   multi_agent_env\Scripts\activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file in the project root:
(Free Gemini key: aistudio.google.com · Free Serper key: serper.dev)

## ▶️ Usage
```bash
python linkedin_post_generator.py
```
Answer the prompts for your topic and length. The post prints to the terminal and saves to the `posts/` folder.

## 💡 Why human-in-the-loop?
The pipeline does the heavy lifting — research, drafting, editing — but the final post is saved as a draft for **you** to review before publishing. You stay in control of what goes on your professional profile.

---
Built by **Saeed Hosseinzadeh**.