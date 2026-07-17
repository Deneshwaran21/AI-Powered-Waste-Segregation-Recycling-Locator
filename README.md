# ♻️ AI Waste Sorter

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)

**Snap a photo of your waste, and our AI will identify the material and connect you with nearby recycling agents.**

---

## 📌 Overview

**AI Waste Sorter** is a full-stack, AI-powered web application built for the **IDEA2IMPACT 2026 Hackathon**. It addresses the critical "last-mile" gap in recycling: confusion about waste types and a lack of localized disposal/recycling information.

Unlike most recycling apps that stop at classification, this solution provides **actionable next steps** by mapping the AI's prediction to a list of relevant local recyclers.

---

## ✨ Key Features

- **🧠 High-Precision AI Core**: Custom-trained ResNet-50 model achieving **95.96% validation accuracy** on 5 waste categories.
- **📸 Instant Classification**: Upload a photo, and the AI identifies the material in milliseconds.
- **🗺️ "Last-Mile" Recycler Locator**: After classification, the app provides a dynamic list of nearby recycling agents who accept that specific material.
- **🎨 Modern, Intuitive UI**: Dark-themed, responsive interface with confidence progress bars, emojis, and real-time feedback.
- **🔒 Privacy First**: All inference runs locally on the server—no data is sent to third-party APIs.

---

## 🚀 Live Demo

The application is deployed and live on Streamlit Cloud. Try it out here:

**👉 [AI Waste Sorter - Live Demo](https://ai-powered-waste-segregation-recycling-locator.streamlit.app/)**

---

## 🛠️ Tech Stack

| Layer | Tools & Frameworks |
| :--- | :--- |
| **AI/ML** | Python, PyTorch, Torchvision, ResNet-50, Transfer Learning |
| **Frontend** | Streamlit, Pillow |
| **Deployment** | Streamlit Community Cloud, Git LFS |
| **Version Control** | Git, GitHub |

---

## 📂 Project Structure
ai-waste-sorter/
├── app.py
├── requirements.txt
├── runtime.txt
├── waste_model.pth
└── README.md

---

## ⚙️ Setup Instructions (Run Locally)

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- **Python 3.11** (Recommended: 3.11.0 - 3.11.9. Avoid Python 3.12+ due to dependency conflicts).
- Git (to clone the repository).

### 2. Clone the Repository
Open your terminal and run:
```bash
git clone (https://github.com/Deneshwaran21/AI-Powered-Waste-Segregation-Recycling-Locator.git)
cd ai-waste-sorter
