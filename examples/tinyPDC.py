from synchrophasor.pdc import Pdc
from synchrophasor.frame import DataFrame

"""
tinyPDC will connect to pmu_ip:pmu_port and send request
for header message, configuration and eventually
to start sending measurements.
"""


if __name__ == "__main__":

    pdc = Pdc(pdc_id=7, pmu_ip="127.0.0.1", pmu_port=1410)
    pdc.logger.setLevel("DEBUG")

    pdc.run()  # Connect to PMU

    header = pdc.get_header()
    print("Header:", header.get_header())

    config = pdc.get_config()
    print("Station Name:", config.get_station_name())
    print("ID Code:", config.get_stream_id_code())
    print("Data Format:", config.get_data_format())
    print("Phasor Num:", config.get_phasor_num())
    print("Analog Num:", config.get_analog_num())
    print("Digital Num:", config.get_digital_num())
    print("Channel Names:", config.get_channel_names())
    print("Phasor Units:", config.get_ph_units())
    print("Analog Units:", config.get_analog_units())
    print("Digital Units:", config.get_digital_units())
    print("Nominal Frequency:", config.get_fnom())
    print("Config Change Count:", config.get_cfg_count())
    print("Data Rate:", config.get_data_rate())

    pdc.start()  # Request to start sending measurements

    while True:

        data = pdc.get()  # Keep receiving data

        if type(data) == DataFrame:
            print(data.get_measurements())

        if not data:
            pdc.quit()  # Close connection
            break
