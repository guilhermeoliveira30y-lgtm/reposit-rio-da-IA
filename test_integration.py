import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestMainEndpoints:
    """Testes para os endpoints da API FastAPI"""
    
    def test_home_endpoint(self):
        """Teste: GET / retorna status da API"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"status": "IA trader online"}
    
    def test_analyze_endpoint_buy_signal(self):
        """Teste: POST /analyze retorna BUY com dados válidos"""
        data = {
            "price": 100.0,
            "trend": "up",
            "volume": 2000
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["score"] == 80
        assert result["decision"] == "BUY"
    
    def test_analyze_endpoint_no_trade(self):
        """Teste: POST /analyze retorna NO TRADE com dados baixos"""
        data = {
            "price": 10.0,
            "trend": "down",
            "volume": 100
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["score"] == 40
        assert result["decision"] == "NO TRADE"
    
    def test_analyze_endpoint_empty_data(self):
        """Teste: POST /analyze com dados vazios"""
        data = {}
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["score"] == 0
        assert result["decision"] == "NO TRADE"
    
    def test_analyze_endpoint_partial_data(self):
        """Teste: POST /analyze com dados parciais"""
        data = {"trend": "up"}
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["decision"] == "BUY"
        assert result["score"] >= 50
    
    def test_analyze_endpoint_high_volume(self):
        """Teste: POST /analyze com volume alto"""
        data = {
            "price": 50.0,
            "trend": "up",
            "volume": 1500
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        # up(50) + high_volume(20) + price(10) = 80
        assert result["score"] == 80
        assert result["decision"] == "BUY"
    
    def test_analyze_endpoint_trend_down(self):
        """Teste: POST /analyze com tendência DOWN"""
        data = {
            "price": 100.0,
            "trend": "down",
            "volume": 1500
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        # down(30) + high_volume(20) + price(10) = 60
        assert result["score"] == 60
        assert result["decision"] == "BUY"
    
    def test_analyze_endpoint_minimal_buy(self):
        """Teste: POST /analyze com score exatamente 60 (BUY mínimo)"""
        data = {
            "price": 50.0,
            "trend": "up",
            "volume": 500
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["score"] == 60
        assert result["decision"] == "BUY"
    
    def test_analyze_endpoint_just_below_buy(self):
        """Teste: POST /analyze com score 59 (NO TRADE)"""
        data = {
            "price": 49.0,
            "trend": "up",
            "volume": 500
        }
        response = client.post("/analyze", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["score"] == 59
        assert result["decision"] == "NO TRADE"


class TestIntegration:
    """Testes de integração da aplicação completa"""
    
    def test_api_health_check(self):
        """Teste: API está respondendo"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_full_workflow_good_trade(self):
        """Teste: workflow completo para um bom trade"""
        # 1. Verificar se API está online
        health = client.get("/")
        assert health.status_code == 200
        
        # 2. Analisar dados favoráveis
        trade_data = {
            "price": 150.0,
            "trend": "up",
            "volume": 2500
        }
        analysis = client.post("/analyze", json=trade_data)
        assert analysis.status_code == 200
        assert analysis.json()["decision"] == "BUY"
    
    def test_full_workflow_bad_trade(self):
        """Teste: workflow completo para um trade ruim"""
        # 1. Verificar se API está online
        health = client.get("/")
        assert health.status_code == 200
        
        # 2. Analisar dados desfavoráveis
        trade_data = {
            "price": 5.0,
            "trend": "down",
            "volume": 50
        }
        analysis = client.post("/analyze", json=trade_data)
        assert analysis.status_code == 200
        assert analysis.json()["decision"] == "NO TRADE"
