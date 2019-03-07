int x=1;
void setup(){
    Serial.begin(9600);
}
void loop(){   
while (x < 10) {
Serial.print(x);
Serial.print(" ");
Serial.print(x*x);
Serial.print(" ");
Serial.println(x*x*x);
x++;
}
}
