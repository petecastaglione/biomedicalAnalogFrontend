from siUnits import *


def getMosValueString(mostype, w, l):
    drainArea = w * 0.2e-6
    sourceArea = drainArea
    drainPerim = 2*( w + 0.2e-6 )
    sourcePerim = drainPerim
    m = 1
    return (f"{mostype}_130n l={num2SiStringRounded(l)} w={num2SiStringRounded(w)} ad={num2SiStringRounded(drainArea)} "
    f"as={num2SiStringRounded(sourceArea)} pd={num2SiStringRounded(drainPerim)} ps={num2SiStringRounded(sourcePerim)} " 
    f"m={m}")


def main():
    mostype = "N"
    w = siString2Num("4u")
    l = siString2Num("2u")    
    drainArea = w * 0.2e-6
    sourceArea = drainArea
    drainPerim = 2*( w + 0.2e-6 )
    sourcePerim = drainPerim
    # m = "{mFirstStage}"
    m = 1

    print(f"{mostype}_130n l={num2SiStringRounded(l)} w={num2SiStringRounded(w)} ad={num2SiStringRounded(drainArea)} "
    f"as={num2SiStringRounded(sourceArea)} pd={num2SiStringRounded(drainPerim)} ps={num2SiStringRounded(sourcePerim)} " 
    f"m={m}")    
    # print(f"{mostype[0]}_1u l={num2SiStringRounded(l)} w={num2SiStringRounded(w)} ad={num2SiStringRounded(drainArea)} "
    #       f"as={num2SiStringRounded(sourceArea)} pd={num2SiStringRounded(drainPerim)} ps={num2SiStringRounded(sourcePerim)} " 
    #       f"m={m}")
    
    
    
    

if __name__ == "__main__":
    main()
    