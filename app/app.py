from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Post, create_db_and_table, get_async_session
from app.images import imagekit


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_table()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File(...)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    caption: Annotated[str, Form()] = "",
):
    try:
        file_bytes = await file.read()

        print(
            f"Filename: {file.filename!r}, "
            f"Content-Type: {file.content_type!r}, "
            f"Size received: {len(file_bytes)} bytes, "
            f"Header: {file_bytes[:16].hex(' ')}"
        )

        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty.",
            )

        filename = file.filename or "uploaded_file"

        # Latest ImageKit SDK API
        upload_result = imagekit.files.upload(
            file=file_bytes,
            file_name=filename,
            tags=["backend-upload"],
            use_unique_file_name=True,
        )

        file_url = getattr(upload_result, "url", None)

        print(
            "ImageKit result:",
            {
                "file_id": getattr(upload_result, "file_id", None),
                "name": getattr(upload_result, "name", None),
                "url": file_url,
                "size": getattr(upload_result, "size", None),
            },
        )

        if not file_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="ImageKit upload failed to return a file URL.",
            )

        content_type = file.content_type or ""

        file_type = "video" if content_type.startswith("video/") else "photo"

        post = Post(
            caption=caption,
            url=file_url,
            file_type=file_type,
            file_name=(getattr(upload_result, "name", None) or filename),
        )

        session.add(post)

        await session.commit()
        await session.refresh(post)

        return post

    except HTTPException:
        raise

    except Exception as exc:
        await session.rollback()

        print(f"Upload error: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload processing failed: {exc}",
        ) from exc

    finally:
        await file.close()


@app.get("/feed")
async def get_feed(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    result = await session.execute(select(Post).order_by(Post.id.desc()))

    posts = result.scalars().all()

    return posts
