import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

EVAL_THRESHOLD = 0.30


def train(
    all_params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.
    """
    # Bonus 1: Cau hinh Tracking URI tu bien moi truong (DagsHub)
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    mlflow.set_tracking_uri(tracking_uri)
    print(f"MLflow Tracking URI: {tracking_uri}")

    # Doc du lieu
    df_train = pd.read_csv(data_path)
    df_eval  = pd.read_csv(eval_path)

    # Bonus 5: Kiem tra phan phoi nhan
    print("\n--- Kiem tra phan phoi nhan (Bonus 5) ---")
    dist = df_train["target"].value_counts(normalize=True).to_dict()
    warning_flag = False
    for label, ratio in dist.items():
        print(f"Lop {label}: {ratio:.2%}")
        if ratio < 0.10:
            print(f"⚠️ CANH BAO: Lop {label} chi chiem {ratio:.2%}, duoi nguong 10%!")
            warning_flag = True
    if not warning_flag:
        print("✅ Phan phoi nhan can bang (>10% moi lop).")

    # Tach dac trung va nhan
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval  = df_eval.drop(columns=["target"])
    y_eval  = df_eval["target"]

    # Bonus 2: Chon loai mo hinh
    model_type = all_params.get("model_type", "random_forest")
    params = all_params.get(model_type, {})
    print(f"\nHuan luyen mo hinh: {model_type}")

    with mlflow.start_run():
        mlflow.log_param("model_type", model_type)
        mlflow.log_params(params)

        if model_type == "random_forest":
            # Tranh truyen trung tham so (n_estimators/random_state/warm_start)
            rf_params = dict(params)
            n_estimators = int(rf_params.pop("n_estimators", 100))
            rf_params.pop("random_state", None)
            rf_params.pop("warm_start", None)
            print(f"RF Params (excluding n_estimators): {rf_params}")
            model = RandomForestClassifier(**rf_params, n_estimators=1, warm_start=True, random_state=42)
            for step in range(1, n_estimators + 1):
                model.n_estimators = step
                model.fit(X_train, y_train)
                preds = model.predict(X_eval)
                acc = accuracy_score(y_eval, preds)
                f1 = f1_score(y_eval, preds, average="weighted")
                mlflow.log_metric("accuracy_curve", acc, step=step)
                mlflow.log_metric("f1_score_curve", f1, step=step)
        
        elif model_type == "gradient_boosting":
            # GradientBoostingClassifier khong ho tro warm_start theo kieu n_estimators don gian nhu RF trong vong lap
            model = GradientBoostingClassifier(**params, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_eval)
            acc = accuracy_score(y_eval, preds)
            f1 = f1_score(y_eval, preds, average="weighted")

        elif model_type == "logistic_regression":
            model = LogisticRegression(**params, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_eval)
            acc = accuracy_score(y_eval, preds)
            f1 = f1_score(y_eval, preds, average="weighted")

        else:
            raise ValueError(f"Khong ho tro model_type: {model_type}")

        # Ghi nhan ket qua cuoi cung
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # Bonus 3: Tao bao cao hieu suat chi tiet
        os.makedirs("outputs", exist_ok=True)
        report = classification_report(y_eval, preds)
        matrix = confusion_matrix(y_eval, preds)
        
        with open("outputs/report.txt", "w") as f:
            f.write(f"MODEL TYPE: {model_type}\n")
            f.write(f"PARAMETERS: {params}\n")
            f.write("-" * 30 + "\n")
            f.write("CLASSIFICATION REPORT:\n")
            f.write(report)
            f.write("\nCONFUSION MATRIX:\n")
            f.write(str(matrix))
        print("✅ Da tao bao cao outputs/report.txt")

        # Luu metrics ra file outputs/metrics.json (Bonus 5: them phan phoi nhan)
        with open("outputs/metrics.json", "w") as f:
            json.dump({
                "accuracy": acc, 
                "f1_score": f1,
                "label_distribution": {str(k): v for k, v in dist.items()}
            }, f)

        # Luu mo hinh
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    return acc


if __name__ == "__main__":
    with open("params.yaml") as f:
        all_params = yaml.safe_load(f)
    train(all_params)

