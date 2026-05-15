#include "CameraProvider.hpp"

CameraProvider::CameraProvider(int deviceID) {
    cap.open(deviceID);
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}

bool CameraProvider::isOpened() {
    return cap.isOpened();
}