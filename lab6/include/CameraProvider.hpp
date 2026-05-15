#ifndef CAMERA_PROVIDER_HPP
#define CAMERA_PROVIDER_HPP

#include <opencv2/opencv.hpp>

class CameraProvider {
public:
    CameraProvider(int deviceID = 0);
    cv::Mat getFrame();
    bool isOpened();
private:
    cv::VideoCapture cap;
};

#endif