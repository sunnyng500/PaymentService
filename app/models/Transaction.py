from sqlalchemy import Column, String, Numeric, BigInteger, ForeignKey, Enum
import enum
from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Transaction(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    # 冪等性 Key：防止前端重複提交導致重複扣款
    request_id = Column(String(64), unique=True, index=True, nullable=False)

    sender_id = Column(BigInteger, ForeignKey("account.id"), nullable=False)
    receiver_id = Column(BigInteger, ForeignKey("account.id"), nullable=False)
    amount = Column(Numeric(20, 2), nullable=False)

    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)

    # 關聯批量任務 (如果是即時轉賬，此欄位為 Null)
    batch_id = Column(BigInteger, ForeignKey("batchtask.id"), nullable=True)
