from pydantic import BaseModel

# Data model representing a receipt.
class Receipt(BaseModel):
    vendor: str     # Name of the vendor for the receipt
    date: str       # Date of the receipt in string format
    amount: float   # Receipt amount
