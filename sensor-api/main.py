from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from air_sensor import AirSensor
from distance_sensor import DistanceSensor
import json

air_sensor = AirSensor()
distance_sensor = DistanceSensor()

host = "0.0.0.0"
port = 8080

sleep(1)


class Server(BaseHTTPRequestHandler):
    def sendJSON(self, object: object, code: int = 200):
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Vary", "Origin")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(object).encode())

    def do_GET(self):
        if self.path == "/api/air":
            air = air_sensor.readAir()
            self.sendJSON({
                "status": "ok",
                "data": [
                    {"label": "Temperature", "value": air.temperature, "unit": "°C"},
                    {"label": "Humidity", "value": air.humidity, "unit": "%"}
                ]
            })

        elif self.path == "/api/distance":
            distance = distance_sensor.readDistance()
            self.sendJSON({
                "status": "ok", "distance": distance,
                "data": [
                    {"label": "Distance", "value": distance, "unit": "cm"},
                ]
            })


def main():
    web_server = HTTPServer((host, port), Server)
    print(f"Server started and listen to {host}:{port}")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

print("Server stopped")
 
