from errorLogParser import *

filepath= r"D:\Facultate\MASTER_AN_1\BLOCURI ANALOGICE AVANSATE\Backp_proj\AO_CP_NMOS\test_ao_cp_n_AC.log"
mosfets = process_mosfet_data(filepath)

for mos in mosfets:
    print(mos)
