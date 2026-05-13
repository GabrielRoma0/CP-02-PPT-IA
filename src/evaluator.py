"""
evaluator.py — Medir qualidade, tokens, consistência e temperatura
Referência: Aula 07 (temperatura) + requisitos do Checkpoint 02
"""

import time
from src.llm_client import LLMClient


def contar_tokens(texto: str) -> int:
    """
    Conta tokens usando tiktoken — requisito obrigatório do checkpoint.
    Referência: Aula 05 (tiktoken mencionado na stack obrigatória).
    """
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(texto))
    except Exception:
        # Fallback: aproximação por palavras
        return len(texto.split())


def medir_acuracia(resposta: str, esperado: str) -> float:
    """
    Mede acurácia por match exato ou por keywords.
    Retorna float entre 0.0 e 1.0.

    Referência: Aula 08 — comparar classificações com output esperado.
    """
    if not resposta or not esperado:
        return 0.0

    resposta_lower = resposta.lower().strip()
    esperado_lower = esperado.lower().strip()

    # Match exato
    if esperado_lower in resposta_lower:
        return 1.0

    # Match por keywords (para tarefas de extração)
    keywords = esperado_lower.split()
    matches = sum(1 for kw in keywords if kw in resposta_lower)
    if len(keywords) > 0:
        return round(matches / len(keywords), 2)

    return 0.0


def medir_consistencia(respostas: list) -> float:
    """
    Mede consistência: mesma pergunta N vezes → percentual de respostas iguais.
    Referência: Aula 06 — Bônus Self-Consistency (CoT 3 vezes + votação).

    Args:
        respostas: lista de strings com N respostas para o mesmo prompt

    Returns:
        Float entre 0.0 e 1.0 (1.0 = todas iguais)
    """
    if len(respostas) <= 1:
        return 1.0

    # Normaliza respostas para comparação
    normalizadas = [r.lower().strip() for r in respostas]

    # Conta a resposta mais frequente
    contagem = {}
    for r in normalizadas:
        contagem[r] = contagem.get(r, 0) + 1

    mais_frequente = max(contagem.values())
    return round(mais_frequente / len(respostas), 2)


def testar_temperatura(prompt: str, temps: list, client: LLMClient, repeticoes: int = 3) -> dict:
    """
    Roda o mesmo prompt com temperaturas diferentes e mede consistência.
    Referência: Aula 07 — 'Para uma mesma persona, varie a temperatura
    (0.1, 0.5, 0.9) e observe as diferenças'.

    Args:
        prompt: Prompt a testar
        temps: Lista de temperaturas, ex: [0.1, 0.5, 1.0]
        client: Instância do LLMClient
        repeticoes: Quantas vezes rodar cada temperatura

    Returns:
        Dict com resultados por temperatura
    """
    resultados = {}

    for temp in temps:
        respostas = []
        tokens_lista = []
        tempos_lista = []

        for _ in range(repeticoes):
            resultado = client.chat(prompt, temperature=temp, max_tokens=100)
            respostas.append(resultado["resposta"])
            tokens_lista.append(resultado["tokens_resposta"])
            tempos_lista.append(resultado["tempo_ms"])

        consistencia = medir_consistencia(respostas)
        tokens_medio = round(sum(tokens_lista) / len(tokens_lista), 1)
        tempo_medio = round(sum(tempos_lista) / len(tempos_lista), 1)

        resultados[str(temp)] = {
            "temperatura": temp,
            "consistencia": consistencia,
            "tokens_medio": tokens_medio,
            "tempo_medio_ms": tempo_medio,
            "respostas": respostas
        }

    return resultados


def avaliar_resultado(
    tecnica: str,
    tarefa: str,
    prompt: str,
    resposta: str,
    esperado: str,
    tokens_prompt: int,
    tokens_resposta: int,
    tempo_ms: int
) -> dict:
    """
    Consolida métricas de um resultado em um dict padronizado.
    Usado para montar o DataFrame do report.
    """
    acuracia = medir_acuracia(resposta, esperado)
    tokens_total = tokens_prompt + tokens_resposta

    return {
        "tecnica": tecnica,
        "tarefa": tarefa,
        "acuracia": acuracia,
        "tokens_prompt": tokens_prompt,
        "tokens_resposta": tokens_resposta,
        "tokens_total": tokens_total,
        "tempo_ms": tempo_ms,
        "resposta_resumida": resposta[:80].replace("\n", " "),
        "esperado": esperado
    }
