from sqlalchemy import Column, String, Numeric, BigInteger
from app.db.base import Base

class Account(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    account_number = Column(String(20), unique=True, index=True, nullable=False)
    # 使用 Numeric 處理金錢，避免浮點數誤差
    balance = Column(Numeric(20, 2), default=0.00, nullable=False)
    currency = Column(String(3), default="HKD")