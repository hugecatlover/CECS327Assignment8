# IoT Devices Monitoring — Project Report

## 1. System Architecture & Approach

This project implements a lightweight, end-to-end IoT monitoring system for two refrigerators and one dishwasher. The core components are:

- **TCP Server (Python)**
  - Binds to user-specified IP/port
  - Listens for client messages
  - Parses natural-language queries and dispatches SQL against a PostgreSQL (NeonDB) backend
- **PostgreSQL Database (NeonDB)**
  - Table **`fridge_data_virtual`** stores JSONB payloads, MQTT topic, and timestamp (`TIMESTAMPTZ`)
  - JSON payloads include `board_name` and sensor readings
- **TCP Client (Python)**
  - Connects to server, prompts user for queries
  - Sends messages, displays server responses

All SQL queries use `CROSS JOIN LATERAL jsonb_each_text` to unpack sensor fields and apply filters (time windows, topic). Results are returned as human-readable text.

---

## 2. Research Findings on IoT Sensors & Data

We selected four sensor types based on cost, availability, and data quality:

| Device       | Sensor                   | Units | Typical Range     | Notes                             |
| ------------ | ------------------------ | ----- | ----------------- | --------------------------------- |
| Refrigerator | **DHT11 Humidity**       | RH %  | 0–100 %           | Low cost, ±5 % accuracy           |
| Refrigerator | **MLX90614 Temp** (opt.) | °C    | –40 °C to +125 °C | Non-contact, ±0.5 °C accuracy     |
| All Devices  | **ACS712 Current**       | A     | –30 A to +30 A    | Hall effect, needs filtering      |
| Dishwasher   | **YF-S201 Water Flow**   | L/min | 1–30 L/min        | Pulse output, requires debouncing |

- **Humidity**: Monitored to prevent spoilage; ideal fridge RH is 20–80 %.
- **Temperature**: (Optional) Ensures safe cooling—32–50 °F (0–10 °C).
- **Current**: Tracks energy usage; aggregated to kWh/day.
- **Water Flow**: Enables per-cycle water efficiency analysis.

---

## 3. Dataniz Metadata Integration

We evaluated Dataniz.com for standardized IoT metadata catalogs.

- **Outcome**: Dataniz’s generic schemas did not match our custom `board_name` and JSON key formats.
- **Actions Taken**:
  1. Consulted Dataniz’s device registry to identify common sensor identifiers.
  2. Mapped those to our payload keys via a manual lookup table.
  3. Stored mappings in code comments and README for future reference.
- **Conclusion**: Dataniz provided valuable naming conventions but was **not directly applicable**—we maintained our own metadata section to ensure exact key matching.

---

## 4. Algorithms, Calculations & Unit Conversions

All data-processing occurs via SQL on the database server:

1. **Average Moisture**

   ```sql
   SELECT board_name,
          AVG((kv.value)::NUMERIC) AS avg_moisture
   FROM fridge_data_virtual
     CROSS JOIN LATERAL jsonb_each_text(payload) AS kv(key,value)
   WHERE kv.key ILIKE '%DHT11_Humidity'
     AND time >= now() - INTERVAL '3 hours'
   GROUP BY board_name;
   ```

   Output: RH % per fridge

2. **Average Water Consumption**

   ```sql
    SELECT AVG((payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor')::NUMERIC)
    FROM fridge_data_virtual
    WHERE payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor' IS NOT NULL;
   ```

   Output: Units/cycle

3. **Max Electricity Consumer**

   ```sql
    WITH consumption AS (
    SELECT board_name,
         SUM(ABS((kv.value)::NUMERIC)) AS total_current
    FROM fridge_data_virtual
    CROSS JOIN LATERAL jsonb_each_text(payload) AS kv(key,value)
    WHERE kv.key ILIKE '%ACS712_Current'
    GROUP BY board_name)
    SELECT device, total_current
    FROM consumption
    ORDER BY total_current DESC
    LIMIT 1;
   ```

   Output: Device with highest cumulative current draw (A)

## 5. Challenges & Solutions

1. Connecting to Neon from python
   Solution:

We used Neon DB's documentation to help us setup the project: https://neon.tech/docs/guides/python

2. Figuring out how to unwrap the payload column with SQL
   Solutions:

W3Schools help us remember and learn new SQL queries to unwrap the data from JSon: https://www.w3schools.com/sql/sql_syntax.asp

3. Figuring out how to cast strings into integers for the AVG()
   Solutions:

We had to do trial and error with SQL queries and guiding ourselves from SQL documentation from multiple sources like W3Schools and Stackoverflow

4. Dynamic Time Handling with SQL query
   Solutions:

We used the time function built in from SQL and compare with our table column named "time" from Neon DB in order to only fetch the specific data from the 3 last 3 hours. Also, before querying we had to populate our NeonDB with data from Dataniz by turning on the sensors again.

## 6. Feedback for **Dataniz.com**

- The notifications for enabling sensors covers the sensors.
- I think Dataniz should recommend sensors depending on the projects needs.
- Data Display should be able to be modified.
- Add more templates for sensors
- The UID should be saved on the site
- The guide isn’t immediately accessible from the actual creation screen
