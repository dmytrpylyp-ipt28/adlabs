#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"

int main() {

    CameraProvider camera("demo.mp4");

    if (!camera.isOpened()) {
        std::cerr << "Error: Camera not found!" << std::endl;
        return -1;
    }

    FrameProcessor processor;
    KeyProcessor keyHandler;
    
    const std::string winName = "OpenCV Lab 6";
    cv::namedWindow(winName, cv::WINDOW_AUTOSIZE);
    
    Mode currentMode = Mode::NORMAL;

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        int key = cv::waitKey(30);
        if (key == 27) break;

        currentMode = keyHandler.process(key);
        processor.process(frame, currentMode);

        cv::imshow(winName, frame);
    }

    cv::destroyAllWindows();
    return 0;

}
