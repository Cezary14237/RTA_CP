from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    tx = message.value
    print(message.value)
    
# TWÓJ KOD   
    if tx.get('amount', 0) > 3000:
        print(f"ALERT: {tx['tx_id']} | {tx['amount']:.2f} PLN | {tx['store']}")
