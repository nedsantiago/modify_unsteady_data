import sys
sys.path.append("./src/")
import logging_config
import logging
import modify_unsteady
import pytest


class TestModifyUnsteady():
    """
    This class tests using an unsteady flow file that has complete lines of data. Example:

    Boundary Location=                ,                ,        ,        ,                ,P01             ,                ,0+225                           ,                                
    Interval=1HOUR
    Flow Hydrograph= 0 
    Stage Hydrograph TW Check=0
    DSS File=/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/0+225/
    DSS Path=.\\DSS Files\\example-dss.dss
    Use DSS=True
    Use Fixed Start Time=False
    Fixed Start Date/Time=,
    Is Critical Boundary=False
    Critical Boundary Flow=
    """
    # declare inputs
    input_path = r"tests\data\ras_model\input01.u01"
    dss_path = r".\DSS Files\example-dss.dss"
    dss_base_internal_path = "/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/"
    # declare expected output
    output_path = r"tests\data\ras_model\output01.u01"
    
    def test_modify_unsteady(self):
        logger = logging.getLogger(__name__)
        # declare inputs
        input_path = self.input_path
        dss_path = self.dss_path
        dss_base_internal_path = self.dss_base_internal_path
        # declare expected output
        output_path = self.output_path

        # save input's initial state for reuse
        init_state = None
        with open(input_path, "r") as file:
            rows = file.readlines()
            init_state = rows.copy()

        # run the script
        ustd_processor = modify_unsteady.UnsteadyFlowFileProcessor()
        ustd_processor = ustd_processor.dss_base_internal_path(dss_base_internal_path).dss_file_path(dss_path)
        
        try:
            ustd_processor.run(input_path, input_path)
        except Exception as e:
            err_msg = f"Failed to complete unsteady flow file modification. {e}"
            logger.error(err_msg)
            # restore initial state
            with open(input_path, "w") as file:
                file.writelines(init_state)
            raise RuntimeError(err_msg)

        # get results of input data
        input_data = None
        with open(input_path, "r") as file:
            rows = file.readlines()
            input_data = rows.copy()

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
    
class TestModifyUnsteady01(TestModifyUnsteady):
    """
    This class tests using an unsteady flow file that has missing lines of data. Example:

    Boundary Location=                ,                ,        ,        ,                ,Perimeter 1     ,                ,PCUNA052                        ,                                
    """
    # declare inputs
    input_path = r"tests\data\ras_model\input.u01"
    dss_path = r".\DSS Files\MalateClogged10.dss"
    dss_base_internal_path = "/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/"
    # declare expected output
    output_path = r"tests\data\ras_model\output.u01"