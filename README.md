# Packet Logger and Cleaner
Both program1 and program2 are focused on packet logging via Wireshark/tshark and tcpdump capture libraries. Both programs can be run individually, with similar UIs. 

## Important Notes
- Capture file size is limited to 10 packets. 
- Number of files created is limited to 3 files. 
- Tested on MacOS and Linux machines

## Program 1 Usage
Program 1 will call tshark or tcpdump capture methods to log 10 packets per file. Option 1 will utilize tshark, while option 2 will utilize tcpdump. Output files will start with a 'w' when from a tshark capture, and 't' when from a tcpdump capture.

`python3 program1.py`

## Program 2 Usage
Program 2 uses a class of Program1 functionality (logging and output file methods) and adds cleaning capabilities. The cleaning will isolate the hex data from each packet and move it to a new file. Output files for cleaning will start with "cleaned_{file_name}" depending on what file was cleaned. 

`python3 program2.py`