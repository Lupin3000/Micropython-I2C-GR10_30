from micropython import const
from machine import I2C, Pin
from utime import sleep


GR10_30_I2C_ADDR = const(0x73)

GR30_10_INPUT_REG_ADDR = const(0x02)
GR30_10_INPUT_REG_DATA_READY = const(0x06)
GR30_10_INPUT_REG_INTERRUPT_STATE = const(0x07)
GR30_10_INPUT_REG_EXIST_STATE = const(0x08)

GR30_10_HOLDING_REG_INTERRUPT_MODE = const(0x09)
GR30_10_HOLDING_REG_RESET = const(0x18)

GESTURE_UP = (1 << 0)
GESTURE_DOWN = (1 << 1)
GESTURE_LEFT = (1 << 2)
GESTURE_RIGHT = (1 << 3)
GESTURE_FORWARD = (1 << 4)
GESTURE_BACKWARD = (1 << 5)
GESTURE_CLOCKWISE = (1 << 6)
GESTURE_COUNTERCLOCKWISE = (1 << 7)
GESTURE_WAVE = (1 << 8)
GESTURE_HOVER = (1 << 9)
GESTURE_UNKNOWN = (1 << 10)
GESTURE_CLOCKWISE_C = (1 << 14)
GESTURE_COUNTERCLOCKWISE_C = (1 << 15)


class DFRobot_GR10_30_I2C:
    """
    MicroPython class for communication with the GR10_30 from DFRobot via I2C
    """

    def __init__(self, sda, scl, i2c_addr=GR10_30_I2C_ADDR, i2c_bus=0):
        """
        Initialize the DFRobot_GR10_30 communication
        :param sda: I2C SDA Pin
        :param scl: I2C SCL Pin
        :param i2c_addr: I2C address
        :param i2c_bus: I2C bus number
        """
        self._addr = i2c_addr
        self._temp_buffer = [0] * 2

        try:
            self._i2c = I2C(i2c_bus, sda=Pin(sda), scl=Pin(scl))
        except Exception as err:
            print(print(f'Could not initialize i2c! bus: {i2c_bus}, sda: {sda}, scl: {scl}, error: {err}'))

    def _write_reg(self, reg, data) -> None:
        """
        Write data to the I2C register
        :param reg: register address
        :param data: data to write
        :return: None
        """
        if isinstance(data, int):
            data = [data]

        try:
            self._i2c.writeto_mem(self._addr, reg, bytearray(data))
        except Exception as err:
            print(f'Write issue: {err}')

    def _read_reg(self, reg, length) -> bytes:
        """
        Reads data from the I2C register
        :param reg: I2C register address
        :param length: number of bytes to read
        :return: bytes
        """
        try:
            result = self._i2c.readfrom_mem(self._addr, reg, length)
        except Exception as err:
            print(f'Read issue: {err}')
            result = [0, 0]

        return result

    def _detect_device_address(self) -> int:
        """
        Detect I2C device address
        :return: int
        """
        r_buf = self._read_reg(GR30_10_INPUT_REG_ADDR, 2)
        data = r_buf[0] << 8 | r_buf[1]

        return data

    def _reset_sensor(self) -> None:
        """
        Reset sensor
        :return: None
        """
        self._temp_buffer[0] = 0x55
        self._temp_buffer[1] = 0x00
        self._write_reg(GR30_10_HOLDING_REG_RESET, self._temp_buffer)

        sleep(0.1)

    def begin(self) -> bool:
        """
        Initialise the sensor
        :return: bool
        """
        if self._detect_device_address() != GR10_30_I2C_ADDR:
            return False

        self._reset_sensor()
        sleep(0.5)

        return True

    def en_gestures(self, gestures) -> None:
        """
        Set what gestures the sensor can recognize
        :param gestures: constants combined with bitwise OR
        :return: None
        """
        gestures = gestures & 0xc7ff

        self._temp_buffer[0] = (gestures >> 8) & 0xC7
        self._temp_buffer[1] = gestures & 0x00ff
        self._write_reg(GR30_10_HOLDING_REG_INTERRUPT_MODE, self._temp_buffer)

        sleep(0.1)

    def get_exist(self) -> bool:
        """
        Get the existence of an object in the sensor detection range
        :return: bool
        """
        r_buf = self._read_reg(GR30_10_INPUT_REG_EXIST_STATE, 2)
        data = r_buf[0] * 256 + r_buf[1]

        return bool(data)

    def get_data_ready(self) -> bool:
        """
        Get if a gesture is detected
        :return: bool
        """
        r_buf = self._read_reg(GR30_10_INPUT_REG_DATA_READY, 2)
        data = r_buf[0] * 256 + r_buf[1]

        if data == 0x01:
            return True
        else:
            return False

    def get_gestures(self) -> int:
        """
        Get the gesture number of an gesture
        :return: int
        """
        r_buf = self._read_reg(GR30_10_INPUT_REG_INTERRUPT_STATE, 2)
        data = (r_buf[0] & 0xff) * 256 + r_buf[1]

        return int(data)
