import json
from groq import Groq

def process_text_with_llm(text, api_key):
    """
    Envia o texto para a API da Groq utilizando o modelo gpt-oss-120b.
    """
    client = Groq(api_key=api_key)

    prompt = f"""
    Você é um assistente especialista em extração de dados corporativos.
    Analise o texto fornecido e extraia as seguintes informações em formato JSON rigoroso:
    
    1. "cliente": Nome da empresa ou cliente citado (se não houver, coloque "Não Identificado").
    2. "categoria": Categoria do serviço/ocorrência (ex: "Suporte TI", "Desenvolvimento", "Consultoria IA", "Infraestrutura", "Outros").
    3. "valor": Valor monetário estimado envolvido (número float, ex: 1500.00). Se não informado, retorne 0.0.
    4. "status": Status do chamado ("Pendente", "Em Andamento", "Concluído").
    5. "urgencia": Nível de urgência ("Baixa", "Média", "Alta").
    6. "resumo": Um resumo executivo de 1 frase do problema ou atividade.

    Responda APENAS o objeto JSON puro. Não adicione marcações Markdown como ```json ou textos explicativos fora do objeto JSON.

    Texto para análise:
    \"\"\"{text}\"\"\"
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_completion_tokens=2048,
            top_p=1,
            stream=False  # Desativado para receber a resposta completa de uma vez
        )

        # Captura o texto retornado
        raw_content = completion.choices[0].message.content

        if not raw_content or not raw_content.strip():
            raise Exception("O modelo retornou uma resposta vazia.")

        raw_content = raw_content.strip()

        # Limpeza caso o modelo retorne blocos de código markdown (```json ... ```)
        if raw_content.startswith("```"):
            raw_content = raw_content.split("\n", 1)[1]
            if raw_content.endswith("```"):
                raw_content = raw_content.rsplit("\n", 1)[0]

        return json.loads(raw_content)

    except json.JSONDecodeError as e:
        raise Exception(f"Falha ao converter resposta em JSON: {e} | Conteúdo bruto: '{raw_content}'")
    except Exception as e:
        raise Exception(f"Erro na API da Groq (openai/gpt-oss-120b): {e}")