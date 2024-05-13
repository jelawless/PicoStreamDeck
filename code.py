import time
import digitalio
import board
import usb_hid
import digitalio
import rotaryio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.GP22,board.GP21,divisor=2)

btn1_pin = board.GP19
btn2_pin = board.GP18
btn3_pin = board.GP17
btn4_pin = board.GP16

keyboard = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)

btn1 = digitalio.DigitalInOut(btn1_pin)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

btn2 = digitalio.DigitalInOut(btn2_pin)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.DOWN

btn3 = digitalio.DigitalInOut(btn3_pin)
btn3.direction = digitalio.Direction.INPUT
btn3.pull = digitalio.Pull.DOWN

btn4 = digitalio.DigitalInOut(btn4_pin)
btn4.direction = digitalio.Direction.INPUT
btn4.pull = digitalio.Pull.DOWN

button_state = None
last_position = encoder.position

while True:
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            keyboard.send(ConsumerControlCode.VOLUME_INCREMENT)
        print(current_position)
    elif position_change < 0:
        for _ in range(-position_change):
            keyboard.send(ConsumerControlCode.VOLUME_DECREMENT)
        print(current_position)
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        print("Button pressed.")
        keyboard.send(ConsumerControlCode.PLAY_PAUSE)
        button_state = None
        
    if btn1.value:    
        kbd.send(Keycode.CONTROL,Keycode.SHIFT,Keycode.TAB)
        time.sleep(0.25)
    elif btn2.value:    
        kbd.send(Keycode.CONTROL,Keycode.TAB)
        time.sleep(0.25)
    elif btn3.value:    
        kbd.send(Keycode.ALT, Keycode.TAB)
        time.sleep(0.25)
    elif btn4.value:    
        kbd.send(Keycode.GUI, Keycode.L)
        time.sleep(0.25)