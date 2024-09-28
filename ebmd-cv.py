#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Built-in modules
import argparse
import logging
import sys

# Added modules
import cv2

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def application(ip: str, user: str, password: str, port: str) -> None:
    """ """

    # RTSP URL
    rtsp_url = f"rtsp://{user}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=0&unicast=true"

    cap = None

    try:
        logging.info("ebmd-cv is running")

        # Open the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            logging.error("Error: Couldn't open the video stream.")
            exit(1)

        # Create a named window in OpenCV
        cv2.namedWindow("RTSP Stream", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "RTSP Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )

        # Read and display the stream
        while True:

            # Read a frame from the stream and decode it
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
        # Log the OpenCV error and exit with an error code
        logging.error(f"OpenCV Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        # Exit the application gracefully
        logging.info("ebmd-cv received a keyboard interrupt.")

    except Exception as e:
        # Log the exception and exit with an error code
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

    finally:
        # Release resources and exit
        if cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()

    # Log successful completion of the application
    logging.info("ebmd-cv has finished successfully.")
    sys.exit(0)


if __name__ == "__main__":
    """ """

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
        "--port", required=False, default="554", help="Port for RTSP (optional)."
    )

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Start the main application with the parsed arguments, defaulting to port 554 if none is provided
    application(args.ip, args.user, args.password, args.port)
