"""
report.py — Gerar tabelas e gráficos comparativos
Referência: Aula 07 (matplotlib para visualizar temperatura)
Stack: matplotlib + pandas (obrigatório no checkpoint)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Para rodar sem display


# ── Estilo visual padrão das aulas (Aula 07 usou dark background) ──
CORES_TECNICAS = {
    "zero_shot": "#6c63ff",
    "few_shot": "#00d4aa",
    "chain_of_thought": "#ffd166",
    "role_prompting": "#ff6b6b"
}
CORES_LISTA = list(CORES_TECNICAS.values())


def gerar_tabela(resultados: list, caminho_csv: str = "output/resultados.csv") -> pd.DataFrame:
    """
    Cria DataFrame com pandas e salva como CSV.
    Referência: Aula 08 — padrão de resultados estruturados.

    Args:
        resultados: Lista de dicts com métricas (saída do evaluator)
        caminho_csv: Caminho para salvar o CSV

    Returns:
        DataFrame com todos os resultados
    """
    df = pd.DataFrame(resultados)

    os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
    df.to_csv(caminho_csv, index=False, encoding="utf-8")

    print(f"\n📊 TABELA COMPARATIVA — {len(df)} resultados\n")
    print(f"{'─' * 80}")

    # Agrupa por técnica para mostrar médias (padrão Aula 08 — pivot)
    resumo = df.groupby("tecnica").agg(
        acuracia_media=("acuracia", "mean"),
        tokens_medios=("tokens_total", "mean"),
        tempo_medio_ms=("tempo_ms", "mean")
    ).round(2)

    print(resumo.to_string())
    print(f"{'─' * 80}")
    print(f"\n✅ CSV salvo em: {caminho_csv}")

    return df


def grafico_acuracia(df: pd.DataFrame, caminho: str = "output/graficos/acuracia.png"):
    """
    Gráfico de barras agrupadas: acurácia por técnica e tarefa.
    Referência: Aula 07 — padrão de gráfico com dark background.
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#0d0f1a")
    ax.set_facecolor("#141628")

    # Agrupa por tarefa e técnica
    pivot = df.pivot_table(
        values="acuracia",
        index="tarefa",
        columns="tecnica",
        aggfunc="mean"
    )

    tarefas = pivot.index.tolist()
    tecnicas = pivot.columns.tolist()
    n_tecnicas = len(tecnicas)
    n_tarefas = len(tarefas)

    largura = 0.18
    x = range(n_tarefas)

    for i, tecnica in enumerate(tecnicas):
        valores = [pivot.loc[t, tecnica] if tecnica in pivot.columns else 0 for t in tarefas]
        offset = (i - n_tecnicas / 2) * largura + largura / 2
        cor = CORES_TECNICAS.get(tecnica, CORES_LISTA[i % len(CORES_LISTA)])
        bars = ax.bar(
            [xi + offset for xi in x],
            valores,
            largura,
            label=tecnica.replace("_", " ").title(),
            color=cor,
            alpha=0.85,
            edgecolor="white",
            linewidth=0.5
        )
        # Valor no topo de cada barra
        for bar, val in zip(bars, valores):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    bar.get_height() + 0.02,
                    f"{val:.0%}",
                    ha="center", va="bottom",
                    color="white", fontsize=8
                )

    ax.set_title("Acurácia por Técnica e Tarefa", color="white", fontsize=13, fontweight="bold")
    ax.set_xlabel("Tarefa", color="white", fontsize=11)
    ax.set_ylabel("Acurácia Média", color="white", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.set_xticks(list(x))
    ax.set_xticklabels(tarefas, color="white", rotation=15, fontsize=9)
    ax.tick_params(colors="white")
    ax.legend(facecolor="#1e2035", labelcolor="white", fontsize=9)

    for spine in ax.spines.values():
        spine.set_color("#2a2d4a")

    plt.tight_layout()
    plt.savefig(caminho, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"📈 Gráfico de acurácia salvo em: {caminho}")


def grafico_custo(df: pd.DataFrame, caminho: str = "output/graficos/custo_tokens.png"):
    """
    Gráfico de barras: tokens médios por técnica.
    Mostra o 'custo' de cada abordagem.
    Referência: Aula 07 (comparar custo de geração).
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0d0f1a")
    ax.set_facecolor("#141628")

    resumo = df.groupby("tecnica")["tokens_total"].mean().round(1)
    tecnicas = resumo.index.tolist()
    valores = resumo.values

    cores = [CORES_TECNICAS.get(t, "#ffffff") for t in tecnicas]

    bars = ax.bar(
        [t.replace("_", "\n") for t in tecnicas],
        valores,
        color=cores,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )

    for bar, val in zip(bars, valores):
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            bar.get_height() + 1,
            f"{val:.0f} tok",
            ha="center", va="bottom",
            color="white", fontsize=9, fontweight="bold"
        )

    ax.set_title("Custo em Tokens por Técnica (Média)", color="white", fontsize=13, fontweight="bold")
    ax.set_ylabel("Tokens Totais (prompt + resposta)", color="white", fontsize=11)
    ax.tick_params(colors="white", labelsize=9)

    for spine in ax.spines.values():
        spine.set_color("#2a2d4a")

    plt.tight_layout()
    plt.savefig(caminho, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"📉 Gráfico de custo salvo em: {caminho}")


def grafico_temperatura(
    resultados_temp: dict,
    caminho: str = "output/graficos/temperatura.png"
):
    """
    Gráfico de consistência por temperatura.
    Referência DIRETA: Aula 07 — softmax_com_temperatura e gráfico
    de distribuição de tokens com variação de temperatura.

    Args:
        resultados_temp: Dict {temp_str: {consistencia, tokens_medio, ...}}
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    temperaturas = sorted([float(k) for k in resultados_temp.keys()])
    consistencias = [resultados_temp[str(t)]["consistencia"] for t in temperaturas]
    tokens_medios = [resultados_temp[str(t)]["tokens_medio"] for t in temperaturas]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.patch.set_facecolor("#0d0f1a")

    # ── Subplot 1: Consistência por temperatura ──
    ax1.set_facecolor("#141628")
    bars = ax1.bar(
        [str(t) for t in temperaturas],
        consistencias,
        color=["#6c63ff", "#00d4aa", "#ffd166"],
        alpha=0.85,
        edgecolor="white",
        linewidth=0.5
    )
    for bar, val in zip(bars, consistencias):
        ax1.text(
            bar.get_x() + bar.get_width() / 2.,
            bar.get_height() + 0.02,
            f"{val:.0%}",
            ha="center", va="bottom",
            color="white", fontsize=10, fontweight="bold"
        )
    ax1.set_title("Consistência por Temperatura", color="white", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Temperatura", color="white")
    ax1.set_ylabel("Consistência (%)", color="white")
    ax1.set_ylim(0, 1.2)
    ax1.tick_params(colors="white")
    for spine in ax1.spines.values():
        spine.set_color("#2a2d4a")

    # ── Subplot 2: Tokens médios por temperatura ──
    ax2.set_facecolor("#141628")
    ax2.plot(
        [str(t) for t in temperaturas],
        tokens_medios,
        color="#ff6b6b",
        marker="o",
        linewidth=2,
        markersize=8
    )
    for i, (t, val) in enumerate(zip(temperaturas, tokens_medios)):
        ax2.annotate(
            f"{val:.0f}",
            (str(t), val),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            color="white",
            fontsize=9
        )
    ax2.set_title("Tokens Médios por Temperatura", color="white", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Temperatura", color="white")
    ax2.set_ylabel("Tokens na Resposta", color="white")
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_color("#2a2d4a")

    plt.suptitle(
        "Efeito da Temperatura — Consistência vs Tokens",
        color="white", fontsize=14, fontweight="bold", y=1.02
    )
    plt.tight_layout()
    plt.savefig(caminho, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"🌡️  Gráfico de temperatura salvo em: {caminho}")


def recomendar(df: pd.DataFrame) -> dict:
    """
    Recomenda automaticamente a melhor técnica por tarefa.
    Baseado na maior acurácia média — critério objetivo e simples.

    Returns:
        Dict {tarefa: {melhor_tecnica, acuracia, justificativa}}
    """
    recomendacoes = {}

    justificativas = {
        "zero_shot": "Boa para tarefas simples que o modelo já conhece bem do pré-treinamento.",
        "few_shot": "Excelente quando há padrões específicos do domínio que precisam ser demonstrados.",
        "chain_of_thought": "Melhor para tarefas que exigem raciocínio lógico ou análise em etapas.",
        "role_prompting": "Ideal quando o tom, especialidade ou restrições da persona são determinantes."
    }

    print("\n" + "=" * 60)
    print("🏆 RECOMENDAÇÃO AUTOMÁTICA POR TAREFA")
    print("=" * 60)

    for tarefa in df["tarefa"].unique():
        df_tarefa = df[df["tarefa"] == tarefa]
        melhor = df_tarefa.groupby("tecnica")["acuracia"].mean().idxmax()
        acuracia = df_tarefa.groupby("tecnica")["acuracia"].mean().max()

        recomendacoes[tarefa] = {
            "melhor_tecnica": melhor,
            "acuracia": round(acuracia, 2),
            "justificativa": justificativas.get(melhor, "Melhor desempenho médio.")
        }

        print(f"\n  📌 Tarefa: {tarefa}")
        print(f"  🥇 Melhor técnica: {melhor.replace('_', ' ').upper()}")
        print(f"  📊 Acurácia: {acuracia:.0%}")
        print(f"  💡 Por quê: {justificativas.get(melhor, '')}")

    print("\n" + "=" * 60)
    return recomendacoes
