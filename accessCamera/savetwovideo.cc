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
    int cam1 = 1;
    int cam2 = 2;

    if (argc >= 3) {
        cam1 = std::atoi(argv[1]);
        cam2 = std::atoi(argv[2]);
    }

    std::string udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port=";
    std::array<int, 5> udpPORT = {9201, 9202, 9203, 9204, 9205};
    std::string udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink";

    std::string udpSendIntegratedPipe1 = udpstrPrevData + std::to_string(udpPORT[cam1 - 1]) + udpstrBehindData;
    std::string udpSendIntegratedPipe2 = udpstrPrevData + std::to_string(udpPORT[cam2 - 1]) + udpstrBehindData;

    std::cout << "udpSendIntegratedPipe1: " << udpSendIntegratedPipe1 << std::endl;
    std::cout << "udpSendIntegratedPipe2: " << udpSendIntegratedPipe2 << std::endl;

    cv::VideoCapture cap1(udpSendIntegratedPipe1);
    if (!cap1.isOpened()) {
        std::cerr << "Error: Unable to open video stream from camera 1" << std::endl;
        return 1;
    }

    cv::VideoCapture cap2(udpSendIntegratedPipe2);
    if (!cap2.isOpened()) {
        std::cerr << "Error: Unable to open video stream from camera 2" << std::endl;
        return 1;
    }

    cv::Mat frame1, frame2;
    int frame_width1 = static_cast<int>(cap1.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height1 = static_cast<int>(cap1.get(cv::CAP_PROP_FRAME_HEIGHT));
    int frame_width2 = static_cast<int>(cap2.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height2 = static_cast<int>(cap2.get(cv::CAP_PROP_FRAME_HEIGHT));

    cv::VideoWriter video1("outputVideo1.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 20, cv::Size(frame_width1, frame_height1));
    if (!video1.isOpened()) {
        std::cerr << "Error: Could not open the output video file for write from camera 1" << std::endl;
        return 1;
    }

    cv::VideoWriter video2("outputVideo2.avi", cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 20, cv::Size(frame_width2, frame_height2));
    if (!video2.isOpened()) {
        std::cerr << "Error: Could not open the output video file for write from camera 2" << std::endl;
        return 1;
    }

    while (true) {
        cap1 >> frame1;
        cap2 >> frame2;

        if (frame1.empty() || frame2.empty()) {
            std::cerr << "Error: Empty frame" << std::endl;
            break;
        }

        video1.write(frame1);
        video2.write(frame2);

        cv::imshow("Camera 1 Frame", frame1);
        cv::imshow("Camera 2 Frame", frame2);
        if (cv::waitKey(30) >= 0) break; // Exit if any key is pressed
    }

    cap1.release();
    cap2.release();
    video1.release();
    video2.release();
    cv::destroyAllWindows();

    return 0;
}
