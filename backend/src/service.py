import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select

from src.database import async_session_maker
from src.models import Alert, StoredFile
from src.schemas import PagedResponse

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage" / "files"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


async def list_files(page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> PagedResponse[StoredFile]:
    page_size = min(page_size, MAX_PAGE_SIZE)
    offset = (page - 1) * page_size
    async with async_session_maker() as session:
        total = (await session.execute(select(func.count()).select_from(StoredFile))).scalar_one()
        result = await session.execute(
            select(StoredFile).order_by(StoredFile.created_at.desc()).offset(offset).limit(page_size)
        )
        items = list(result.scalars().all())
    return PagedResponse(items=items, total=total, page=page, page_size=page_size)


async def list_alerts(page: int = 1, page_size: int = DEFAULT_PAGE_SIZE) -> PagedResponse[Alert]:
    page_size = min(page_size, MAX_PAGE_SIZE)
    offset = (page - 1) * page_size
    async with async_session_maker() as session:
        total = (await session.execute(select(func.count()).select_from(Alert))).scalar_one()
        result = await session.execute(
            select(Alert).order_by(Alert.created_at.desc()).offset(offset).limit(page_size)
        )
        items = list(result.scalars().all())
    return PagedResponse(items=items, total=total, page=page, page_size=page_size)


async def get_file(file_id: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return file_item


async def create_file(title: str, upload_file: UploadFile) -> StoredFile:
    content = await upload_file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    file_id = str(uuid4())
    suffix = Path(upload_file.filename or "").suffix
    stored_name = f"{file_id}{suffix}"
    stored_path = STORAGE_DIR / stored_name
    stored_path.write_bytes(content)

    file_item = StoredFile(
        id=file_id,
        title=title,
        original_name=upload_file.filename or stored_name,
        stored_name=stored_name,
        mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
        size=len(content),
        processing_status="uploaded",
    )
    async with async_session_maker() as session:
        session.add(file_item)
        await session.commit()
        await session.refresh(file_item)
    return file_item


async def update_file(file_id: str, title: str) -> StoredFile:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        file_item.title = title
        await session.commit()
        await session.refresh(file_item)
        return file_item


async def delete_file(file_id: str) -> None:
    async with async_session_maker() as session:
        file_item = await session.get(StoredFile, file_id)
        if not file_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        stored_path = STORAGE_DIR / file_item.stored_name
        if stored_path.exists():
            stored_path.unlink()
        await session.delete(file_item)
        await session.commit()


async def create_alert(file_id: str, level: str, message: str) -> Alert:
    alert = Alert(file_id=file_id, level=level, message=message)
    async with async_session_maker() as session:
        session.add(alert)
        await session.commit()
        await session.refresh(alert)
        return alert
