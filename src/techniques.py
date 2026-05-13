"""
techniques.py — 4 técnicas de prompting: ZS, FS, CoT, Role
Referência: Aula 06 (Zero-Shot, Few-Shot, CoT) + Aula 07 (Role Prompting)
"""

import json
import os
from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot


def zero_shot(tarefa: dict, input_dados: str) -> str:
    """
    Monta prompt Zero-Shot — sem exemplos.
    Referência: Aula 06 — 'O modelo resolve sem exemplos'.

    Args:
        tarefa: dict com campos nome, instrucao, formato_output
        input_dados: texto de entrada

    Returns:
        Prompt montado via prompt_builder (Aula 05)
    """
    # Padrão da Aula 06: instrução clara + formato de saída definido
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        input_dados=input_dados,
        formato_output=tarefa["formato_output"]
    )
    return prompt


def few_shot(tarefa: dict, input_dados: str, exemplos: list) -> str:
    """
    Monta prompt Few-Shot com exemplos no formato Input: ... → Output: ...
    Referência: Aula 06 — 'Fornecer K exemplos para guiar o modelo'.

    Args:
        tarefa: dict com campos nome, instrucao, formato_output
        input_dados: texto de entrada
        exemplos: lista de dicts com 'input' e 'output'

    Returns:
        Prompt montado com exemplos
    """
    # Converte exemplos para o formato de tuplas usado na Aula 05
    exemplos_tuplas = [(ex["input"], ex["output"]) for ex in exemplos]

    # Monta com a função da Aula 05
    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        input_dados=input_dados,
        formato_output=tarefa["formato_output"],
        exemplos=exemplos_tuplas
    )
    return prompt


def chain_of_thought(tarefa: dict, input_dados: str, passos: list) -> str:
    """
    Monta prompt com Chain-of-Thought (raciocínio passo a passo).
    Referência: Aula 06 — 'O modelo pensa antes de responder'.

    Args:
        tarefa: dict com campos nome, instrucao, formato_output
        input_dados: texto de entrada
        passos: lista de strings com passos do raciocínio

    Returns:
        Prompt com instrução de CoT
    """
    # Monta prompt base (Aula 05)
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        input_dados=input_dados,
        formato_output=tarefa["formato_output"]
    )

    # Adiciona CoT (Aula 06)
    prompt_cot = adicionar_cot(prompt_base, passos)
    return prompt_cot


def role_prompting(tarefa: dict, input_dados: str, persona: dict) -> tuple:
    """
    Monta prompt com Role Prompting usando persona detalhada.
    Referência: Aula 07 — 'System Prompts e Personas'.

    Args:
        tarefa: dict com campos nome, instrucao, formato_output
        input_dados: texto de entrada
        persona: dict com 'system_prompt', 'temperatura', 'max_tokens'

    Returns:
        Tupla (system_prompt, user_prompt) — padrão da Aula 07
    """
    system = persona["system_prompt"]

    # User prompt com a tarefa (padrão Aula 07)
    user_prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        input_dados=input_dados,
        formato_output=tarefa["formato_output"]
    )

    return (system, user_prompt)


def carregar_personas(caminho: str = "prompts/system_prompts.json") -> dict:
    """Carrega personas do arquivo JSON — padrão de dados das aulas."""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_exemplos(caminho: str = "data/examples.json") -> dict:
    """Carrega exemplos few-shot do arquivo JSON."""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
