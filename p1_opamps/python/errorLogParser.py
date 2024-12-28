
import os
from siUnits import *


class MOSFET:
    def __init__(self, name):
        self.name = name
        self.type = None
        self.vgs = None
        self.vds = None
        self.vdsat = None
        self.vth = None
        self.id = None
        self.gm = None
        self.gds = None
        self.rds = None
        self.region = None

    def __repr__(self):
        # return f"Name: {self.name}, Type: {self.type}, Vds: {self.vds}, Vdsat: {self.vdsat}, Region: {self.region}"
     return f"Name: {self.name}, Type: {self.type}, Vgs: {num2SiStringRounded(self.vgs)}, Vth: {num2SiStringRounded(self.vth)}, Id: {num2SiStringRounded(self.id)}, Vds: {num2SiStringRounded(self.vds)}, Vdsat: {num2SiStringRounded(self.vdsat)}, Region: {self.region}, gm: {num2SiStringRounded(self.gm)}, rds: {num2SiStringRounded(self.rds)}"


def process_mosfet_data(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    parts = content.split("--- BSIM3 MOSFETS ---\n")
    if len(parts) < 2:
        raise ValueError("Could not find MOSFET data section.")

    mosfet_data = parts[1]
    mosfets = []
    current_mosfets = []
    lines = mosfet_data.strip().split('\n')

    # pmosIdentifier = pmosIdentifier
    pmosIdentifier = "p_130n"

    for line in lines:
        line = line.strip()
        if line.startswith("Name:"):
            names = line.split("Name:")[1].split()
            if current_mosfets:
                mosfets.extend(current_mosfets)
                current_mosfets = []
            for name in names:
                current_mosfets.append(MOSFET(name))
        elif line.startswith("Model:"):
            types = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                mosfet.type = types[i]
        elif line.startswith("Vds:"):
            vds_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                vds = float(vds_values[i])
                if mosfet.type == pmosIdentifier:
                    vds = -vds
                mosfet.vds = vds
        elif line.startswith("Vdsat:"):
            vdsat_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                vdsat = float(vdsat_values[i])
                if mosfet.type == pmosIdentifier:
                    vdsat = -vdsat
                mosfet.vdsat = vdsat
        elif line.startswith("Vgs:"):
            vgs_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):            
                vgs = float(vgs_values[i])                
                if mosfet.type == pmosIdentifier:
                    vgs = -vgs
                mosfet.vgs = vgs   
                if mosfet.name == "m:x1:8":
                    print("vgs: ", mosfet.vgs)
        elif line.startswith("Vth:"):
            vth_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                vth = float(vth_values[i])
                if mosfet.type == pmosIdentifier:
                    vth = -vth
                mosfet.vth = vth  
        elif line.startswith("Id:"):
            id_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                id = float(id_values[i])
                if mosfet.type == pmosIdentifier:
                    id = -id
                mosfet.id = id   
        elif line.startswith("Gm:"):
            gm_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                mosfet.gm = float(gm_values[i])
        elif line.startswith("Gds:"):
            gds_values = line.split(":")[1].split()
            for i, mosfet in enumerate(current_mosfets):
                mosfet.gds = float(gds_values[i])
                mosfet.rds = 1/float(gds_values[i])
        
    mosfets.extend(current_mosfets)

    for mosfet in mosfets:
        if mosfet.vds > mosfet.vdsat:
            mosfet.region = "saturation"
        else:
            mosfet.region = "linear"
    return mosfets


# if __name__ == "__main__":
#     try:
#         mosfets = process_mosfet_data(os.path.join("..", "BandGap_Bamba_2vbe_dc.log")) #Replace with your file name
#         for mosfet in mosfets:
#             print(mosfet)
#     except FileNotFoundError:
#         print("Error: Input file not found.")
#     except ValueError as e:
#         print(f"Error: {e}")
