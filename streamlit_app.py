import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Fitness & Diet Tracker", page_icon="🏋️‍♂️", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stMetric {
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #ff4b4b;
    }
    h1 {
        color: #ff4b4b;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ AI-Powered Fitness & Diet Recommender")
st.markdown("### *Your Intelligent Health Assistant*")

menu = ["👤 Create Profile & Predict", "🧑‍💻 User Profile Dashboard", "📊 Global Analytics", "👥 View All Users"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "👤 Create Profile & Predict":
    st.header("✨ Create a New Profile")
    st.markdown("Fill out the form below to register and get an instant ML-driven health prediction.")
    
    with st.form("user_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            uid = st.text_input("Unique ID (e.g., U001)")
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)
            mental_health = st.slider("Mental Health Score (1-10)", 1, 10, 5)
            sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=7.0)
            water_intake = st.number_input("Water Intake (Liters)", min_value=0.0, max_value=10.0, value=2.0)
            workout = st.number_input("Workouts per week", min_value=0, max_value=14, value=3)
        with col3:
            diet = st.selectbox("Dietary Habits", ["Balanced", "High-calorie", "Low-calorie"])
            family_history = st.selectbox("Family History of Obesity", ["no", "yes"])
            smoking = st.selectbox("Smoking Habits", ["No", "Yes"])
            alcohol = st.selectbox("Alcohol Consumption", ["Never", "Sometimes", "Frequently", "Always"])
            has_trainer = st.checkbox("Has Personal Trainer?", value=False)
            
            # Default calorie value to meet model requirements if needed
            calories = st.number_input("Daily Calorie Intake", min_value=500, max_value=10000, value=2000)

        submit = st.form_submit_button("🚀 Save & Predict Health Status")

    if submit:
        if not uid or not name:
            st.error("Please enter a Unique ID and Name.")
        else:
            payload = {
                "id": uid, "name": name, "age": age, "height": height, "weight": weight,
                "mental_health": mental_health, "sleep_hours": sleep_hours, "workout": workout,
                "water_intake": water_intake, "family_history_obesity": family_history,
                "smoking_habits": smoking, "alcohol_consumption": alcohol,
                "has_personal_trainer": has_trainer, "calories": calories, "diet": diet, "gender": gender
            }
            
            with st.spinner("Saving data and consulting ML Model..."):
                res = requests.post(f"{API_URL}/create", json=payload)
                if res.status_code == 201:
                    st.success(f"Profile for {name} added successfully! ✅")
                    
                    # Call Predict Endpoint
                    pred_res = requests.post(f"{API_URL}/predict", json=payload)
                    if pred_res.status_code == 200:
                        pred_data = pred_res.json()
                        prediction = pred_data.get('predicted_obesity_level', 'Unknown')
                        st.info(f"🧠 **Machine Learning Prediction:** Based on the metrics provided, the model classifies {name}'s health status as **{prediction}**.")
                        st.balloons()
                else:
                    st.error(f"Error: {res.json().get('detail', res.text)}")

elif choice == "👥 View All Users":
    st.header("👥 Registered Users Database")
    res = requests.get(f"{API_URL}/view")
    if res.status_code == 200 and res.json():
        df = pd.DataFrame(res.json())
        st.dataframe(df, width='stretch')
    else:
        st.warning("No users found in the database. Please add some users first.")

elif choice == "�‍💻 User Profile Dashboard":
    st.header("🧑‍💻 User Profile & Health Dashboard")
    res = requests.get(f"{API_URL}/view")
    if res.status_code == 200 and res.json():
        users = res.json()
        user_options = {u['id']: u.get('name', f"Unknown ({u['id']})") for u in users}
        
        st.markdown("Select a user to view their complete health profile, lifestyle metrics, and AI recommendations.")
        selected_id = st.selectbox("Select Registered User", options=list(user_options.keys()), format_func=lambda x: f"{x} - {user_options[x]}")
        
        if selected_id:
            user_data = next((u for u in users if u['id'] == selected_id), None)
            
            if user_data:
                st.markdown("---")
                # Profile Header
                col1, col2, col3 = st.columns([1, 1.5, 1])
                with col1:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
                with col2:
                    st.subheader(f"✨ {user_data.get('name', 'Unknown User')}")
                    st.write(f"**ID:** `{user_data.get('id')}` | **Age:** {user_data.get('age', 'N/A')} | **Gender:** {user_data.get('gender', 'N/A')}")
                    st.write(f"**Height:** {user_data.get('height', 'N/A')}cm | **Weight:** {user_data.get('weight', 'N/A')}kg")
                with col3:
                    bmi = user_data.get('bmi', 0)
                    if isinstance(bmi, (int, float)):
                        st.metric("Current BMI", f"{bmi:.1f}")
                    else:
                        st.metric("Current BMI", "N/A")
                
                st.markdown("---")
                # Metrics & Radar Chart
                sc1, sc2 = st.columns([1, 1.5])
                with sc1:
                    st.markdown("### 📊 Key Statistics")
                    st.write(f"- **Dietary Habits:** {user_data.get('diet', 'N/A')}")
                    st.write(f"- **Avg Daily Calories:** {user_data.get('calories', 'N/A')} kcal")
                    st.write(f"- **Personal Trainer:** {'Yes' if user_data.get('has_personal_trainer') else 'No'}")
                    st.write(f"- **Family History:** {user_data.get('family_history_obesity', 'N/A')}")
                    st.write(f"- **Smoking:** {user_data.get('smoking_habits', 'N/A')} | **Alcohol:** {user_data.get('alcohol_consumption', 'N/A')}")
                
                with sc2:
                    # Radar chart for lifestyle
                    categories = ['Mental Health', 'Sleep (hrs)', 'Water (L)', 'Workout (days)']
                    vals = [
                        user_data.get('mental_health', 0), 
                        user_data.get('sleep_hours', user_data.get('sleep', 0)), 
                        user_data.get('water_intake', 0), 
                        user_data.get('workout', 0)
                    ]
                    fig = go.Figure(data=go.Scatterpolar(
                        r=vals,
                        theta=categories,
                        fill='toself',
                        marker=dict(color='#ff4b4b'),
                        line=dict(color='#ff4b4b')
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                        showlegend=False,
                        margin=dict(l=20, r=20, t=20, b=20),
                        height=250
                    )
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 🤖 AI Health Plan & Recommendations")
                rc1, rc2 = st.columns(2)
                
                with rc1:
                    st.info("#### 🥗 Diet Engine")
                    diet_res = requests.get(f"{API_URL}/recommend/diet/{selected_id}")
                    if diet_res.status_code == 200:
                        d_data = diet_res.json()
                        st.write(f"**Predicted Status:** {d_data.get('predicted_status', 'N/A')}")
                        st.success(d_data.get('diet_recommendation', 'N/A'))
                        
                with rc2:
                    st.info("#### 💪 Workout Engine")
                    work_res = requests.get(f"{API_URL}/recommend/workout/{selected_id}")
                    if work_res.status_code == 200:
                        w_data = work_res.json()
                        st.write(f"**Smart Health Score:** {w_data.get('health_score', 'N/A')}")
                        st.warning(w_data.get('workout_recommendation', 'N/A'))
    else:
        st.warning("Please add some users first to view profiles.")

elif choice == "📊 Global Analytics":
    st.header("📊 Application Analytics & ML Retraining")
    
    col1, col2, col3 = st.columns(3)
    
    # Error handling wrappers for analytics
    try:
        res_bmi = requests.get(f"{API_URL}/stats/average_bmi")
        if res_bmi.status_code == 200:
            data = res_bmi.json()
            col1.metric("Average User BMI", data.get('average_bmi', 0))
    except Exception:
        col1.warning("No BMI data")
        
    try:
        res_diet = requests.get(f"{API_URL}/stats/popular-diet")
        if res_diet.status_code == 200:
            data = res_diet.json()
            col2.metric("Most Popular Diet", data.get('most_popular_diet', 'N/A'))
    except Exception:
        col2.warning("No Diet data")
            
    try:
        res_health = requests.get(f"{API_URL}/stats/health-overview")
        if res_health.status_code == 200:
            data = res_health.json()
            col3.metric("Users w/ Trainer", data.get('percentage_with_trainer', '0%'))
    except Exception:
        col3.warning("No Trainer data")

    st.markdown("---")
    st.subheader("🤖 Continuous Machine Learning")
    st.markdown("Trigger a background pipeline to retrain the Random Forest model on the newest dataset, ensuring recommendations adapt over time.")
    
    if st.button("🔄 Trigger Model Retraining Pipeline"):
        try:
            retrain_res = requests.post(f"{API_URL}/retrain")
            if retrain_res.status_code == 200:
                st.success("Background training task started! The model weights will automatically cross-load once complete.")
            else:
                st.error("Failed to start retraining process.")
        except Exception as e:
            st.error(f"Cannot connect to backend: {e}")