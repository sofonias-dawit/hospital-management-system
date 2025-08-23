# ai-module/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

# 1. Load the dataset
try:
    data = pd.read_csv('symptoms_dataset.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: symptoms_dataset.csv not found. Make sure it's in the ai-module directory.")
    exit()

# 2. Prepare the data
# Features (X) are all columns except 'Disease'
X = data.drop('Disease', axis=1)
# Target (y) is the 'Disease' column
y = data['Disease']

# Get feature names for later use in the API
feature_names = list(X.columns)
print(f"Features used for training: {feature_names}")

# 3. Split the data (optional for this simple case, but good practice)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
print("Model trained successfully.")

# 5. Save the trained model and the feature list to files
model_filename = 'disease_predictor.joblib'
features_filename = 'model_features.joblib'

joblib.dump(model, model_filename)
joblib.dump(feature_names, features_filename)

print(f"Model saved to {model_filename}")
print(f"Model features saved to {features_filename}")

# 6. (Optional) Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model accuracy on test data: {accuracy * 100:.2f}%")