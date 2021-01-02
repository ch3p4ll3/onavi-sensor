import subprocess
import os


def get_sensor_path():
	sensor_id = "04e2_1410"
	proc = subprocess.Popen(['ls', '/dev/serial/by-id/'], stdout=subprocess.PIPE)
	proc = proc.stdout.read().decode()

	for i in proc.split("\n"):
		if sensor_id in i:
			return os.path.realpath(f"/dev/serial/by-id/{i}")
