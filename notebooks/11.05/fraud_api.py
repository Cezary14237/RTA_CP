from fastapi import FastAPI
from pydantic import BaseModel
import pickle, numpy as np
 
app = FastAPI(title="Fraud Detection API")
 
model = pickle.load(open('fraud_model.pkl', 'rb'))
 
class Transaction(BaseModel):
    amount: float
    is_electronics: int
    tx_per_minute: int
 
@app.post("/score")
def score(tx: Transaction):
    X = np.array([[tx.amount, tx.is_electronics, tx.tx_per_minute]])
    prediction     = model.predict(X)[0]
 
    return {
        **tx,
        "is_fraud":          prediction,
        "model":             "random_forest",
    }
 
@app.get("/health")
def health():
    return {"status": "ok"}
