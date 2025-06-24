import random

from synchrophasor.frame import ConfigFrame2
from synchrophasor.pmu import Pmu


"""
randomPMU will listen on ip:port for incoming connections.
After request to start sending measurements - random
values for phasors will be sent.
"""


if __name__ == "__main__":

    pmu = Pmu(ip="0.0.0.0", port=9991)
    pmu.logger.setLevel("DEBUG")

    cfg = ConfigFrame2(1,  # PMU_ID
                       1000000,  # TIME_BASE
                       1,  # Number of PMUs included in data frame
                       "Random Station",  # Station name
                       1,  # Data-stream ID(s)
                       (True, True, True, True),  # Data format - POLAR; PH - REAL; AN - REAL; FREQ - REAL;
                       6,  # Number of phasors
                       1,  # Number of analog values
                       1,  # Number of digital status words
                       ["VA", "VB", "VC", "IA", "IB", "IC", "ANALOG1", "BREAKER 1 STATUS",
                        "BREAKER 2 STATUS", "BREAKER 3 STATUS", "BREAKER 4 STATUS", "BREAKER 5 STATUS",
                        "BREAKER 6 STATUS", "BREAKER 7 STATUS", "BREAKER 8 STATUS", "BREAKER 9 STATUS",
                        "BREAKER A STATUS", "BREAKER B STATUS", "BREAKER C STATUS", "BREAKER D STATUS",
                        "BREAKER E STATUS", "BREAKER F STATUS", "BREAKER G STATUS"],  # Channel Names
                       [(0, "v"), (0, "v"), (0, "v"), (0, "i"), (0, "i"), (0, "i")],  # Conversion factor for phasor channels - (float representation, not important)
                       [(1, "pow")],  # Conversion factor for analog channels
                       [(0x0000, 0xffff)],  # Mask words for digital status words
                       50,  # Nominal frequency
                       1,  # Configuration change count
                       30)  # Rate of phasor data transmission)

    pmu.set_configuration(cfg)
    pmu.set_header("Hey! I'm randomPMU! Guess what? I'm sending random measurements values!")

    pmu.run()

    while True:
        if pmu.clients:
            pmu.send_data(phasors=[(random.uniform(215.0, 240.0), random.uniform(-0.017, 0.017)),
                                   (random.uniform(215.0, 240.0), random.uniform(2.077, 2.112)),
                                   (random.uniform(215.0, 240.0), random.uniform(-2.112, -2.077)),
                                   (random.uniform(4, 10)       , random.uniform(0.506, 0.541)),
                                   (random.uniform(4, 10)       , random.uniform(2.601, 2.635)),
                                   (random.uniform(4, 10)       , random.uniform(-1.588, -1.553))],
                          analog=[9.91],
                          digital=[0x0001])

    pmu.join()
