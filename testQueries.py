DATABASE_URL = "postgresql://neondb_owner:npg_PeyFuf37rBwh@ep-dawn-cake-a5vgb7zl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

import os
import asyncio
import asyncpg


async def main():
    # Use the hardcoded connection string
    connection_string = DATABASE_URL

    # Create a connection pool
    pool = await asyncpg.create_pool(connection_string)

    # Acquire a connection from the pool
    async with pool.acquire() as conn:

        print("Available columns:")
        for row in schema_rows:
            print(row["column_name"])

        # Try alternative query using the timestamp from your example
        rows = await conn.fetch(
            "SELECT payload->>'Moisture Meter - Moisture Meter', time as time_value FROM fridge_data_virtual WHERE topic = 'home/kitchen/fridge' AND payload->>'Moisture Meter - Moisture Meter' IS NOT NULL AND time > NOW() - INTERVAL '3 hours' ORDER BY time DESC;"
        )
        rows2 = await conn.fetch(
            "SELECT AVG(CAST(CAST ((payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor') AS NUMERIC(19,4)) AS INT)) FROM fridge_data_virtual WHERE ((payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor') IS NOT NULL);"
        )

    # Close the pool
    await pool.close()

    # Print the results
    print("\nMoisture Meter Results:")
    for row in rows:
        print(f"Value: {row[0]}, Time: {row[1]}")


# Run the asynchronous main function
asyncio.run(main())
