"""
tasks.py — Tarefas do domínio: classificação, extração, sumarização
Referência: Aula 08 — Prompts para Tarefas Específicas
Domínio escolhido: Atendimento ao Cliente (e-commerce)
"""

# ============================================================
# Definição das 3 tarefas do domínio
# Padrão da Aula 08: cada tarefa é um dict com todos os campos
# ============================================================

TAREFAS = {

    # ── TAREFA 1: Classificação de Sentimento ──
    # Referência: Aula 08 — Classificação Multi-Classe
    "classificacao_sentimento": {
        "nome": "classificacao_sentimento",
        "tipo": "classificacao",
        "instrucao": (
            "Classifique o sentimento do texto como "
            "POSITIVO, NEGATIVO, NEUTRO ou MISTO."
        ),
        "formato_output": (
            "Responda APENAS com:\n"
            "Sentimento: [POSITIVO/NEGATIVO/NEUTRO/MISTO]\n"
            "Confiança: [Alta/Média/Baixa]\n"
            "Justificativa: [1 frase]"
        ),
        # Exemplos para few-shot (Aula 06)
        "exemplos_fewshot": [
            {
                "input": "Produto excelente, chegou antes do prazo!",
                "output": "Sentimento: POSITIVO\nConfiança: Alta\nJustificativa: Elogio claro ao produto e à entrega."
            },
            {
                "input": "Veio quebrado e o suporte não respondeu.",
                "output": "Sentimento: NEGATIVO\nConfiança: Alta\nJustificativa: Problemas com produto e atendimento."
            },
            {
                "input": "O produto chegou no prazo mas embalagem estava amassada.",
                "output": "Sentimento: MISTO\nConfiança: Média\nJustificativa: Aspecto positivo e negativo simultâneos."
            },
        ],
        # Passos para CoT (Aula 06)
        "passos_cot": [
            "Identifique palavras e expressões positivas no texto",
            "Identifique palavras e expressões negativas no texto",
            "Compare o peso de cada lado",
            "Classifique o sentimento predominante",
        ],
        # Persona para role prompting (Aula 07)
        "persona": "analista_cx",
    },

    # ── TAREFA 2: Extração de Dados Estruturados ──
    # Referência: Aula 08 — Extração de Entidades
    "extracao_dados": {
        "nome": "extracao_dados",
        "tipo": "extracao",
        "instrucao": (
            "Extraia as informações estruturadas do texto de reclamação abaixo. "
            "Identifique: produto, problema relatado, urgência e pedido do cliente."
        ),
        "formato_output": (
            "Responda em formato estruturado:\n"
            "Produto: [nome do produto]\n"
            "Problema: [descrição do problema]\n"
            "Urgência: [ALTA/MÉDIA/BAIXA]\n"
            "Pedido: [o que o cliente quer]"
        ),
        # Exemplos para few-shot (Aula 06)
        "exemplos_fewshot": [
            {
                "input": "Meu notebook Dell comprado há 2 dias parou de carregar. Preciso para o trabalho urgente!",
                "output": "Produto: Notebook Dell\nProblema: Não carrega\nUrgência: ALTA\nPedido: Troca ou reparo urgente"
            },
            {
                "input": "A camiseta tamanho M que comprei veio com costura solta. Gostaria de trocar.",
                "output": "Produto: Camiseta M\nProblema: Costura solta\nUrgência: BAIXA\nPedido: Troca do produto"
            },
        ],
        # Passos para CoT (Aula 06)
        "passos_cot": [
            "Identifique o produto mencionado no texto",
            "Descreva o problema relatado pelo cliente",
            "Avalie o nível de urgência baseado nas palavras usadas",
            "Identifique o que o cliente está pedindo",
        ],
        # Persona para role prompting (Aula 07)
        "persona": "especialista_suporte",
    },

    # ── TAREFA 3: Sumarização de Reviews ──
    # Referência: Aula 08 — Sumarização
    "sumarizacao_review": {
        "nome": "sumarizacao_review",
        "tipo": "sumarizacao",
        "instrucao": (
            "Resuma o review do cliente em exatamente 2 frases curtas. "
            "Mantenha apenas os fatos mais importantes para a equipe de produto."
        ),
        "formato_output": (
            "Resumo:\n"
            "1. [Primeira frase — aspecto principal]\n"
            "2. [Segunda frase — recomendação ou crítica central]"
        ),
        # Exemplos para few-shot (Aula 06)
        "exemplos_fewshot": [
            {
                "input": (
                    "Comprei o fone de ouvido bluetooth há uma semana. "
                    "O som é incrível, grave potente, mas o conforto deixa a desejar "
                    "depois de 2 horas de uso. A bateria dura bem, uns 20 horas. "
                    "Vale o preço, mas poderia ter almofadas melhores."
                ),
                "output": (
                    "1. Fone com excelente qualidade sonora e bateria duradoura (20h).\n"
                    "2. Conforto é o ponto fraco; almofadas precisam de melhoria."
                )
            },
            {
                "input": (
                    "Produto chegou rápido, em 2 dias. A embalagem estava perfeita. "
                    "Só que o produto em si não funciona como descrito no anúncio. "
                    "O filtro de água não filtra partículas menores que 5 microns como prometido."
                ),
                "output": (
                    "1. Entrega rápida e embalagem preservada, sem danos.\n"
                    "2. Produto não cumpre especificação técnica anunciada (filtragem abaixo do prometido)."
                )
            },
        ],
        # Passos para CoT (Aula 06)
        "passos_cot": [
            "Identifique o aspecto mais positivo mencionado",
            "Identifique o aspecto mais negativo ou crítica principal",
            "Formule frase 1 com o ponto principal do review",
            "Formule frase 2 com a recomendação ou crítica central",
        ],
        # Persona para role prompting (Aula 07)
        "persona": "analista_produto",
    },
}


def listar_tarefas() -> list:
    """Retorna lista com os nomes das tarefas disponíveis."""
    return list(TAREFAS.keys())


def obter_tarefa(nome: str) -> dict:
    """Retorna o dict de uma tarefa pelo nome."""
    if nome not in TAREFAS:
        raise ValueError(f"Tarefa '{nome}' não encontrada. Disponíveis: {listar_tarefas()}")
    return TAREFAS[nome]
