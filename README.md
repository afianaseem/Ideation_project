## 🎉 iBoothMe Event Ideation App

This AI-powered tool helps experiential event planners generate **creative, tech-enhanced event concepts** using iBoothMe solutions such as:

- 📸 AI Photo Booths  
- 🎧 Audio/Video Booths  
- 🧸 Personalized Giveaways  
- 🎯 Smart Vending Machines  
- 🎬 Immersive Storytelling

Built with **Gradio** for a fast and intuitive web UI, and powered by **OpenAI GPT-4**, it analyzes your event description and generates 6–7 unique, high-impact ideas tailored to your theme.

---

## 🚀 Features

- 🔍 Extracts smart keywords from your event description  
- 🌐 Searches for similar inspiration online  
- 🧠 Generates original event ideas using GPT-4  
- 🎨 Easy-to-use Gradio web interface  
- 🛡️ Automatically ignores sensitive data like `.env` and `venv` via `.gitignore`

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/afianaseem/Ideation_project.git
cd Ideation_project
```

2. Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # On Windows
# Or: source venv/bin/activate   # On Mac/Linux
```

3. Install Requirements
```bash
pip install -r requirements.txt
```

4. Add your OpenAI API Key
Create a .env file in the root directory:
```bash
OPENAI_API_KEY=your_openai_key_here
```

5. Run the App
```bash
python main.py
```
Then open the Gradio link in your browser

## 📦 Requirements
```nginx
gradio
openai
python-dotenv
```
(Already listed in requirements.txt)
