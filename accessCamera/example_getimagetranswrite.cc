/**
 * @file example_getRectFrame.cc
 * @brief This file is part of UnitreeCameraSDK.
 * @details This example demonstrates how to receive and save video frames via UDP.
 * @author SunMingzhe
 * @date 2021.12.07
 * @version 1.1.0
 * @copyright Copyright (c) 2020-2021, Hangzhou Yushu Technology Stock CO.LTD. All Rights Reserved.
 */

#include <opencv2/opencv.hpp>
#include <iostream>
#include <array>

int main(int argc, char** argv)
{
    std::string IpLastSegment = "162"; // Example IP segment, modify as needed
    int cam = 1;
    if (argc >= 2)
        cam = std::atoi(argv[1]);

    std::string udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port=";
    std::array<int, 5> udpPORT = {9201, 9202, 9203, 9204, 9205};
    std::string udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink";
    std::string udpSendIntegratedPipe = udpstrPrevData + std::to_string(udpPORT[cam - 1]) + udpstrBehindData;

    std::cout << "udpSendIntegratedPipe: " << udpSendIntegratedPipe << std::endl;

    cv::VideoCapture cap(udpSendIntegratedPipe);
    if (!cap.isOpened()) {
        std::cerr << "Error: Unable to open video stream" << std::endl;
        return 1;
    }

    cv::Mat frame;
    int frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    cv::VideoWriter video("outputVideo.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 20, cv::Size(frame_width, frame_height));

    if (!video.isOpened()) {
        std::cerr << "Error: Could not open the output video file for write" << std::endl;
        return 1;
    }

    while (true) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Error: Empty frame" << std::endl;
            break;
        }

        video.write(frame);
        cv::imshow("Frame", frame);
        if (cv::waitKey(30) >= 0) break; // Exit if any key is pressed
    }

    cap.release();
    video.release();
    cv::destroyAllWindows();

    return 0;
}
