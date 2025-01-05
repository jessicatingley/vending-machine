// Hardware setup constants
const int sensorPin = 2;
const int stepPin = 3;
const int dirPin = 4;
const int LEDPin = 5;
const int buzzerPin = 6;
const int buttonPin = 13;
const float stepsPerRev = 200.;
const float pinThreeFreq = 490.196;

// State machine variables
float numRevs = 0;
char command = 'n';
byte nextState;
byte dispFlag = 0;
byte buzzFlag = 0;
byte revFlag = 0;
int LEDVal = 0;
unsigned long startTime = 0;
unsigned long resetStartTime = 0;
unsigned long stepperStart;
unsigned long revStart;
int stepCount = 0;
const byte idle = 0;
const byte dispensing = 1;
const byte reloading = 2;
const byte empty = 3;
const byte reset = 4;


void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(LEDPin, OUTPUT);
  pinMode(sensorPin, INPUT);
  pinMode(buttonPin, INPUT);
  Serial.begin(38400);
  nextState = 0;
}

void loop() {
  if((millis() - startTime) >= 50){
    startTime = millis();
    if(Serial.available() > 0){
      command = Serial.read();
    }
  }
  if((millis() - resetStartTime) >= 1000){
    resetStartTime = millis();
    Serial.print(LEDVal);  // Only write reset state every 1 sec
  }
  ControlTask();
}


void ControlTask(void){
  int x = 0;
  int reading = 0;

  switch(nextState){
    // IDLE STATE
    case idle:
      // Action
      reading = digitalRead(sensorPin);

      // Exit
      if(reading){
        nextState = empty;  // No object detected -- go to empty state
      }
      else if(command == 'b') { 
        nextState = reloading;  // Reverse button pressed -- go to reverse state
      }
      // ON CAMPUS BUTTON: !DIGITALREAD(BUTTONPIN)
      else if(!digitalRead(buttonPin)){
        nextState = reset;  // Reset button pressed -- reset system
      }
      else if(command != 'n') {
        // Ensure system is reset before dispensing again
        if(LEDVal){}
        else{
          nextState = dispensing;  // Dispense button pressed -- go to dispensing state
        }
      }
      break;

    // DISPENSING STATE
    case dispensing:
      // Entry
      if(!dispFlag){
        // Match number of items to be dispensed with number of revolutions to turn
        switch(command){
        case '1': numRevs = 1.; break;
        case '2': numRevs = 2.; break;
        case '3': numRevs = 3.; break;
        case '4': numRevs = 4.; break;
        case '5': numRevs = 5.; break;
        default:
          command = 'n';
          nextState = idle;
          return;
        }
        dispFlag = 1;
        // Prep for stepper movement
        stepCount = 0;
        digitalWrite(dirPin, HIGH);
        stepperStart = millis();
      }

      // Action
      analogWrite(stepPin, 128);  // PWM to stepper motor
      
      // Exit
      if((millis() - stepperStart) >= ((stepsPerRev/pinThreeFreq)*numRevs)*1000){
        analogWrite(stepPin, 0);
        command = 'n';
        nextState = idle;
        dispFlag = 0;
      }
      break;
    
    // RELOADING STATE
    case reloading:
      // Entry
      if(!revFlag){
        // Prep for stepper movement
        digitalWrite(dirPin, LOW);
        revFlag = 1;
        revStart = millis();
      }
      
      // Action
      analogWrite(stepPin, 128);  // PWM to stepper motor
      
      // Exit
      if((millis() - revStart) >= (stepsPerRev/pinThreeFreq)*1000){
        analogWrite(stepPin, 0);
        command = 'n';
        nextState = idle;
        revFlag = 0;
      }
      break;

    // EMPTY STATE
    case empty:
      // Entry
      if(!buzzFlag){
        tone(buzzerPin, 262, 2000);
        digitalWrite(LEDPin, HIGH);
        LEDVal = HIGH;
        buzzFlag = 1;
      }

      // Exit -- may only exit to reloading state
      if(command == 'b'){
        nextState = reloading;
      }
      break;
    
    // RESET STATE
    case reset:
      // Action
      reading = digitalRead(sensorPin);
      
      // Exit -- check that system is no longer empty
      if(!reading){
        digitalWrite(LEDPin, LOW);
        LEDVal = LOW;
        buzzFlag = 0;
        nextState = idle;
      }
      else{
        nextState = idle;
      }

    default:
      nextState = idle;
    
  }
}
