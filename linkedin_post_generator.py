"""LinkedIn Post Generator — a multi-agent pipeline (Researcher -> Writer -> Editor)."""

import os

# Keep CrewAI's helper storage
os.environ.setdefault(
    "CREWAI_STORAGE_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".crewai_storage"),
)

from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

load_dotenv()


def build_crew():
    gemini = LLM(model="gemini/gemini-2.5-flash")
    search_tool = SerperDevTool()

    researcher = Agent(
        role="Research Analyst",
        goal="Find current, factual, relevant information about the given topic",
        backstory="You are a meticulous researcher. You never invent facts — you search the web and report real findings. Use at most 2–3 targeted searches; don't over-search.",
        tools=[search_tool],
        llm=gemini,
        verbose=True,
    )

    writer = Agent(
        role="LinkedIn Content Writer",
        goal="Write an engaging, professional LinkedIn post grounded in the research",
        backstory="You are a seasoned content creator known for punchy hooks and clear posts people want to read.",
        llm=gemini,
        verbose=True,
    )

    editor = Agent(
        role="Content Editor",
        goal="Polish a draft LinkedIn post into a final, publish-ready version",
        backstory="You are a sharp editor who HATES hype. You cut superlatives and buzzwords, and prefer concrete specifics over grand claims. You make posts sound like a thoughtful expert, not a hype account.",
        llm=gemini,
        verbose=True,
    )

    research_task = Task(
        description="Research the topic: '{topic}'. Search the web for recent facts, statistics, examples, and developments. Focus on current, credible information.",
        expected_output="A clear bullet-point list of key findings with sources where possible.",
        agent=researcher,
    )

    write_post = Task(
        description="Using the research findings, write an engaging LinkedIn post (~{word_count} words) about '{topic}'. Start with a strong hook and weave in real facts from the research.",
        expected_output="A draft LinkedIn post of about {word_count} words, grounded in the research.",
        agent=writer,
        context=[research_task],
    )

    edit_task = Task(
        description=(
            "Review the draft LinkedIn post. Improve it: make the hook stronger, "
            "cut buzzwords and filler, tighten the flow, and add light line breaks so "
            "it's easy to read on LinkedIn. Keep it around {word_count} words and keep "
            "all facts accurate. Output ONLY the final, polished post — nothing else."
        ),
        expected_output="The final, polished LinkedIn post, ready to publish.",
        agent=editor,
        context=[research_task,write_post],
    )

    return Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_post, edit_task],
        verbose=True,
    )

def save_post(post_text, topic):
    """Save the finished post to a timestamped file in the posts/ folder."""
    os.makedirs("posts", exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    # turn the topic into a safe, short filename
    slug = "".join(c if c.isalnum() or c in " -_" else "" for c in topic)[:40].strip().replace(" ", "_")
    filename = f"posts/post_{stamp}_{slug}.md"

    with open(filename, "w", encoding="utf-8") as f:   # utf-8 = handles emojis 🎯
        f.write("# LinkedIn Post Draft\n\n")
        f.write(f"**Topic:** {topic}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(post_text)

    return filename

def main():
    print("=== LinkedIn Post Generator ===\n")
    topic = input("📝 What should the post be about? ")
    word_count = input("🔢 Roughly how many words? (e.g. 150) ") or "150"

    crew = build_crew()
    result = crew.kickoff(inputs={"topic": topic, "word_count": word_count})

    post_text = str(result)   # turn the result into plain text

    print("\n\n========== FINAL POLISHED POST ==========\n")
    print(post_text)

    filename = save_post(post_text, topic)   # save it
    print(f"\n💾 Saved to: {filename}")


if __name__ == "__main__":
    main()