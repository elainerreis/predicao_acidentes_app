"""
home_model_metrics.py

Calcula e exibe as métricas do modelo.
"""

import pandas as pd
import streamlit as st

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


def preparar_dados_xgboost(X: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas object para category,
    conforme utilizado durante o treinamento.
    """

    X = X.copy()

    for col in X.select_dtypes(include=["object"]).columns:
        X[col] = X[col].astype("category")

    return X


def preparar_categorias_teste(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> pd.DataFrame:
    """
    Garante que o conjunto de teste utilize
    exatamente as mesmas categorias do treino.
    """

    X_test = X_test.copy()

    for col in X_train.select_dtypes(include=["category"]).columns:

        X_test[col] = X_test[col].astype("category")

        X_test[col] = X_test[col].cat.set_categories(
            X_train[col].cat.categories
        )

    return X_test


def calculate_metrics(
    model,
    X_train,
    X_test,
    y_test,
):
    """
    Calcula as métricas do modelo.
    """

    X_train = preparar_dados_xgboost(X_train)

    X_test = preparar_categorias_teste(
        X_train,
        X_test,
    )

    y_pred = model.predict(X_test)

    y_prob = model.predict_proba(X_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-score": f1_score(y_test, y_pred),
        "ROC AUC": roc_auc_score(y_test, y_prob),
    }


def show_metrics(metrics):
    """
    Exibe as métricas do modelo.
    """

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Accuracy",
        f"{metrics['Accuracy']:.3f}",
    )

    c2.metric(
        "Precision",
        f"{metrics['Precision']:.3f}",
    )

    c3.metric(
        "Recall",
        f"{metrics['Recall']:.3f}",
    )

    c4.metric(
        "F1-score",
        f"{metrics['F1-score']:.3f}",
    )

    c5.metric(
        "ROC AUC",
        f"{metrics['ROC AUC']:.3f}",
    )