import io
import pytest


@pytest.mark.asyncio
async def test_list_files_empty(client):
    response = await client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1


@pytest.mark.asyncio
async def test_upload_and_list_file(client):
    file_content = b"hello world"
    response = await client.post(
        "/files",
        data={"title": "Test File"},
        files={"file": ("test.txt", io.BytesIO(file_content), "text/plain")},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test File"
    assert data["original_name"] == "test.txt"
    assert data["size"] == len(file_content)
    assert data["processing_status"] == "uploaded"

    list_response = await client.get("/files")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1


@pytest.mark.asyncio
async def test_upload_empty_file_returns_400(client):
    response = await client.post(
        "/files",
        data={"title": "Empty"},
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_file(client):
    response = await client.post(
        "/files",
        data={"title": "My Doc"},
        files={"file": ("doc.txt", io.BytesIO(b"content"), "text/plain")},
    )
    file_id = response.json()["id"]

    get_response = await client.get(f"/files/{file_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == file_id


@pytest.mark.asyncio
async def test_get_file_not_found(client):
    response = await client.get("/files/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_file_title(client):
    response = await client.post(
        "/files",
        data={"title": "Old Title"},
        files={"file": ("f.txt", io.BytesIO(b"data"), "text/plain")},
    )
    file_id = response.json()["id"]

    patch_response = await client.patch(f"/files/{file_id}", json={"title": "New Title"})
    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_file(client):
    response = await client.post(
        "/files",
        data={"title": "To Delete"},
        files={"file": ("del.txt", io.BytesIO(b"bye"), "text/plain")},
    )
    file_id = response.json()["id"]

    del_response = await client.delete(f"/files/{file_id}")
    assert del_response.status_code == 204

    get_response = await client.get(f"/files/{file_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_pagination(client):
    for i in range(5):
        await client.post(
            "/files",
            data={"title": f"File {i}"},
            files={"file": (f"f{i}.txt", io.BytesIO(b"x"), "text/plain")},
        )

    page1 = await client.get("/files?page=1&page_size=3")
    assert page1.status_code == 200
    data = page1.json()
    assert data["total"] == 5
    assert len(data["items"]) == 3
    assert data["page"] == 1

    page2 = await client.get("/files?page=2&page_size=3")
    data2 = page2.json()
    assert len(data2["items"]) == 2
    assert data2["page"] == 2
