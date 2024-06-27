#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

// BLE services and characteristics
BLEService controlService("12345678-1234-1234-1234-1234567890ab");
BLEService dataService("12345678-1234-1234-1234-1234567890ac");
BLEByteCharacteristic startStopCharacteristic("12345678-1234-1234-1234-1234567890ad", BLERead | BLEWrite);
BLECharacteristic sensorDataCharacteristic("12345678-1234-1234-1234-1234567890ae", BLERead | BLENotify, 56); // 14 floats * 4 bytes each
BLECharacteristic derivedDataCharacteristic("12345678-1234-1234-1234-1234567890af", BLERead | BLENotify, 4);

bool recording = false;

// Last update time for data characteristic
unsigned long lastUpdateData = 0;
unsigned long lastUpdateDerived = 0;

// Update intervals in milliseconds
const unsigned long updateIntervalData = 50;
const unsigned long updateIntervalDerived = 30000; // 30 seconds

// Step detection variables
const float stepThreshold = 1.0;
int numSteps = 0;

// Buffer to store acceleration data
const int bufferSize = 1200; // 1200 samples for 60 seconds at 20 Hz (50 ms interval)
float accelerationBuffer[bufferSize][3];
int bufferIndex = 0;

void setup() {
  Serial.begin(9600);

  // // Wait for serial monitor to open
  // while (!Serial);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }

  // Initialize IMU
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  // Set device name
  BLE.setLocalName("InsoleDevice");
  BLE.setAdvertisedService(controlService);
  BLE.setAdvertisedService(dataService);

  // Add characteristics to services
  controlService.addCharacteristic(startStopCharacteristic);
  dataService.addCharacteristic(sensorDataCharacteristic);
  dataService.addCharacteristic(derivedDataCharacteristic);

  // Add services
  BLE.addService(controlService);
  BLE.addService(dataService);

  // Set service to advertise
  BLE.setAdvertisedService(controlService);

  // Start advertising
  BLE.advertise();
  Serial.println("BLE device is now advertising, waiting for connection...");
}

void loop() {
  BLEDevice central = BLE.central();
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      if (startStopCharacteristic.written()) {
        uint8_t value = startStopCharacteristic.value();
        if (value == 1) {
          startRecording();
        } else if (value == 0) {
          stopRecording();
        }
      }

      if (recording) {
        unsigned long currentMillis = millis();

        if (sensorDataCharacteristic.subscribed() && currentMillis - lastUpdateData >= updateIntervalData) {
          collectAndSendSensorData();
          lastUpdateData = currentMillis;
        }

        if (derivedDataCharacteristic.subscribed() && currentMillis - lastUpdateDerived >= updateIntervalDerived) {
          detectAndSendSteps();
          lastUpdateDerived = currentMillis;
        }
      }
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

void startRecording() {
  Serial.println("Start recording");
  recording = true;
  BLE.setAdvertisedService(dataService);
}

void stopRecording() {
  Serial.println("Stop recording");
  recording = false;
  BLE.setAdvertisedService(controlService);
}

void print_array(float arr[], int n) {
  for (int i = 0; i < n; i++) {
    Serial.print(arr[i]);
    Serial.print(", ");
  }
  Serial.println();
}

void collectAndSendSensorData() {
  float acceleration[3];
  float gyro[3];
  float analogReadings[8];
  uint8_t bytesToSend[56]; // 14 floats * 4 bytes each

  IMU.readAcceleration(acceleration[0], acceleration[1], acceleration[2]);
  IMU.readGyroscope(gyro[0], gyro[1], gyro[2]);

  const int analogPins[] = {A0, A1, A2, A3, A4, A5, A6, A7};
  for (int i = 0; i < 8; i++) {
    analogReadings[i] = analogRead(analogPins[i]);
  }

  // Store acceleration data in buffer
  accelerationBuffer[bufferIndex][0] = acceleration[0];
  accelerationBuffer[bufferIndex][1] = acceleration[1];
  accelerationBuffer[bufferIndex][2] = acceleration[2];
  bufferIndex = (bufferIndex + 1) % bufferSize; // Circular buffer

  memcpy(bytesToSend, acceleration, 12);
  memcpy(bytesToSend + 12, gyro, 12);
  memcpy(bytesToSend + 24, analogReadings, 32);

  sensorDataCharacteristic.writeValue(bytesToSend, sizeof(bytesToSend));
  Serial.print("Sensor Data: ");
  print_array(acceleration, 3);
  print_array(gyro, 3);
  print_array(analogReadings, 8);
}

void detectAndSendSteps() {
  int steps = 0;

  // Process buffered data for step detection
  for (int i = 1; i < bufferSize - 1; i++) {
    float magnitude = sqrt(sq(accelerationBuffer[i][0]) + sq(accelerationBuffer[i][1]) + sq(accelerationBuffer[i][2]));
    if (magnitude > stepThreshold) {
      float prevMagnitude = sqrt(sq(accelerationBuffer[i-1][0]) + sq(accelerationBuffer[i-1][1]) + sq(accelerationBuffer[i-1][2]));
      float nextMagnitude = sqrt(sq(accelerationBuffer[i+1][0]) + sq(accelerationBuffer[i+1][1]) + sq(accelerationBuffer[i+1][2]));
      if (magnitude > prevMagnitude && magnitude > nextMagnitude) {
        steps++;
      }
    }
  }
  numSteps += steps;
  // convert to bytes
  uint8_t bytesToSend[4];
  memcpy(bytesToSend, &numSteps, 4);
  derivedDataCharacteristic.writeValue(bytesToSend, sizeof(bytesToSend));
  Serial.print("Number of Steps: ");
  Serial.println(numSteps);
}
