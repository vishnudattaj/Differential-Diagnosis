import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib

testing = pd.read_csv("/workspaces/3rd-period-isp-differential-diagnosis/Flask_Login/Testing.csv")
training = pd.read_csv("/workspaces/3rd-period-isp-differential-diagnosis/Flask_Login/Training.csv")

X_train = training.iloc[:, 0:132]
y_train = training.iloc[:, 132]

X_test = testing.iloc[:, 0:132]
y_test = testing.iloc[:, 132]

X = pd.concat([X_train, X_test])
y = pd.concat([y_train, y_test])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

model = xgb.XGBClassifier(
    max_depth=3,
    learning_rate=0.01,
    n_estimators=200,
    reg_lambda=1,
    subsample=0.8,
    objective='multi:softprob',
    eval_metric='mlogloss',
    random_state=42
)

print("Training XGBoost model...")
model.fit(X_train, y_train_encoded)

y_pred_encoded = model.predict(X_test)
y_pred = label_encoder.inverse_transform(y_pred_encoded)
accuracy = np.mean(y_pred == y_test)
print(f"Test accuracy: {accuracy:.4f}")
print("Classification report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, filename="/workspaces/3rd-period-isp-differential-diagnosis/xgboostModel.joblib")
joblib.dump(label_encoder, filename="/workspaces/3rd-period-isp-differential-diagnosis/label_encoder.joblib")