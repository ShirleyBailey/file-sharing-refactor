from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette import status

from src.schemas import AlertItem, FileItem, FileUpdate, PagedResponse
from src.service import (
    STORAGE_DIR,
    create_file,
    delete_file,
    get_file,
    list_alerts,
    list_files,
    update_file,
)
from src.tasks import scan_file_for_threats

app = FastAPI(title="File Exchange API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/files", response_model=PagedResponse[FileItem])
async def list_files_view(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return await list_files(page=page, page_size=page_size)


@app.get("/alerts", response_model=PagedResponse[AlertItem])
async def list_alerts_view(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return await list_alerts(page=page, page_size=page_size)


@app.post("/files", response_model=FileItem, status_code=201)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
):
    file_item = await create_file(title=title, upload_file=file)
    scan_file_for_threats.delay(file_item.id)
    return file_item


@app.get("/files/{file_id}", response_model=FileItem)
async def get_file_view(file_id: str):
    return await get_file(file_id)


@app.patch("/files/{file_id}", response_model=FileItem)
async def update_file_view(file_id: str, payload: FileUpdate):
    return await update_file(file_id=file_id, title=payload.title)


@app.get("/files/{file_id}/download")
async def download_file(file_id: str):
    file_item = await get_file(file_id)
    stored_path = STORAGE_DIR / file_item.stored_name
    if not stored_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )


@app.delete("/files/{file_id}", status_code=204)
async def delete_file_view(file_id: str):
    await delete_file(file_id)
