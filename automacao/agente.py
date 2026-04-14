import json
import httpx
import os
from datetime import datetime
from pathlib import Path

API_BASE = "http://localhost:8000" #padrao do meu pc
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = BASE_DIR / "data"
JSON_PATH = JSON_DIR / "alertas.json"

GEMINI_API_KEY = "SUA_CHAVE_API" #use uma chave de api do google gemini pra usar.


def buscar_inativos() -> list[dict]:
    response = httpx.get(f"{API_BASE}/membros/inativos") #requisicao get buscando membros inativos
    response.raise_for_status() #nao deixa ele inicializar sem a api estar ligada
    return response.json()

def gerar_mensagem(membro: dict) -> str:
    tipo = membro["tipo_inatividade"]
    nome = membro["nome"]
    dias_presenca = membro["dias_sem_presenca"]
    dias_dizimo = membro["dias_sem_dizimo"]

    contextos = {
        "presenca": f"o membro está ausente dos cultos há {dias_presenca} dias, mas ainda contribui com dízimo",
        "dizimo": f"o membro esta presente na igreja, mas sem registro de dízimo há {dias_dizimo} dias",
        "ambos": f"o membro esta ausente dos cultos há {dias_presenca} dias e sem dízimo há {dias_dizimo} dias",
    }

    contexto = contextos.get(tipo, "inativo recentemente")

    prompt = f"""Você é um pastor evangélico muito acolhedor e se preocupa genuinamente com cada membro da sua congregação.
    Sua tarefa é escrever uma mensagem de WhatsApp para {nome}.
    O contexto atual dessa pessoa é: {contexto}.

    DIRETRIZES ESTRITAS:
    - Tom: Caloroso, pastoral e humano. Nunca seja cobrativo, burocrático ou formal demais.
    - Pessoalidade: Mencione o nome da pessoa naturalmente no texto.
    - Regra de Presença: Se o contexto indicar ausência nos cultos, demonstre saudade e pergunte com carinho se está tudo bem com ela e sua família.
    - Regra de Dízimo: Se o contexto indicar ausência apenas de dízimo/ofertas, NUNCA mencione dinheiro, finanças ou dízimo diretamente. Fale apenas sobre a importância da participação dela na comunidade e na obra.
    - Regra de Ambos: Se faltarem ambos, priorize 100% o cuidado humano e espiritual, esquecendo a parte financeira.
    - Formato: Máximo de 3 parágrafos curtos. Use linguagem natural de WhatsApp.
    - Emojis: Use no máximo 1 ou 2 emojis adequados (ex: 🙏, 🙌, 💙).
    - Limite: Não invente informações sobre a pessoa ou eventos da igreja.

    Responda APENAS com o texto da mensagem final, sem saudações externas, aspas ou explicações adicionais."""
    #esse ai foi o prompt q eu criei pra gerar para cada membro inativo
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        
        if response.status_code != 200:
            print(f" resposta de erro do google: {response.text}")
            response.raise_for_status()
            
        dados = response.json()
        texto_final = dados["candidates"][0]["content"]["parts"][0]["text"]
        return texto_final.strip()
        
    except Exception as e:
        print(f"Erro ao consultar IA para {nome}: {e}")
        return f"Olá {nome}, sentimos sua falta! Como você e sua família estão? "

def salvar_alertas(alertas: list[dict]) -> None:
    os.makedirs(JSON_DIR, exist_ok=True)
    existentes = []
    if JSON_PATH.is_file():
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                conteudo = f.read()
                if conteudo.strip(): #garante q n ta vazio
                    existentes = json.loads(conteudo)
        except Exception as e:
            print(f"Aviso ao ler JSON antigo: {e}. Criando novo.")

    existentes.extend(alertas)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existentes, f, indent=2, ensure_ascii=False) #garante os acentos corretos e nao ficakr esstranho


def rodar_agente() -> None:
    print("buscando membros inativos...")
    inativos = buscar_inativos()

    if not inativos:
        print("nenuhm membro encontrado")
        return

    print(f" existem {len(inativos)} membro(s) inativo(s) encontrado(s)\n")

    alertas_gerados = []

    for membro in inativos:
        print(f"gernando mensagem para {membro['nome']} ({membro['tipo_inatividade']})...")
        mensagem = gerar_mensagem(membro)

        alerta = {
            "membro_id": membro["id"],
            "nome": membro["nome"],
            "telefone": membro["telefone"],
            "tipo_inatividade": membro["tipo_inatividade"],
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat(),
        }

        alertas_gerados.append(alerta)
        print(f"{mensagem[:80]}...\n")

    salvar_alertas(alertas_gerados)
    print(f"{len(alertas_gerados)} alerta(s) salvos em alertas.json")

if __name__ == "__main__":
    rodar_agente()
