import os
import socket
import ipaddress
import psycopg2
from psycopg2.extras import RealDictCursor


# 1) NeonDB connection
def get_database():
    url = "postgresql://neondb_owner:npg_PeyFuf37rBwh@ep-dawn-cake-a5vgb7zl-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
    try:
        conn = psycopg2.connect(url, sslmode="require")
        print("✅ Connected to NeonDB successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to NeonDB: {e}")
        return None


# 2) Business logic
def process_query(query, conn):
    q = query.lower()

    with conn.cursor() as cur:
        if "average moisture" in q:
            cur.execute(
                """
                SELECT
                  payload->>'board_name'      AS fridge,
                  AVG((kv.value)::NUMERIC)    AS avg_moisture
                FROM fridge_data_virtual
                  -- expand the JSON payload into key/value pairs
                  CROSS JOIN LATERAL jsonb_each_text((payload::JSONB)) AS kv(key, value)
                WHERE
                  topic = 'home/IOTDevices'
                  -- match only the DHT11_Humidity fields (both Fridge1 and Fridge2)
                  AND kv.key ILIKE '%DHT11_Humidity'
                  -- restrict to the past 3 hours
                  AND time >= now() - INTERVAL '3 hours'
                GROUP BY
                  payload->>'board_name'
                ORDER BY
                  fridge;
                """
            )
            results = cur.fetchall()
            if not results:
                return "No moisture data available in the past 3 hours."

            response = "Average moisture in kitchen fridges over the past 3 hours:"
            for fridge, avg in results:
                response += f"\n{fridge}: {avg:.2f} RH%"
            return response

        elif "average water consumption" in q:
            cur.execute(
                """
                SELECT AVG(CAST(CAST ((payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor') AS NUMERIC(19,4)) AS INT)) FROM fridge_data_virtual WHERE ((payload->>'YF-S201 - Smart Dishwasher Water Usage Sensor') IS NOT NULL);
                """,
            )
            avg = cur.fetchone()[0]
            if avg is None:
                return "No dishwasher water‐level data available."
            return (
                f"Average water consumption per cycle in smart dishwasher: "
                f"{avg:.2f} units"
            )

        elif "consumed more electricity" in q or "more electricity" in q:
            cur.execute(
                """
                WITH consumption AS (
                  SELECT
                    payload->>'board_name'                       AS device,
                    SUM(ABS((kv.value)::NUMERIC))                AS total_current
                  FROM fridge_data_virtual
                  CROSS JOIN LATERAL jsonb_each_text(payload::JSONB) AS kv(key, value)
                  WHERE
                    topic = 'home/IOTDevices'
                    AND kv.key   ILIKE '%ACS712_Current'
                  GROUP BY
                    payload->>'board_name'
                )
                SELECT
                  device,
                  total_current
                FROM
                  consumption
                ORDER BY
                  total_current DESC
                LIMIT 1;
                """
            )
            result = cur.fetchone()
            if result is None:
                return "No electricity consumption data available."

            device, total_current = result
            return f"The device that consumed the most electricity is {device} with {total_current:.2f} units."

    return "Sorry, I can only answer about average moisture, water consumption, or electricity consumption right now."


# 3) TCP server
def tcp_server():
    # bind info
    localIP = input("What is the IP address? ").strip()
    try:
        ipaddress.ip_address(localIP)
    except ValueError:
        print("Invalid IP address.")
        return

    try:
        port = int(input("What is the Port number of server? ").strip())
        if not (0 < port <= 65535):
            print("Port number must be between 1 and 65535.")
            return
    except ValueError:
        print("Port must be a number. Please try again.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((localIP, port))
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Error: Port {port} is already in use. Try a different port.")
        else:
            print(f"Socket binding error: {e}")
        return
    except Exception as e:
        print(f"Socket binding error: {e}")
        return

    print(f"Waiting for client on {localIP}:{port}...")
    sock.listen(5)

    # Connect to database with a timeout
    print("Connecting to database...")
    conn = get_database()
    if conn is None:
        print(
            "Failed to connect to database. Make sure your internet connection is working."
        )
        print(
            "Continuing without database connection. Only basic functionality will be available."
        )
        # You could choose to return here, but we'll continue for debugging purposes
    else:
        print("Database connected successfully!")

    print(f"Server is ready and listening on {localIP}:{port}")
    print("Waiting for client connection...")

    try:
        client_sock, client_addr = sock.accept()
        print(f"Connection from {client_addr}")

        while True:
            try:
                msg = client_sock.recv(1024).decode().strip()
                if not msg or msg.lower() == "exit":
                    print(f"Client {client_addr} disconnected.")
                    break

                print(f"[Client] {msg}")

                if conn is not None:
                    resp = process_query(msg, conn)
                else:
                    resp = "Server is running in limited mode due to database connection issue."

                print(f"[Server] {resp!r}")
                client_sock.send(resp.encode())

            except ConnectionResetError:
                print(f"Connection with {client_addr} reset.")
                break
            except Exception as e:
                print(f"Error processing message: {e}")
                try:
                    client_sock.send(
                        f"Error processing your request: {str(e)}".encode()
                    )
                except:
                    pass
                break

        client_sock.close()
    except KeyboardInterrupt:
        print("\nServer shutdown requested by user.")
    except Exception as e:
        print(f"Error accepting connection: {e}")
    finally:
        if conn:
            conn.close()
        sock.close()
        print("Server shut down.")


if __name__ == "__main__":
    tcp_server()
