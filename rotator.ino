#include <ESP8266WiFi.h>
 
const char* ssid = "DELL G5 SE";
const char* password = "sreyansh";

int Step = 0; //GPIO0---D3 of Nodemcu--Step of stepper motor driver
int Dir  = 2; //GPIO2---D4 of Nodemcu--Direction of stepper motor driver

WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);
 pinMode(Step, OUTPUT); //Step pin as output
 pinMode(Dir,  OUTPUT); //Direcction pin as output
 digitalWrite(Step, LOW); // Currently no stepper motor movement
 digitalWrite(Dir, LOW);  
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address on serial monitor
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");    //URL IP to be typed in mobile/desktop browser
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request
  int i=0;
  int value = LOW;
 
  if (request.indexOf("/Command=forward") != -1)  { //Move 50 steps forward                                                                 
    digitalWrite(Dir, HIGH); //Rotate stepper motor in clock wise direction
          for( i=1;i<=50;i++){
          digitalWrite(Step, HIGH);
          delay(10);
          digitalWrite(Step, LOW);
          delay(10);}
    value = HIGH; 
  }
 
  if (request.indexOf("/Command=backward") != -1)  { //Move 50 steps backwards
    digitalWrite(Dir, LOW); //Rotate stepper motor in anti clock wise direction
          for( i=1;i<=50;i++){
          digitalWrite(Step, HIGH);
          delay(10);
          digitalWrite(Step, LOW);
          delay(10);}
    value = LOW;
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<h1 align=center>Stepper motor controlled over WiFi</h1><br><br>");
  client.print("Stepper motor moving= ");
 
  if(value == HIGH) {
    client.print("Forward");
  } else {
    client.print("Backward");
  }
  client.println("<br><br>");
  client.println("<a href=\"/Command=forward\"\"><button>Forward </button></a>");
  client.println("<a href=\"/Command=backward\"\"><button>Backward </button></a><br />");  
  client.println("</html>");
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}
