const int ledPins[] = {8,7,6,5,4};
const int trigPin = 3;
const int echoPin = 2;
long last_time = 0;
long time;
long filtered_time;

void setup() {
  for (int i = 0; i < 5; i++){
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  time = pulseIn(echoPin, HIGH); //microseconds

  if (last_time){
    filtered_time = (int)(last_time*0.8) + int(time*0.2);
  }
  else{
    filtered_time = time;
  }

  int level = map(time, 0, 3000, 5, 0);
  level = constrain(level, 0, 5);

  for (int i = 0; i < 5; i++){
    if (level >= i + 1){
      digitalWrite(ledPins[i], HIGH);
    }
    else{
      digitalWrite(ledPins[i], LOW);
    }
  }
  last_time = filtered_time;
  Serial.println(level);
  delay(50);
}
