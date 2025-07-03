import gradio as gr
import re
import time
from dotenv import load_dotenv
import os
from openai import OpenAI

# 🔐 Load API Key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def extract_keywords(paragraph):
    prompt = f"""
You are an expert in experiential event planning.

Extract 5–10 short, specific, and thematic keywords or concepts from the event description below. These will be used to inspire immersive, tech-powered event ideas.

Each keyword should be 2–4 words long and describe a concrete idea or theme (e.g., "AR photo booths", "smart vending", "interactive storytelling").

Event Description:
"{paragraph}"

Return the keywords as a comma-separated list.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )

    keywords_raw = response.choices[0].message.content
    keywords = re.split(r'[,\n]', keywords_raw)
    return [kw.strip() for kw in keywords if kw.strip()]


def extract_keywords_from_title_and_link(title, link):
    prompt = f"""
You are an expert in event innovation.

Given the title and link below, extract 3–5 short, specific, and meaningful keywords or themes (2–4 words each) that describe what the page is about.

Title: {title}
Link: {link}

Return the keywords as a comma-separated list.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=150
    )

    raw = response.choices[0].message.content
    return [kw.strip() for kw in re.split(r'[,\n]', raw) if kw.strip()]


def search_similar_events_and_products_openai(keywords):
    input_text = f"Generate 10 useful URLs for experiential event ideas or iBoothMe.com inspiration related to the keywords: {', '.join(keywords)}"
    
    try:
        print("🌐 Using OpenAI web search tool...")
        response = client.responses.create(
            model="gpt-4.1",
            tools=[{"type": "web_search_preview"}],
            input=input_text
        )
        content = response.output_text
        results = []
        for line in content.strip().split("\n"):
            if "http" in line:
                parts = line.split(" - ", 1)
                if len(parts) == 2:
                    results.append((parts[0].strip(), parts[1].strip()))
                else:
                    url = line.strip()
                    results.append((url, url))
        return results[:10]
    except Exception as e:
        print(f"Search failed: {e}")
        return []


def generate_event_ideas(paragraph, search_links):
    search_summary = "\n".join([f"- {title}: {url}" for title, url in search_links])

    prompt = f"""
You are an expert event strategist for iBoothMe, a company offering creative experiences like AI photo booths, smart vending machines, audio booths, personalization stations, and immersive visual storytelling.

Based on the event description below, generate 6–7 **unique and diverse** iBoothMe-powered event ideas.

**Event Description:**
{paragraph}

**Inspiration from Related Ideas:**
{search_summary}

💡 **Your Task:**
Create ideas that are immersive, memorable, and creatively use iBoothMe’s **photo, video, and audio**-based technologies. Do **not** use AR, VR, projection mapping, or other tech-heavy elements.

You can optionally include:
- Studio Ghibli-inspired visuals **(in just one idea)**
- Personalized giveaways (e.g., Labibu dolls, custom t-shirts, stickers)
- Audio booths, video diaries, face filters, sound remixes, or creative vending

❗ Important:
- Avoid using AR, VR, holograms, or projection domes
- Don’t repeat formats like photo booths
- Every idea should have a **creative title** and a **detailed explanation** of how iBoothMe enhances the experience

Return only the final ideas in markdown format.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.95,
        max_tokens=1000
    )

    return response.choices[0].message.content


def main_workflow(paragraph):
    print("🚀 Started workflow")

    if not paragraph.strip():
        return "❌ Please enter an event description."
    
    print("🔍 Extracting keywords from paragraph...")
    base_keywords = extract_keywords(paragraph)

    print("🌐 Searching using OpenAI tool...")
    links = search_similar_events_and_products_openai(base_keywords)

    print("🔍 Extracting extra keywords from titles and links...")
    link_keywords = []
    for title, url in links:
        link_keywords.extend(extract_keywords_from_title_and_link(title, url))
    
    all_keywords = sorted(set(base_keywords + link_keywords))

    print("🧠 Generating ideas...")
    ideas = generate_event_ideas(paragraph, links)

    keyword_summaries = []
    for kw in all_keywords[:10]:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"Give a short one-line event idea description using the keyword: {kw}"}],
                temperature=0.6,
                max_tokens=60
            )
            description = response.choices[0].message.content.strip()
            keyword_summaries.append(f"- **{kw.title()}**: {description}")
        except:
            keyword_summaries.append(f"- **{kw.title()}**")
    
    formatted_links = "\n".join(keyword_summaries)

    return f"""

🌐 **Relevant Ideas:**  
{formatted_links}

💡 **Event Concepts Based on iBoothMe:**  
{ideas}
"""


# 🎨 Gradio UI
with gr.Blocks(title="iBoothMe Event Ideation App") as demo:
    gr.Markdown("## 🎉 iBoothMe Event Idea Generator\nDescribe your event goal and receive 6–7 interactive, tech-powered ideas!")

    paragraph = gr.Textbox(label="📝 Describe Your Event (e.g. Women's Day, Product Launch)", lines=4)

    submit_btn = gr.Button("🚀 Generate Event Concepts")
    output = gr.Markdown()

    submit_btn.click(
        fn=main_workflow,
        inputs=[paragraph],
        outputs=output,
        show_progress=True
    )

demo.launch(inline=False,share=True)
