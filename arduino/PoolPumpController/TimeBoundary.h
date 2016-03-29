/*******************************************************************************
 * TimeBoundary
 * Class for keeping track of daily time boundaries.
 * Created By: Ron Smith
 * Copyright ©2016 That Ain't Working, All Rights Reserved
 *******************************************************************************/

#include <limits.h>

#ifndef _TimeBoundary_h
#define _TimeBoundary_h

class TimeBoundary {

  public:
    int hour;
    int minute;

    TimeBoundary(int h=0, int m=0): hour(h), minute(m) { }
    
    TimeBoundary(TimeBoundary const &other): hour(other.hour), minute(other.minute) { }
    
    void operator = (TimeBoundary const &other) {
      hour = other.hour;
      minute = other.minute;
    }
    
    bool operator == (TimeBoundary const &other) {
      return (hour == other.hour && minute == other.minute);
    }
    
    bool operator < (TimeBoundary const &other) {
      if (hour < other.hour) return true;
      if (hour == other.hour) return minute < other.minute;
      return false;
    }
    
    bool operator <= (TimeBoundary const &other) {
      if (hour < other.hour) return true;
      if (hour == other.hour) return minute <= other.minute;
      return false;
    }
    
    bool operator > (TimeBoundary const &other) {
      if (hour > other.hour) return true;
      if (hour == other.hour) return minute > other.minute;
      return false;
    }
    
    bool operator >= (TimeBoundary const &other) {
      if (hour > other.hour) return true;
      if (hour == other.hour) return minute >= other.minute;
      return false;
    }
};

const TimeBoundary MAX_TIME_BOUNDARY(INT_MAX, INT_MAX);

#endif // _TimeBoundary_h

