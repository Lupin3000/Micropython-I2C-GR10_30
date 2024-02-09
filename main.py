from lib.DFRobot_GR10_30_I2C import (DFRobot_GR10_30_I2C, GESTURE_UP, GESTURE_DOWN, GESTURE_LEFT, GESTURE_RIGHT,
                                     GESTURE_FORWARD, GESTURE_BACKWARD, GESTURE_CLOCKWISE_C, GESTURE_COUNTERCLOCKWISE_C)
from micropython import const
from utime import sleep


SDA_PIN = const(21)
SCL_PIN = const(22)


def setup(sensor) -> None:
    """
    Set up the DFRobot GR10_30 sensor
    :param sensor: instance of DFRobot_GR10_30_I2C
    :return: None
    """
    while not sensor.begin():
        print('Try sensor initialization')
        sleep(1)

    print('Sensor initialized')
    sensor.en_gestures(GESTURE_UP | GESTURE_DOWN |
                       GESTURE_LEFT | GESTURE_RIGHT |
                       GESTURE_FORWARD | GESTURE_BACKWARD |
                       GESTURE_CLOCKWISE_C | GESTURE_COUNTERCLOCKWISE_C)


def get_gestures(sensor) -> int:
    """
    Get the gesture if from the GR_10_30 sensor
    :param sensor: instance of DFRobot_GR10_30_I2C
    :return: int
    """
    gesture_id: int = 0

    if sensor.get_data_ready():
        gesture_id = sensor.get_gestures()

    return gesture_id


if __name__ == '__main__':
    gesture_sensor = DFRobot_GR10_30_I2C(sda=SDA_PIN, scl=SCL_PIN)
    setup(sensor=gesture_sensor)

    print('Start hand gestures:')

    while True:
        gesture = get_gestures(sensor=gesture_sensor)

        if gesture == GESTURE_UP:
            print(f'Gesture: {gesture} up')

        if gesture & GESTURE_DOWN:
            print(f'Gesture: {gesture} down')

        if gesture & GESTURE_LEFT:
            print(f'Gesture: {gesture} left')

        if gesture == GESTURE_RIGHT:
            print(f'Gesture: {gesture} right')

        if gesture == GESTURE_FORWARD:
            print(f'Gesture: {gesture} forward')

        if gesture == GESTURE_BACKWARD:
            print(f'Gesture: {gesture} backward')

        if gesture == GESTURE_CLOCKWISE_C:
            print(f'Gesture: {gesture} clockwise continues')

        if gesture == GESTURE_COUNTERCLOCKWISE_C:
            print(f'Gesture: {gesture} counter clockwise continues')

        sleep(0.1)
