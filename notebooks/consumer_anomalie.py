from kafka import KafkaConsumer
import json
from datetime import datetime
from collections import defaultdict

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

history = defaultdict(list)

for message in consumer:
    tx = message.value
    u_id = tx['user_id']
    now = datetime.fromisoformat(tx['timestamp'])
    history[u_id].append(now)
    history[u_id] = [t for t in history[u_id] if (now - t).total_seconds() <= 60]
    if len(history[u_id]) > 3:
        print(f"ALERT: Użytkownik {u_id} wykonał {len(history[u_id])} transakcje w ciągu 60s!")
        print(f"Ostatnia: {tx['tx_id']} w {tx['store']}")
