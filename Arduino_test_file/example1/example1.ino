String get;

void setup() {
  
  //setting baurd rate
  Serial.begin(115200);
  
}

void loop(){
 while (Serial.available() >0 )
 {
   Serial.println("please send somthing");
   if (Serial.available() >0 ){
   
     get = Serial.readString();
     Serial.println(get);
   }
   
 }
  
}
