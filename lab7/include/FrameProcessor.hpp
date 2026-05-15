#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    FrameProcessor();
    void process(cv::Mat& frame, Mode mode);
private:
    cv::dnn::Net net;
    void detectFaces(cv::Mat& frame);
};

#endif