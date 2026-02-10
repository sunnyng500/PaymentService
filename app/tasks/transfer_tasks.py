from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_transfer import TransferRepository


class BatchTransferTask:
    def __init__(self, session: AsyncSession = Depends()):
        self.repo = TransferRepository(session)
    async def run_batch_process(self,transfer_data:list):

        await self.repo.batch_transfer(transfer_data)

