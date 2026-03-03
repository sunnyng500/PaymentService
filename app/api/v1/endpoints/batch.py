from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import BatchRequest
from app.db import session
from ...crud import crud_transfer

router = APIRouter()


@router.post("/batch-transfer", status_code=202)
async def create_batch_transfer(
        payload: BatchRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(session.get_async_db)
):
    # 1. 寫入資料庫：狀態設為 PENDING (快速寫入，不做實際轉賬)
    batch_id = await crud_transfer.batch_transfer(db, payload)

    # 2. 丟背景處理 (或是推送到 Celery 佇列)
    background_tasks.add_task(process_batch_transfer_job, batch_id)

    # 3. 立即回傳，不讓客戶端等待
    return {"batch_id": batch_id, "message": "Batch processing started"}