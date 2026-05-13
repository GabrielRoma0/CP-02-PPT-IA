"""
llm_client.py — Conexão com Ollama API
Referência: Aula 05 — padrão do professor (Client + chat)
"""

import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama.com")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
MODEL_NAME = "gpt-oss:120b"


class LLMClient:
    """
    Classe para conectar com a API do Ollama.
    Baseada no padrão do professor nas Aulas 05, 06, 07 e 08.
    """

    def __init__(self):
        # Padrão de autenticação da Aula 05
        self.host = OLLAMA_HOST
        self.api_key = OLLAMA_API_KEY
        self.model = MODEL_NAME

    def chat(self, prompt: str, system: str = "", temperature: float = 0.3, max_tokens: int = 300) -> dict:
        """
        Envia um prompt para o LLM e retorna resposta + métricas.
        Retorna dict com: resposta, tokens_prompt, tokens_resposta, tempo_ms
        Baseado no padrão de chamada das Aulas 05, 06, 07 e 08.
        """
        # Monta o conteúdo da mensagem (Aula 07 — system prompt como prefixo)
        if system:
            conteudo = f"{system}\n\nUser: {prompt}\nAssistant:"
        else:
            conteudo = prompt

        inicio = time.time()

        # Tentativa com retry (tratamento de erros — requisito do checkpoint)
        for tentativa in range(3):
            try:
                # Chamada REST direta (padrão das aulas)
                url = f"{self.host}/api/chat"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": conteudo}],
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "stop": ["User:", "\n\n\n"]
                    },
                    "stream": False
                }

                response = requests.post(url, json=payload, headers=headers, timeout=60)
                response.raise_for_status()
                dados = response.json()

                fim = time.time()
                tempo_ms = int((fim - inicio) * 1000)

                resposta_texto = dados.get("message", {}).get("content", "").strip()

                # Contar tokens via tiktoken (requisito do evaluator)
                tokens_prompt = self._contar_tokens(conteudo)
                tokens_resposta = self._contar_tokens(resposta_texto)

                return {
                    "resposta": resposta_texto,
                    "tokens_prompt": tokens_prompt,
                    "tokens_resposta": tokens_resposta,
                    "tempo_ms": tempo_ms
                }

            except requests.exceptions.Timeout:
                print(f"  ⚠️ Timeout na tentativa {tentativa + 1}/3...")
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️ Erro de conexão: {e}")
                time.sleep(2)
            except Exception as e:
                return {
                    "resposta": f"⚠️ {e}",
                    "tokens_prompt": 0,
                    "tokens_resposta": 0,
                    "tempo_ms": 0
                }

        return {
            "resposta": "⚠️ Falha após 3 tentativas",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": 0
        }

    def _contar_tokens(self, texto: str) -> int:
        """Conta tokens via tiktoken — requisito do evaluator.py"""
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(texto))
        except Exception:
            # Fallback simples se tiktoken falhar
            return len(texto.split())
