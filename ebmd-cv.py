#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import cv2

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def application(ip: str, user: str, password: str, port: str = "554") -> None:
    """
    Main application for connecting to an RTSP stream and displaying it using OpenCV.

    Args:
        ip (str): The IP address of the RTSP server.
        user (str): The username for RTSP authentication.
        password (str): The password for RTSP authentication.
        port (str): The port for the RTSP server. Defaults to 554.

    Raises:
        SystemExit: If an error occurs during stream fetching or processing.
    """
    rtsp_url = f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=0&unicast=true"
    cap = None

    try:
        logging.info("ebmd-cv is running")

        # Open the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            logging.error("Error: Couldn't open the video stream.")
            sys.exit(1)

        # Create a named window in OpenCV
        cv2.namedWindow("RTSP Stream", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "RTSP Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )

        # Read and display the stream
        while True:
            ret, frame = cap.read()

            if not ret:
                logging.error("Failed to fetch frame.")
                break

            # Display the frame
            cv2.imshow("RTSP Stream", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except cv2.error as e:
        # Handle OpenCV-specific errors
        logging.error(f"OpenCV Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        # Graceful shutdown on keyboard interrupt
        logging.info("ebmd-cv received a keyboard interrupt.")

    except Exception as e:
        # General exception handling
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        # Release resources and close the OpenCV windows
        if cap is not None and cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()

    logging.info("ebmd-cv has finished successfully.")
    sys.exit(0)


if __name__ == "__main__":
    """
    Parses command-line arguments and starts the RTSP stream application.
    """
    parser = argparse.ArgumentParser(description="RTSP stream viewer.")

    # Add required command-line arguments
    parser.add_argument("--ip", required=True, help="IP address of the target server.")
    parser.add_argument(
        "--user", required=True, help="Username for RTSP authentication."
    )
    parser.add_argument(
        "--password", required=True, help="Password for RTSP authentication."
    )
    parser.add_argument(
        "--port", default="554", help="Port for RTSP (optional, defaults to 554)."
    )

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Start the main application with the parsed arguments
    application(args.ip, args.user, args.password, args.port)
