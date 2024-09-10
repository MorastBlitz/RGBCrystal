import os
import wifi
import socketpool
import time
import board
import neopixel

from adafruit_httpserver import Server, Request, Response, GET, NO_REQUEST, REQUEST_HANDLED_RESPONSE_SENT
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import AMBER, AQUA, GOLD, OLD_LACE, PURPLE, JADE

colors = [AMBER, AQUA, GOLD, OLD_LACE, PURPLE, JADE]
global i
i = 0

#print(dir(board))
pixel_pin = board.D1
num_pixels = 12
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.4, auto_write=False, pixel_order=ORDER
)

pulse_amber = Pulse(pixels, speed=0.1, color=AMBER, period=8, breath=1, min_intensity=0.1)
pulse_aqua = Pulse(pixels, speed=0.1, color=AQUA, period=8, breath=1, min_intensity=0.1)
rainbow = Rainbow(pixels, speed=0.1, period=8)
sparkle_amber = Sparkle(pixels, speed=0.3, color=AMBER, num_sparkles=2)
sparkle_aqua = Sparkle(pixels, speed=0.3, color=AQUA, num_sparkles=2)


pixels.fill(AMBER)
pixels.show()


HTML_TEMPLATE = """
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ESP32-S3-Zero HTTPServer</title>
    </head>
    <body>
        <p><strong>Crystal Control Center</stong></p>
        
        <p>Current Status: {insert}</P>

        <a href="/">
            <button>Crystal OFF</button>
        </a><br /><br />
        <a href="/change_bright">
            <button>Change Brightness</button>
        </a><br /><br />
        <a href="/change_color">
            <button>Change Color</button>
        </a><br /><br />
        <a href="/pulse_amber">
            <button>Pulse Amber</button>
        </a><br /><br />
        <a href="/pulse_aqua">
            <button>Pulse Aqua</button>
        </a><br /><br />
        <a href="/rainbow">
            <button>Rainbow</button>
        </a><br /><br />
        <a href="/sparkle_amber">
            <button>Sparkle Amber</button>
        </a><br /><br />
        <a href="/sparkle_aqua">
            <button>Sparkle Aqua</button>
        </a><br /><br />

    </body>
</html>
"""

#ipv4 =  ipaddress.IPv4Address("192.168.1.42")
#netmask =  ipaddress.IPv4Address("255.255.255.0")
#gateway =  ipaddress.IPv4Address("192.168.1.1")
#wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)

print()
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

global request_path
request_path = '/'

@server.route("/", GET)
def client(request: Request):

    pixels.fill((0, 0, 0))
    pixels.show()

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("OFF")), content_type="text/html")


@server.route("/change_bright", GET)
def client(request: Request):

    if pixels.brightness == 0.2:
        pixels.brightness=0.4
    elif pixels.brightness == 0.4:
        pixels.brightness=0.6
    elif pixels.brightness == 0.6:
        pixels.brightness=0.8
    elif pixels.brightness == 0.8:
        pixels.brightness=1
    elif pixels.brightness == 1:
        pixels.brightness=0.2

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Brightness: " + str(pixels.brightness))), content_type="text/html")


@server.route("/change_color", GET)
def client(request: Request):

    global i

    pixels.fill(colors[i])
    pixels.show()

    i += 1
    if i == 6:
        i = 0

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=(colors[i])), content_type="text/html")


@server.route("/pulse_amber", GET)
def client(request: Request):

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Pulse Amber")), content_type="text/html")


@server.route("/pulse_aqua", GET)
def client(request: Request):

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Pulse Aqua")), content_type="text/html")


@server.route("/rainbow", GET)
def client(request: Request):

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Rainbow")), content_type="text/html")


@server.route("/sparkle_amber", GET)
def client(request: Request):

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Sparkle Amber")), content_type="text/html")


@server.route("/sparkle_aqua", GET)
def client(request: Request):

    global request_path
    request_path = request.path

    return Response(request, HTML_TEMPLATE.format(insert=("Sparkle Aqua")), content_type="text/html")


server.start(str(wifi.radio.ipv4_address))


while True:
    try:
        pool_result = server.poll()

        if request_path == '/pulse_amber':
            pulse_amber.animate()

        if request_path == '/pulse_aqua':
            pulse_aqua.animate()

        if request_path == '/rainbow':
            rainbow.animate()

        if request_path == '/sparkle_amber':
            sparkle_amber.animate()

        if request_path == '/sparkle_aqua':
            sparkle_aqua.animate()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            print(pool_result)
            print(request_path)
            pass

    except OSError as error:
        print(error)
        continue
   
