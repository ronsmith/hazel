cmake_minimum_required(VERSION 3.5)
project(PoolPumpController)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    PoolPumpController.ino
    PumpRelay.cpp
    PumpRelay.h
    TemperatureSensor.cpp
    TemperatureSensor.h
    TimeBoundary.h)

add_executable(PoolPumpController ${SOURCE_FILES})