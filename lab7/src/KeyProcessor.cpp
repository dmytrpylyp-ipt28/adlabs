#include "KeyProcessor.hpp"

Mode KeyProcessor::process(int key) {
    if (key == '0') currentMode = Mode::NORMAL;
    else if (key == '1') currentMode = Mode::INVERT;
    else if (key == '2') currentMode = Mode::CANNY;
    else if (key == '3') currentMode = Mode::GRAY;
    else if (key == '4') currentMode = Mode::GLITCH;
    else if (key == 'f' || key == 'F') currentMode = Mode::FACE;
    
    return currentMode;
}