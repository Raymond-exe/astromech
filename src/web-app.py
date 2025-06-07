from flask import Flask, Response, request, jsonify
import io
from picamera2 import Picamera2
from libcamera import controls
from PIL import Image
import struct
import subprocess
import time
from threading import Thread
from PiPCA9685 import PCA9685

# Modified from tutorial: https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/



# # # # # # # # # # # # # # # # # #
#         CONFIG SETTINGS         #
# # # # # # # # # # # # # # # # # #

STREAM_RESOLUTION = (720, 540)

SERVO_PWM_NEUTRAL = 450
SERVO_PWM_SCALE = 350
SERVO_FREQ = 60

LEFT_SERVO = 0
RIGHT_SERVO = 1
HEAD_SERVO = 15

########## DO NOT TOUCH ##########
app = Flask(__name__)
wifi_device = "wlan0"

pca = PCA9685()
pca.set_pwm_freq(SERVO_FREQ)
##################################



# # # # # # # # # # # # # # # # # # # # # # # # #
#         DROID SERVO CONTROL + WEBPAGE         #
# # # # # # # # # # # # # # # # # # # # # # # # #

@app.route('/control')
def webpg_control():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Droid Control</title>
        <link rel="stylesheet" type="text/css" href="/static/control.css">
    </head>
    <body>
        <img id="video-background" src="/video" class="flip-img"/>

        <div id="left-touch" class="control-area"></div>
        <div id="right-touch" class="control-area"></div>
        <script src="/static/control.js"></script>
        <script src="/static/audio.js"></script>
    </body>
    </html>
    """

@app.route('/touch', methods=['POST'])
def handle_touch():
    data = request.get_json()
    zone = data.get('zone')
    x = data.get('x')
    y = data.get('y')

    if (zone == 'left'):
        leftSpeed = motorTransferFunction(x, y)
        rightSpeed = motorTransferFunction(-x, y)
        pca.set_pwm(LEFT_SERVO, 0, pwmFrom(leftSpeed))
        pca.set_pwm(RIGHT_SERVO, 0, pwmFrom(rightSpeed))

    if (zone == 'right'):
        pca.set_pwm(HEAD_SERVO, 0, pwmFrom(x))

    return jsonify(status="ok")

# speed: -1.0 -> 1.0
def pwmFrom(speed):
    if (speed > +1.0): speed = +1.0
    if (speed < -1.0): speed = -1.0
    return round(speed * SERVO_PWM_SCALE) + SERVO_PWM_NEUTRAL

# https://www.desmos.com/3d/ql8ob6axnw
# converts X/Y coords to a speed from -1 -> 1
def motorTransferFunction(x, y):
    absX = abs(x)
    absY = abs(y)
    if (x * y <= 0):
        return max(absX, absY) * (1 if y >= 0 else -1)
    elif (absX <= absY):
        return y - 0.5 * x
    elif (absX >= absY):
        return -x + 1.5 * y
    return 0

@app.route('/debug', methods=['POST'])
def debugPrint():
    print(request.data)
    return jsonify(status="ok")



# # # # # # # # # # # # # # # # # # # #
#         WIFI CONFIG WEBPAGE         #
# # # # # # # # # # # # # # # # # # # #

@app.route('/wifi')
def webpg_wifi():
    result = subprocess.check_output(["nmcli", "--colors", "no", "-m", "multiline", "--get-value", "SSID", "dev", "wifi", "list", "ifname", wifi_device])
    ssids_list = result.decode().split('\n')
    dropdowndisplay = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Astromech Wifi Config</title>
        </head>
        <body>
            <h1>Astromech Wifi Configuration</h1>
            <form action="/submit" method="post">
                <label for="ssid">Choose a WiFi network:</label>
                <select name="ssid" id="ssid">
        """
    for ssid in ssids_list:
        only_ssid = ssid.removeprefix("SSID:")
        if len(only_ssid) > 0:
            dropdowndisplay += f"""
                    <option value="{only_ssid}">{only_ssid}</option>
            """
    dropdowndisplay += f"""
                </select>
                <p/>
                <label for="password">Password: <input type="password" name="password"/></label>
                <p/>
                <input type="submit" value="Connect">
            </form>
        </body>
        </html>
        """
    return dropdowndisplay

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        print(*list(request.form.keys()), sep = ", ")
        ssid = request.form['ssid']
        password = request.form['password']
        connection_command = ["nmcli", "--colors", "no", "device", "wifi", "connect", ssid, "ifname", wifi_device]
        if len(password) > 0:
          connection_command.append("password")
          connection_command.append(password)
        result = subprocess.run(connection_command, capture_output=True)
        if result.stderr:
            return "Error: failed to connect to wifi network: <i>%s</i>" % result.stderr.decode()
        elif result.stdout:
            return "Success: <i>%s</i>" % result.stdout.decode()
        return "Error: failed to connect."



# # # # # # # # # # # # # # # # # # # # # # # #
#         VIDEO STREAM INIT + WEBPAGE         #
# # # # # # # # # # # # # # # # # # # # # # # #

camera = None # initialized in init_camera()
frame_buffer = None # Background camera thread to transfer frames

# Initialize camera
def init_camera():
    global camera
    # print("Initializing Picamera2()...")
    camera = Picamera2()
    camera.configure(camera.create_video_configuration(main={"size": STREAM_RESOLUTION}))
    camera.start()
    # camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    # print("Camera initialized successfully!")

def capture_frames():
    global frame_buffer, camera
    while (True):
        if (camera is not None):
            frame = camera.capture_array()
            img = Image.fromarray(frame).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            frame_buffer = buf.getvalue()
        time.sleep(0.05)  # ~20 FPS

video_thread = Thread(target=init_camera)
video_thread.start()
frame_thread = Thread(target=capture_frames, daemon=True)
frame_thread.start()

@app.route('/video')
def webpg_video():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_stream():
    while True:
        if frame_buffer is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   frame_buffer + b'\r\n')
        time.sleep(0.05)



# # # # # # # # # # # # # # # # # # # # # # # #
#         AUDIO STREAM INPUT / OUTPUT         #
# # # # # # # # # # # # # # # # # # # # # # # #

# Pi mic -> iPhone speaker
@app.route('/audio') 
def audio_tx():
    def generate():
        cmd = [ 'ffmpeg', '-f', 'alsa', '-ac', '1', '-i', 'hw:0', '-acodec', 'libopus', '-ar', '48000', '-f', 'ogg', '-' ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        while True:
            data = process.stdout.read(4096)
            if not data:
                break
            yield data

    return Response(generate(), mimetype='audio/ogg')

# iPhone mic -> Pi speaker
@app.route('/mic', methods=['POST'])
def audio_rx():
    proc = subprocess.Popen(
        ['ffmpeg', '-i', '-', '-f', 'alsa', '-ac', '1', 'hw:1'],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    proc.stdin.write(request.data)
    proc.stdin.close()
    proc.wait()
    return "ok"


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=80)
