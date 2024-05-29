# Nexus/Qualys report parser

Python scripts to parse Nessus and Qualys report into xlsx tables. 

To get a Nessus Json file from a .nessus file, you can use Nessus_Map project : https://github.com/Ebryx/Nessus_Map, 
You can then turn it into yaml with the convertor script. 

For Qualys file, you can directly download the XML file from your Qualys scan result and turn it into yaml format with the same previous script. 

You can then run the nessus.py script for nessus files and qualys.py for qualys files