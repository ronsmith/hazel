/*******************************************************************************
 * TemperatureSensor
 * Class for handling the LM61 temperature sensor.
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#ifndef _TemperatureSensor_h
#define _TemperatureSensor_h

#define LM61_OFFSET 0.6
#define TMP36_OFFSET 0.5

class TemperatureSensor {

  public:
    int pin;
    int mvref;
    int mvoff;
    unsigned long logInterval;

    TemperatureSensor();

    void begin(int pin, int mvoff=0, int mvref=0, unsigned long logInterval=0);
    void loop();

    int celcius();
    int farenheit();
    int millivolts();

    void logTemp();

  private:
    int buffer[10];
    int index;
    unsigned long lastLogTime;
};

#endif // _TemperatureSensor_h

