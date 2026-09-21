import io
import os
import random
import base64
import zipfile
import logging
import re
import unicodedata
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image

from vector_engine import render_detailed_coloring_page, analyze_figure_identity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("catolere-backend")

app = FastAPI(
    title="Gerador de Páginas de Colorir Católicas e Bíblicas",
    description="API autônoma para geração de páginas de colorir com traços pretos e fundo 100% transparente."
)

# CORS liberado para o Frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    name: str

class ImageResult(BaseModel):
    id: int
    figure_id: str
    figure_name: str
    saint_code: str
    seed: int
    situation: str
    prompt: str
    image_base64: str

class GenerateResponse(BaseModel):
    figure: str
    figure_id: str
    figure_title: str
    images: List[ImageResult]

class ZipItem(BaseModel):
    filename: str
    image_base64: str

class ZipRequest(BaseModel):
    figure_name: str
    images: List[ZipItem]

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "device": "cpu",
        "engine": "Autonomous Sacred Line-Art Vector Generator (Strict Safe-Bounds 100% Alpha)",
        "rembg_ready": True
    }

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)

def generate_dynamic_profile(figure_name: str) -> dict:
    """Gera metadados contextuais, situações e prefixos fiéis ao nome buscado."""
    meta = analyze_figure_identity(figure_name)
    clean_slug = slugify(figure_name)
    
    # Prefixo de identificador baseado no nome
    words = [w for w in re.split(r'[\s_]+', clean_slug) if w not in ['de', 'do', 'da', 'dos', 'das', 'e', 'o', 'a']]
    if len(words) >= 2:
        prefix = f"{words[0][:4].upper()}-{words[1][:4].upper()}"
    elif len(words) == 1:
        prefix = words[0][:7].upper()
    else:
        prefix = "SANTO"

    # Contextualização das 5 cenas baseada na persona
    if meta["is_michael"]:
        title = f"{figure_name} — Defensor Celestial e Príncipe da Milícia Divina"
        situations = [
            f"Em adoração celestial diante do trono de Deus com asas majestosas e mãos postas",
            f"Caminhando triunfante sobre as nuvens celestes com a lança da luz divina",
            f"Sorrindo com serenidade e coragem, trazendo a bênção e o amparo dos Céus",
            f"Defendendo os fiéis e vencendo as trevas com seu escudo da verdade e espada sagrada",
            f"Proclamando 'Quem como Deus?' e sustentando a balança da justiça divina"
        ]
    elif meta["is_angel"]:
        title = f"{figure_name} — Mensageiro e Guardião Celestial"
        situations = [
            f"Em oração reverente e louvor com asas abertas iluminadas pela graça divina",
            f"Caminhando pelos céus em missão sagrada guiando os passos dos fiéis",
            f"Sorrindo com ternura angélica e transmitindo a bênção da paz aos corações",
            f"Acolhendo e protegendo as famílias sob suas asas luminosas",
            f"Ensinando os caminhos da fé com o sagrado pergaminho dos Céus"
        ]
    elif meta["is_warrior"]:
        title = f"{figure_name} — Guerreiro da Fé e Soldado de Cristo"
        situations = [
            f"Em oração fervorosa buscando a fortaleza de Deus antes da batalha da vida",
            f"Caminhando com coragem e determinação empunhando o estandarte da vitória",
            f"Sorrindo com paz no coração ao abençoar os devotos",
            f"Vencendo os obstáculos com o escudo da esperança e a espada da justiça",
            f"Ensinando a perseverança e fidelidade com a palavra de Deus"
        ]
    elif meta["is_francis"]:
        title = f"{figure_name} — Exemplo de Humildade, Paz e Amor à Criação"
        situations = [
            f"Rezando em profunda união com Deus com um passarinho pousado no ombro e mãos postas",
            f"Caminhando pacificamente pelo bosque com seu cajado entre os animais da floresta",
            f"Sorrindo com afeto fraternal e abençoando toda a criação com a pomba da paz",
            f"Ajudando os necessitados partilhando o pão com generosidade e compaixão",
            f"Pregando e ensinando o Cântico das Criaturas aos pássaros e irmãos da natureza"
        ]
    elif meta["is_mary"]:
        title = f"{figure_name} — Mãe de Misericórdia e Rainha Celestial"
        situations = [
            f"Rezando em recolhimento sobre nuvens suaves com coroa de doze estrelas e Santo Terço",
            f"Caminhando suavemente pelo caminho de lírios e rosas abençoando os fiéis",
            f"Sorrindo com amor maternal acolhedor trazendo consolo aos corações",
            f"Acolhendo e protegendo os filhos e famílias sob as dobras de seu manto sagrado",
            f"Ensinando a oração e a pureza de coração através do Santo Rosário"
        ]
    elif meta["is_teresa"]:
        title = f"{figure_name} — Apóstola da Caridade e Exemplo de Amor ao Próximo"
        situations = [
            f"Em oração silenciosa e profunda entrega segurando a cruz de Cristo",
            f"Caminhando com simplicidade e humildade levando a luz da esperança",
            f"Sorrindo com ternura infinita: 'A paz começa com um sorriso acolhedor'",
            f"Ajudando com amor incondicional alimentando e cuidando dos necessitados",
            f"Ensinando que pequenas coisas feitas com imenso amor transformam o mundo"
        ]
    elif meta["is_joseph"]:
        title = f"{figure_name} — Patrono das Famílias e Protetor do Menino Jesus"
        situations = [
            f"Em oração vigilante agradecendo a Deus a bênção do lar e da família",
            f"Caminhando com seu cajado que floresce lírios guiando o pequeno Jesus",
            f"Sorrindo com amor paterno enquanto o Menino Jesus abençoa a todos",
            f"Trabalhando com dedicação e retidão na oficina de carpintaria de Nazaré",
            f"Ensinando com paciência e sabedoria os preceitos sagrados da vida"
        ]
    elif meta["is_jesus"]:
        title = f"{figure_name} — O Bom Pastor e Luz do Mundo"
        situations = [
            f"Em comunhão e oração ao Pai Celestial sob o céu estrelado de Getsêmani",
            f"Caminhando como Bom Pastor pelos campos verdes carregando a ovelhinha nos ombros",
            f"Sorrindo com amor divino infinito acolhendo as criancinhas nos braços",
            f"Ajudando a multidão com compaixão e multiplicando os pães e peixes",
            f"Pregando o Sermão da Montanha e ensinando as Bem-Aventuranças com as Escrituras"
        ]
    elif meta["is_peter"]:
        title = f"{figure_name} — Apóstolo da Fé e Pescador de Homens"
        situations = [
            f"Em oração fervorosa agradecendo a graça e a misericórdia de Deus",
            f"Caminhando com passos de fé e coragem sobre as águas na missão apostólica",
            f"Sorrindo com alegria fraterna ao abençoar a comunidade reunida",
            f"Ajudando na pesca milagrosa e partilhando o alimento com o povo",
            f"Ensinando o Santo Evangelho com as Sagradas Chaves do Reino dos Céus"
        ]
    elif meta["is_moses"]:
        title = f"{figure_name} — Profeta da Aliança e Libertador Bíblico"
        situations = [
            f"Em oração no cume do Monte Sinai envolvido pela glória radiante de Deus",
            f"Caminhando com seu cajado milagroso guiando o povo em liberdade",
            f"Sorrindo com serenidade paternal ao abençoar as famílias da congregação",
            f"Fazendo brotar água pura da rocha para saciar o povo no deserto",
            f"Proclamando e ensinando com autoridade as Sagradas Tábuas dos Dez Mandamentos"
        ]
    else:
        title = f"{figure_name} — Testemunho Vivo de Fé e Devoção Sagrada"
        situations = [
            f"Em oração fervorosa e recolhimento diante da presença sagrada de Deus",
            f"Caminhando com passos serenos e firmes na peregrinação da vida",
            f"Sorrindo com bondade e transmitindo a bênção e a paz divina a todos",
            f"Ajudando com amor e generosidade os irmãos e necessitados da comunidade",
            f"Ensinando e testemunhando a sabedoria das Sagradas Escrituras"
        ]

    return {
        "id": clean_slug,
        "name": figure_name,
        "title": title,
        "prefix": prefix,
        "situations": situations
    }

@app.post("/api/generate", response_model=GenerateResponse)
def generate_coloring_pages(req: GenerateRequest):
    figure_name = req.name.strip()
    if not figure_name:
        raise HTTPException(status_code=400, detail="O nome da figura/santo é obrigatório.")

    profile = generate_dynamic_profile(figure_name)
    results: List[ImageResult] = []

    for i in range(5):
        seed = random.randint(100000, 999999)
        situation = profile["situations"][i]
        saint_code = f"{profile['prefix']}-{(i+1):02d}"
        
        prompt = (
            f"Coloring book page for kids, thick uniform black outlines, 2D vector style, "
            f"{figure_name} {situation}, centered composition, zero edge cropping, 100% transparent background."
        )
        
        logger.info(f"Gerando arte vetorial padronizada: {profile['name']} [{saint_code}] | Cena #{i+1}")
        
        # Gera arte vetorial com auto-padding garantido de 70px e fundo 100% alfa
        transparent_img = render_detailed_coloring_page(figure_name, i, seed)
        
        # Converte para PNG Base64
        buffered = io.BytesIO()
        transparent_img.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64_str}"
        
        results.append(
            ImageResult(
                id=i + 1,
                figure_id=profile["id"],
                figure_name=figure_name,
                saint_code=saint_code,
                seed=seed,
                situation=situation,
                prompt=prompt,
                image_base64=data_uri
            )
        )

    return GenerateResponse(
        figure=figure_name,
        figure_id=profile["id"],
        figure_title=profile["title"],
        images=results
    )

@app.post("/api/download-zip")
def download_zip(payload: ZipRequest):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, item in enumerate(payload.images, start=1):
            raw_b64 = item.image_base64
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            img_data = base64.b64decode(raw_b64)
            
            clean_filename = f"{slugify(payload.figure_name)}_variacao_{idx}.png"
            zip_file.writestr(clean_filename, img_data)
            
    zip_buffer.seek(0)
    filename = f"paginas_colorir_{slugify(payload.figure_name)}.zip"
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
