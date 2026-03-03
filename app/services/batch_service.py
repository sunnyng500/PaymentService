

class TransferService:
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
