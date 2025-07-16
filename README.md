# 📚 QA-ChatBot – AI-Powered Chatbot with Gemini API, FastAPI & Streamlit

Welcome!  
This repository contains the complete source code and setup instructions for **QA-ChatBot** – an AI chatbot built with the Gemini API as its brain, using **FastAPI** for the backend, and **Streamlit** for an intuitive web-based frontend.

This project is designed to help you learn how to integrate modern generative AI APIs into a full-stack Python application.

---

## ✨ Overview

**QA-ChatBot** is:
- ⚡ Lightweight and fast, thanks to FastAPI.
- 🧠 Powered by Google's Gemini API to generate human-like responses.
- 🖼️ Visual and interactive, thanks to the Streamlit frontend.
- 🛠️ Easy to configure and extend, so you can experiment or build your own features on top.

---

## 🎯 Goals & Motivation

This project was created to:
- Demonstrate how to connect a **FastAPI backend** with a **Streamlit frontend**.
- Explore real-time AI chat powered by an external LLM (Gemini).
- Learn best practices in Python API development and deployment.
- Serve as a starter template for more advanced chatbot ideas.

---

## 📦 Project Structure

```plaintext
.
ai_chat_project/
├── README.md                  # 📚 Project documentation
├── .gitignore                 # 🚫 Files & folders to ignore in Git
├── backend/
│   ├── main.py                # 🚀 FastAPI backend entry point
│   ├── chat_model.py          # 🧠 Chat logic (rule-based or model integration)
│   └── requirements.txt       # 📦 Backend Python dependencies
├── frontend/
│   └── app.py                 # 🎨 Streamlit frontend app
└── Dockerfile                 # 🐳 Dockerfile to build container image
