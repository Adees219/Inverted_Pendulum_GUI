

import json

class ConfigModel:

    def __init__(self):

        #valores iniciales
        self.type = "system_config"

        self.amperaje = 800

        self.microstep = 16

        self.velocidad_maxima = 32000

        self.aceleracion = 150000

        self.control_period_us = 1000

        self.telemetry_period_ms = 20

        self.offset_AS5600 = 283.0

    def to_dict(self):
        #formato
        return {
            "type": self.type,
            "current_ma": self.amperaje,
            "microsteps": self.microstep,
            "max_speed_steps_s": self.velocidad_maxima,
            "acceleration_steps_s2": self.aceleracion,
            "control_period_us": self.control_period_us,
            "telemetry_period_ms": self.telemetry_period_ms,
            "encoder_offset_deg": self.offset_AS5600
        }
    
    def to_json(self):
        #json
        return json.dumps(
            self.to_dict(),
            indent=4
        )
    