from dataclasses import dataclass


@dataclass
class GMeasurement:
    x: float
    y: float
    z: float
    time: float

    @property
    def to_list(self):
        return [self.time, round(self.x, 18), round(self.y, 18), round(self.z, 18)]


@dataclass
class MssMeasurement:
    x: float
    y: float
    z: float
    time: float
    
    @property
    def to_g(self) -> GMeasurement:
        return GMeasurement(self.x / 9.80665, self.y / 9.80665, self.z / 9.80665, self.time)
    
    @property
    def to_list(self):
        return [self.time, round(self.x, 18), round(self.y, 18), round(self.z, 18)]
