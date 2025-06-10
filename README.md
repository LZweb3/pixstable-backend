# Backend API - KYC/KYB PixStable

Este backend em Flask serve para receber dados dos formulários de KYC e KYB e gerenciar clientes.

## Endpoints da API

- `POST /submit_kyc` → Recebe dados de formulário KYC + arquivos
- `POST /submit_kyb` → Recebe dados de formulário KYB + arquivos
- `GET /clients` → Retorna lista de clientes
- `GET /client/<id>` → Retorna detalhes de um cliente + URLs dos documentos
- `POST /client/<id>/status` → Aprova/Reprova um cliente

## Deploy recomendado

1. Suba esta pasta `/backend/` em um repositório no GitHub
2. Conecte seu GitHub no [Render.com](https://render.com) ou [Railway.app](https://railway.app)
3. Configure o deploy como Web Service com:

```
Start command: gunicorn app:app
```

**OU**:

Para testes locais:

```bash
pip install -r requirements.txt
python app.py
```

## Estrutura de arquivos

- `/uploads/` → onde ficam os documentos enviados
- `database.db` → banco de dados SQLite gerado automaticamente