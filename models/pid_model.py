import json


class PIDModel:


    UP = "up"
    DOWN = "down"

    def __init__(self):


        self.mode = self.DOWN

        self.kp = 900.0

        self.ki = 0.001

        self.kd = 0.001

    def to_dict(self):


        return {

            "mode": self.mode,

            "kp": self.kp,

            "ki": self.ki,

            "kd": self.kd
        }

    def to_json(self):

        return json.dumps(
            self.to_dict(),
            indent=4  
        )