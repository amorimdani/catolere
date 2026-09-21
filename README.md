# Catolê Colorir — Gerador de Páginas de Colorir com Fundo Transparente

Aplicação web completa e autônoma para gerar páginas de colorir infantis de Santos Católicos e Figuras Bíblicas com fundo 100% transparente (canal alfa), sem dependência de APIs comerciais externas.

## Arquitetura
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React, JSZip.
- **Backend**: Python FastAPI, Hugging Face Diffusers (`stabilityai/sdxl-turbo`), `rembg` (remoção de fundo para canal alfa), PIL.
- **Variações**: Loop com 5 seeds aleatórias e variações contextuais dinâmicas (`praying`, `walking`, `smiling`, `helping`, `teaching`).

---

## Como Executar Localmente

### 1. Backend (FastAPI)

1. Abra um terminal na pasta `backend`:
   ```bash
   cd backend
   ```

2. Crie e ative um ambiente virtual Python (recomendado):
   ```bash
   python -m venv venv
   # No Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   > **Nota de GPU (Opcional)**: Se possuir GPU NVIDIA com CUDA, instale a versão compatível do PyTorch:
   > `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121`

4. Inicie o servidor FastAPI:
   ```bash
   python main.py
   # Ou via uvicorn:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   O backend estará rodando em: `http://localhost:8000` (Documentação Swagger em `http://localhost:8000/docs`).

---

### 2. Frontend (React + Vite)

1. Abra outro terminal na pasta `frontend`:
   ```bash
   cd frontend
   ```

2. Instale os pacotes npm (caso ainda não tenha instalado):
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
   Acesse a interface no navegador em: `http://localhost:5173`.

---

## Funcionalidades
- **Grid com 5 Ilustrações Simultâneas**: Geração simultânea de 5 variantes exclusivas para cada Santo/Personagem Bíblico.
- **Fundo 100% Transparente**: Traços pretos limpos com remoção de fundo por IA via `rembg`, visualizáveis sobre padrão xadrez.
- **Download Individual & ZIP**: Botão 'Baixar PNG' individual para cada uma das 5 imagens e botão global 'Baixar Todas (ZIP)'.
