#include <WiFi.h>
#include <HTTPClient.h>

// ===============================
// WIFI CONFIG
// ===============================
const char* ssid     = "knzlw";
const char* password = "harisganteng";

// ===============================
// SERVER FLASK
// ===============================
const char* serverURL = "http://10.222.191.117:5000/send_data";
// GANTI IP sesuai yang muncul di terminal Flask

// ===============================
// PIR CONFIG
// ===============================
#define PIR_PIN 18   

// ===============================
// TIMER
// ===============================
unsigned long lastSend = 0;
const unsigned long interval = 3000; // 3 detik

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(PIR_PIN, INPUT);

  // ===============================
  // CONNECT WIFI
  // ===============================
  WiFi.begin(ssid, password);
  Serial.print("🔌 Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi Connected");
  Serial.print("📡 ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long now = millis();
  if (now - lastSend >= interval) {
    lastSend = now;

    int pirValue = digitalRead(PIR_PIN);

    Serial.print("👤 PIR State: ");
    Serial.println(pirValue);

    sendToFlask(pirValue);
  }
}

// ===============================
// SEND DATA → FLASK
// ===============================
void sendToFlask(int pir) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"pir\": " + String(pir) + "}";

    int responseCode = http.POST(payload);

    if (responseCode > 0) {
      Serial.print("✅ Flask Response: ");
      Serial.println(responseCode);
    } else {
      Serial.print("❌ Failed Send: ");
      Serial.println(responseCode);
    }

    http.end();
  } else {
    Serial.println("❌ WiFi Disconnected");
  }
}
