from onavi_sensor import OnaviSensor
from logger import Logger


def main():
    sensor = OnaviSensor()


    with Logger(sensor) as logger:
        logger.loop()


if __name__ == '__main__':
    main()
