import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

EVAL_THRESHOLD = 0.70


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho RandomForestClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia.

    Tra ve:
        accuracy (float): do chinh xac tren tap danh gia.
    """

    # TODO 1: Doc du lieu huan luyen va danh gia
    df_train = pd.read_csv(data_path)
    df_eval  = pd.read_csv(eval_path)

    # TODO 2: Tach dac trung (X) va nhan (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval  = df_eval.drop(columns=["target"])
    y_eval  = df_eval["target"]

    with mlflow.start_run():

        # TODO 3: Ghi nhan cac sieu tham so
        mlflow.log_params(params)

        # TODO 4: Khoi tao va huan luyen RandomForestClassifier
        # Su dung warm_start=True de tang dan so luong cay va ghi nhan ket qua qua tung buoc (step)
        n_estimators = params.pop("n_estimators")
        model = RandomForestClassifier(**params, n_estimators=1, warm_start=True, random_state=42)

        for step in range(1, n_estimators + 1):
            model.n_estimators = step
            model.fit(X_train, y_train)

            # TODO 5: Du doan tren tap danh gia va tinh chi so
            preds = model.predict(X_eval)
            acc   = accuracy_score(y_eval, preds)
            f1    = f1_score(y_eval, preds, average="weighted")

            # TODO 6: Ghi nhan chi so vao MLflow theo tung step de tao Line chart
            mlflow.log_metric("accuracy_curve", acc, step=step)
            mlflow.log_metric("f1_score_curve", f1, step=step)

        # Ghi nhan ket qua cuoi cung (1 lan duy nhat) de tao Bar chart
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        # Khoi phuc lai params de log va luu model sau khi chay xong
        params["n_estimators"] = n_estimators
        mlflow.sklearn.log_model(model, "model")

        # TODO 7: In ket qua ra man hinh
        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # TODO 8: Luu metrics ra file outputs/metrics.json
        # File nay duoc doc boi GitHub Actions o Buoc 2
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/metrics.json", "w") as f:
            json.dump({"accuracy": acc, "f1_score": f1}, f)

        # TODO 9: Luu mo hinh ra file models/model.pkl
        # File nay duoc upload len GCS o Buoc 2
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    # TODO 10: Tra ve acc
    return acc


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
