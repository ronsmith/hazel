/*******************************************************************************
 * PumpRelay
 * Class for handling the relay for turning the pump on/off.
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#include <Arduino.h>
#include <TimeLib.h>
#include "PumpRelay.h"

PumpRelay::PumpRelay() : 
  pin(0), 
  freezeTempC(0), 
  onTime(ULONG_MAX), 
  offTime(ULONG_MAX), 
  freezeGuardEnabled(false),
  overrideButtonPressed(false), 
  timerOn(false), 
  coilStatus(LOW)
  { }

void PumpRelay::begin(int pin, int freezeTempC, TimeBoundary const &onTime, TimeBoundary const &offTime) {
  this->pin = pin;
  this->freezeTempC = freezeTempC;
  this->onTime = onTime;
  this->offTime = offTime;
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void PumpRelay::loop(int tempC, bool override)  {
  int coilVal = LOW;
  if (tempC <= freezeTempC) { // freeze guard always takes precedence
    if (!freezeGuardEnabled) {
      Serial.println(F("Freeze Guard ENABLED"));
      freezeGuardEnabled = true;
    }
    coilVal = HIGH;
  } else {
    if (freezeGuardEnabled) {
      Serial.println(F("Freeze Guard DISABLED"));
      freezeGuardEnabled = false;
    }
    if (override) {
      if (!overrideButtonPressed) {
        Serial.println(F("Override Button PRESSED"));
        overrideButtonPressed = true;
      }
      coilVal = HIGH;
    } else {
      if (overrideButtonPressed) {
        Serial.println(F("Override Button RELEASED"));
        overrideButtonPressed = false;
      }
      TimeBoundary tbNow(hour(), minute());
      if (tbNow >= onTime && tbNow <= offTime) {
        if (!timerOn) {
          Serial.println(F("Timer ON"));
          timerOn = true;
        }
        coilVal = HIGH;
      } else {
        if (timerOn) {
          Serial.println(F("Timer OFF"));
          timerOn = false;
        }
      }
    }
  }
  if (coilStatus != coilVal) {
    coilStatus = coilVal;
    Serial.print(F("Relay "));
    Serial.println(coilVal == HIGH ? F("ON") : F("OFF"));
  }
  digitalWrite(pin, coilVal);
}
