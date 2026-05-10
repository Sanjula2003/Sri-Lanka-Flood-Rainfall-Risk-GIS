import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("../data/rainfall_flood_risk.csv")

# Encode categorical columns
label_encoders = {}

categorical_columns = [
    "district",
    "drainage_condition",
    "flood_risk"
]

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features
X = df[
    [
        "district",
        "monthly_rainfall_mm",
        "river_level_m",
        "soil_saturation_percent",
        "population_density",
        "flood_history_count",
        "drainage_condition"
    ]
]

# Target
y = df["flood_risk"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model and encoders
joblib.dump(model, "flood_risk_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("Flood risk model and encoders saved successfully.")