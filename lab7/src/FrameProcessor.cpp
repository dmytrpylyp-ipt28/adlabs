#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() {
    net = cv::dnn::readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
}

void FrameProcessor::detectFaces(cv::Mat& frame) {
    if (frame.empty()) return;

    int frameHeight = frame.rows;
    int frameWidth = frame.cols;

    cv::Mat blob = cv::dnn::blobFromImage(frame, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
    net.setInput(blob);
    
    cv::Mat detections = net.forward();

    cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

    for (int i = 0; i < detectionMat.rows; i++) {
        float confidence = detectionMat.at<float>(i, 2);

        if (confidence > 0.5) { // 
            int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameWidth);
            int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameHeight);
            int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameWidth);
            int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameHeight);

            // Малюємо рамку та текст
            cv::rectangle(frame, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(0, 255, 0), 2);
            std::string label = cv::format("Face: %.2f%%", confidence * 100);
            cv::putText(frame, label, cv::Point(x1, y1 - 10), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 2);
        }
    }
}

void FrameProcessor::process(cv::Mat& frame, Mode mode) {
    if (frame.empty()) return;

    if (mode == Mode::FACE) {
        detectFaces(frame);
    } 
    else if (mode == Mode::INVERT) {
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
}