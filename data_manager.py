import psycopg2
import pandas as pd 
from sqlalchemy import create_engine

'''
Python Script to execute PSQL queries in Python.
This queries will create some statistics from telemetry sent from an IoT device to a DB.
It will handle dates conversion (timestamp --> date) and range between dates.
'''

### Create Conection
engine = create_engine('postgresql://postgres:postgres@ip_to_conect_to:5432/thingsboard')

### Queries

### In & Out queries

engine.execute("INSERT INTO ts_kv SELECT tabla_rosa.entity_type, tabla_rosa.entity_id, 'in_count', tabla_rosa.times, null, null, null, tabla_rosa.count FROM (SELECT ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, date_trunc('week', TO_TIMESTAMP(ts_kv.ts / 1000)::date) AS weekly, COUNT(ts_kv.key), MIN(ts_kv.ts) AS times FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'in' AND ts_kv.entity_type LIKE 'DEVICE' GROUP BY ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, weekly) as tabla_rosa;")

engine.execute("INSERT INTO ts_kv SELECT tabla_rosa.entity_type, tabla_rosa.entity_id, 'out_count', tabla_rosa.times, null, null, null, tabla_rosa.count FROM (SELECT ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, date_trunc('week', TO_TIMESTAMP(ts_kv.ts / 1000)::date) AS weekly, COUNT(ts_kv.key), MIN(ts_kv.ts) AS times FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'out' AND ts_kv.entity_type LIKE 'DEVICE' GROUP BY ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, weekly) as tabla_rosa;")

engine.execute("DELETE FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'in' AND ts_kv.entity_type LIKE 'DEVICE'")

engine.execute("DELETE FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'out' AND ts_kv.entity_type LIKE 'DEVICE'")

### inOutBalance queries

engine.execute("INSERT INTO ts_kv SELECT tabla_rosa.entity_type, tabla_rosa.entity_id, 'inOutBalance_avg', tabla_rosa.times, null, null, null, tabla_rosa.avg_t FROM (SELECT ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, date_trunc('week', TO_TIMESTAMP(ts_kv.ts / 1000)::date) AS weekly, AVG(ts_kv.long_v) AS avg_t, MIN(ts_kv.ts) AS times FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'inOutBalance' AND ts_kv.entity_type LIKE 'ASSET' GROUP BY ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, weekly) as tabla_rosa;")

engine.execute("INSERT INTO ts_kv SELECT tabla_rosa.entity_type, tabla_rosa.entity_id, 'inOutBalance_max', tabla_rosa.times, null, null, null, tabla_rosa.avg_t FROM (SELECT ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, date_trunc('week', TO_TIMESTAMP(ts_kv.ts / 1000)::date) AS weekly, MAX(ts_kv.long_v) AS avg_t, MIN(ts_kv.ts) AS times FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'inOutBalance' AND ts_kv.entity_type LIKE 'ASSET' GROUP BY ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, weekly) as tabla_rosa;")

engine.execute("INSERT INTO ts_kv SELECT tabla_rosa.entity_type, tabla_rosa.entity_id, 'inOutBalance_min', tabla_rosa.times, null, null, null, tabla_rosa.avg_t FROM (SELECT ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, date_trunc('week', TO_TIMESTAMP(ts_kv.ts / 1000)::date) AS weekly, MIN(ts_kv.long_v) AS avg_t, MIN(ts_kv.ts) AS times FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'inOutBalance' AND ts_kv.entity_type LIKE 'ASSET' GROUP BY ts_kv.entity_type, ts_kv.entity_id, ts_kv.key, weekly) as tabla_rosa;")

engine.execute(" DELETE FROM ts_kv WHERE TO_TIMESTAMP(ts_kv.ts / 1000)::date < NOW() - interval '1 month' AND ts_kv.key like 'inOutBalance' AND ts_kv.entity_type LIKE 'ASSET'")
