import file_dialog
from re import search
from os.path import relpath


def main():
    # set these values
    hec_ras_dir = file_dialog.request_open_folder("Please provide HEC-RAS directory")
    ustd_dir = file_dialog.request_open_file("Please provide Unsteady Flow file")
    dss_abs_file_path = file_dialog.request_open_file("Please provide DSS file")
    
    dss_file_path = ".\\" + relpath(dss_abs_file_path, start=hec_ras_dir)
    dss_base_path = "/IRREGULAR/TIMESERIES/FLOW/01Jan1990/IR-Decade/"

    ustd_processor = UnsteadyFlowFileProcessor()
    # add needed settings to the unsteady flow file processor
    ustd_processor = ustd_processor.dss_base_path(dss_base_path).dss_file_path(dss_file_path)
    # modify the unsteady flow file
    ustd_processor.run(ustd_dir)

class UnsteadyFlowFileProcessor():
    """
    This object encapsulates the process for manipulating an unsteady flow file to apply a single dss
    file's data.
    """
    
    def dss_base_path(self, dss_base_path):
        """
        This method holds the dss base path which is the path inside the dss file needed to find the
        timeseries data.
        """
        self.dss_base_path = dss_base_path
        return self
    
    def dss_file_path(self, dss_file_path):
        """
        This method holds the dss file path which is the directory and filename where the dss file sits
        in the computer.
        """
        self.dss_file_path = dss_file_path
        return self

    def get_param_name(self, row:str):
        """
        This method parses the string and gets the paramter name. An example parameter name would be:
        Boundary Location=
        DSS File=
        DSS Path=
        Use DSS=
        """

        # get all characters before '=' sign
        match_found = search("^(.*?)=", row).group()[:-1]
        if match_found:
            return match_found
        else:
            return ""
    
    def get_bcline_id(self, row:str):
        """
        This method finds the id name in a row (if any) in an unsteady flow file
        """
        self.bcline_id = row[121:153].strip()
    
    def process_line(self, row: str, param_name: str):
        """
        This method takes a string and a parameter name and returns a reformatted
        string that will work with a HEC-RAS unsteady flow data file.
        """
        if param_name == "Boundary Location":
            self.get_bcline_id(row)
            return row
        elif param_name == "DSS File":
            return "DSS File=" + self.dss_base_path + self.bcline_id + "/\n"
        elif param_name == "DSS Path":
            return "DSS Path=" + self.dss_file_path + "\n"
        elif param_name == "Use DSS":
            return "Use DSS=True\n"
        else:
            return row

    def run(self, path_unsteady):

        # open file
        with open(path_unsteady, "r") as file:
            # iterate through file
            rows = file.readlines()
            for i in range(len(rows)):
                # process depending on the param name
                param_name = self.get_param_name(rows[i])
                rows[i] = self.process_line(rows[i], param_name)
                # print(f"param_name:{param_name}, for row: {rows[i]}")
        
        with open(path_unsteady, "w") as file:
            file.writelines(rows)


if __name__ == "__main__":
    main()