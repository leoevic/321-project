# MQTT

This project uses the Mosquitto MQTT broker for communication between the game and the dashboard. The following things are worth noticing:

- The Mosquitto broker is also being run with Docker.
- The Mosquitto broker saves persisted data every five seconds to disk.