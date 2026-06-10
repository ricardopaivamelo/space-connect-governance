from __future__ import annotations
import pandas as pd
import numpy as np

REGIONS = ["Amazônia", "Cerrado", "Pantanal", "Mata Atlântica", "Caatinga"]
CATEGORIES = ["Queimada", "Seca", "Enchente", "Baixa criticidade"]


def load_mock_satellite_data(seed: int = 42, days: int = 90) -> pd.DataFrame:
    """Simula dados satelitais/climáticos para dashboard de risco ambiental."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="D")
    rows = []
    for date in dates:
        for region in REGIONS:
            temp = rng.normal(30, 4)
            rain = max(0, rng.gamma(2.0, 8.0) - rng.uniform(0, 6))
            humidity = np.clip(rng.normal(58, 18), 15, 98)
            ndvi = np.clip(rng.normal(0.52, 0.18), 0.05, 0.90)
            wind = max(0, rng.normal(18, 7))
            population = int(rng.integers(25_000, 600_000))
            fire_hotspots = max(0, int(rng.poisson(max(1, temp - humidity / 3 + wind / 4))))
            flood_index = max(0, rain * 0.8 + (humidity - 70) * 0.3)
            drought_index = max(0, temp * 1.4 + wind * 0.7 - rain * 1.1 - humidity * 0.4)
            if fire_hotspots > 22 or drought_index > 35:
                category = "Queimada" if fire_hotspots >= drought_index / 2 else "Seca"
            elif flood_index > 28:
                category = "Enchente"
            else:
                category = "Baixa criticidade"
            rows.append({
                "data": date,
                "regiao": region,
                "temperatura_c": round(float(temp), 1),
                "chuva_mm": round(float(rain), 1),
                "umidade_pct": round(float(humidity), 1),
                "ndvi": round(float(ndvi), 2),
                "vento_kmh": round(float(wind), 1),
                "focos_calor": fire_hotspots,
                "indice_enchente": round(float(flood_index), 1),
                "indice_seca": round(float(drought_index), 1),
                "populacao_exposta": population,
                "categoria": category,
            })
    return pd.DataFrame(rows)
