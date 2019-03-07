void setup(){
    Serial.begin(9600);
}

void loop(){
    for (int angle = 0; angle < 360; angle ++){
        Serial.print(sin(angle * (PI/180)));
        Serial.print(" ");
        Serial.println(cos(angle * (PI/180)));
    }
}
