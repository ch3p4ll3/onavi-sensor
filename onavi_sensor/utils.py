import subprocess
import os


class Utils:
    @staticmethod
    def get_sensor_serial_port() -> str:
        sensor_id = "04e2_1410"
        proc = subprocess.Popen(['ls', '/dev/serial/by-id/'], stdout=subprocess.PIPE)
        (output, err) = proc.communicate()
        proc.wait()

        for i in output.decode().split("\n"):
            if sensor_id in i:
                return os.path.realpath(f"/dev/serial/by-id/{i}")
