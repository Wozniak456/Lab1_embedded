from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""

        if not self.accelerometer_file or not self.gps_file:
            raise ValueError("Files not opened for reading.")

        while True:
            accelerometer_data = self.accelerometer_file.readline().strip().split(',')
            gps_data = self.gps_file.readline().strip().split(',')

            if accelerometer_data and gps_data:
                try:
                    accelerometer = Accelerometer(int(accelerometer_data[0]), int(accelerometer_data[1]),
                                                  int(accelerometer_data[2]))
                    gps = Gps(float(gps_data[0]), float(gps_data[1]))
                    time = datetime.now()
                    return AggregatedData(accelerometer, gps, time, config.USER_ID)
                except Exception as e:
                    print(f"Error reading data from files: {e}")
                    self.gps_file.seek(0)
                    self.gps_file.readline()
                    self.read()

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        try:
            self.accelerometer_file = open(self.accelerometer_filename, 'r')
            self.gps_file = open(self.gps_filename, 'r')

            self.accelerometer_file.readline()
            self.gps_file.readline()
        except Exception as e:
            print(f"Error opening files: {e}")
            raise

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
