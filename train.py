import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

def train_and_save_model():
    data_path = 'dataset/Obesity and Lifestyle Data.csv'
    if not os.path.exists(data_path):
        print("Data not found")
        return False
        
    df = pd.read_csv(data_path)
    
    if 'mental_health' not in df.columns:
        df['mental_health'] = 5 
    if 'sleep_hours' not in df.columns:
        df['sleep_hours'] = 7 

    X = df.drop(['Obesity_Level'], axis=1, errors='ignore')
    if 'Obesity_Level_Label' in X.columns:
        X = X.drop('Obesity_Level_Label', axis=1)
        
    y_raw = df['Obesity_Level']
    
    numeric_features = ['Age', 'Height', 'Weight', 'Physical_Activity_Frequency', 'Water_Intake', 'mental_health', 'sleep_hours']
    categorical_features = ['Gender', 'Family_History_Obesity', 'Smoking_Habits']
    ordinal_features = ['Dietary_Habits', 'Alcohol_Consumption']
    
    num_cols = [c for c in numeric_features if c in X.columns]
    cat_cols = [c for c in categorical_features if c in X.columns]
    ord_cols = [c for c in ordinal_features if c in X.columns]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ('ord', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), ord_cols)
        ])
        
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42, n_estimators=50))
    ])
    
    model.fit(X, y_raw)
    
    os.makedirs('Model', exist_ok=True)
    with open('Model/model.pkl', 'wb') as f:
        # Saving just the model since RandomForest handles string labels natively
        pickle.dump(model, f)
        
    print("Model trained and saved to Model/model.pkl")
    return True

if __name__ == '__main__':
    train_and_save_model()