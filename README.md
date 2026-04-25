# IA Trader API

API FastAPI para análise de trades com inteligência artificial.

## Funcionalidades

- ✅ Análise automática de tendências de mercado
- ✅ Scoring inteligente baseado em múltiplos parâmetros
- ✅ Decisões de compra em tempo real

## Instalação

```bash
pip install -r requirements.txt
```

## Como usar

### 1. Iniciar o servidor

```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

### 2. Endpoints disponíveis

#### GET /
Status da API

```bash
curl http://localhost:8000/
```

Resposta:
```json
{
  "status": "IA trader online"
}
```

#### POST /analyze
Analisa dados de trade e retorna uma decisão

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "price": 150.50,
    "trend": "up",
    "volume": 1500
  }'
```

**Parâmetros:**
- `price` (float): Preço atual do ativo
- `trend` (string): Tendência do mercado ("up" ou "down")
- `volume` (int): Volume de negociação

**Resposta:**
```json
{
  "score": 80,
  "decision": "BUY"
}
```

## Lógica de Scoring

- **Tendência UP**: +50 pontos
- **Tendência DOWN**: +30 pontos
- **Volume > 1000**: +20 pontos
- **Preço > 0**: +10 pontos

**Decisão:**
- Score >= 60: **BUY**
- Score < 60: **NO TRADE**

## Documentação Interativa

Acesse a documentação automática em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Licença

MIT
