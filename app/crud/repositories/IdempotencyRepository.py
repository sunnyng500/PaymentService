from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...models.Transaction import Transaction, TransactionStatus


class IdempotencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_key(self, request_id: str):
        """
        Retrieve a transaction by its request_id (idempotency key).
        Returns the transaction if it exists, None otherwise.
        """
        stmt = select(Transaction).where(Transaction.request_id == request_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_key(self, request_id: str, sender_id: int, receiver_id: int, amount: float):
        """
        Create a new idempotency key by creating a transaction record.
        Returns the created transaction.
        """
        transaction = Transaction(
            request_id=request_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            amount=amount,
            status=TransactionStatus.PENDING
        )
        self.db.add(transaction)
        await self.db.flush()
        return transaction

    async def update_status(self, request_id: str, status: TransactionStatus):
        """
        Update the status of a transaction by its request_id.
        Returns True if successful, False otherwise.
        """
        stmt = select(Transaction).where(Transaction.request_id == request_id)
        result = await self.db.execute(stmt)
        transaction = result.scalar_one_or_none()

        if transaction:
            transaction.status = status
            await self.db.flush()
            return True
        return False
