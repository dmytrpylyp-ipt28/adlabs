#include "CameraProvider.hpp"

CameraProvider::CameraProvider(std::string source) {
    if (source == "0") {
        cap.open(0);
    } else {
        cap.open(source);
    }
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}

bool CameraProvider::isOpened() {
    return cap.isOpened();
}
