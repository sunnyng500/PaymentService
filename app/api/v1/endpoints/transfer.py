from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas import TransferSchema

router = APIRouter()
@router.post("/transfer/immediate")
async def transfer_immediate(payload: TransferSchema, db: AsyncSession = Depends(get_db)):
    pass
@router.post("/transfer/batch",status_code=200)
async def create_batch():
    pass