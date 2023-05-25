from dataclasses import dataclass
from opentrons.simulate import simulate, format_runlog
from io import StringIO
from python_scripts.report_builder import build_report
from python_scripts.general_runners import Runner
from python_scripts.script_writer import create_transformation_protocol
import python_scripts.transformation as transformation_script

@dataclass
class TransformationRunner(Runner):
    plasmid_names: list[str] = None
    competent_cell_names: list[str] = None
    samples: list[str] = None
    plasmid_antibiotics: list[str] = None
    competent_antibiotics: list[str] = None
    
    @property
    def assay(self):
        return "Transformation"

    def check_args(self, **kwargs):
        if not kwargs.get("plasmids", []) or not kwargs.get("competent_cells", []) or not kwargs.get("competent_antibiotics", []) or not kwargs.get("plasmid_antibiotics", []):
            return "you have not written any plasmid, competent cell name(s) or are missing certain antibiotics. Write some in text box(es), refresh this cell and press submit again."
        
        
        self.plasmid_names = kwargs.get("plasmids", [])
        self.competent_cell_names = kwargs.get("competent_cells", [])
        self.samples = kwargs.get("samples", [])
        self.plasmid_antibiotics = kwargs.get("plasmid_antibiotics", [])
        self.competent_antibiotics = kwargs.get("competent_antibiotics", [])

    def get_changed(self):
        content = open(self.get_script().__file__).readlines()
        changed = []
        for line in content:
            if line.startswith("rows ="):
                line = "rows = %s\n" % self.rows
            if line.startswith("columns ="):
                line = "columns = %s\n" % self.cols
            changed.append(line)
        return changed
        
    def run(self, **kwargs):
        assert self.plasmid_names is not None, "setup not completed"

        changed = self.get_changed()
        protocol_file = StringIO("".join(changed))

        # simulate() the protocol, keeping the runlog
        runlog, _bundle = simulate(protocol_file)
        extra_lines = "\n".join([
            self.build_log_line("Plasmid name(s):" , self.plasmid_names.replace("\n", ", " )),
            self.build_log_line("Competent cell name(s):" , self.competent_cell_names.replace("\n", ", " )),
            self.build_log_line("Number of samples:" , str(self.samples)),
            self.build_log_line("Antibiotics used for plasmid(s):", ", ".join(self.plasmid_antibiotics)),
            self.build_log_line("Antibiotics used for competent cell:", ", ".join(self.competent_antibiotics)),
        ])

        create_transformation_protocol(self, self.rows, self.cols)
        build_report(self, runlog, extra_lines=extra_lines)
    
    def build_log_line(self, key, value):
        line = key
        line += (40 - len(key)) * " "
        return line + value

    @staticmethod
    def get_script():
        return transformation_script