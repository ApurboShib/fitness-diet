<div align="center">

# 🏋️‍♂️ Personal Fitness & Diet Recommender System

An intelligent, API-driven backend designed to help users make informed decisions about their health, fitness, and nutrition.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()


_Automatically analyzes your health stats to provide optimal workout and nutritional plans._

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Getting Started](#-getting-started)
- [API Documentation & Examples](#-api-documentation--examples)
- [Machine Learning Roadmap](#-machine-learning-roadmap)

---

## 💡 About The Project

Building an effective fitness routine requires an understanding of diverse health metrics. The **Personal Fitness & Diet Recommender System** acts as an intelligent digital assistant. It securely stores human biometric and lifestyle data, dynamically calculates underlying risk factors (like BMI and custom Health Scores), and outputs actionable wellness insights.

Currently utilizing a rule-based recommendation engine, the project is architected with a decoupled Machine Learning microservice (`ml_main.py`) to easily swap to intelligent predictive models in upcoming iterations.

---

## ✨ Key Features

- 🧑‍⚕️ **Comprehensive Health Profiling:** Records data covering dimensions from sleep cycle duration and daily steps to mental health self-assessments.
- 🔢 **Dynamic Metric Computation:** Automatically calculates accurate BMI and algorithmic Health Scores at database entry or update.
- 🥗 **Actionable Recommendations:** Delivers personalized macros/diet suggestions and weekly workout volumes based on real-time biometric tracking.
- 🔍 **Advanced Multi-parameter Search:** Query system records using combinations of parameters (e.g., _Find users with high protein diets exactly between age 25-30_).
- 📊 **Statistical Analytics Engine:** Endpoints for surfacing macro trends—such as the most popular diets, average cohort BMI, and personal trainer success rates.
- 💾 **Lightweight Persistence:** Uses an accessible, highly portable `personal_info.json` datastore (No heavy SQL setups required for prototyping).

---

## 🛠️ Tech Stack

- **Language:** `Python 3.10+`
- **Framework:** `FastAPI` (High performance, async-ready web framework)
- **Data Validation:** `Pydantic` (Strict type hinting and data payload validation)
- **ASGI Server:** `Uvicorn` (Lightning-fast ASGI server implementation)

---

## 📂 Project Architecture

```text
fitness-diet/
├── main.py                # Core application entrypoint & API router
├── ml_main.py             # Decoupled microservice for future Machine Learning models
├── personal_info.json     # JSON-based structured data storage
├── __pycache__/           # Compiled bytecode (Ignored by source control)
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
   https://github.com/ApurboShib/fitness-diet
   cd fitness-diet
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install fastapi uvicorn pydantic
   ```

4. **Launch the Server**

   ```bash
   uvicorn main:app --reload
   ```

5. **Verify**
   Open your browser and navigate to `http://127.0.0.1:8000`. You should see the welcome system message!

---

## 🌐 API Documentation & Examples

Because this project utilizes FastAPI, your interactive API documentation is automatically generated. Once the server is running, visit:

- **Interactive UI (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative UI (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoint Sub-Systems

<details>
<summary><b>1. User Management (CRUD)</b></summary>

| Method | Endpoint              | Purpose                             |
| :----- | :-------------------- | :---------------------------------- |
| `POST` | `/create`             | Register a new user                 |
| `GET`  | `/view`               | Retrieve everything                 |
| `GET`  | `/view/{person_id}`   | Retrieve specific user by unique ID |
| `PUT`  | `/update/{person_id}` | Modify existing user parameters     |

</details>

<details>
<summary><b>2. Recommendations & Analysis</b></summary>

| Method | Endpoint                  | Purpose                                   |
| :----- | :------------------------ | :---------------------------------------- |
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

## 🤖 Machine Learning Roadmap

The next major release will pivot from static threshold-based recommendations to a full **Predictive Machine Learning Pipeline**.

**The `ml_main.py` Service will handle:**

1. **Feature Engineering:** Automated One-Hot Encoding parsing of user dimensions (Diet, Gender) + MinMax Scaling for numeric fields (Height, Weight).
2. **Model Serving:** Loading standard artifacts (`.pkl` dumps via Scikit-Learn or Joblib).
3. **Inference:** Dedicated `/predict-custom` and `/predict-diet` endpoints bridging the core database with intelligent predictions.

_Future tools expected for this module: `pandas`, `scikit-learn`, `numpy`._

---

<p align="center">
  <i>Developed to build healthier habits through data-driven precision.</i>
</p>
