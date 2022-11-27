# Acoustics
### Group 12
Authors:
Christina Kjær, s183594 
Julie Bech Liengaard, s193800


## Link to video-presentation
https://dtudk.sharepoint.com/:v:/s/AdvancedBIM-Group12/ETXdgWR_mA9FqZMgu68qcgsBK-ZITXPsEgCvOCMpC1CkoQ?e=rbv9wZ

## Step-by-step guide

### main.py
Code for importing, analysing and displaying information from the imported .ifc file. 

### Setup and run
   + Open the main file and run the line "pip install playsound" in the terminal or command prompt. 
   + If the code doesn't work, try this: 
   + open command prompt and type:
      
     1. pip uninstall playsound
     2. pip install playsound==1.2.2

This is also written in the top lines of the script

### Once you run the code it extracts data from the .ifc file that is in the \model folder. 
   A list of all spaces are displayed with a prompt asking to enter a space. 
   It is important to type correctly with capitol first letter, otherwise it will not recognize the space and ask the person to type again.
   
   Then it displays information that is used for simple acoustic measures, such as volume and area. 
   
   It asks if you want to listen to how the space would sound, with yes/no answer available (capitol letter doesn't matter here). 
   Then it asks if the user wants to listen to a short music of speech sample. 
     The code responds to "usi" (meaning music) so completely correct spelling (e.g. Danish spelling) doesn't matter, and will otherwise play speech per default. 
     If the user responds "no" the code will stop. 
   
   If the user wants to run a different space they will have to run the code again.


### Script functions: 
####  Assumptions and flaws/inaccuracies are listed
importing model from \model folder

finding all spaces and prompts the user to write the space they want information about. The input is stored as a space name. 

extraction of room data
- space Name, LongName and Level
- space properties Volume, Area, Height
- Height is reduced to get floor to ceiling (therefore specific for this model)
- Area is currently for floor and ceiling and is calculated for walls (by the height and assuming the room is quadratic, therefore less accuracy, but using Sabine's equation this is not a big issue)

function findAbs is defining absorption coefficients based on lecture note "Environmental and Architectural Acoustics" from course Building Acoustics.

function absCoefficients
- finds LongName and finds all materials for each building element
- selects the material facing the space (sometimes first and sometimes last in .RelatingMaterial.ForLayerSet.MaterialLayers, therefore specific for this model)
- uses function findAbs to define absorption coefficients for surface areas 
  in this model all walls in a space have the same absorption coefficient (which could be improved for the future work)

prints reverberation time with 2 decimals

function playSound
- rounds RT to neares .1 decimal (so 0.1, 0.2, 0.3 etc.) this small round is barely audible 
- plays the sound with corresponding RT 
sample choice selects music in function playSound if "usi" is in the string input from the user and otherwise speech sample

#### readAudio.m 
This script is a tool used in the course Acoustic Signal Processing and we are not the authors

#### IRs_with_fixed_RTs.m
This script creates an impulse response with a fixed RT based on a decay (highly room dependend and is therefore not accurate specific to the room since we have no room boundaries as input)
It gives an example of what this reverberation time could sound like.
The impulse responses are convolved with two audiofiles. 
The sound files are saved and stored in \samples. 

## Future work
If we had more time to develope on the script, we would have collected the specific wall areas and the specific room geometry. As it is now, we assume that every room is quadratic. Thus, the script calculates the total wall area of the room with the room area and the room height as input. This method is okay since we use Sabine's equation to determine the reverberation time which doesn't take in the room geometry but only uses the absorption area and volume of the room, and since the surface material of all the walls is plasterboard. Acoustics will, however, be affected based on whether the walls are parallel or not, but this will not be considered at this level.
