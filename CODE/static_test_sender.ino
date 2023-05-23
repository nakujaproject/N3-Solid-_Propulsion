#include <HX711_ADC.h>
#include <EEPROM.h>
#include <SPI.h>
#include <RF24.h>

// NRF24L01 module setup
RF24 radio(9, 10); // CE, CSN pins for the NRF24L01 module
const uint64_t pipe = 0xE8E8F0F0E1LL; // Address for communication between the modules

// define the pins for HX711 connections

const int HX711_dout = 8; // mcu > HX711 dout pin
const int HX711_sck = 9; // mcu > HX711 sck pin

HX711_ADC LoadCell(HX711_dout, HX711_sck);


// Function to calibrate the load cell
void calibrate() {
  // Dummy calibration procedure
  Serial.println("Starting calibration...");
  
  float knownWeight = 100.0;  // Known weight in grams
  float measuredWeight = 0.0; // Placeholder for measured weight

  // Prompt the user to place the known weight on the load cell
  Serial.println("Place the known weight on the load cell...");
  delay(5000); // Allowing time to place the weight
  
  // Read the load cell value after stabilization
  measuredWeight = LoadCell.getData();

  // Calculate the calibration factor
  float calibrationFactor = knownWeight / measuredWeight;
  
  // Set the calibration factor
  LoadCell.setCalFactor(calibrationFactor);
  
  // Save the calibration factor to EEPROM
  EEPROM.put(calVal_eepromAddress, calibrationFactor);
  
  Serial.println("Calibration complete!");
  Serial.print("Calibration factor: ");
  Serial.println(calibrationFactor);
}

void changeSavedCalFactor() {
  // Dummy function to change the saved calibration factor
  
  Serial.println("Enter the new calibration factor:");

  // Wait for user input
  while (!Serial.available()) {
    // Waiting for user input
  }

  // Read the user input
  float newCalibrationFactor = Serial.parseFloat();

  // Set the new calibration factor
  LoadCell.setCalFactor(newCalibrationFactor);

  // Save the new calibration factor to EEPROM
  EEPROM.put(calVal_eepromAddress, newCalibrationFactor);

  Serial.println("Calibration factor updated!");
}


void setup() {
  // Initialize HX711 ADC and load cell
  LoadCell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  LoadCell.setCalFactor(calibration_factor); // Set the calibration factor

  // NRF24L01 module setup
  radio.begin();
  radio.openWritingPipe(pipe);
  radio.setPALevel(RF24_PA_HIGH);

  Serial.begin(57600);
  delay(10);
  Serial.println();
  Serial.println("Model Rocket Test Stand Rig V.1.4");

  LoadCell.begin();
  long stabilizingTime = 2000;
  boolean _tare = false; 
  LoadCell.start(stabilizingTime, _tare);

  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU > HX711 wiring and pin designations");
    while (1);
  } else {
    LoadCell.setCalFactor(1.0); // user set calibration value (float), initial value 1.0 may be used for this sketch
    Serial.println("Startup is complete");
  }

  while (!LoadCell.update());
  calibrate(); // start calibration procedure
}

void loop() {
  // Read load cell data
  float load = LoadCell.getData();

  // Send load cell data wirelessly using NRF24L01 module
  radio.write(&load, sizeof(load));

  static boolean newDataReady = false;
  const int serialPrintInterval = 0; // increase value to slow down serial print activity

  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      Serial.print("Load_cell output val: ");
      Serial.println(i);
      newDataReady = false;
      t = millis();
    }
  }

  // receive command from serial terminal
  if (Serial.available() > 0) {
    float i;
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay(); // tare
    else if (inByte == 'r') calibrate(); // calibrate
    else if (inByte == 'c') changeSavedCalFactor(); // edit calibration value manually
  }

  // check if the last tare operation is complete
  if (LoadCell.getTareStatus() == true) {
    Serial.println("Tare complete");
  }

  // Check for serial commands or other operations

 
}