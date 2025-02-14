import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
import joblib

testing = pd.read_csv("/workspaces/3rd-period-isp-differential-diagnosis/Flask_Login/Testing.csv")
training = pd.read_csv("/workspaces/3rd-period-isp-differential-diagnosis/Flask_Login/Training.csv")

X_train = training.iloc[:, 0:132]
y_train = training.iloc[:, 132]

X_test = testing.iloc[:, 0:132]
y_test = testing.iloc[:, 132]

X = pd.concat([X_train, X_test])
y = pd.concat([y_train, y_test])

print(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
rfc = RandomForestClassifier(random_state=10)
rfc.fit(X_train, y_train)

y_pred = rfc.predict(X_test)
skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(rfc, X_train, y_train, cv=skf)
print(scores)
print(classification_report(y_test, y_pred))

features = pd.DataFrame(rfc.feature_importances_, index=X_train.columns)

features.to_csv("features.csv")

joblib.dump(rfc, filename="/workspaces/3rd-period-isp-differential-diagnosis/randomForestModel.joblib")