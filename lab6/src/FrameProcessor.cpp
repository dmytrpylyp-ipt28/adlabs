#include "FrameProcessor.hpp"

void FrameProcessor::process(cv::Mat& frame, Mode mode) {
    if (frame.empty()) return;

    if (mode == Mode::INVERT) {
        cv::bitwise_not(frame, frame);
    } 
    else if (mode == Mode::CANNY) {
        cv::Mat gray, edges;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::Canny(gray, edges, 100, 200);
        cv::cvtColor(edges, frame, cv::COLOR_GRAY2BGR);
    } 
    else if (mode == Mode::GRAY) {
        cv::Mat gray;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::cvtColor(gray, frame, cv::COLOR_GRAY2BGR);
    }
    else if (mode == Mode::GLITCH) {
        std::vector<cv::Mat> channels;
        cv::split(frame, channels);
        cv::copyMakeBorder(channels[2], channels[2], 0, 0, 20, 0, cv::BORDER_CONSTANT, 0);
        channels[2] = channels[2](cv::Rect(0, 0, frame.cols, frame.rows));
        cv::merge(channels, frame);
    }
    
    cv::putText(frame, "Mode ID: " + std::to_string((int)mode), 
                cv::Point(20, 40), cv::FONT_HERSHEY_SIMPLEX, 0.8, 
                cv::Scalar(0, 255, 255), 2);
}