// C++ code to capture video from UDP stream
#include <opencv2/opencv.hpp>
#include <iostream>
int main(int argc, char** argv)
{
    // std::string IpLastSegment = "15";
    std::string IpLastSegment = "162";
    int cam = 1;
    if (argc >= 2)
        cam = std::atoi(argv[1]);
    std::string udpstrPrevData = "udpsrc address=192.168.123." + IpLastSegment + " port=";
    std::array<int, 5> udpPORT = std::array<int, 5>{9201, 9202, 9203, 9204, 9205};
    // std::string udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! omxh264dec ! videoconvert ! appsink";
    std::string udpstrBehindData = " ! application/x-rtp,media=video,encoding-name=H264 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink";
    std::string udpSendIntegratedPipe = udpstrPrevData + std::to_string(udpPORT[cam - 1]) + udpstrBehindData;
    std::cout << "udpSendIntegratedPipe:" << udpSendIntegratedPipe << std::endl;
    cv::VideoCapture cap(udpSendIntegratedPipe);

    if (!cap.isOpened())
        return 0;
    cv::Mat frame;

    // hetzelfde als bij example get imagetrans

    // Python script to detect persons using YOLO model
    #include <pybind11/embed.h>
    namespace py = pybind11;
    py::scoped_interpreter guard{};
    py::object YOLO = py::module_::import("ultralytics").attr("YOLO");
    py::object model = YOLO("best.pt");
    py::object cv2 = py::module_::import("cv2");
    py::object math = py::module_::import("math");

    while (1)
    {
        cap >> frame;
        if (frame.empty())
            break;

        // Convert the frame to a Python object
        py::array_t<uint8_t> img = py::array_t<uint8_t>({ frame.rows, frame.cols, frame.channels() }, frame.data);

        // Run the YOLO model
        py::object results = model(img, py::arg("stream") = true);

        for (auto r : results)
        {
            auto boxes = r.attr("boxes");

            for (auto box : boxes)
            {
                auto xyxy = box.attr("xyxy")[0];
                int x1 = xyxy[0].cast<int>();
                int y1 = xyxy[1].cast<int>();
                int x2 = xyxy[2].cast<int>();
                int y2 = xyxy[3].cast<int>();

                cv::rectangle(frame, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(0, 0, 255), 3);

                float confidence = box.attr("conf")[0].cast<float>();
                confidence = std::ceil(confidence * 100) / 100;

                std::string text = "Person " + std::to_string(confidence);
                cv::putText(frame, text, cv::Point(x1, y1), cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(255, 0, 0), 2);
            }
        }

        cv::imshow("Video", frame);
        if (cv::waitKey(20) == 27) // Press 'ESC' to exit
            break;
    }
    cap.release(); // Release resources
    cv::destroyAllWindows();
    return 0;
}
