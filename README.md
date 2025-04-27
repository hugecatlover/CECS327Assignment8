# IoT Monitoring System

## Diagram

In this assignment, you will build a complete end-to-end IoT system as shown in Figure. This project will integrate the TCP client/server you created in Assignment 6, your database from Assignment 7, and IoT sensor data to process and analyze user queries. You are also expected to incorporate metadata for each IoT device created in dataniz to enhance the system's functionality.

![image](https://github.com/user-attachments/assets/ec7792d7-2434-4582-9e36-9f01252a73ba)

## Description

This project is an IoT monitoring system designed to handle queries related to IoT devices. It consists of a TCP server, a client interface, and integration with a MongoDB database to retrieve IoT data. The system supports real-time queries about average moisture, water consumption, and electricity usage for connected devices.

### Features

- **Query Support**:

  1. Average moisture in a refrigerator.
  2. Average water consumption in a dishwasher.
  3. Electricity consumption across multiple devices.

- **Metadata Integration**: Metadata from IoT devices is integrated for better data management.

- **Data Aggregation**: Efficient data aggregation for electricity consumption over the last 24 hours.

- **Debugging Tools**: Enhanced debugging for better issue tracking.

## Prerequisites

1. **Python Environment**

   - Python 3.7 or higher installed on both server and client machines.
   - (Optional) Use a virtual environment (e.g., venv or conda).

2. **Python Dependencies**
   - Install required packages via pip:
     ```bash
     pip install psycopg2-binary
     ```

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:hugecatlover/CECS327Assignment8.git
   cd /CECS327Assignment8
   ```

2. **Setup NeonDB**:
   - Ensure your NeonDB instance is running.
   - Add your IoT data from Dataniz to a collection named `IOT_virtual` in a database named `test`.

### Example Data Structures

```json
{
  "timestamp": "1745721907",
  "topic": "home/IOTDevices",
  "parent_asset_uid": "kq0-7a7-80g-d1b",
  "asset_uid": "87h-029-yao-jz5",
  "board_name": "Fridge2_RPi4",
  "fridge2-ACS712_Current": "-11.7389",
  "fridge2-MLX90614_Temp": "-13.2410",
  "DHT11 - fridge2-DHT11_Humidity": "50.8383"
}
```

```json
{
  "timestamp": "1745721907",
  "topic": "home/IOTDevices",
  "parent_asset_uid": "wmz-541-8p0-ib8",
  "asset_uid": "96z-l46-90r-z7o",
  "board_name": "Fridge1_RPi4",
  "Fridge1-ACS712 - ACS712_Current": "-32.8605",
  "Fridge1-mlx90614 - MLX90614_Temp": "-14.9706",
  "Fridge1-1DHT11 - DHT11_Humidity": "43.4481"
}
```

```json
{
  "timestamp": "1745721908",
  "topic": "home/IOTDevices",
  "parent_asset_uid": "rj1-48v-x01-4o6",
  "asset_uid": "s1q-918-81e-lbt",
  "board_name": "Dishwasher_RPi4",
  "Dish-ACS712_Current": "24.1053",
  "Dish-YF-S201 - YFS201_Flow": "4.1028"
}
```

## Running the System

1. **Run the Server**

   - The server connects to the database and listens for incoming queries.

   ```bash
   python server.py
   ```

   - Enter the IP Address and Port Number when prompted. The server will wait for client connections and process queries.

2. **Run the Client**
   - The client allows you to send queries to the server.
   ```bash
   python client.py
   ```
   - Enter the server's IP Address and Port Number.
   - Choose from the available queries:
     1. "average moisture"
     2. "average water consumption"
     3. "consumed more electricity"

## Metadata for IoT Devices

IoT devices are identified using the following metadata:

```
board_name (string): Unique device identifier.

Examples: Fridge1_RPi4, Fridge2_RPi4, Dishwasher_RPi4.

Sensors:

  DHT11 Humidity:
    - DHT11 - fridge2-DHT11_Humidity
    - Fridge1-1DHT11 - DHT11_Humidity
    Measures relative humidity (%) inside each fridge.

  MLX90614 Temperature (optional):
    - fridge2-MLX90614_Temp
    - Fridge1-mlx90614 - MLX90614_Temp
    Measures object temperature (°C).

  ACS712 Current:
    - fridge2-ACS712_Current
    - Fridge1-ACS712 - ACS712_Current
    - Dish-ACS712_Current
    Measures electrical current draw (A).

  Water Flow / Usage (Dishwasher):
    - Dish-YF-S201 - YFS201_Flow: Measures water flow rate (L/min).
    - YF-S201 - Smart Dishwasher Water Usage Sensor: Measures total water usage per cycle.
```

This metadata is integrated into the server code for efficient data retrieval and processing.

## Justification for Metadata Integration

Metadata from dataniz is fully integrated into the system. Device identification and sensor mapping rely on board_name and sensor-specific fields to ensure accurate data retrieval and processing.

## DEMO (Screenshots)
