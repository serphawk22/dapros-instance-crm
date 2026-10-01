from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
    """))
    tables = [row[0] for row in result.fetchall()]
    print(f"Total tables: {len(tables)}")
    non_empty = []
    for t in tables:
        try:
            cnt = conn.execute(text(f'SELECT count(*) FROM "{t}"')).scalar()
            if cnt > 0:
                non_empty.append((t, cnt))
        except Exception as e:
            pass
    print("Non-empty tables:", non_empty)
