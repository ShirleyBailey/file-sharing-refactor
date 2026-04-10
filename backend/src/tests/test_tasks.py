import io
import pytest

from src.tasks import _scan_file_for_threats, _extract_file_metadata, _send_file_alert
from src.service import get_file, create_alert
import src.service as service_module


@pytest.mark.asyncio
async def test_scan_clean_file(client, tmp_path):
    upload = await client.post(
        "/files",
        data={"title": "Clean"},
        files={"file": ("clean.txt", io.BytesIO(b"safe content"), "text/plain")},
    )
    file_id = upload.json()["id"]

    await _scan_file_for_threats(file_id)

    file_item = await get_file(file_id)
    assert file_item.scan_status == "clean"
    assert file_item.requires_attention is False


@pytest.mark.asyncio
async def test_scan_suspicious_extension(client):
    upload = await client.post(
        "/files",
        data={"title": "Suspicious"},
        files={"file": ("virus.exe", io.BytesIO(b"MZ"), "application/octet-stream")},
    )
    file_id = upload.json()["id"]

    await _scan_file_for_threats(file_id)

    file_item = await get_file(file_id)
    assert file_item.scan_status == "suspicious"
    assert file_item.requires_attention is True
    assert ".exe" in file_item.scan_details


@pytest.mark.asyncio
async def test_extract_metadata_text(client, tmp_path):
    content = b"line1\nline2\nline3"
    upload = await client.post(
        "/files",
        data={"title": "Text"},
        files={"file": ("text.txt", io.BytesIO(content), "text/plain")},
    )
    file_id = upload.json()["id"]

    await _scan_file_for_threats(file_id)
    await _extract_file_metadata(file_id)

    file_item = await get_file(file_id)
    assert file_item.processing_status == "processed"
    assert file_item.metadata_json is not None
    assert file_item.metadata_json["line_count"] == 3


@pytest.mark.asyncio
async def test_extract_metadata_missing_file(client, tmp_path, monkeypatch):
    upload = await client.post(
        "/files",
        data={"title": "Ghost"},
        files={"file": ("ghost.txt", io.BytesIO(b"data"), "text/plain")},
    )
    file_id = upload.json()["id"]

    # Remove the stored file to simulate missing file
    import os
    for f in tmp_path.iterdir():
        os.remove(f)

    await _extract_file_metadata(file_id)

    file_item = await get_file(file_id)
    assert file_item.processing_status == "failed"


@pytest.mark.asyncio
async def test_send_alert_for_clean_file(client):
    upload = await client.post(
        "/files",
        data={"title": "Alert Clean"},
        files={"file": ("ok.txt", io.BytesIO(b"ok"), "text/plain")},
    )
    file_id = upload.json()["id"]

    await _scan_file_for_threats(file_id)
    await _extract_file_metadata(file_id)
    await _send_file_alert(file_id)

    alerts_response = await client.get("/alerts")
    items = alerts_response.json()["items"]
    assert any(a["file_id"] == file_id and a["level"] == "info" for a in items)
