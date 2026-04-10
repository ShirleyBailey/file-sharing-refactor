import io
import pytest

from src.service import create_alert


@pytest.mark.asyncio
async def test_list_alerts_empty(client):
    response = await client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_alerts_pagination(client):
    # Upload a file to get a valid file_id
    upload = await client.post(
        "/files",
        data={"title": "Alert Test"},
        files={"file": ("a.txt", io.BytesIO(b"data"), "text/plain")},
    )
    file_id = upload.json()["id"]

    for i in range(5):
        await create_alert(file_id=file_id, level="info", message=f"Alert {i}")

    page1 = await client.get("/alerts?page=1&page_size=3")
    assert page1.status_code == 200
    data = page1.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3

    page2 = await client.get("/alerts?page=2&page_size=3")
    assert len(page2.json()["items"]) == 2


@pytest.mark.asyncio
async def test_alert_levels(client):
    upload = await client.post(
        "/files",
        data={"title": "Level Test"},
        files={"file": ("b.txt", io.BytesIO(b"data"), "text/plain")},
    )
    file_id = upload.json()["id"]

    await create_alert(file_id=file_id, level="critical", message="Critical issue")
    await create_alert(file_id=file_id, level="warning", message="Warning issue")
    await create_alert(file_id=file_id, level="info", message="All good")

    response = await client.get("/alerts")
    items = response.json()["items"]
    levels = {item["level"] for item in items}
    assert levels == {"critical", "warning", "info"}
