/*******************************************************************************
 * TemperatureSensor
 * Class for handling the LM61 temperature sensor.
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#include <Arduino.h>
#include "TemperatureSensor.h"

static const long VCC_SCALE = 1.1 * 1023 * 1000;

/**
 * Attempt to calculate the actual voltage currently powering the chip using the internal 1.1V reference.
 * This can be more accurate if a Vref measured with a voltmeter is provided as a baseline.
 */
static int readVcc() {
  // Read 1.1V reference against AVcc
  // set the reference to Vcc and the measurement to the internal 1.1V reference
  #if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
    ADMUX = _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #elif defined (__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
    ADMUX = _BV(MUX5) | _BV(MUX0);
  #elif defined (__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
    ADMUX = _BV(MUX3) | _BV(MUX2);
  #else
    ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
  #endif  

  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Start conversion
  while (bit_is_set(ADCSRA,ADSC)); // measuring

  uint8_t low  = ADCL; // must read ADCL first - it then locks ADCH  
  uint8_t high = ADCH; // unlocks both

  long result = (high<<8) | low;

  result = VCC_SCALE / result; // Calculate Vcc (in mV)
  return (int)result; // Vcc in millivolts
}


TemperatureSensor::TemperatureSensor(): 
  pin(0), mvoff(0), mvref(0), logInterval(0), lastLogTime(0), index(0) 
  { }

void TemperatureSensor::begin(int pin, int mvoff, int mvref, unsigned long logInterval)  
{
  this->pin = pin;
  this->mvoff = mvoff;
  this->mvref = mvref;
  this->logInterval = logInterval;
  if (!mvref) this->mvref = readVcc();
  pinMode(pin, INPUT);
  for (int i = 0; i < 10; i++) {
    buffer[i] = analogRead(pin);
    delay(10);  
  }
}


void TemperatureSensor::loop() {
  buffer[index++] = analogRead(pin);
  if (index >=10) index = 0;
  if (logInterval && (millis() - lastLogTime > logInterval)) {
    lastLogTime = millis();
    logTemp();
  }
}


int TemperatureSensor::celcius() {
  return map(millivolts(), 300, 1600, -30, 100);
}


int TemperatureSensor::farenheit() {
  return map(millivolts(), 300, 1600, -22, 212);
}


int TemperatureSensor::millivolts() {
  int total = analogRead(pin);
  for (int i = 1; i < 10; i++) total += buffer[i];
  return map(total/10, 0, 1023, 0, mvref) + mvoff;
}


void TemperatureSensor::logTemp() {
    Serial.print(F("Temp: "));
    Serial.print(millivolts());
    Serial.print(F("mV, "));
    Serial.print(celcius());
    Serial.print(F("C, "));
    Serial.print(farenheit());
    Serial.println(F("F"));
}

