from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.repositories import TransactionRepository

from app.db.session import get_async_db
from ..models import Account
from ..models.Transaction import Transaction


async def process_batch_transfer_job(batch_id: str):
    async with get_async_db() as db:

        details = await db.execute(
            select(Transaction).
            filter_by(batch_id=batch_id))

        for item in details.scalars():
            try:
                async with db.begin():  # start auto transaction

                    account = await db.execute(
                        select(Account).filter_by(id=sender_id).with_for_update()
                    )
                    # 執行扣款與入帳邏輯...
                    # 更新 item 狀態為 SUCCESS
                await db.commit()
            except Exception as e:
                await db.rollback()
                # 標記該筆明細失敗，但不影響整批其他交易
