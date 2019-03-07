#define NUMBER 10
int x;
void setup(){
    Serial.begin(9600);
    x = NUMBER;
}
void loop(){
    Serial.println(x);
    x++;
}
