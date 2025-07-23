import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load your dataset
df = pd.read_csv("features.csv")

# Split features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Use non-stratified split to avoid class-count errors
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "pvp_rank_model.pkl")
print("✅ Model saved as pvp_rank_model.pkl")
input("\nPress Enter to exit...")
