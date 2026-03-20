<div align="center">

# 🏋️‍♂️ AI Personal Fitness & Diet Recommender System

An intelligent, API-driven backend and interactive web frontend designed to help users make informed decisions about their health, fitness, and nutrition.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

_Automatically analyzes your health stats to provide optimal workout and nutritional plans using Machine Learning._

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
- [API Documentation & Examples](#-api-documentation--examples)
- [Machine Learning Implementation](#-machine-learning-implementation)

---

## 💡 About The Project

Building an effective fitness routine requires an understanding of diverse health metrics. The **AI Personal Fitness & Diet Recommender System** acts as an intelligent digital assistant. It securely stores human biometric and lifestyle data, dynamically calculates underlying risk factors (like BMI and custom Health Scores), and outputs actionable wellness insights.

Transitioning from a rule-based engine, the project now integrates an end-to-end Machine Learning pipeline utilizing Scikit-learn's `RandomForestClassifier`. Additionally, a fully interactive frontend dashboard built with Streamlit has been introduced to allow intuitive visual explorations of metrics, predictions, and analytics.

---

## ✨ Key Features

- 🧑‍⚕️ **Comprehensive Health Profiling:** Records data covering dimensions from sleep cycle duration and daily steps to mental health self-assessments.
- 🧠 **Machine Learning Predictions:** An integrated classification model that predicts fitness traits and intelligently clusters users based on historical tracking.
- 🖥️ **Interactive Web Dashboard:** A sleek, user-friendly Streamlit frontend mapping directly to FastAPI backend operations with real-time UI updates and data visualizations.
- 🔢 **Dynamic Metric Computation:** Automatically calculates accurate BMI and algorithmic Health Scores at database entry or update.
- 🥗 **Actionable Recommendations:** Delivers personalized macros/diet suggestions and weekly workout volumes based on real-time biometric tracking.
- 🔍 **Advanced Multi-parameter Search:** Query system records using combinations of parameters (e.g., _Find users with high protein diets exactly between age 25-30_).
- 📊 **Statistical Analytics Engine:** Endpoints for surfacing macro trends—such as the most popular diets, average cohort BMI, and personal trainer success rates.
- 💾 **Lightweight Persistence:** Uses an accessible, highly portable `personal_info.json` datastore for the primary CRUD database.

---

## 🛠️ Tech Stack

- **Language:** `Python 3.10+`
- **Backend Framework:** `FastAPI` (High performance, async-ready web framework)
- **Frontend Framework:** `Streamlit` (Interactive data-apps)
- **Machine Learning:** `Scikit-Learn`, `Pandas`, `Numpy`
- **Data Validation:** `Pydantic` (Strict type hinting and data payload validation)
- **Data Visualization:** `Plotly`
- **ASGI Server:** `Uvicorn`

---

## 📂 Project Architecture

```text
fitness-diet/
├── main.py                # Core FastAPI application entrypoint & API router
├── streamlit_app.py       # Interactive Streamlit frontend dashboard
├── train.py               # ML model automated training pipeline config
├── app.py                 # Auxiliary ML model loading script
├── personal_info.json     # JSON-based structured user data storage
├── dataset/               # Raw datasets (e.g., Obesity and Lifestyle Data.csv)
├── Model/                 # Saved models (model.pkl) and Jupyter notebooks
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

Follow these steps to get a local development environment up and running.

### Prerequisites

Make sure you have Python installed on your local machine.

- Python >= 3.8

### Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/ApurboShib/fitness-diet.git
   cd fitness-diet
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install fastapi uvicorn pydantic pandas scikit-learn streamlit plotly requests
   ```

4. **Train the Initial Machine Learning Model**

   ```bash
   python train.py
   # This will process the CSV dataset and output a `Model/model.pkl` file used by the API.
   ```

5. **Launch the FastAPI Server (Terminal 1)**

   ```bash
   uvicorn main:app --reload
   ```

6. **Launch the Streamlit Dashboard (Terminal 2)**

   Open a new terminal window, activate your environment, and run:

   ```bash
   streamlit run streamlit_app.py
   ```

---

## 🌐 API Documentation & Examples

Because this project utilizes FastAPI, your interactive API documentation is automatically generated. Once the server is running, visit:

- **Interactive UI (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative UI (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoint Sub-Systems

<details>
<summary><b>1. User Management (CRUD)</b></summary>

| Method   | Endpoint              | Purpose                             |
| :------- | :-------------------- | :---------------------------------- |
| `POST`   | `/create`             | Register a new user                 |
| `GET`    | `/view`               | Retrieve everything                 |
| `GET`    | `/view/{person_id}`   | Retrieve specific user by unique ID |
| `PUT`    | `/update/{person_id}` | Modify existing user parameters     |
| `DELETE` | `/delete/{person_id}` | Remove an existing user             |

</details>

<details>
<summary><b>2. Recommendations & ML Predictions</b></summary>

| Method | Endpoint                  | Purpose                                   |
| :----- | :------------------------ | :---------------------------------------- |
| `POST` | `/predict`                | Dynamic machine learning predictions      |
| `POST` | `/retrain`                | Retrain the ML model dynamically          |
| `GET`  | `/recommend/diet/{id}`    | Outputs a specialized nutritional roadmap |
| `GET`  | `/recommend/workout/{id}` | Outputs a tailored exercise regimen       |

</details>

<details>
<summary><b>3. Search & Statistics</b></summary>

| Method | Endpoint                 | Purpose                                                          |
| :----- | :----------------------- | :--------------------------------------------------------------- |
| `GET`  | `/search`                | Deep filter (name, age min/max, diet, trainer status)            |
| `GET`  | `/sort`                  | Order whole dataset ascending/descending by height, weight, etc. |
| `GET`  | `/stats/average_bmi`     | Calculates global platform BMI                                   |
| `GET`  | `/stats/popular-diet`    | Finds the most frequent diet regimen globally                    |
| `GET`  | `/stats/health-overview` | High-level demographics overview                                 |

</details>

<br>

### 💡 Example: Creating a User

**POST** `http://127.0.0.1:8000/create`

```json
{
  "id": "USR-999",
  "name": "Joy Shib",
  "age": 24,
  "height": 1.7,
  "weight": 68.0,
  "mental_health": 8,
  "workout": 4,
  "has_personal_trainer": false,
  "calories": 2100,
  "diet": "Mediterranean",
  "gender": "male"
}
```

---

## 🤖 Machine Learning Implementation

The current backend fully integrates an active Machine Learning pipeline using `Scikit-Learn`:

1. **Feature Engineering & Preprocessing (`train.py`):** Uses a `ColumnTransformer` to handle `StandardScaler` for numeric values, `OneHotEncoder` for categoricals, and `OrdinalEncoder` mapping.
2. **Model Architecture:** Implements a `RandomForestClassifier` packaged within a unified Pipeline ensuring incoming JSON inference data is preprocessed identically to training data.
3. **Automated Serving:** Handled dynamically inside `main.py` where `.pkl` weights are mapped to Live Endpoints (`/predict` & `/retrain`), replacing previously static/threshold-based logic.

---

<p align="center">
  <i>Developed to build healthier habits through data-driven precision and ML predictions.</i>
</p>
