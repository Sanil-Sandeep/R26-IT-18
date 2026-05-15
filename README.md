<div align="center">

<h1>Adaptive Emotion-Aware E-Learning Platform</h1>
<h3>for Deaf O/L ICT Students</h3>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React_+_Vite-18.0+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)

[![MediaPipe](https://img.shields.io/badge/MediaPipe-Computer_Vision-FF6F00?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![ESP32](https://img.shields.io/badge/ESP32-IoT_Wearable-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://espressif.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[![SLIIT](https://img.shields.io/badge/Institution-SLIIT-003087?style=for-the-badge&logo=graduation-cap&logoColor=white)](https://sliit.lk)
[![Research](https://img.shields.io/badge/Type-Academic_Research-8b5cf6?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/Status-Active_Development-22c55e?style=for-the-badge)]()
[![Year](https://img.shields.io/badge/Year-2026-f59e0b?style=for-the-badge)]()

<br/>

> **🎓 AI-Powered Inclusive E-Learning Ecosystem for Deaf O/L ICT Students**
> Using Computer Vision · Knowledge Graphs · NLP · Sign-Supported Learning · IoT-Based Assistive Technologies

<br/>

[📖 Introduction](#-introduction) • [🎯 Objectives](#-research-objectives) • [🚀 Features](#-key-features) • [🏗️ Architecture](#%EF%B8%8F-system-architecture) • [🛠️ Tech Stack](#%EF%B8%8F-technologies-used) • [⚙️ Installation](#%EF%B8%8F-installation-guide) • [👨‍💻 Contributors](#-contributors)

</div>

---

## 📖 Introduction

Traditional e-learning platforms are built for hearing students and rely heavily on:

- 🔊 Audio explanations and spoken instructions
- 📄 Text-heavy educational materials
- 🔇 Static learning environments with no accessibility adaptations

This creates **major accessibility barriers** for deaf and hard-of-hearing students — especially when learning complex **Information and Communication Technology (ICT)** concepts at the O/L level.

The **Adaptive Emotion-Aware E-Learning Platform for Deaf O/L ICT Students** is an AI-powered adaptive learning ecosystem specifically engineered to bridge this gap by integrating:

| Module | Description |
|--------|-------------|
| 🧠 **Real-Time Attention Monitoring** | Webcam-based distraction detection and missed-segment identification |
| 📚 **Knowledge Graph Learning** | Concept relationship mapping with adaptive popup reinforcement |
| 🤖 **Emotion-Aware NLP Chatbot** | Mode-aware educational assistance that adapts to student emotion |
| ✋ **Text-to-Sign Avatar** | Visual sign language support with gloss conversion and fingerspelling fallback |
| 📳 **Smart Haptic Wristband** | ESP32-based IoT wearable delivering tactile learning notifications |
| 📊 **Predictive Analytics** | Learning behavior forecasting and engagement dashboards |

<br/>

---

## 🎯 Research Objectives

### 🏆 Main Objective
> Develop an AI-powered adaptive e-learning ecosystem that improves accessible digital education for deaf O/L ICT students.

### 🔍 Specific Objectives

- ✅ Monitor student **attention and engagement** in real-time using computer vision
- ✅ Detect **distracted learning behavior** using EAR and head pose estimation
- ✅ Identify **missed lesson segments** and trigger adaptive popup support
- ✅ Deliver **emotion-aware chatbot assistance** through EARA model adaptation
- ✅ Support **sign-based visual learning** via text-to-sign avatar rendering
- ✅ Improve concept understanding using **Knowledge Graph** relationships
- ✅ Introduce **wearable haptic feedback** through ESP32 smart wristband
- ✅ Enhance **inclusive education** with predictive learning analytics

<br/>

---

## 🚀 Key Features

<table>
<tr>
<td width="50%">

### 🧠 Real-Time Emotion & Attention Monitoring

- 📷 Webcam-based continuous attention monitoring
- 👁️ Eye Aspect Ratio (EAR) analysis
- 🎯 Head pose estimation
- 📊 Attention behavior analytics dashboard
- ⚠️ Missed segment detection & alerting
- 🗂️ Attention history tracking & logging

</td>
<td width="50%">

### 📚 Knowledge Graph-Based Learning Support

- 🕸️ Concept relationship mapping
- ❓ Intelligent popup question delivery (GQSA)
- 🔗 Prerequisite concept awareness
- 🖼️ Diagram-assisted learning panels
- 🔁 Adaptive reinforcement learning loops

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Emotion-Aware Adaptive Chatbot

- 📘 Learning Mode vs Exam Mode detection
- 💡 EARA — Emotion-Aware Response Adaptation
- 🎨 Dynamic answer style generation
- 📖 Curriculum-aware educational assistance
- 🔄 Concept revision & re-entry support
- 📈 Dynamic difficulty escalation engine

</td>
<td width="50%">

### ✋ Adaptive Text-to-Sign Avatar System

- 🔤 Text-to-gloss conversion pipeline
- 🤲 Gloss-to-gesture landmark mapping
- ▶️ Sign playback viewer with replay support
- 🖐️ Fingerspelling fallback mechanism
- 📜 Transcript-integrated sign learning

</td>
</tr>
<tr>
<td width="50%">

### 📳 Smart Haptic Wristband (IoT)

- 📳 Real-time vibration alert system
- 🖥️ OLED notification display
- 🎛️ Personalized tactile feedback profiles
- ⚡ ESP32-based embedded integration
- 🔔 Multi-alert type support

</td>
<td width="50%">

### 📊 Predictive Learning Analytics

- 📈 Engagement trend forecasting
- 📋 Missed segment reports
- 🧩 Concept mastery tracking
- 👩‍🏫 Educator-facing analytics dashboard
- 🔮 Early intervention predictions

</td>
</tr>
</table>

<br/>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                            STUDENT                                  │
│                   (Deaf O/L ICT Learner)                            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   FRONTEND  (React + Vite)                          │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ ┌─────────────┐  │
│  │  Attention   │ │  Knowledge   │ │  Chatbot   │ │ Sign Avatar │  │
│  │  Dashboard   │ │  Graph UI    │ │  Interface │ │   Viewer    │  │
│  └──────────────┘ └──────────────┘ └────────────┘ └─────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │  WebSockets + REST APIs (Axios)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   BACKEND  (FastAPI)                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ ┌─────────────┐  │
│  │   Attention  │ │  Knowledge   │ │   NLP &    │ │  Sign &     │  │
│  │   Routes     │ │  Graph API   │ │  Chatbot   │ │  Avatar API │  │
│  └──────────────┘ └──────────────┘ └────────────┘ └─────────────┘  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     AI / ML SERVICES                                 │
│                                                                      │
│  ┌──────────────────────┐   ┌──────────────────────────────────┐    │
│  │  TEPA Model          │   │  EARA Model                      │    │
│  │  Temporal Emotion &  │   │  Emotion-Aware Response          │    │
│  │  Attention Analysis  │   │  Adaptation                      │    │
│  └──────────────────────┘   └──────────────────────────────────┘    │
│                                                                      │
│  ┌──────────────────────┐   ┌──────────────────────────────────┐    │
│  │  GQSA Algorithm      │   │  Sign Avatar Engine              │    │
│  │  Graph-Based Popup   │   │  Gloss + Gesture Mapping         │    │
│  │  Question Selection  │   │  (MediaPipe Landmarks)           │    │
│  └──────────────────────┘   └──────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────┐   ┌──────────────────────────────────────────┐
│  MongoDB Database    │   │  IoT Wearable Feedback System            │
│  ├─ Student Profiles │   │  ┌────────────┐  ┌────────────────────┐  │
│  ├─ Attention Logs   │   │  │ ESP32 Mini │  │  OLED Display      │  │
│  ├─ Learning Data    │   │  │ Board      │  │  Vibration Motor   │  │
│  └─ Graph Datasets   │   │  └────────────┘  └────────────────────┘  │
└──────────────────────┘   └──────────────────────────────────────────┘
```

<br/>

---

## 🧩 Component Breakdown

<details>
<summary><strong>🧠 Component 01 — Real-Time Emotion & Attention Monitoring Learning Support System</strong></summary>

<br/>

**Overview:** Continuously monitors student engagement using webcam-based computer vision to detect distraction, track missed segments, and trigger adaptive popup learning support.

### Core Features
- Real-time webcam monitoring with MediaPipe Face Mesh
- Eye Aspect Ratio (EAR) and head pose tracking
- Attention event logging and missed lesson segment detection
- Diagram-supported popup learning delivery
- GQSA-based intelligent question selection

### 🔬 Proposed Novel Models

#### TEPA — Temporal Emotion & Attention Pattern Analysis
> Continuously analyzes attention behavior, detects distraction periods, and stores attention patterns for adaptive response triggering.

#### GQSA — Graph-Based Question Selection Algorithm
> Selects intelligent popup questions by reasoning over the current concept node, its prerequisite relationships, and avoiding repeated question delivery.

### Technologies
`MediaPipe` `OpenCV` `WebSockets` `FastAPI` `React` `MongoDB`

</details>

<details>
<summary><strong>✋ Component 02 — Adaptive Text-to-Sign Avatar and Transcript-Based Learning Support System</strong></summary>

<br/>

**Overview:** Converts lesson text into sign language gestures using gloss mapping and MediaPipe landmark rendering, providing a visual sign-supported learning channel.

### Core Features
- Text-to-gloss conversion pipeline
- Sign gesture mapping and playback rendering
- Fingerspelling fallback mechanism
- Replay-assisted learning guidance
- Transcript-integrated sign support
- Visual concept panel generation

### 🎨 Design Contributions
- Dual-coding learning support architecture
- Spatial-linguistic pairing for visual learning
- Glassmorphism UI design
- Landmark-based gesture rendering system

### Technologies
`FastAPI` `React + Vite` `Gemini 2.5 Flash` `Pollinations.ai` `MediaPipe Landmark Rendering` `MongoDB`

</details>

<details>
<summary><strong>🤖 Component 03 — NLP-Based Emotion-Aware, Intent-Aware Adaptive Chatbot</strong></summary>

<br/>

**Overview:** An educational chatbot that detects student emotion and learning mode, adapting explanation styles dynamically to maximize comprehension and engagement.

### Core Features
- Emotion-aware response adaptation (EARA model)
- Learning Mode vs Exam Mode detection
- Knowledge Graph prerequisite awareness
- Dynamic answer style and difficulty adaptation
- Answer compression mode for quick revision
- Forgetting curve reinforcement scheduling

### 🔬 Proposed Novel Model

#### EARA — Emotion-Aware Response Adaptation
> The chatbot dynamically adjusts its explanation style based on detected student state:

| Detected State | Response Adaptation |
|----------------|---------------------|
| 😊 Understanding | Advance to next concept |
| 😕 Confusion | Simplify and use visual aids |
| 😴 Distraction | Inject engagement triggers |
| 😑 Boredom | Switch to interactive mode |

### Technologies
`NLP Adaptive Assistance` `FastAPI` `React + Vite` `MongoDB` `REST APIs`

</details>

<details>
<summary><strong>📳 Component 04 — Smart Haptic Wristband and Predictive Learning Analytics System</strong></summary>

<br/>

**Overview:** ESP32-based IoT wearable that delivers tactile learning notifications and supports a predictive analytics dashboard for educators.

### Core Features
- Smart vibration alerts for learning events
- OLED notification display system
- Personalized tactile feedback profiles
- Real-time distraction and engagement alerts
- Learning reminder system
- Predictive learning analytics engine

### 🔔 Supported Alert Types

| Alert Type | Trigger |
|------------|---------|
| 📳 Distraction Alert | Attention drop detected |
| 💬 Chatbot Reply Alert | New chatbot message ready |
| ❓ Popup Question Alert | Knowledge check triggered |
| 📅 Exam Reminder Alert | Upcoming exam detected |

### Hardware Components

| Component | Purpose |
|-----------|---------|
| ESP32 Mini Board | Main microcontroller |
| OLED Display | Visual notifications |
| Vibration Motor | Tactile haptic feedback |
| Push Button | Student interaction input |
| Breadboard Prototype | Hardware integration |

### Technologies
`ESP32` `FastAPI` `React + Vite` `MongoDB` `REST APIs`

</details>

<br/>

---

## 🛠️ Technologies Used

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | React + Vite | UI & real-time interface rendering |
| **Backend** | FastAPI | API gateway & ML service orchestration |
| **Database** | MongoDB | Student data, logs & graph datasets |
| **Computer Vision** | MediaPipe + OpenCV | Face mesh, EAR, head pose tracking |
| **NLP Engine** | Adaptive NLP Assistance | Emotion-aware chatbot responses |
| **AI Models** | EARA · TEPA · GQSA | Novel proposed research models |
| **Real-Time Comm.** | WebSockets | Live attention monitoring stream |
| **IoT Wearable** | ESP32 | Haptic feedback wristband |
| **External APIs** | Gemini 2.5 Flash · Pollinations.ai | Sign avatar content generation |
| **HTTP Client** | Axios + REST APIs | Frontend-backend communication |
| **Visualization** | Landmark-Based Gesture Rendering | Sign avatar playback |

<br/>

---

## 📂 Project Structure

```
Adaptive-Emotion-Aware-E-Learning-Platform-for-Deaf-O-L-ICT-Students/
│
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── 📁 models/          # Pydantic data models
│   │   ├── 📁 routes/          # FastAPI route handlers
│   │   ├── 📁 services/        # Business logic & AI services
│   │   ├── 📁 core/            # Core configuration & utilities
│   │   ├── 📁 datasets/        # Learning datasets & graphs
│   │   └── 📁 utils/           # Helper functions
│   │
│   ├── 📄 main.py              # FastAPI application entry point
│   └── 📄 requirements.txt     # Python dependencies
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/      # Reusable React components
│   │   ├── 📁 pages/           # Application page views
│   │   ├── 📁 hooks/           # Custom React hooks
│   │   ├── 📁 services/        # API service layers
│   │   ├── 📁 assets/          # Static assets & icons
│   │   └── 📁 utils/           # Frontend utilities
│   │
│   ├── 📄 package.json
│   └── 📄 vite.config.js
│
├── 📁 datasets/
│   ├── 📁 knowledge_graph/     # ICT concept relationships & maps
│   ├── 📁 gesture_datasets/    # Hand gesture landmark data
│   ├── 📁 transcript_datasets/ # Lesson transcript data
│   └── 📁 popup_question_data/ # GQSA question banks
│
├── 📁 hardware/
│   ├── 📁 esp32_wristband/     # ESP32 firmware & wiring diagrams
│   └── 📁 oled_display/        # OLED display configuration
│
├── 📁 docs/                    # Research documentation
├── 📁 screenshots/             # UI screenshots
└── 📄 README.md
```

<br/>

---

## ⚙️ Installation Guide

### Prerequisites

Make sure you have the following installed:

- **Python** `3.10+`
- **Node.js** `18+` with `npm`
- **MongoDB** (local or Atlas cloud)
- **Git**

---

### 1️⃣ Clone the Repository



---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
```

**Activate Virtual Environment:**

```bash
# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

**Run the Backend Server:**

```bash
uvicorn main:app --reload
```

> Backend available at: `http://localhost:8000`  
> Swagger API Docs: `http://localhost:8000/docs`

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

> Frontend available at: `http://localhost:5173`

---

### 4️⃣ ESP32 Wristband Setup

```bash
cd hardware/esp32_wristband
# Flash firmware using Arduino IDE or PlatformIO
# See hardware/esp32_wristband/README.md for full wiring guide
```

---

### 🌐 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=adaptive_learning_db
API_KEY=your_api_key
GEMINI_API_KEY=your_gemini_api_key
```

<br/>

---


## 📊 Datasets Used

### 🕸️ Knowledge Graph Datasets
- ICT concept relationship graphs (O/L curriculum aligned)
- Prerequisite learning pathway maps
- Popup question structures & answer banks

### ✋ Sign Gesture Datasets
- Hand gesture landmark coordinates
- Gloss-to-gesture mapping tables
- Fingerspelling gesture data

### 📈 Learning Analytics Data
- Attention event logs
- Missed segment records
- Student interaction sequences

<br/>

---

## 🔬 Research Contributions

| # | Contribution |
|---|-------------|
| 1 | **TEPA Model** — Temporal Emotion & Attention Pattern Analysis for continuous learning behavior monitoring |
| 2 | **EARA Model** — Emotion-Aware Response Adaptation enabling dynamic chatbot explanation style switching |
| 3 | **GQSA Algorithm** — Graph-Based Question Selection Algorithm for intelligent prerequisite-aware popup delivery |
| 4 | **Sign Avatar Pipeline** — End-to-end text-to-sign avatar rendering with fingerspelling fallback |
| 5 | **IoT Haptic Learning** — ESP32 wearable integration for tactile-based educational notifications |
| 6 | **Inclusive AI Ecosystem** — First integrated platform combining all above for deaf O/L ICT learners |

<br/>

---

## 📈 Commercialization & Sustainability

### 🎯 Target Users

| User Group | Use Case |
|------------|----------|
| 🎓 Deaf O/L ICT Students | Primary learners — core platform users |
| 🏫 Inclusive Education Schools | School-wide accessibility integration |
| 🏛️ Educational Institutions | Institution licensing for ICT departments |
| 🌍 Special Education Programs | NGO and government-backed accessibility programs |

### 💰 Revenue Model

- 🏫 **School Subscriptions** — Per-student or institution-wide plans
- ☁️ **SaaS Educational Platform** — Cloud-hosted multi-tenant deployment
- 🤝 **Government & NGO Partnerships** — Accessibility initiative grants
- 📊 **Premium Analytics Features** — Educator-facing predictive dashboards

### 🌐 Future Expansion

- 🇱🇰 **Sinhala / Tamil language support**
- 📱 **Mobile learning applications**
- 🤖 **Real-time AI tutoring system**
- 📚 **Multi-subject educational expansion**
- 🌍 **Regional sign language support**

<br/>

---

## 👨‍💻 Contributors

<div align="center">

| Student ID | Name | Component |
|------------|------|-----------|
| IT22211200 | **Tharaka W A K N** | 🧠 Component 01 — Real-Time Emotion & Attention Monitoring Learning Support System |
| IT22197764 | **Mendis L B L** | ✋ Component 02 — Adaptive Text-to-Sign Avatar and Transcript-Based Learning Support System |
| IT22185884 | **Kothalawala L S S** | 🤖 Component 03 — NLP-Based Emotion-Aware, Intent-Aware Adaptive Chatbot |
| IT19131948 | **Nawarathna I K K R B** | 📳 Component 04 — Smart Haptic Wristband and Predictive Learning Analytics System |

</div>

<br/>

---

## 🏫 Academic Information

<div align="center">

| Field | Details |
|-------|---------|
| 🏛️ **Institution** | SLIIT — Sri Lanka Institute of Information Technology |
| 🏢 **Faculty** | Faculty of Computing |
| 📅 **Year** | 2026 |
| 🔬 **Research Type** | Final Year Research Project |

</div>

**Research Areas:**  
`Artificial Intelligence` `Inclusive Education` `Adaptive Learning` `Computer Vision` `Natural Language Processing` `IoT-Based Assistive Technologies` `Sign Language Processing` `Knowledge Graphs`

<br/>

---

## 🧠 Future Improvements

- [ ] Advanced 3D avatar rendering for sign playback
- [ ] Larger and more diverse educational datasets
- [ ] Enhanced predictive analytics with LSTM models
- [ ] Sinhala and Tamil multi-language support
- [ ] Real-time AI tutoring system integration
- [ ] Cloud deployment (AWS / GCP / Azure)
- [ ] Mobile application (React Native)
- [ ] Enhanced ESP32 wearable hardware v2
- [ ] Multi-subject platform expansion beyond ICT

<br/>

---

## 🙏 Acknowledgements

We express our sincere gratitude to:

- 🏫 **SLIIT Faculty of Computing** — for providing research infrastructure and guidance
- 👨‍🏫 **Project Supervisors & Evaluators** — for their invaluable academic mentorship
- 🌍 **Open-Source AI Communities** — MediaPipe, FastAPI, React, MongoDB
- ♿ **Accessibility & Inclusive Education Initiatives** — for inspiring this research direction
- 🤟 **Deaf Communities in Sri Lanka** — for the motivation behind this work

<br/>

---

<div align="center">

**⭐ If this project helped you, please give it a star!**

[![Star](https://img.shields.io/github/stars/Sanil-Sandeep/R26-IT-18?style=social)](https://github.com/Sanil-Sandeep/R26-IT-18)

<br/>

```
Adaptive Emotion-Aware E-Learning Platform for Deaf O/L ICT Students
Improving Inclusive Digital Education Through AI-Powered Adaptive Learning
SLIIT Faculty of Computing © 2026
```

</div>
