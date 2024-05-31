import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import sys

# Initialize GStreamer
Gst.init(None)

# Define the pipeline
pipeline = Gst.parse_launch(
    "udpsrc port=9201 ! "
    "application/x-rtp, media=video, encoding-name=H264 ! "
    "rtph264depay ! "
    "h264parse ! "
    "avdec_h264 ! "
    "videoconvert ! "
    "autovideosink"
)

# Create a GLib Main Loop
loop = GLib.MainLoop()

def on_message(bus, message):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-Of-Stream reached")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error received from element {}: {}".format(message.src.get_name(), err))
        print("Debugging information: {}".format(debug))
        loop.quit()

# Get the pipeline's bus and add the message handler
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", on_message)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

try:
    # Run the main loop
    loop.run()
except KeyboardInterrupt:
    pass

# Free resources
pipeline.set_state(Gst.State.NULL)