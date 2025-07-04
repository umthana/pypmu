import random
import math

from synchrophasor.frame import ConfigFrame2
from synchrophasor.pmu import Pmu


"""
randomPMU will listen on ip:port for incoming connections.
After request to start sending measurements - random
values for phasors will be sent.
"""


if __name__ == "__main__":

    pmu = Pmu(ip="127.0.0.1", port=1410)
    pmu.logger.setLevel("DEBUG")
    
    ph_v_conversion = int(400 / 65535 * 100000)  # Voltage phasor conversion factor
    ph_i_conversion = int(100 / 32768 * 100000)  # Current phasor conversion factor

    cfg = ConfigFrame2(
        1410,  # PMU_ID (use the port as ID if needed, or set as required)
        1000000,  # TIME_BASE
        3,  # Number of PMUs included in data frame
        ['Station A', 'Station B', 'Station C'],  # Station names
        [1, 2, 3],  # Data-stream ID(s)
        [(True, False, True, False), 
         (True, False, True, False),   # Data format (COORD_TYPE, PHASOR_TYPE, ANALOG_TYPE, FREQ_TYPE)
         (True, False, True, False)],  # TYPE: true = float/polar, false = integer/rectangular.
        [2, 2, 2],  # Number of phasors
        [0, 0, 0],  # Number of analog values
        [0, 0, 0],  # Number of digital status words
        [['Va', 'Ia'], ['Vb', 'Ib'], ['Vc', 'Ic']],  # Channel Names (padded)
        [[(ph_v_conversion, 'v'), (ph_i_conversion, 'i')], 
         [(ph_v_conversion, 'v'), (ph_i_conversion, 'i')], 
         [(ph_v_conversion, 'v'), (ph_i_conversion, 'i')]],  # Phasor units
        [[], [], []],  # Analog units
        [[], [], []],  # Digital units
        [50, 50, 50],  # Nominal frequency
        [0, 0, 0],  # Configuration change count
        50  # Data rate
    )

    pmu.set_configuration(cfg)
    pmu.set_header("Hey! I'm randomPMU! Guess what? I'm sending random measurements values!")

    pmu.run()

    while True:
        if pmu.clients:
            pmu.send_data(
                phasors=[
                    [
                        (random.uniform(220, 230), 0),  # Station A, Va
                        (10, -math.pi/6)    # Station A, Ia
                    ],
                    [
                        (random.uniform(220, 230), -2*math.pi/3),  # Station B, Vb
                        (10, -5*math.pi/6)   # Station B, Ib
                    ],
                    [
                        (random.uniform(220, 230), 2*math.pi/3), # Station C, Vc
                        (10, math.pi/2)   # Station C, Ic
                    ]
                ],
                stat=[0, 0, 0],
                analog=[[], [], []],   # No analog values
                digital=[[], [], []],   # No digital values
                freq=[0, 0, 0],  # frequency
                dfreq=[0, 0, 0] # Rate of change of frequency
            )

    pmu.join()
