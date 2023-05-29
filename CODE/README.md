# Static Test Application

This repository contains three code files for conducting a static test with Arduino. The purpose of this test is to send static test data from one Arduino board to another, receive the data on the other arduino board connected to the computer, and display it using a Python-based user interface (UI).

## Contents

- `static_test_sender.ino`: Arduino code for sending static test data.
- `static_test_receiver.ino`: Arduino code for receiving static data from an Arduino.
- `uimotor.py`: Python code for creating the user interface to monitor static test values.

## Prerequisites

To run the static test application, you will need the following:

- Arduino IDE: To upload the `static_test_sender.ino` & `static_test_receiver.ino` code to the Arduino boards.
- Arduino compiler: To compile and run the `static_test_receiver.ino` & `static_test_sender.ino` code.
- Python: To run the `uimotor.py` Python script.

## Customization

- You can modify the `static_test_sender.ino` code to change the static test data being sent from the Arduino board.

- The `uimotor.py` Python script can be customized to enhance the user interface or perform additional data processing as per your requirements.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

