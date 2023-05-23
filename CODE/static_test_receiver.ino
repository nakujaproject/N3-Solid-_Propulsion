#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN pins for the NRF24L01 module
const uint64_t pipe = 0xE8E8F0F0E1LL; // Address for communication between the modules
const int MAX_DATA_POINTS = 100; // Maximum number of data points to store
float receivedDataArray[MAX_DATA_POINTS]; // Array to store received data
int dataCount = 0; // Counter variable for the number of received values

void setup() {
  // NRF24L01 module setup
  radio.begin();
  radio.openReadingPipe(1, pipe);
  radio.setPALevel(RF24_PA_HIGH);

  Serial.begin(57600);

  // rest of setup code
}

void loop() {
  if (radio.available()) {
    float receivedData;
    radio.read(&receivedData, sizeof(receivedData));
    
    // Store received data in the array
    
    if (dataCount < MAX_DATA_POINTS) {
      receivedDataArray[dataCount] = receivedData;
      dataCount++;
    }
    
    Serial.print("Received data: ");
    Serial.println(receivedData);
  }

  // rest of code

}