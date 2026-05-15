#ifndef KEY_PROCESSOR_HPP
#define KEY_PROCESSOR_HPP

enum class Mode { NORMAL, INVERT, CANNY, GRAY, GLITCH, FACE };

class KeyProcessor {
public:
    Mode process(int key);
private:
    Mode currentMode = Mode::NORMAL;
};

#endif