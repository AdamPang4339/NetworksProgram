#!/usr/bin/env python3

"""
program2.py

This program captures traffic from a network and saves traffic in a txt file within
the same directory as this file. Cleaned versions of the packets within the 
capture process will be outputted to another file as well.

Notes:
* Output files are overwritten upon reruns of the program. *
- Capture file size limited to 10 packets.
- Number of files created limited to 3 files. 
- Tested on MacOS and Linux machines

Author: Adam Pang
Contact: akp4339@rit.edu
Date Created: 2024-11-09
Last Modified: 2024-11-10
"""

import program1


def prompt_menu_action():
    """Print out new Program 2 menu prompt"""
    print(f"\n*** Please select an activity and then the number of capture files. ***")
    print(f"    1 - Capture with Wireshark AND clean packets")
    print(f"    2 - Capture with tcpdump AND clean packets")
    print(f"    x - Exit the program")

    return input("   What would you like to do? ")


class Program2(program1.Program1):

    def __init__(self):
        super().__init__()
    

    def clean_file(self, file_name):
        """
        Cleans the capture file, retaining only the hexdump data and truncating to 42 bytes.
        Cleaned file output will be generated in a new file named cleaned_{file_name}

        Args:
            file_name (string): File to be cleaned
        """
        try:
            cleaned_file_name = "cleaned_" + file_name
            # Open the input file for reading
            with open(file_name, 'r') as file:
                lines = file.readlines()

            cleaned_packets = []
            current_packet = ""
            tdump_file = False

            # Wireshark output indices
            wireshark_hex_data = 5
            wireshark_symbols = 53
            # tcpdump output indices
            tdump_hex_data = 7
            tdump_symbols = 48

            # Iterate through each line and gather hex data
            for line in lines:
                line = line.strip()  # Remove any leading/trailing whitespace

                # Empty line signifies a new packet in wireshark output
                if line == '':
                    tdump_file = False
                    if current_packet:
                        cleaned_packets.append(current_packet)
                    current_packet = ""
                    continue
                # Colon in the third character of the first line signifies a packet in tcpdump
                elif line[2] == ':':
                    tdump_file = True
                    if current_packet:
                        cleaned_packets.append(current_packet)
                    current_packet = ""
                    continue

                # Get only the hex data without spaces between bytes
                if not tdump_file:
                    hex_dump = line[wireshark_hex_data:wireshark_symbols].strip().replace(" ", "")
                else:
                    hex_dump = line[tdump_hex_data:tdump_symbols].strip().replace(" ", "")

                current_packet += hex_dump
            
            # Sanity check for when a file may not end with a new line
            if current_packet:
                cleaned_packets.append(current_packet)

            # Write all cleaned packets to the new file
            with open(cleaned_file_name, 'w') as cleaned_file:
                for packet in cleaned_packets:
                    # Truncate to 84 characters, which is 42 bytes
                    truncated = packet[:84]
                    cleaned_file.write(truncated + '\n\n')

            print(f"\tFile '{file_name}' cleaned successfully. Output is in {cleaned_file_name}")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            print(f"An error occurred while cleaning the file '{file_name}': {e}")


def main():
    """
    Main capture program. Executes main menu loop to prompt user for tshark or tcpdump
    traffic logging. Capabilities for cleaning files exist as well for Program 2.
    """
    # Output system start message from Program1
    program1.output_banner()

    # Create Program2 Object
    p2 = Program2()

    # Loop menu until quit message is received
    while True:
        user_input = prompt_menu_action().strip()

        # Check for quit command
        if user_input.lower() == "x":
            break
        
        # Check for valid commands
        try:
            if p2.is_valid_input(user_input):
                if user_input == "1":
                    # Run wireshark capture
                    num_files = int(input("*** Beginning Wireshark/tshark capture AND cleaning. How many files? "))

                    # Check for valid number of files
                    if (p2.check_num_files(num_files)):
                        # Save number of files
                        p2.set_num_files(num_files)

                        # Begin capture process
                        for i in range(num_files):
                            p2.capture_wireshark(i)

                        print(f"*** Finished Wireshark/tshark capture - Moving to cleaning process. ***\n")

                    # Clean generated files
                    print(f"*** Cleaning {p2.num_files} Wireshark/tshark capture file(s).")

                    for i in range(p2.num_files):
                        p2.clean_file(f"w{p2.wireshark_file_count + i}.txt")

                    # Update Program2 Object's file_count for output file numbering
                    p2.add_file_count("w", num_files)

                    print(f"*** Finished cleaning Wireshark file(s) - Returning to menu. ***")
                elif user_input == "2":
                    # Run tcpdump capture
                    num_files = int(input("*** Beginning tcpdump capture AND cleaning. How many files? "))

                    # Check for valid number of files
                    if (p2.check_num_files(num_files)):
                        # Save number of files
                        p2.set_num_files(num_files)

                        # Begin capture process
                        for i in range(num_files):
                            p2.capture_tcpdump(i)
                        
                        print(f"*** Finished tcpdump capture - Moving to cleaning process. ***\n")

                        # Clean generated files
                        print(f"*** Cleaning {p2.num_files} Wireshark/tshark capture file(s).")

                        for i in range(p2.num_files):
                            p2.clean_file(f"t{p2.wireshark_file_count + i}.txt")

                        # Update Program2 Object's file_count for output file numbering
                        p2.add_file_count("t", num_files)

                        print(f"*** Finished tcpdump capture - Returning to menu. ***")

        except Exception as e:
            program1.print_error("Invalid input")
            continue
    

if __name__ == "__main__":
    main()


"""
Sources:

- ChatGPT: Generated default file header comment block format. Header content was written by the author, Adam Pang. 
- TCPDump Man Pages: https://www.tcpdump.org/manpages/tcpdump.1.html#:~:text=tcpdump%20prints%20out%20a%20description%20of%20the%20contents%20of%20packets
    - Researched and utilized options specified within the TCPdump man pages
- TShark Man Pages: https://www.wireshark.org/docs/man-pages/tshark.html
    - Researched and utilized options specified within the Tshark man pages
"""