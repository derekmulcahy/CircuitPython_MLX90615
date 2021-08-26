"""
`mlx90615`
====================================================

CircuitPython module for the MLX90615 IR object temperature sensor.

* Author(s): Mikey Sklar based on code from these projects:
  Limor Fried - https://github.com/adafruit/Adafruit-MLX90614-Library
  Bill Simpson - https://github.com/BillSimpson/ada_mlx90614
  Mike Causer - https://github.com/mcauser/micropython-mlx90614
  Adafruit - https://github.com/adafruit/Adafruit_CircuitPython_MLX90614

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from micropython import const

import adafruit_bus_device.i2c_device as i2c_device


# imports

__version__ = "1.0.0"
__repo__= "https://github.com/derekmulcahy/CircuitPython_MLX90615"

# Internal constants:
_MLX90615_I2CADDR = const(0x5B)

# RAM
_MLX90615_RAWIR = const(0x05)
_MLX90615_TA = const(0x26)
_MLX90615_TO = const(0x27)

# EEPROM
_MLX90615_PWMTMIN = const(0x00)
_MLX90615_PWMTRANGE = const(0x01)
_MLX90615_CONFIG = const(0x02)
_MLX90615_EMISS = const(0x03)
_MLX90615_ID1 = const(0x0E)
_MLX90615_ID2 = const(0x0F)


class MLX90615:
    """Create an instance of the MLX90615 temperature sensor.

    :param ~busio.I2C i2c_bus: The I2C bus the MLX90615 is connected to.
                               Do not use an I2C bus speed of 400kHz. The sensor only works
                               at the default bus speed of 100kHz.
    :param int address: I2C device address. Defaults to :const:`0x5B`.

    **Quickstart: Importing and using the MLX90615**

        Here is an example of using the :class:`MLX90615` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            import mlx90615

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()
            mlx = mlx90615.MLX90615(i2c)

        Now you have access to the :attr:`object_temperature` attribute

        .. code-block:: python

            temperature = mlx.object_temperature

    """

    def __init__(self, i2c_bus, address=_MLX90615_I2CADDR):
        self._device = i2c_device.I2CDevice(i2c_bus, address)
        self.buf = bytearray(2)

    @property
    def ambient_temperature(self):
        """Ambient Temperature in Celsius."""
        return self._read_temp(_MLX90615_TA)

    @property
    def object_temperature(self):
        """Object Temperature in Celsius."""
        return self._read_temp(_MLX90615_TO)

    def _read_temp(self, register):
        temp = self._read_16(register)
        temp *= 0.02
        temp -= 273.15
        return temp

    def _read_16(self, register):
        # Read and return a 16-bit unsigned big endian value read from the
        # specified 16-bit register address.
        with self._device as i2c:
            self.buf[0] = register
            i2c.write_then_readinto(self.buf, self.buf, out_end=1)
            return self.buf[1] << 8 | self.buf[0]
