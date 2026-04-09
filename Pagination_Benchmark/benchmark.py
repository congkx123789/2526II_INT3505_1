import sqlite3
import time
import random
import os

DB_NAME = "pagination_demo.db"
NUM_RECORDS = 1000000

def setup_database():
    print(f"--- Setting up database with {NUM_RECORDS} records ---")
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Batch insert for speed
    batch_size = 50000
    for i in range(0, NUM_RECORDS, batch_size):
        data = [(f"Item {j}",) for j in range(i, i + batch_size)]
        cursor.executemany("INSERT INTO items (name) VALUES (?)", data)
        print(f"Inserted {i + batch_size} records...")
    
    conn.commit()
    conn.close()
    print("Database setup complete.\n")

def benchmark_offset(offset, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    start_time = time.perf_counter()
    cursor.execute(f"SELECT * FROM items LIMIT ? OFFSET ?", (limit, offset))
    cursor.fetchall()
    end_time = time.perf_counter()
    
    conn.close()
    return end_time - start_time

def benchmark_cursor(last_id, limit=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    start_time = time.perf_counter()
    cursor.execute(f"SELECT * FROM items WHERE id > ? LIMIT ?", (last_id, limit))
    cursor.fetchall()
    end_time = time.perf_counter()
    
    conn.close()
    return end_time - start_time

def run_benchmarks():
    offsets = [0, 1000, 10000, 100000, 500000, 900000]
    
    print(f"{'Offset':<15} | {'Offset Time (ms)':<20} | {'Cursor Time (ms)':<20}")
    print("-" * 60)
    
    for offset in offsets:
        # Offset Benchmark
        offset_time = benchmark_offset(offset) * 1000  # to ms
        
        # Cursor Benchmark (we assume we know the last_id, which for this simple case is same as offset)
        cursor_time = benchmark_cursor(offset) * 1000 # to ms
        
        print(f"{offset:<15} | {offset_time:<20.4f} | {cursor_time:<20.4f}")

if __name__ == "__main__":
    setup_database()
    run_benchmarks()
