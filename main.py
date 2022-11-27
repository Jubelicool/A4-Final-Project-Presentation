## Group 12
#  Authors: Christina Kjær, s183594 & Julie Bech Liengaard, s193800
#  Last edit 27.11.22

from tokenize import Name
import ifcopenshell
import math
## REMEMBER TO INSTALL PLAYSOUND:
# pip install playsound
## If the code doesn't work, try this: 
## open command prompt and type
# pip uninstall playsound
## .. and then
# pip install playsound==1.2.2

from playsound import playsound

## Load model from folder \model
model = ifcopenshell.open("model/Duplex_A_20110907.ifc")

## Get all the spaces in your file by
spaces = model.by_type("IfcSpace")             
for space in spaces: 
        space.LongName
        print(space.LongName) #"\n"+

## Prompts the user to write the space they want information about
def selectRoom(spaces):
    name = input("Enter space: ")
    a = []
    for i in spaces:
        a.append(i.LongName)

    if str(name) in a:
        idx = a.index(str(name))
        print("You selected " + a[idx])
    else:
        print("Room not found in this model. Please try again.")
        selectRoom(spaces)
    return name

name = selectRoom(spaces)

## Get room properties from selected space (Find in blender by selecting e.g. A102 (Current File\Collections\IfcSpace/A102 --> orange square object properties --> PSet_Revit_Dimensions)).
## Prints [LongName, Level, Area, Height, Volume] for the selected space   
def extractRoomData(model,name): 
    spaces = model.by_type("IfcSpace")
    for space in spaces: 
        if space.LongName == str(name): #Prints only for the selected space
            Name = space.LongName
            print("\n"+ space.Name, space.LongName)
            Level = space.Decomposes[0].RelatingObject.Name
            print(space.Decomposes[0].RelatingObject.Name)
            for definition in space.IsDefinedBy: #Find in Excel in column N in IfcSpace 
                
                if definition.is_a("IfcRelDefinesByProperties"): # filter results
                    property_set = definition.RelatingPropertyDefinition
                                        
                    ## Sort by the name of the propertySet
                    if property_set.Name == "PSet_Revit_Dimensions": #PSet_Revit_Dimensions
                        if property_set.HasProperties:
                            for property in property_set.HasProperties:
                            
                            ## sort by the name of the property
                                if property.Name == "Volume":           
                                    Volume = round(property.NominalValue.wrappedValue,2)
                                    print("Volume = ", Volume)
                                    
                                if property.Name == "Unbounded Height":    
                                    Height = round(property.NominalValue.wrappedValue - 0.5,2) #To get floor to ceiling in stead of floor to floor
                                    print("Height = ", Height)
                                    
                                if property.Name == "Area":
                                    # We assume area for the floor and ceiling is the same
                                    S_floor = round(property.NominalValue.wrappedValue,2)
                                    S_ceil = S_floor
                                    print("Area of floor and ceiling = ", S_floor)
                                    #space_entities.append(property.NominalValue.wrappedValue)
                            # Wall areas calculated assuming the room is rectangular
                            S_walls = round(math.sqrt(S_floor) * Height * 4 , 2)
                            print("Area of walls = ", S_walls)
    return Name, Level, S_floor, S_ceil, S_walls, Height, Volume

[Name, Level, S_floor, S_ceil, S_walls, Height, Volume] = extractRoomData(model,name)

## Define function with absorption coefficients (found in lecture note "Environmental and Architectural Acoustics" from course Building Acoustics)
def findAbs(material): 
    if "Concrete" in material: 
        abs = 0.02
    elif "Plasterboard" in material:
        abs = 0.25
    elif "Wood - Flooring" in material: 
        abs = 0.1
    elif "Lumber" in material:
        abs = 0.1
    elif "Tile" in material:
        abs = 0.01
    else: 
        print("Material not recognized")
    # print("Absorption coefficients for this material is" + str(abs))
    return abs

## Material extraction for each space
def absCoefficients(name):
    for space in spaces: 
        if space.LongName == str(name): #Prints only for the selected space
        # Name = space.LongName
        # print("\n"+ Name)
   
            SM = [] #Surface material parameter

            for i in space.BoundedBy:
                try: 
                    SM.append(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName)
                    if "Floor:Finish" in i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName:
                        abs_floor = findAbs(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.MaterialLayers[0].Material.Name)

                    elif "Ceiling" in i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName:
                        abs_ceil = findAbs(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.MaterialLayers[-1].Material.Name)
                    
                    elif "Wall" in i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName:
                        abs_wall = findAbs(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.MaterialLayers[-1].Material.Name)    
                    
                    elif "Floor" in i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName:
                        abs_floor = findAbs(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.MaterialLayers[-1].Material.Name)

                    # elif "Roof" in i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.LayerSetName:
                    #     abs_roof = findAbs(i.RelatedBuildingElement.HasAssociations[0].RelatingMaterial.ForLayerSet.MaterialLayers[-1].Material.Name)    
                except: 
                    "None" == any     
    return abs_floor, abs_ceil, abs_wall, abs_floor
    
[abs_floor, abs_ceil, abs_wall, abs_floor] = absCoefficients(name)

print("\n" + "Reverberation time for " + str(name) + " is:")
## TEST af RT
RT = round(0.16*Volume/(S_floor*abs_floor + S_ceil*abs_ceil + S_walls * abs_wall),2)
print("RT =", RT)

## Prompts the user to write the space they want information about
yes_no = input("\n" + "Would you like to listen to how the space sounds?" + "\n" + "Type Yes or No: " + "\n")

def playSound(RT, sampleChoice):
    # Round RT to get a whole number (2 decimals)
    RTround = round(RT, 1)
    if "ee" in sampleChoice:
        if RTround == 0.1:
            playsound('input/rat_01.wav')
        elif RTround == 0.2:
            playsound('input/rat_02.wav')
        elif RTround == 0.3:
            playsound('input/rat_03.wav')
        elif RTround == 0.4:
            playsound('input/rat_04.wav')
        elif RTround == 0.5:
            playsound('input/rat_05.wav')
        elif RTround == 0.6:
            playsound('input/rat_06.wav')
        elif RTround == 0.7:
            playsound('input/rat_07.wav')
        elif RTround == 0.8:
            playsound('input/rat_08.wav')
        elif RTround == 0.9:
            playsound('input/rat_09.wav')
        else: 
            print("Reverberation time couldn't be calculated")
    elif "ic" in sampleChoice:
        if RTround == 0.1:
            playsound('input/Lofi_01.wav')
        elif RTround == 0.2:
            playsound('input/Lofi_02.wav')
        elif RTround == 0.3:
            playsound('input/Lofi_03.wav')
        elif RTround == 0.4:
            playsound('input/Lofi_04.wav')
        elif RTround == 0.5:
            playsound('input/Lofi_05.wav')
        elif RTround == 0.6:
            playsound('input/Lofi_06.wav')
        elif RTround == 0.7:
            playsound('input/Lofi_07.wav')
        elif RTround == 0.8:
            playsound('input/Lofi_08.wav')
        elif RTround == 0.9:
            playsound('input/Lofi_09.wav')
        else: 
            print("Reverberation time couldn't be calculated")
    else: 
            print("Reverberation time couldn't be calculated")

if "es" in str(yes_no):
    sampleChoice = input("Choose music or speech sample: " + "\n")
    if "usi" in str(sampleChoice):
        sampleChoice = "music"
        playSound(RT, sampleChoice)
    else:
        sampleChoice = "speech"
        playSound(RT, sampleChoice)
else:
    print("Okay, have a nice day.")
