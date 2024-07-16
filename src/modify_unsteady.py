import file_dialog
from os.path import relpath
import logging_config
import logging


def main():
    # set these values
    hec_ras_dir = file_dialog.request_open_folder("Please provide HEC-RAS directory")
    ustd_dir = file_dialog.request_open_file("Please provide Unsteady Flow file")
    dss_abs_file_path = file_dialog.request_open_file("Please provide DSS file")
    
    dss_file_path = ".\\" + relpath(dss_abs_file_path, start=hec_ras_dir)
    dss_base_internal_path = "/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/"

    ustd_processor = UnsteadyFlowFileProcessor()
    # add needed settings to the unsteady flow file processor
    ustd_processor = ustd_processor.dss_base_internal_path(dss_base_internal_path).dss_file_path(dss_file_path)
    # modify the unsteady flow file
    ustd_processor.run(ustd_dir)

class UnsteadyFlowFileProcessor():
    """
    This object encapsulates the process for manipulating an unsteady flow file to apply a single dss
    file's data.
    """

    logger = logging.getLogger(__name__)
    
    def dss_base_internal_path(self, dss_base_internal_path):
        """
        This method holds the dss base path which is the path inside the dss file needed to find the
        timeseries data.
        """
        self.dss_base_internal_path = dss_base_internal_path
        return self
    
    def dss_file_path(self, dss_file_path):
        """
        This method holds the dss file path which is the directory and filename where the dss file sits
        in the computer.
        """
        self.dss_file_path = dss_file_path
        return self
    
    def get_bcline_id(self, row:str):
        """
        This method finds the id name in a row (if any) in an unsteady flow file
        """
        self.bcline_id = row[121:153].strip()
    
    def process_line(self, row: str):
        """
        This method takes a string and a parameter name and returns a reformatted
        string that will work with a HEC-RAS unsteady flow data file.
        """
        self.logger.debug(f"in process_line row:{repr(row)}")
        if row.startswith("Boundary Location"):
            self.logger.debug(f"Activating get_bcline_id, got result {self.get_bcline_id(row)}")
            self.get_bcline_id(row)
            return row
        elif row.startswith("DSS File"):
            return "DSS File=" + self.dss_file_path + "\n"
        elif row.startswith("DSS Path"):
            return "DSS Path=" + self.dss_base_internal_path + self.bcline_id + "/\n"
        elif row.startswith("Use DSS"):
            return "Use DSS=True\n"
        else:
            return row
    
    def _preprocess(self, path_unsteady) -> list:
        # open file
        self.logger.debug(f"BEGINNING: preprocessing...")
        with open(path_unsteady, "r") as file:
            # iterate through file
            rows = file.readlines()
            # preprocess lines
            processed_rows = list()
            for i in range(len(rows)):
                # process depending on the current param name
                is_current_bcline_row = rows[i].startswith("Boundary Location")
                is_next_interval = rows[i].startswith("Interval")
                self.logger.debug(f"Parameter names: 0:{is_current_bcline_row}, 1:{is_next_interval}")
                # append current row to processed row
                processed_rows.append(rows[i])
                # if current param is Boundary Location and next param is not Interval
                if is_current_bcline_row and not(is_next_interval):
                    # then append new rows to processed row
                    self.logger.debug(f"Adding new rows")
                    processed_rows.append("Interval=1HOUR\n")
                    processed_rows.append("Flow Hydrograph= 0 \n")
                    processed_rows.append("Stage Hydrograph TW Check=0\n")
                    processed_rows.append("DSS File=\n")
                    processed_rows.append("DSS Path=\n")
                    processed_rows.append("Use DSS=\n")
                    processed_rows.append("Use Fixed Start Time=False\n")
                    processed_rows.append("Fixed Start Date/Time=,\n")
                    processed_rows.append("Is Critical Boundary=False\n")
                    processed_rows.append("Critical Boundary Flow=\n")
        self.logger.debug(f"COMPLETED: test preprocessing...\n")
        return processed_rows
    
    def run(self, path_unsteady):
        rows = self._preprocess(path_unsteady)
        for i in range(len(rows)):
            # process depending on the current param name
            self.logger.debug(f"Iteration#{i} before process row: {repr(rows[i])}")
            rows[i] = self.process_line(rows[i])
            self.logger.debug(f"Iteration#{i} after  process row: {repr(rows[i])}")
        
        with open(path_unsteady, "w") as file:
            file.writelines(rows)


if __name__ == "__main__":
    main()