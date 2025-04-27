# IoT Monitoring System

## Diagram

- In this assignment, you will build a complete end-to-end IoT system as shown in Figure. This project will integrate the TCP client/server you created in Assignment 6, your
  database from Assignment 7, and IoT sensor data to process and analyze user queries.
  You are also expected to incorporate metadata for each IoT device created in dataniz to
  enhance the system's functionality

![image](https://github.com/user-attachments/assets/ec7792d7-2434-4582-9e36-9f01252a73ba)

## Description

This project is an IoT monitoring system designed to handle queries related to IoT devices. It consists of a TCP server, a client interface, and integration with a MongoDB database to retrieve IoT data. The system supports real-time queries about average moisture, water consumption, and electricity usage for connected devices.
Features

Query Support:

1. Average moisture in a refrigerator.
2. Average water consumption in a dishwasher.
3. Electricity consumption across multiple devices.

Metadata Integration: Metadata from IoT devices is integrated for better data management.

Data Aggregation: Efficient data aggregation for electricity consumption over the last 24 hours.

Debugging Tools: Enhanced debugging for better issue tracking.

Prerequisites

- Python 3.x
- MongoDB instance (local or cloud, e.g., MongoDB Atlas)
- Required Python libraries:

        pymongo
        tabulate
        pytz

Installation

Clone the repository:

    git clone git@github.com:lf813/cecs327-a8-group42.git

and

    cd IoT-Monitoring-System

Install dependencies:

    pip install pymongo tabulate pytz

Setup MongoDB:

- Ensure your MongoDB instance is running.

Add your IoT data to a collection named IOT_virtual in a database named test. Example structure:

        {
          "cmd": "publish",
          "payload": {
            "board_name": "Raspberry Pi 4 - RefrigeradoraBoard",
            "DHT11 - RefrigeradoraMoistureSensor": "65.36",
            "ACS712 - RefrigeradoraAmmeter": "0.68",
            "YF-S201 - SensorAgua": "20.3"
          },
          "time": "2024-11-30T06:38:16.000Z"
        }

## Running the System

1. Run the Server

The server connects to the database and listens for incoming queries.

    python server.py

- Enter the IP Address and Port Number when prompted. The server will wait for client connections and process queries.

2. Run the Client

The client allows you to send queries to the server.

    python client.py

- Enter the server's IP Address and Port Number.

Choose from the available queries:

1. Average moisture in a refrigerator.
2. Average water consumption in a dishwasher.
3. Device with the highest electricity consumption.

## Metadata for IoT Devices

IoT devices are identified using the following metadata:

        Refrigerator 1:
                board_name: `"Raspberry Pi 4 - RefrigeradoraBoard"`
                Sensors:
                        DHT11 - RefrigeradoraMoistureSensor**: Measures moisture levels.
                        ACS712 - RefrigeradoraAmmeter**: Measures electricity consumption.

        Refrigerator 2:
                board_name: `"board 1 7078fb94-74ef-4712-9eec-62f3aaefac90"`
                Sensors:
                        sensor 1 7078fb94-74ef-4712-9eec-62f3aaefac90**: Measures moisture levels.
                        sensor 2 7078fb94-74ef-4712-9eec-62f3aaefac90**: Measures electricity consumption.

        Dishwasher:
                board_name: `"board 1 1a3e32aa-6115-475c-8993-3fadf9b4d46e"`
                Sensors:
                        YF-S201 - SensorAgua: Measures water consumption.

This metadata is integrated into the server code for efficient data retrieval and processing.

## Justification for Metadata Integration

Metadata from dataniz is fully integrated into the system. Device identification and sensor mapping rely on board_name and sensor-specific fields to ensure accurate data retrieval and processing.

## DEMO (Screenshots)

- Run Server code on the TCP server from Google Cloud(Compute Engine)

![image](https://github.com/user-attachments/assets/4aea733f-4147-4d79-8cb0-0024f8abfa92)

![image](https://github.com/user-attachments/assets/bfd4a73b-b8db-4395-acb7-fd059c3956cf)

- Than run the Client Code on your laptop

![image](https://github.com/user-attachments/assets/0bcb7419-4ddd-4935-a3b1-3d7a41a16e31)

![image](https://github.com/user-attachments/assets/e8f9d413-dd2a-445e-bd94-fcc8ec642254)
