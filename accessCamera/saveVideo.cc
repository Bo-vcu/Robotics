#include <opencv2/opencv.hpp>
#include <iostream>
#include <array>

int main(int argc, char** argv) {
    // std::string IpLastSegment = "15";
    std::string IpLastSegment = "162";
    int cam = 1;
    if (argc >= 2)
        cam = std::atoi(argv[1]);
    std::string udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port=";
    // Ports: front, chin, left, right, abdomen
    std::array<int, 5> udpPORT = {9201, 9202, 9203, 9204, 9205};
    std::string udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink";
    std::string udpSendIntegratedPipe = udpstrPrevData + std::to_string(udpPORT[cam - 1]) + udpstrBehindData;
    std::cout << "udpSendIntegratedPipe: " << udpSendIntegratedPipe << std::endl;
    cv::VideoCapture cap(udpSendIntegratedPipe);
    if (!cap.isOpened())
        return 0;

    // Define the codec and create VideoWriter object.
    // 'XVID' is a codec for .avi files. You can use 'MJPG' for .avi or 'mp4v' for .mp4 files.
    int codec = cv::VideoWriter::fourcc('m', 'p', '4', 'v');
    // Specify the output file name, codec, frame rate, and frame size
    cv::VideoWriter outputVideo("output.mp4", codec, 30.0, cv::Size((int)cap.get(cv::CAP_PROP_FRAME_WIDTH), (int)cap.get(cv::CAP_PROP_FRAME_HEIGHT)));

    if (!outputVideo.isOpened()) {
        std::cout << "Could not open the output video file for write" << std::endl;
        return -1;
    }

    cv::Mat frame;
    while (true) {
        cap >> frame;
        if (frame.empty())
            break;

        // Write the frame into the file
        outputVideo.write(frame);
    }

    cap.release(); // Release resources
    outputVideo.release(); // Release the VideoWriter
    return 0;
}
