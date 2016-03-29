/*******************************************************************************
 * PumpRelay
 * Class for handling the relay for turning the pump on/off.
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#ifndef _PumpRelay_h
#define _PumpRelay_h

#include "TimeBoundary.h"


class PumpRelay {

  public:
    int freezeTempC = 2;
    
    TimeBoundary onTime;
    TimeBoundary offTime;

    PumpRelay();
    
    void begin(int pin, int freezeTempC=2, TimeBoundary const &onTime=MAX_TIME_BOUNDARY, TimeBoundary const &offTime=MAX_TIME_BOUNDARY);
    void loop(int tempC, bool override=false);

    bool isFreezeGuardEnabled() { return freezeGuardEnabled; }
    bool isOverrideButtonPressed() { return overrideButtonPressed; }
    bool isTimerOn() { return timerOn; }
    bool isRelayOn() { return coilStatus == HIGH; }

  private:
    int pin;
    bool freezeGuardEnabled;
    bool overrideButtonPressed;
    bool timerOn;
    int coilStatus;
};

#endif // _PumpRelay_h
