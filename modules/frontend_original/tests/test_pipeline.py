from providers.climate_provider import load_mock_satellite_data, REGIONS, CATEGORIES
from pipelines.risk_pipeline import calculate_risk_score, filter_data, summarize_metrics, recommended_action


def test_pipeline_generates_expected_columns():
    raw = load_mock_satellite_data(seed=1, days=10)
    df = calculate_risk_score(raw)
    assert "risco_score" in df.columns
    assert "nivel_risco" in df.columns
    assert len(df) == 10 * len(REGIONS)


def test_filters_and_metrics_work():
    df = calculate_risk_score(load_mock_satellite_data(seed=2, days=10))
    start = df["data"].min().date()
    end = df["data"].max().date()
    filtered = filter_data(df, start, end, [REGIONS[0]], CATEGORIES, 0)
    assert set(filtered["regiao"].unique()) == {REGIONS[0]}
    metrics = summarize_metrics(filtered)
    assert metrics["focos_calor"] >= 0
    assert isinstance(recommended_action(filtered), str)
