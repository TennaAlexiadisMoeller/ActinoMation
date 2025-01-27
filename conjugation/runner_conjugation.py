from dataclasses import dataclass
from opentrons.simulate import simulate, format_runlog
from io import StringIO
from actinomation.common import build_report
from actinomation.common import Runner
from actinomation.conjugation import create_conjugation_protocol
import actinomation.conjugation.conjugation_tubesto96well_template as conjugation_script

@dataclass
class ConjugationRunner(Runner):
    ecoli_tubes: list[str] = None
    conjugation_mix: dict[str, str] = None
    ecoli: list[str] = None
    streptomyces: list[str] = None
    plasmid_antibiotics: list[str] = None
    competent_antibiotics: list[str] = None

    @property
    def assay(self):
        return "Conjugation"

    def check_args(self, **kwargs):
        if not kwargs.get("ecoli", []) or not kwargs.get("streptomyces", []) or not kwargs.get("competent_antibiotics", []) or not kwargs.get("plasmid_antibiotics", []):
            return "you have not written any plasmid, competent cell name(s) or are missing certain antibiotics. Write some in text box(es), refresh this cell and press submit again."
        
        
        self.ecoli = kwargs.get("ecoli", [])
        self.streptomyces = kwargs.get("streptomyces", [])
        self.conjugation_mix = kwargs.get("conjugation_mix", {})
        self.ecoli_tubes = kwargs.get("ecoli_tubes", [])
        self.plasmid_antibiotics = kwargs.get("plasmid_antibiotics", [])
        self.competent_antibiotics = kwargs.get("competent_antibiotics", [])

    def get_changed(self):
        content = open(self.get_script().__file__).readlines()
        changed = []
        for line in content:
            if line.startswith("default_uses ="):
                line = "default_uses = %s\n" % self.conjugation_mix
            if line.startswith("ecoli_tubes ="):
                line = "ecoli_tubes = %s\n" % self.ecoli_tubes
            changed.append(line)
        return changed

    def run(self):
        assert self.ecoli_tubes is not None, "setup not completed"
        changed = self.get_changed()
        protocol_file = StringIO("".join(changed))

        # simulate() the protocol, keeping the runlog
        runlog, _bundle = simulate(protocol_file)
        extra_lines = "\n".join([
            self.build_log_line("Ecoli name(s):", ", ".join(self.ecoli)),
            self.build_log_line("Streptomyces name(s):" , ", ".join(self.streptomyces)),
            self.build_log_line("Antibiotic(s) used for plasmid(s):", ", ".join(self.plasmid_antibiotics)),
            self.build_log_line("Antibiotic(s) used for competent cell:", ", ".join(self.competent_antibiotics)),
        ])
        create_conjugation_protocol(self, self.conjugation_mix, self.ecoli_tubes)
        build_report(self, runlog, extra_lines=extra_lines)

    def build_log_line(self, key, value):
        line = key
        line += (40 - len(key)) * " "
        return line + value
    
    @staticmethod
    def get_script():
        return conjugation_script

    
test = ConjugationRunner()
test.check_args(ecoli=["e1"], streptomyces=["s1"], ecoli_tubes=["e1"], conjugation_mix={"e1": "1"})
#test.run()