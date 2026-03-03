from http.client import HTTPException

from fastapi.params import Depends
from sentry_sdk.ai.monitoring import set_ai_pipeline_name
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert
from ..models import Account
from ..db.session import get_async_db
from ..models.Transaction import Transaction


class TransferService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db
        # realtime

    async def create_realtime_transfer(self, send_id: int, receiver_id: int, amount: float):
        async with self.db.begin() as session:  # db.begin() is to start transaction
            # 1.check sender
            sender_statement = (
                select(Account)
                .where(Account.id == send_id)
                .with_for_update()  # lock the account
            )
            # this is a big task
            result = session.execute(sender_statement)
            sender_account = result.scalar_one_or_none()
            if not sender_account or sender_account.balance < 0:
                raise HTTPException(status_code=400, detail=" sender account not exit or the balance is not sufficient")
            # 2.check receiver
            receiver_statement = (
                select(Account)
                .where(Account.id == receiver_id)
                .with_for_update()  # add exclude lock
            )
            result = session.execute(receiver_statement)
            receiver_account = result.scalar_one_or_none()
            if not receiver_account:
                raise HTTPException(status_code=400, detail="the account is not exist")
            # 3.balance
            sender_account.balance -= amount
            receiver_account.balance += amount
        # 4 request uuid

        # 5. record
        new_transfer = Transaction(

        )