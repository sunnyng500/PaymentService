from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert
from ..models import Account
from ..db.session import get_async_db

class TransferRepository:
    def __init__(self,db:AsyncSession = Depends(get_async_db)):
        self.db = db
    #realtime
    async def create_realtime_transfer(self,send_id:int,receiver_id:int,amount:float):
        async with self.db.begin() as session:
         sender_statement = (
             select(Account).where(Account.id == send_id).with_for_update()
         )
         result = session.execute(sender_statement)
         sender_account = result.scalar_one_or_none()



    async def batch_transfer(self,receiver_ids:list[dict]):
        """
               高吞吐量寫入優化
               """
        if not transfers:
            return

        # 使用 insert().values() 是 SQLAlchemy 異步寫入最快的方式
        stmt = insert(Transfer).values(transfers)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_stauts(self):
        pass
