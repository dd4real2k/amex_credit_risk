from src.predict import score_to_risk_band

def test_risk_band_low():
    assert score_to_risk_band(0.1) == "Low"

def test_risk_band_medium():
    assert score_to_risk_band(0.4) == "Medium"

def test_risk_band_high():
    assert score_to_risk_band(0.7) == "High"

def test_risk_band_critical():
    assert score_to_risk_band(0.9) == "Critical"
