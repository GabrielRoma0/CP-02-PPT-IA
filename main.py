"""
main.py — Ponto de entrada do Prompt Toolkit
Executa o fluxo completo: inputs → techniques → evaluator → report

Referências:
- Aula 05: montar_prompt, anatomia do prompt
- Aula 06: Zero-Shot, Few-Shot, Chain-of-Thought
- Aula 07: Role Prompting, personas, temperatura
- Aula 08: tarefas específicas (classificação, extração, sumarização)

Uso: python main.py
"""

import json
import os
import sys
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa os módulos do projeto
from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TAREFAS, listar_tarefas, obter_tarefa
from src.evaluator import avaliar_resultado, testar_temperatura, contar_tokens
from src.report import (
    gerar_tabela,
    grafico_acuracia,
    grafico_custo,
    grafico_temperatura,
    recomendar
)


# ============================================================
# Funções auxiliares — padrão de print das aulas
# ============================================================

def separador(char="=", tamanho=60):
    print(char * tamanho)


def titulo(texto):
    separador()
    print(f"  {texto}")
    separador()


def carregar_dados(caminho: str) -> dict:
    """Carrega arquivo JSON — padrão das aulas."""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# Fluxo Principal
# ============================================================

def main():
    titulo("🐍 PROMPT TOOLKIT — Checkpoint 02 · FIAP 2026")
    print("  Domínio: Atendimento ao Cliente (e-commerce)")
    print("  Técnicas: Zero-Shot · Few-Shot · CoT · Role Prompting")
    print("  Tarefas: Classificação · Extração · Sumarização\n")

    # ── 1. Carregar configurações ──
    print("📁 Carregando configurações...\n")

    inputs = carregar_dados("data/inputs.json")
    exemplos_db = carregar_dados("data/examples.json")
    personas_db = carregar_dados("prompts/system_prompts.json")

    client = LLMClient()
    todos_resultados = []

    # ── 2. Para cada TAREFA ──
    for nome_tarefa in listar_tarefas():
        tarefa = obter_tarefa(nome_tarefa)
        inputs_tarefa = inputs[nome_tarefa]
        exemplos = exemplos_db.get(nome_tarefa, [])
        persona_key = tarefa["persona"]
        persona = personas_db[persona_key]

        titulo(f"📌 TAREFA: {nome_tarefa.upper().replace('_', ' ')}")
        print(f"  Tipo: {tarefa['tipo']}")
        print(f"  Inputs: {len(inputs_tarefa)} | Exemplos few-shot: {len(exemplos)}\n")

        # ── 3. Para cada input × cada técnica ──
        for item in inputs_tarefa:
            input_texto = item["input"]
            esperado = item["esperado"]

            print(f"  📩 Input: \"{input_texto[:60]}...\"")

            # ── Técnica 1: Zero-Shot (Aula 06) ──
            prompt_zs = zero_shot(tarefa, input_texto)
            resultado_zs = client.chat(prompt_zs, temperature=0.3, max_tokens=200)
            r_zs = avaliar_resultado(
                tecnica="zero_shot",
                tarefa=nome_tarefa,
                prompt=prompt_zs,
                resposta=resultado_zs["resposta"],
                esperado=esperado,
                tokens_prompt=resultado_zs["tokens_prompt"],
                tokens_resposta=resultado_zs["tokens_resposta"],
                tempo_ms=resultado_zs["tempo_ms"]
            )
            todos_resultados.append(r_zs)
            print(f"    0️⃣  Zero-Shot:        acurácia={r_zs['acuracia']:.0%} | tokens={r_zs['tokens_total']}")

            # ── Técnica 2: Few-Shot (Aula 06) ──
            prompt_fs = few_shot(tarefa, input_texto, exemplos)
            resultado_fs = client.chat(prompt_fs, temperature=0.3, max_tokens=200)
            r_fs = avaliar_resultado(
                tecnica="few_shot",
                tarefa=nome_tarefa,
                prompt=prompt_fs,
                resposta=resultado_fs["resposta"],
                esperado=esperado,
                tokens_prompt=resultado_fs["tokens_prompt"],
                tokens_resposta=resultado_fs["tokens_resposta"],
                tempo_ms=resultado_fs["tempo_ms"]
            )
            todos_resultados.append(r_fs)
            print(f"    📋 Few-Shot:         acurácia={r_fs['acuracia']:.0%} | tokens={r_fs['tokens_total']}")

            # ── Técnica 3: Chain-of-Thought (Aula 06) ──
            passos = tarefa["passos_cot"]
            prompt_cot = chain_of_thought(tarefa, input_texto, passos)
            resultado_cot = client.chat(prompt_cot, temperature=0.5, max_tokens=300)
            r_cot = avaliar_resultado(
                tecnica="chain_of_thought",
                tarefa=nome_tarefa,
                prompt=prompt_cot,
                resposta=resultado_cot["resposta"],
                esperado=esperado,
                tokens_prompt=resultado_cot["tokens_prompt"],
                tokens_resposta=resultado_cot["tokens_resposta"],
                tempo_ms=resultado_cot["tempo_ms"]
            )
            todos_resultados.append(r_cot)
            print(f"    🔗 Chain-of-Thought: acurácia={r_cot['acuracia']:.0%} | tokens={r_cot['tokens_total']}")

            # ── Técnica 4: Role Prompting (Aula 07) ──
            system_prompt, user_prompt = role_prompting(tarefa, input_texto, persona)
            resultado_role = client.chat(
                user_prompt,
                system=system_prompt,
                temperature=persona["temperatura"],
                max_tokens=persona["max_tokens"]
            )
            r_role = avaliar_resultado(
                tecnica="role_prompting",
                tarefa=nome_tarefa,
                prompt=user_prompt,
                resposta=resultado_role["resposta"],
                esperado=esperado,
                tokens_prompt=resultado_role["tokens_prompt"],
                tokens_resposta=resultado_role["tokens_resposta"],
                tempo_ms=resultado_role["tempo_ms"]
            )
            todos_resultados.append(r_role)
            print(f"    🎭 Role Prompting:   acurácia={r_role['acuracia']:.0%} | tokens={r_role['tokens_total']}")
            print()

    # ── 4. Gerar relatório ──
    titulo("📊 GERANDO RELATÓRIO COMPARATIVO")

    df = gerar_tabela(todos_resultados)
    grafico_acuracia(df)
    grafico_custo(df)
    recomendacoes = recomendar(df)

    # ── 5. Teste de temperatura no melhor prompt ──
    titulo("🌡️  TESTE DE TEMPERATURA (Aula 07)")
    print("  Testando o prompt de classificação de sentimento")
    print("  com temperaturas: 0.1, 0.5, 1.0 (3 repetições cada)\n")

    tarefa_temp = obter_tarefa("classificacao_sentimento")
    input_temp = "Produto excelente, chegou antes do prazo! Recomendo a todos."
    prompt_temp = zero_shot(tarefa_temp, input_temp)

    resultados_temp = testar_temperatura(
        prompt=prompt_temp,
        temps=[0.1, 0.5, 1.0],
        client=client,
        repeticoes=3
    )

    grafico_temperatura(resultados_temp)

    # ── Resumo final ──
    separador()
    print("\n✅ EXECUÇÃO CONCLUÍDA!\n")
    print("📁 Arquivos gerados:")
    print("   output/resultados.csv")
    print("   output/graficos/acuracia.png")
    print("   output/graficos/custo_tokens.png")
    print("   output/graficos/temperatura.png")
    separador()


if __name__ == "__main__":
    main()
