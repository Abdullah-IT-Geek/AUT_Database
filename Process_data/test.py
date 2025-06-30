from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import pandas  as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
from sklearn.svm import SVC
import json
import numpy as np
import matplotlib.pyplot as plt

try:
    with open("../mqtt_data.json", "r") as f:
        data = json.load(f)
except Exception as e:
    print("Fehler beim Laden der JSON-Datei:", e)
    exit()
    
    
try:
    drop_oscillation_entries = data.get("drop_oscillation",{})
    drop_oscillation_df = pd.DataFrame([
        {
            "bottle": entry["bottle"],
            "drop_oscillation": [float(val) for val in entry["drop_oscillation"]]
        }
        for entry in drop_oscillation_entries.values()
    ])
except Exception as e:
    print("Keine Werte vorhanden:", e)
    exit()   
try:
    ground_truth_entries = data.get("ground_truth",{})
    ground_truth_df = pd.DataFrame([
        {
            "bottle": entry["bottle"],
            "is_cracked": entry["is_cracked"]
        }
        for entry in ground_truth_entries.values()
    ])
except Exception as e:
    print("Keine Werte vorhanden:", e)
    exit()  
    
for table_idx, (index, row) in enumerate(drop_oscillation_df.iterrows()):
    print(table_idx, row["bottle"], row["drop_oscillation"])
    

    
try:
    for table_idx, (index, row) in enumerate(drop_oscillation_df.iterrows()):
        if table_idx < 5: 
            plt.plot(range(len(row["drop_oscillation"])), row["drop_oscillation"], label=f"Flasche {row['bottle']}")

    plt.xlabel("Sample-size")
    plt.ylabel("Amplitude")
    plt.title("drop_oscillation für die ersten 4 Flaschen")
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, label="Null-Linie")
    plt.legend()
    plt.grid(True)
    plt.show()
except Exception as e:
    print("Fehler beim Plotten der Drop Oscillations:", e)
  
  
df_merged_data = pd.merge(drop_oscillation_df,ground_truth_df, on="bottle")


df_merged_data["Mean"] = df_merged_data["drop_oscillation"].apply(np.mean)
df_merged_data["STD"] = df_merged_data["drop_oscillation"].apply(np.std)
df_merged_data["Minimum"] = df_merged_data["drop_oscillation"].apply(np.min)
df_merged_data["Maximum"] = df_merged_data["drop_oscillation"].apply(np.max)
df_merged_data["RMS"] = df_merged_data["drop_oscillation"].apply(lambda x: np.sqrt(np.mean(np.square(x))))
df_merged_data.head()

counts, bins = np.histogram(df_merged_data["RMS"], bins="auto")

# Talwert finden = Bin mit minimaler Häufigkeit zwischen den Peaks
mask = (bins[:-1] > 0.3) & (bins[:-1] < 0.8)
min_count_index = np.argmin(counts[mask])

bins_in_range = bins[:-1][mask]
Schwellwert = bins_in_range[min_count_index]

print(f"Threshold (Talwert zwischen Peaks): {Schwellwert:.3f}")

# Plot zur Kontrolle
plt.hist(df_merged_data["RMS"], bins="auto", edgecolor='black')
plt.axvline(Schwellwert, color='red', linestyle='dashed', label=f'Threshold: {Schwellwert:.3f}')
plt.xlabel("RMS")
plt.ylabel("Häufigkeit")
plt.title("Histogramm der RMS-Werte mit Threshold")
plt.legend()
plt.grid(True)
plt.show()

df_merged_data["is_cracked_drop_oscillation"] = df_merged_data["RMS"].apply(lambda x: 1 if x > Schwellwert else 0)
df_merged_data.head()

feature_cols = ["RMS", "Mean", "STD", "Minimum", "Maximum"]
X = df_merged_data[feature_cols]
Y = df_merged_data["is_cracked"]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.25, random_state=42, stratify=Y
)

results = []

# Modelltraining
model_1 = LogisticRegression()
model_1.fit(X_train, y_train)

# 🔍 Vorhersage auf Trainingsdaten
y_pred_train_logreg = model_1.predict(X_train)

print("\n=== Logistic Regression Confusion Matrix (Training) ===")
cm_train_logreg = confusion_matrix(y_train, y_pred_train_logreg)
print(cm_train_logreg)

print("\n=== Logistic Regression Classification Report (Training) ===")
print(classification_report(y_train, y_pred_train_logreg))

ConfusionMatrixDisplay(confusion_matrix=cm_train_logreg).plot()
plt.title("Logistic Regression Confusion Matrix (Training)")
plt.show()

# 🔍 Vorhersage auf Testdaten
y_pred_test_logreg = model_1.predict(X_test)

print("\n=== Logistic Regression Confusion Matrix (Test) ===")
cm_test_logreg = confusion_matrix(y_test, y_pred_test_logreg)
print(cm_test_logreg)

print("\n=== Logistic Regression Classification Report (Test) ===")
print(classification_report(y_test, y_pred_test_logreg))

ConfusionMatrixDisplay(confusion_matrix=cm_test_logreg).plot()
plt.title("Logistic Regression Confusion Matrix (Test)")
plt.show()


y_train = y_train.astype(int)
y_test = y_test.astype(int)
y_pred_train_logreg = y_pred_train_logreg.astype(int)
y_pred_test_logreg = y_pred_test_logreg.astype(int)

results.append({
    "Modell": "Logistic Regression",
    "Train Accuracy": accuracy_score(y_train, y_pred_train_logreg),
    "Test Accuracy": accuracy_score(y_test, y_pred_test_logreg),
    "Train F1": f1_score(y_train, y_pred_train_logreg),
    "Test F1": f1_score(y_test, y_pred_test_logreg),
})


model_2 = KNeighborsClassifier(n_neighbors=3)
model_2.fit(X_train, y_train)

y_pred_train_knn = model_2.predict(X_train)

print("\n=== KNN Confusion Matrix (Training) ===")
cm_train_knn = confusion_matrix(y_train, y_pred_train_knn)
print(cm_train_knn)

print("\n=== KNN Classification Report (Training) ===")
print(classification_report(y_train, y_pred_train_knn))

ConfusionMatrixDisplay(confusion_matrix=cm_train_knn).plot()
plt.title("KNN Confusion Matrix (Training)")
plt.show()

y_pred_test_knn = model_2.predict(X_test)

print("\n=== KNN Confusion Matrix (Test) ===")
cm_test_knn = confusion_matrix(y_test, y_pred_test_knn)
print(cm_test_knn)

print("\n=== KNN Classification Report (Test) ===")
print(classification_report(y_test, y_pred_test_knn))

ConfusionMatrixDisplay(confusion_matrix=cm_test_knn).plot()
plt.title("KNN Confusion Matrix (Test)")
plt.show()

y_train = y_train.astype(int)
y_test = y_test.astype(int)
y_pred_train_knn = y_pred_train_knn.astype(int)
y_pred_test_knn = y_pred_test_knn.astype(int)

results.append({
    "Modell": "KNN",
    "Train Accuracy": accuracy_score(y_train, y_pred_train_knn),
    "Test Accuracy": accuracy_score(y_test, y_pred_test_knn),
    "Train F1": f1_score(y_train, y_pred_train_knn),
    "Test F1": f1_score(y_test, y_pred_test_knn),
})


# Modelltraining
model_3 = SVC()
model_3.fit(X_train, y_train)
# Vorhersage auf Trainingsdaten
y_pred_train_svc = model_3.predict(X_train)

print("\n=== SVC Confusion Matrix (Training) ===")
cm_train_svc = confusion_matrix(y_train, y_pred_train_svc)
print(cm_train_svc)

print("\n=== SVC Classification Report (Training) ===")
print(classification_report(y_train, y_pred_train_svc))

ConfusionMatrixDisplay(confusion_matrix=cm_train_svc).plot()
plt.title("SVC Confusion Matrix (Training)")
plt.show()

# Vorhersage auf Testdaten
y_pred_test_svc = model_3.predict(X_test)

print("\n=== SVC Confusion Matrix (Test) ===")
cm_test_svc = confusion_matrix(y_test, y_pred_test_svc)
print(cm_test_svc)

print("\n=== SVC Classification Report (Test) ===")
print(classification_report(y_test, y_pred_test_svc))

ConfusionMatrixDisplay(confusion_matrix=cm_test_svc).plot()
plt.title("SVC Confusion Matrix (Test)")
plt.show()

y_train = y_train.astype(int)
y_test = y_test.astype(int)
y_pred_train_svc = y_pred_train_svc.astype(int)
y_pred_test_svc = y_pred_test_svc.astype(int)

results.append({
    "Modell": "SVC",
    "Train Accuracy": accuracy_score(y_train, y_pred_train_svc),
    "Test Accuracy": accuracy_score(y_test, y_pred_test_svc),
    "Train F1": f1_score(y_train, y_pred_train_svc),
    "Test F1": f1_score(y_test, y_pred_test_svc),
})

model_4 = RandomForestClassifier(random_state=42)
model_4.fit(X_train, y_train)

#Vorhersage auf Trainingsdaten
y_pred_train_rf = model_4.predict(X_train)

print("\n=== Random Forest Confusion Matrix (Training) ===")
cm_train_rf = confusion_matrix(y_train, y_pred_train_rf)
print(cm_train_rf)

print("\n=== Random Forest Classification Report (Training) ===")
print(classification_report(y_train, y_pred_train_rf))

ConfusionMatrixDisplay(confusion_matrix=cm_train_rf).plot()
plt.title("Random Forest Confusion Matrix (Training)")
plt.show()

# Vorhersage auf Testdaten
y_pred_test_rf = model_4.predict(X_test)

print("\n=== Random Forest Confusion Matrix (Test) ===")
cm_test_rf = confusion_matrix(y_test, y_pred_test_rf)
print(cm_test_rf)

print("\n=== Random Forest Classification Report (Test) ===")
print(classification_report(y_test, y_pred_test_rf))

ConfusionMatrixDisplay(confusion_matrix=cm_test_rf).plot()
plt.title("Random Forest Confusion Matrix (Test)")
plt.show()

y_train = y_train.astype(int)
y_test = y_test.astype(int)
y_pred_train_rf = y_pred_train_rf.astype(int)
y_pred_test_rf = y_pred_test_rf.astype(int)

results.append({
    "Modell": "Random Forest",
    "Train Accuracy": accuracy_score(y_train, y_pred_train_rf),
    "Test Accuracy": accuracy_score(y_test, y_pred_test_rf),
    "Train F1": f1_score(y_train, y_pred_train_rf),
    "Test F1": f1_score(y_test, y_pred_test_rf),
})

df_result = pd.DataFrame(results)
print(df_result)