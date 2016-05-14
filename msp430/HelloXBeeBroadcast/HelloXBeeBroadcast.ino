// Hello XBee Broadcast
// Author: Ron Smith, That Ain't Working

char buffer[11];

int bcast_init = 0;

const int FAST = 200;
const int SLOW = 500;

void blink(int pin, int count, int spd) {
    for (int c = 0; c < count; c++) {
        digitalWrite(pin, HIGH);
        delay(spd);
        digitalWrite(pin, LOW);
        delay(spd);
    }
}

void setup() {
    pinMode(RED_LED, OUTPUT);
    digitalWrite(RED_LED, LOW);
    pinMode(GREEN_LED, OUTPUT);
    digitalWrite(GREEN_LED, LOW);
    Serial.begin(9600);
    Serial.setTimeout(5000); // 5 seconds
    delay(1000);
}

void loop() {
    if (!bcast_init) {
        blink(GREEN_LED, 3, FAST);
        Serial.print("+++");                                // enter command mode
        if (Serial.readBytesUntil('\r', buffer, 5) > 0) {   // wait for OK
            if (buffer[0] == 'O' && buffer[1] == 'K') {
                Serial.print("ATDH0,ATDLFFFF,ATWR,ATCN\r"); // set destination address to broadcast
                while (Serial.available()) Serial.read();   // ignore all the responses
                bcast_init = 1;
            } else {
                 blink(RED_LED, 4, SLOW);   
            }
        } else {
            blink(RED_LED, 3, SLOW);
        }
    } else {
        Serial.print("Hello from MSP430!\r");
        blink(GREEN_LED, 1, SLOW);
        delay(10000);
    }
}
