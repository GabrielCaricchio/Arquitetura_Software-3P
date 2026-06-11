import json
import re
import requests


def _fallback_story(profile: dict) -> dict:
    """História local de reserva caso a API falhe ou a chave não exista."""
    name = profile.get("name", "Aluno")
    favorite_story = profile.get("favorite_story", "livros mágicos")
    favorite_activity = profile.get("favorite_activity", "desenhar")
    reading_level = profile.get("reading_level", "iniciante")

    title = f"A Aventura de {name} e o Livro Estrelado"
    content = (
        f"{name} acordou em um hospital cheio de estrelas brilhantes. "
        f"Lá, encontrou um livro mágico que mudava de cor conforme o nível de leitura: {reading_level}. "
        f"No primeiro capítulo, o livro contou uma história parecida com {favorite_story}. "
        f"Depois, {name} descobriu uma sala de atividades onde podia {favorite_activity}. "
        f"Cada página mostrava que aprender também pode ser uma aventura gentil, divertida e cheia de coragem."
    )

    challenges = [
        {
            "question": f"Qual foi o livro ou tema favorito que apareceu na história de {name}?",
            "answer": favorite_story,
        },
        {
            "question": f"O que {name} gostou de fazer na sala de atividades?",
            "answer": favorite_activity,
        },
        {
            "question": f"Como a leitura foi apresentada na história?",
            "answer": reading_level,
        },
    ]
    return {"title": title, "content": content, "challenges": challenges}


def _extract_json(text: str):
    """Tenta extrair um JSON mesmo quando a IA devolve texto extra."""
    if not text:
        return None

    # Primeiro tenta achar um bloco JSON direto.
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        raw = match.group(0)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    return None


def generate_story(profile: dict, api_key: str, model: str, base_url: str) -> dict:
    """Gera história e 3 perguntas usando OpenRouter.

    Se a API não responder, o sistema continua funcionando com uma versão local.
    """
    fallback = _fallback_story(profile)

    if not api_key:
        return fallback

    prompt = f"""
Crie uma história curta e acolhedora para alfabetização hospitalar em português do Brasil.
Retorne APENAS JSON válido no formato:
{{
  "title": "título",
  "content": "história em texto corrido",
  "challenges": [
    {{"question": "pergunta 1", "answer": "resposta 1"}},
    {{"question": "pergunta 2", "answer": "resposta 2"}},
    {{"question": "pergunta 3", "answer": "resposta 3"}}
  ]
}}

Dados do aluno:
Nome: {profile.get("name")}
Idade: {profile.get("age")}
Obra favorita: {profile.get("favorite_story")}
Atividade favorita: {profile.get("favorite_activity")}
Nível de leitura: {profile.get("reading_level")}

A história deve ser simples, mágica, positiva e apropriada para crianças.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Trilhas Mágicas",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Você responde somente com JSON válido."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()

        parsed = None
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = _extract_json(text)

        if not parsed:
            return fallback

        title = parsed.get("title") or fallback["title"]
        content = parsed.get("content") or fallback["content"]
        challenges = parsed.get("challenges") or fallback["challenges"]

        normalized = []
        for challenge in challenges[:3]:
            normalized.append(
                {
                    "question": challenge.get("question", "Pergunta sem texto."),
                    "answer": challenge.get("answer", "Resposta não informada."),
                }
            )

        while len(normalized) < 3:
            normalized.append(fallback["challenges"][len(normalized)])

        return {"title": title, "content": content, "challenges": normalized}

    except Exception:
        return fallback
