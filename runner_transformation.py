from dataclasses import dataclass
from opentrons.simulate import simulate, format_runlog
from io import StringIO
from python_scripts.report_builder import build_report
from python_scripts.general_runners import Runner
import python_scripts.transformation as transformation_script

@dataclass
class TransformationRunner(Runner):
    plasmid_names: list[str] = None
    competent_cell_names: list[str] = None
    samples: list[str] = None
    
    @property
    def assay(self):
        return "Transformation"

    def check_args(self, **kwargs):
        if not kwargs.get("plasmids", []) or not kwargs.get("competent_cells", []):
            return "you have not written any plasmid or competent cell name(s). Write some in text box(es), refresh this cell and press submit again."
        
        self.plasmid_names = kwargs.get("plasmids", [])
        self.competent_cell_names = kwargs.get("competent_cells", [])
        self.samples = kwargs.get("samples", [])

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
        ])
        build_report(self, runlog, extra_lines=extra_lines)
    
    def build_log_line(self, key, value):
        line = key
        line += (27- len(key)) * " "
        return line + value

    @staticmethod
    def get_script():
        return transformation_script