# led_controller.py
import config

if config.ENABLE_LEDS:
    from gpiozero import LED

    # Using edge pins for physical convenience
    led_green = LED(16)
    led_blue = LED(20)
    led_red = LED(21)

    led_green.off()
    led_blue.off()
    led_red.off()


def update_leds(rpm_ratio):
    """Updates physical LEDs based on current RPM ratio."""
    if not config.ENABLE_LEDS:
        return

    if rpm_ratio >= 0.76:
        led_green.on()
    else:
        led_green.off()

    if rpm_ratio >= 0.85:
        led_blue.on()
    else:
        led_blue.off()

    if rpm_ratio >= 0.90:
        led_red.on()
    else:
        led_red.off()


def cleanup():
    """Turns off all LEDs safely before exit."""
    if config.ENABLE_LEDS:
        led_green.off()
        led_blue.off()
        led_red.off()
