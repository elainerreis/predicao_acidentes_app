"""
home_model_metrics.py

Exibe as métricas finais do modelo XGBoost
na página inicial da aplicação.
"""

import streamlit as st


MODEL_METRICS = {
    "accuracy": 0.852,
    "precision": 0.517,
    "recall": 0.782,
    "f1_score": 0.623,
    "roc_auc": 0.910,
}


def show_model_metrics() -> None:
    """
    Exibe as métricas obtidas pelo modelo
    no conjunto de teste.
    """

    st.subheader("Desempenho do Modelo")

    (
        col_accuracy,
        col_precision,
        col_recall,
        col_f1,
        col_roc_auc,
    ) = st.columns(
        5,
        gap="small",
    )

    with col_accuracy:
        st.metric(
            label="Acurácia",
            value=f"{MODEL_METRICS['accuracy']:.3f}",
        )

    with col_precision:
        st.metric(
            label="Precisão",
            value=f"{MODEL_METRICS['precision']:.3f}",
        )

    with col_recall:
        st.metric(
            label="Recall",
            value=f"{MODEL_METRICS['recall']:.3f}",
        )

    with col_f1:
        st.metric(
            label="F1-score",
            value=f"{MODEL_METRICS['f1_score']:.3f}",
        )

    with col_roc_auc:
        st.metric(
            label="ROC AUC",
            value=f"{MODEL_METRICS['roc_auc']:.3f}",
        )

    st.caption(
        """
        As métricas foram calculadas no conjunto de teste. A precisão,
        o recall e o F1-score referem-se à classe positiva, composta pelos
        registros classificados como graves.
        """
    )