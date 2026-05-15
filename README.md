# Prompt Toolkit — Checkpoint 02

**Disciplina:** Prompt Engineering and Artificial Intelligence  
**Instituição:** FIAP — Ciência da Computação · 2026  
**Módulo 2 — Aulas 05 a 08**  
**Domínio:** Atendimento ao Cliente (e-commerce)

---
##  Participantes

| Nome                     | RM     |
|--------------------------|--------|
| Fernando Hideki Rosa Oda | 571408 |
| Gabriel Botelho Romão    | 570589 |
| Léo Moreno Sambo         | 569556 |
| Thor Ferreira Camargo    | 569543 |

---

##  O que é este projeto?

Toolkit Python que aplica automaticamente as **4 técnicas de prompting** a qualquer tarefa de negócio, compara resultados e recomenda a melhor abordagem.

**Técnicas implementadas:**
- 0️⃣ **Zero-Shot** — sem exemplos (Aula 06)
- 📋 **Few-Shot** — com exemplos no formato `Input → Output` (Aula 06)
- 🔗 **Chain-of-Thought** — raciocínio passo a passo (Aula 06)
- 🎭 **Role Prompting** — personas com system prompt detalhado (Aula 07)

**Tarefas do domínio:**
1. Classificação de Sentimento (Aula 08)
2. Extração de Dados de Reclamações (Aula 08)
3. Sumarização de Reviews (Aula 08)

---

##  Stack

| Componente | Tecnologia |
|-----------|-----------|
| Linguagem | Python 3.10+ |
| LLM | Ollama API — `gpt-oss:120b` |
| Tokens | tiktoken |
| Visualização | matplotlib + pandas |
| Ambiente | venv + pip |

---

##  Como instalar e executar

### 1. Clone o projeto
### 1.1. Entre no diretório do trabalho
```bash
cd prompt-toolkit
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute o toolkit

```bash
python main.py
```

---

##  Estrutura do Projeto

```
prompt-toolkit/
├── README.md
├── requirements.txt
├── .env
├── main.py                    # Ponto de entrada
├── src/
│   ├── __init__.py
│   ├── llm_client.py          # Conexão com Ollama API (Aula 05)
│   ├── prompt_builder.py      # Anatomia do prompt (Aula 05)
│   ├── techniques.py          # 4 técnicas: ZS, FS, CoT, Role (Aulas 06+07)
│   ├── tasks.py               # 3 tarefas do domínio (Aula 08)
│   ├── evaluator.py           # Métricas: tokens, acurácia, consistência
│   └── report.py              # Tabela CSV + 3 gráficos
├── data/
│   ├── inputs.json            # 5+ inputs reais por tarefa
│   └── examples.json          # Exemplos para few-shot
├── prompts/
│   ├── system_prompts.json    # 3 personas detalhadas (Aula 07)
│   └── templates.json         # Templates por tarefa
├── output/
│   ├── resultados.csv
│   └── graficos/
└── docs/
    └── CP02_NomeDoGrupo.pdf
```

---

##  Saídas geradas

| Arquivo | Descrição |
|---------|-----------|
| `output/resultados.csv` | Tabela com acurácia, tokens e tempo por técnica × input |
| `output/graficos/acuracia.png` | Barras agrupadas: acurácia por técnica e tarefa |
| `output/graficos/custo_tokens.png` | Tokens médios por técnica |
| `output/graficos/temperatura.png` | Consistência e tokens por temperatura (0.1, 0.5, 1.0) |

---

## Personas (Aula 07)

| Persona | Nome | Tarefa | Temperatura |
|---------|------|--------|-------------|
| `analista_cx` | Ana | Classificação de Sentimento | 0.3 |
| `especialista_suporte` | Max | Extração de Dados | 0.3 |
| `analista_produto` | Carol | Sumarização de Reviews | 0.5 |

---

## Referências das Aulas

- **Aula 05** — Anatomia do prompt (`prompt_builder.py`)
- **Aula 06** — Zero-Shot, Few-Shot, Chain-of-Thought (`techniques.py`)
- **Aula 07** — Role Prompting, temperaturas (`techniques.py`, `evaluator.py`)
- **Aula 08** — Tarefas específicas: classificação, extração, sumarização (`tasks.py`)
