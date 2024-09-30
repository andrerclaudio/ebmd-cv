
# RTSP Stream Viewer (ebmd-cv)

This Python script allows you to connect to and view an RTSP stream using OpenCV. It requires an IP address, username, password, and optionally a port for RTSP connection.

## Requirements

- Python 3.x
- OpenCV
- argparse
- logging

## Installation

1. Install Python dependencies using pip:

    ```bash
    pip install opencv-python argparse
    ```

## Usage

Run the script using the following command format:

```bash
./ebmd-cv.py --ip <IP_ADDRESS> --user <USERNAME> --password <PASSWORD> [--port <PORT>]
```

- `--ip`: The IP address of the RTSP server.
- `--user`: The username for RTSP authentication.
- `--password`: The password for RTSP authentication.
- `--port`: (Optional) The port for RTSP. Defaults to `554` if not provided.

### Example:

```bash
./ebmd-cv.py --ip 192.168.1.100 --user admin --password password123 --port 554
```

## How It Works

- The script establishes an RTSP connection using the provided credentials.
- It opens a fullscreen window and displays the video stream.
- Press `q` to exit the stream.

## Error Handling

- The script logs any errors that occur during the connection or video fetching process.
- Handles OpenCV-specific errors, as well as general exceptions.
- Supports graceful shutdown on `KeyboardInterrupt` (e.g., pressing `Ctrl+C`).

## Logging

Logs are outputted to the console with timestamp and log level.

## Exit Codes

- `0`: Successful completion.
- `1`: An error occurred (e.g., could not open video stream, failed to fetch frame).
