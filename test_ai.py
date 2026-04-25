import pytest
from ai import analyze_trade


class TestAnalyzeTrade:
    """Testes para a função analyze_trade"""
    
    def test_buy_signal_strong(self):
        """Teste: sinal BUY com score alto"""
        data = {
            "price": 100.0,
            "trend": "up",
            "volume": 2000
        }
        result = analyze_trade(data)
        
        assert result["score"] == 80
        assert result["decision"] == "BUY"
    
    def test_buy_signal_minimal(self):
        """Teste: sinal BUY com score mínimo"""
        data = {
            "price": 50.0,
            "trend": "up",
            "volume": 500
        }
        result = analyze_trade(data)
        
        assert result["score"] == 60
        assert result["decision"] == "BUY"
    
    def test_no_trade_signal(self):
        """Teste: sinal NO TRADE com score baixo"""
        data = {
            "price": 10.0,
            "trend": "down",
            "volume": 100
        }
        result = analyze_trade(data)
        
        assert result["score"] == 40
        assert result["decision"] == "NO TRADE"
    
    def test_high_volume_bonus(self):
        """Teste: bônus de volume alto"""
        data = {
            "price": 100.0,
            "trend": "down",
            "volume": 1500
        }
        result = analyze_trade(data)
        
        # down(30) + high_volume(20) + price(10) = 60
        assert result["score"] == 60
        assert result["decision"] == "BUY"
    
    def test_zero_price(self):
        """Teste: preço zero não adiciona pontos"""
        data = {
            "price": 0,
            "trend": "up",
            "volume": 1500
        }
        result = analyze_trade(data)
        
        # up(50) + high_volume(20) = 70
        assert result["score"] == 70
        assert result["decision"] == "BUY"
    
    def test_missing_fields(self):
        """Teste: campos ausentes usam valores padrão"""
        data = {}
        result = analyze_trade(data)
        
        # No trend, no volume > 1000, no price > 0
        assert result["score"] == 0
        assert result["decision"] == "NO TRADE"
    
    def test_trend_up_score(self):
        """Teste: tendência UP adiciona 50 pontos"""
        data = {
            "price": 1,
            "trend": "up",
            "volume": 100
        }
        result = analyze_trade(data)
        
        # up(50) + price(10) = 60
        assert result["score"] == 60
    
    def test_trend_down_score(self):
        """Teste: tendência DOWN adiciona 30 pontos"""
        data = {
            "price": 1,
            "trend": "down",
            "volume": 100
        }
        result = analyze_trade(data)
        
        # down(30) + price(10) = 40
        assert result["score"] == 40
