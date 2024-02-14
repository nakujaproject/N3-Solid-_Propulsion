/*
  NAKUJA PROGECT
  MAIN RESPONDENT
  - Receive & log Load Cell data
  - Remote ignition
*/


// Include Libraries
#include <WiFi.h>
#include <esp_now.h>

// Define LED and pushbutton state booleans-------------------------------------
bool buttonDown = false;

// Define LED and pushbutton pins-------------------------------------------------
#define STATUS_BUTTON 32

// loadCell values-------------------------------
String thrustGen[2000];
int check = 0;
unsigned int t = 0;
bool start = false;
bool monitor = true;

void formatMacAddress(const uint8_t *macAddr, char *buffer, int maxLength)
// Formats MAC Address
{
  snprintf(buffer, maxLength, "%02x:%02x:%02x:%02x:%02x:%02x", macAddr[0], macAddr[1], macAddr[2], macAddr[3], macAddr[4], macAddr[5]);
}


void receiveCallback(const uint8_t *macAddr, const uint8_t *data, int dataLen)
// Called when data is received
{
  // Only allow a maximum of 250 characters in the message + a null terminating byte
  char buffer[ESP_NOW_MAX_DATA_LEN + 1];
  int msgLen = min(ESP_NOW_MAX_DATA_LEN, dataLen);
  strncpy(buffer, (const char *)data, msgLen);

  // Make sure we are null terminated
  buffer[msgLen] = 0;

  // Format the MAC address
  char macStr[18];
  formatMacAddress(macAddr, macStr, 18);

  // Send Debug log message to the serial port-----------------------------
  //Serial.printf("Received message from: %s - %s\n", macStr, buffer);

  //Add message to array---------------------------------------------
  if(!start && monitor){
    //Serial.println(buffer);
  }
  
  if((check < 1995) && start){
    thrustGen[check] = buffer;
    //Serial.print("Started: ");
    Serial.print(millis());
    Serial.print(", ");
    Serial.println(buffer);
    check++;
  }
  
  
//------------------------------------------------------------------------
}


void sentCallback(const uint8_t *macAddr, esp_now_send_status_t status)
// Called when data is sent
{
  char macStr[18];
  formatMacAddress(macAddr, macStr, 18);
  //Serial.print("Last Packet Sent to: ");
  //Serial.println(macStr);
  //Serial.print("Last Packet Send Status: ");
  //Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}

void broadcast(const String &message)
// Emulates a broadcast
{
  // Broadcast a message to every device in range
  uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  esp_now_peer_info_t peerInfo = {};
  memcpy(&peerInfo.peer_addr, broadcastAddress, 6);
  if (!esp_now_is_peer_exist(broadcastAddress))
  {
    esp_now_add_peer(&peerInfo);
  }
  // Send message
  esp_err_t result = esp_now_send(broadcastAddress, (const uint8_t *)message.c_str(), message.length());

  // Print results to serial monitor
  if (result == ESP_OK)
  {
    //Serial.println("Broadcast message success");
  }
  else if (result == ESP_ERR_ESPNOW_NOT_INIT)
  {
    Serial.println("ESP-NOW not Init.");
  }
  else if (result == ESP_ERR_ESPNOW_ARG)
  {
    Serial.println("Invalid Argument");
  }
  else if (result == ESP_ERR_ESPNOW_INTERNAL)
  {
    Serial.println("Internal Error");
  }
  else if (result == ESP_ERR_ESPNOW_NO_MEM)
  {
    Serial.println("ESP_ERR_ESPNOW_NO_MEM");
  }
  else if (result == ESP_ERR_ESPNOW_NOT_FOUND)
  {
    Serial.println("Peer not found.");
  }
  else
  {
    Serial.println("Unknown error");
  }
}

void setup()
{

  // Set up Serial Monitor
  Serial.begin(115200);
  delay(1000);

  // Set ESP32 in STA mode to begin with
  WiFi.mode(WIFI_STA);
  Serial.println("ESP-NOW Broadcast");

  // Print MAC address
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());

  // Disconnect from WiFi
  WiFi.disconnect();

  // Initialize ESP-NOW
  if (esp_now_init() == ESP_OK)
  {
    Serial.println("ESP-NOW Init Success");
    esp_now_register_recv_cb(receiveCallback);
    esp_now_register_send_cb(sentCallback);
  }
  else
  {
    Serial.println("ESP-NOW Init Failed");
    delay(3000);
    ESP.restart();
  }

  // Pushbutton uses built-in pullup resistor------------------------------------
  pinMode(STATUS_BUTTON, INPUT_PULLUP);

}

void loop()
{

  if (digitalRead(STATUS_BUTTON))
  {

    // Detect the transition from low to high
    
      buttonDown = true;
      // Send a message
      broadcast("on");
      start = true;
      Serial.println("Started: ");
      check = 0;
      
   
    
    // Delay to avoid bouncing
    delay(5000);
  }
  else
  {
    // Reset the button state
    buttonDown = false;
  }
  
  if((millis() > t + 10000) && start){
    for(int i = 0; i < check; i++){
      Serial.print(thrustGen[i]);
      Serial.print(", ");
      t = millis();
    }
    Serial.println();
  }
  if(check > 1990){
    Serial.println("DONE!");
    //------------------------------------------------------------------------
    for(int i = 0; i < check; i++){
      Serial.print(thrustGen[i]);
      Serial.print(", ");
    
    }
    check = 0;
    start = false;
    //monitor = false; 
  }
  //--------------------------------------------------------------------------
  if(Serial.available() > 0)
  {
    for(int i = 0; i < 1490; i++){
      Serial.print(thrustGen[i]);
      Serial.print(", ");
    
    }
    char v = Serial.read();
  }
  
}