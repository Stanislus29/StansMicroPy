# Chapter 8: Wi-Fi Manager

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library ```wifiManager.py```

---

## Entity Relationship

**Entity Relationship Model: ```WiFiManager```**

**Entity: WiFiManager**

**Attributes (Properties / State)**

```wlan``` → ```network.WLAN``` object configured in station mode (```STA_IF```). Handles the Wi-Fi radio.

```server_socket``` → TCP server socket bound to the board's IP address and configured port. Listens for incoming client connections.

```client_socket``` → The currently connected client socket (or ```None``` if no client is connected).

**Methods (Behaviours)**

```__init__(SSID, PASSWORD, port=12345)``` → Constructor; activates the Wi-Fi radio, connects to the specified network, waits until connected, prints the assigned IP address, and opens a TCP server socket listening on the given port.

```wait_for_client()``` → Blocks until a client connects to the TCP server. Accepts the connection, stores the client socket, prints the client address, and returns the socket object.

```receive_command()``` → Reads up to 1024 bytes from the connected client, decodes it as UTF-8, strips whitespace, and returns the command string. Returns ```None``` if no client is connected, the client disconnects, or an error occurs.

```close_client()``` → Closes the current client socket and sets it to ```None```.

```close()``` → Closes the client socket, closes the server socket, disconnects from Wi-Fi, and deactivates the radio. Full teardown.

**Relationships**

- WiFiManager ↔ WLAN
    - 1 WiFiManager controls 1 ```network.WLAN``` interface (mandatory). Configured as station mode (```STA_IF```) — the board connects to an existing network rather than creating one.

- WiFiManager ↔ Server Socket
    - 1 WiFiManager opens 1 TCP server socket (mandatory). Bound to the board's assigned IP on the specified port.

- WiFiManager ↔ Client Socket
    - 1 WiFiManager maintains 0 or 1 active client connection at a time. Accepts one client via ```wait_for_client()```.

- WiFiManager ↔ Network Modules
    - Depends on MicroPython's ```network```, ```socket```, and ```time``` modules.
