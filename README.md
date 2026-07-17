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

### 3. Create a Virtual Environment
python -m venv venv

Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

### 4. Install Dependencies
pip install -r requirements.txt

### 5. Download the AI Model
The waste_model.pth file is large (~300MB). If it is not already in the root directory:
Option A (Git LFS): Ensure Git LFS is installed and run git lfs pull.
Option B (Manual): Download the file from the Releases or the link in the repository and place it in the root folder.

### 6. Run the Application
python -m streamlit run app.py

The app will open automatically in your default browser at http://localhost:8501.

### 📸 How to Use
Open the app in your browser.

Click the "Upload a photo of your waste" section.

Select a .jpg, .jpeg, or .png image of your waste.

Click the "🔍 Identify & Find Recyclers" button.

The AI will display:

The predicted waste category with a large emoji.

A confidence score (0-100%).

A list of nearby recycling agents that accept that specific material.

If the confidence is high (≥90%), you'll see virtual celebration balloons! 🎈

### AI Model Details
Architecture: ResNet-50 (Pre-trained on ImageNet).

Methodology: Transfer Learning.

Convolutional base was frozen to retain general visual features.

The final classifier head was replaced with a custom Sequential block.

Dataset: 5 custom categories (plastic_bottles, chips_packets, cardboard_paper, metal_cans, organic_kitchen).

Performance: Achieved 95.96% validation accuracy on a holdout test set.

Optimization: Trained using the Adam optimizer with CrossEntropyLoss.


---

### 💡 Quick Instructions for You:

1.  Copy the entire block of code above.
2.  In your GitHub repository, click **"Add file"** → **"Create new file"**.
3.  Name it `README.md`.
4.  Paste the code.
5.  Scroll down and click **"Commit new file"**.

This README is comprehensive, professional, and will immediately impress anyone (including the judges) who visits your GitHub repo. 🚀♻️
