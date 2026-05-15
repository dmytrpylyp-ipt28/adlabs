#ifndef CAMERA_PROVIDER_HPP
#define CAMERA_PROVIDER_HPP

#include <opencv2/opencv.hpp>

#include <string>

class CameraProvider {
public:
    CameraProvider(std::string source);
    cv::Mat getFrame();
    bool isOpened();
private:
    cv::VideoCapture cap;
};

#endif
