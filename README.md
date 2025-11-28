# 🌍 LuxeTravel AI — Intelligent Multi-Agent Travel Concierge
### Google AI Agents Intensive — Capstone Project (Fall 2025)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Production-success?style=for-the-badge"/>
</p>

---

## 📖 Overview

**LuxeTravel AI** is a powerful **multi-agent travel planning system** that automates research, hotel finding, and itinerary creation.  
Instead of manually browsing dozens of websites, LuxeTravel’s agents **research**, **curate**, and **deliver a complete itinerary in seconds**.

Designed for the **Concierge Agents Track**, this project demonstrates:

- Multi-Agent Orchestration  
- Tool-Augmented Agents (Web Search)  
- Google Gemini Reasoning  
- Session Memory  
- Real-time Observability in Streamlit  

---

## 🤖 Multi-Agent Team

### **1. 🕵️ Researcher Agent — “The Scout”**
**Tools:** DuckDuckGo Search  
**Tasks:**
- Live weather  
- Travel advisories  
- Events & festivals  
- Cultural insights  

---

### **2. 🏨 Hotel & Dining Agent — “The Concierge”**
**Tools:** DuckDuckGo Search  
**Tasks:**
- Hotels based on budget  
- Dining recommendations  
- Price comparison  
- Ratings-based filtering  

---

### **3. 📅 Planner Agent — “The Architect”**
**Tools:** Pure LLM  
**Tasks:**
- Day-by-day itinerary  
- Cost estimation  
- Travel flow optimization  
- Final trip summary  

---

## 🏗️ Architecture

```mermaid
graph TD
    A[User Input] --> B[Streamlit UI]
    B --> C[🕵️ Researcher Agent]
    C --> M1[Session Memory]

    M1 --> D[🏨 Hotel Agent]
    D --> M2[Session Memory]

    M2 --> E[📅 Planner Agent]
    E --> B[Final Itinerary]
````

### **Core Architecture Features**

* Live data via Web Search
* Sequential multi-agent pipeline
* Session-based memory
* Real-time status updates
* Gemini-powered synthesis

---

## 🛠️ Tech Stack

| Component             | Technology              |
| --------------------- | ----------------------- |
| Frontend UI           | Streamlit               |
| Multi-Agent Framework | Agno (Phidata)          |
| AI Model              | Google Gemini 1.5 Flash |
| Tools                 | DuckDuckGo Web Search   |
| Environment           | Python 3.11+            |

---

## 🚀 Installation & Setup

### **1. Clone Repo**

```bash
git clone https://github.com/kiruthiyan/luxe-travel-ai.git
cd luxe-travel-ai
```

### **2. Create Virtual Environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### **3. Install Requirements**

```bash
pip install -r requirements.txt
```

### **4. Add API Key**

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_api_key_here
```

Get your free key from **Google AI Studio**.

### **5. Run App**

```bash
streamlit run app.py
```

---

## 💡 How to Use

1. Choose destination, dates, budget, and interests
2. Click **"Design My Perfect Trip"**
3. Agents run sequentially:

   * Researcher
   * Hotel Finder
   * Planner
4. View results in:

   * **Itinerary**
   * **Research**
   * **Hotels & Dining**

---

## 🏆 Capstone Requirements Checklist

| Requirement                           | Status                           |
| ------------------------------------- | -------------------------------- |
| Multi-Agent System                    | ✅ Done                           |
| Tools (Search, Custom)                | ✅ DuckDuckGo Web Search          |
| Gemini Model                          | ✅ 1.5 Flash                      |
| Memory                                | ✅ Session Memory                 |
| Observability                         | ✅ UI Live Status                 |
| Sequential / Parallel / Scoped Agents | ✅ Sequential Pipeline            |
| Agent Evaluation                      | ⚠️ Optional                      |
| A2A Protocol                          | ⚠️ Optional                      |
| Deployment                            | ⚠️ Can Deploy to Streamlit Cloud |

---

## 📦 requirements.txt

```text
streamlit
agno
google-generativeai
duckduckgo-search
python-dotenv
tenacity
```

---

## 🤝 License

MIT License.
Built with ❤️ for the **Google AI Agents Intensive Capstone Project**.

---
