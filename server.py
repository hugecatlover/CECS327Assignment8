import os
import socket
import ipaddress
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import pytz


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

    # compute last 3 hours in LA, then to UTC
    la = pytz.timezone("America/Los_Angeles")
    now_la = datetime.now(la)
    ago_la = now_la - timedelta(hours=3)
    now_utc = now_la.astimezone(pytz.utc)
    ago_utc = ago_la.astimezone(pytz.utc)

    with conn.cursor() as cur:
        if "average moisture" in q:
            cur.execute(
                """
                SELECT AVG((payload->>'Moisture Meter - Moisture Meter')::FLOAT) AS avg_m
                FROM fridge_data_virtual
                WHERE topic IN (%s, %s)
                  AND time BETWEEN %s AND %s
                """,
                ("home/kitchen/fridge", "home/kitchen/fridge1", ago_utc, now_utc),
            )
            avg = cur.fetchone()[0]
            if avg is None:
                return "No moisture data available in the past 3 hours."
            return (
                f"Average moisture in kitchen fridge(s) over the past 3 hours "
                f"(PST): {avg:.2f} RH%"
            )

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

    return "Sorry, I can only answer about average moisture or water consumption right now."


# 3) TCP server
def tcp_server():
    # bind info
    localIP = input("What is the IP address? ").strip()
    try:
        ipaddress.ip_address(localIP)
    except ValueError:
        print("Invalid IP address.")
        return

    port = int(input("What is the Port number of server? ").strip())
    if not (0 < port <= 65535):
        print("Port number must be between 1 and 65535.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((localIP, port))
    except Exception as e:
        print(f"Socket binding error: {e}")
        return

    print(f"Waiting for client on {localIP}:{port}...")
    sock.listen(5)

    conn = get_database()
    if conn is None:
        return

    client_sock, client_addr = sock.accept()
    print(f"Connection from {client_addr}")

    while True:
        try:
            msg = client_sock.recv(1024).decode().strip()
            if not msg or msg.lower() == "exit":
                print(f"Client {client_addr} disconnected.")
                break

            print(f"[Client] {msg}")
            resp = process_query(msg, conn)
            print(f"[Server] {resp!r}")
            client_sock.send(resp.encode())

        except ConnectionResetError:
            print(f"Connection with {client_addr} reset.")
            break

    client_sock.close()
    conn.close()
    sock.close()
    print("Server shut down.")


if __name__ == "__main__":
    tcp_server()
