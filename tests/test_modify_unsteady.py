import sys
sys.path.append("./src/")
import logging_config
import logging
import modify_unsteady
import pytest


def test_modify_unsteady01():
    logger = logging.getLogger(__name__)

    # declare input and expected output
    input_path = r"tests\data\ras_model\input.u01"
    output_path = r"tests\data\ras_model\output.u01"
    dss_path = r".\DSS Files\MalateClogged10.dss"
    
    # save initial of input state to memory
    init_state = None
    with open(input_path, "r") as file:
        rows = file.readlines()
        init_state = rows.copy()

    # run the script
    dss_base_internal_path = "/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/"
    ustd_processor = modify_unsteady.UnsteadyFlowFileProcessor()
    ustd_processor = ustd_processor.dss_base_internal_path(dss_base_internal_path).dss_file_path(dss_path)
    ustd_processor.run(input_path)

    # get results of input data
    input_data = None
    with open(input_path, "r") as file:
        rows = file.readlines()
        input_data = rows.copy()

    # write result to a temp.log file
    with open(r"tests\temp.log", "w") as file:
        file.writelines(input_data)

    # get expected output results data
    output_data = None
    with open(output_path, "r") as file:
        rows = file.readlines()
        output_data = rows.copy()

    # assert input and output are the same
    err_msg = f"Input data and output data do not match, given:\nRESULTED:{input_data}\n---VS---\nEXPECTED:{output_data}"
    if not input_data == output_data:
        logger.error(err_msg)
        raise AssertionError(err_msg)
        

    # restore initial state
    with open(input_path, "w") as file:
        file.writelines(init_state)

