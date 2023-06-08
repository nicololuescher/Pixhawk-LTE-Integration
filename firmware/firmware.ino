#include <WiFi.h>
#include <SoftwareSerial.h>

// Wi-Fi network credentials
const char* ssid = "<YOUR SSID>";
const char* password = "<YOUR PASSWORD>";

// TCP server settings
const char* server_address = "<YOUR SERVER ADDRESS>";
const int server_port = 5761;

WiFiClient client;
SoftwareSerial swSerial(16, 17);  // RX, TX, change accordingly

void setup() {
  Serial.begin(115200);
  swSerial.begin(57600);
  delay(10);

  // Connect to Wi-Fi
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to TCP server
  Serial.println("Connecting to TCP server...");
  if (client.connect(server_address, server_port)) {
    Serial.println("Connected to TCP server");
  } else {
    Serial.println("Failed to connect to TCP server");
  }
}

enum ReadState { WAIT_START, READ_LENGTH, READ_DATA };

ReadState state = WAIT_START;
uint8_t payload_length = 0;
size_t bytesRead = 0;
const size_t bufferSize = 1024;
uint8_t buffer[bufferSize];

void loop() {
  // Read data from software serial and send it over the TCP connection
  while (swSerial.available()) {
    uint8_t c = swSerial.read();
    switch (state) {
      case WAIT_START:
        if (c == 0xFD) {
          buffer[bytesRead++] = c;
          state = READ_LENGTH;
        }
        break;
      case READ_LENGTH:
        payload_length = c;
        buffer[bytesRead++] = c;
        state = READ_DATA;
        break;
      case READ_DATA:
        buffer[bytesRead++] = c;
        if (bytesRead == payload_length + 12) {
          client.write(buffer, bytesRead);
          bytesRead = 0;
          state = WAIT_START;
        }
        break;
    }
  }

  // Read data from the TCP connection and write it to software serial
  if (client.available()) {
    uint8_t c = client.read();
    swSerial.write(c);
  }

  //delay(1); // Add a small delay to prevent flooding the output
}
