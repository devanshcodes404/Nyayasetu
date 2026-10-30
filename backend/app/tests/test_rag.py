from app.services.ai.factory import get_ai_provider
from app.services.ai.mock_provider import MockAIProvider


def test_ai_provider_factory_and_mock(client, auth_headers):
    provider = get_ai_provider()
    assert isinstance(provider, MockAIProvider)

    # Test research endpoint returning Part 2 readiness response
    resp = client.post(
        "/api/v1/research/ask",
        json={"query": "What are the rules regarding floor tests in Maharashtra Assembly?", "scope": "all"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "reserved_for_part_2"
    assert "MockAIProvider" in data["provider"]

