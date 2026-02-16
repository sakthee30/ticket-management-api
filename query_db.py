#!/usr/bin/env python3
"""
Database Query Executor
Run SQL queries against your SQLite database
"""

from app.database import engine, SessionLocal
from sqlalchemy import text

def run_query(sql_query: str):
    """Execute a SQL query and return results"""
    try:
        with SessionLocal() as session:
            result = session.execute(text(sql_query))
            
            # Try to fetch results for SELECT queries
            if result.returns_rows:
                rows = result.fetchall()
                session.commit()
                print(f"\n✓ Query executed successfully!")
                print(f"Rows returned: {len(rows) if rows else 0}")
                if rows:
                    print("\nResults:")
                    for row in rows:
                        print(row)
            else:
                # For INSERT/UPDATE/DELETE queries
                affected_rows = result.rowcount
                session.commit()
                print(f"\n✓ Query executed successfully!")
                print(f"Rows affected: {affected_rows}")
                
    except Exception as e:
        print(f"\n✗ Error executing query: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("SQLite Database Query Executor")
    print("=" * 50)
    
    while True:
        print("\nEnter your SQL query (or 'exit' to quit):")
        query = input("> ").strip()
        
        if query.lower() == 'exit':
            print("Goodbye!")
            break
            
        if not query:
            print("Please enter a valid query")
            continue
            
        run_query(query)
