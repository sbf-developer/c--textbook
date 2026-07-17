cmake_minimum_required(VERSION 3.23)
project(taskledger VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(TASKLEDGER_ENABLE_WARNINGS "Enable strong compiler warnings" ON)

add_library(taskledger_lib
    src/task.cpp
)
target_include_directories(taskledger_lib PUBLIC include)
target_compile_features(taskledger_lib PUBLIC cxx_std_23)

if(TASKLEDGER_ENABLE_WARNINGS)
    if(MSVC)
        target_compile_options(taskledger_lib PRIVATE /W4 /permissive-)
    else()
        target_compile_options(taskledger_lib PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion)
    endif()
endif()

add_executable(taskledger app/main.cpp)
target_link_libraries(taskledger PRIVATE taskledger_lib)

include(CTest)
if(BUILD_TESTING)
    add_executable(taskledger_tests tests/test_task.cpp)
    target_link_libraries(taskledger_tests PRIVATE taskledger_lib)
    add_test(NAME taskledger_tests COMMAND taskledger_tests)
endif()

