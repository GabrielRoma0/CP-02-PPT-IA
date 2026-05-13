"""
prompt_builder.py — Montar prompts por anatomia
Referência: Aula 05 — função montar_prompt() do professor
"""


def montar_prompt(
    instrucao: str,
    contexto: str = "",
    input_dados: str = "",
    formato_output: str = "",
    exemplos: list = None
) -> str:
    """
    Monta um prompt estruturado com os 4 componentes da anatomia.
    Baseado EXATAMENTE na função montar_prompt() da Aula 05.

    Args:
        instrucao: O que o modelo deve fazer (obrigatório)
        contexto: Informações de fundo
        input_dados: Dados sobre os quais agir
        formato_output: Como a resposta deve ser formatada
        exemplos: Lista de tuplas (input, output) para few-shot

    Returns:
        String do prompt completo e formatado
    """
    # Validação: instrução não pode estar vazia (Aula 05 — boas práticas)
    if not instrucao:
        raise ValueError("A instrução é obrigatória e não pode estar vazia.")

    partes = []

    if contexto:
        partes.append(f"Contexto: {contexto}")

    partes.append(f"Instrução: {instrucao}")

    if exemplos:
        partes.append("\nExemplos:")
        for i, (inp, out) in enumerate(exemplos, 1):
            partes.append(f"  Exemplo {i}:")
            partes.append(f"    Input: {inp}")
            partes.append(f"    Output: {out}")

    if input_dados:
        partes.append(f"\nInput: {input_dados}")

    if formato_output:
        partes.append(f"\nFormato de saída: {formato_output}")

    return "\n".join(partes)


def adicionar_exemplos(prompt: str, exemplos: list) -> str:
    """
    Adiciona exemplos few-shot a um prompt já montado.
    Referência: Aula 06 — padrão few-shot do professor.

    Args:
        prompt: Prompt base
        exemplos: Lista de dicts com 'input' e 'output'

    Returns:
        Prompt com exemplos no formato Input: ... → Output: ...
    """
    if not exemplos:
        return prompt

    bloco_exemplos = "\nExemplos:\n"
    for ex in exemplos:
        bloco_exemplos += f"Input: \"{ex['input']}\" → Output: \"{ex['output']}\"\n"

    return prompt + bloco_exemplos


def adicionar_cot(prompt: str, passos: list) -> str:
    """
    Adiciona instrução de chain-of-thought a um prompt.
    Referência: Aula 06 — técnica CoT do professor.

    Args:
        prompt: Prompt base
        passos: Lista de strings descrevendo cada passo de raciocínio

    Returns:
        Prompt com instrução de raciocínio passo a passo
    """
    if not passos:
        return prompt + "\n\nVamos pensar passo a passo:"

    instrucao_cot = "\n\nResolva passo a passo:\n"
    for i, passo in enumerate(passos, 1):
        instrucao_cot += f"{i}. {passo}\n"

    instrucao_cot += "\nMostre cada etapa do raciocínio:"

    return prompt + instrucao_cot
