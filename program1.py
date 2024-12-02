#!/usr/bin/env python3

"""
program1.py

This program captures traffic from a network and saves traffic in a txt file within
the same directory as this file. 

Notes:
* Output files are overwritten upon reruns of the program. *
- Capture file size limited to 10 packets.
- Number of files created limited to 3 files. 
- Tested on MacOS and Linux machines

Author: Adam Pang
Contact: akp4339@rit.edu
Date Created: 2024-10-04
Last Modified: 2024-10-04
"""

import subprocess, os

MAX_FILES = 3
MAX_PACKETS = 10

########################################################
# Stand alone organization functions
########################################################

def output_banner():
    """Print out starting screen banner"""
    print(f"####################################")
    print(f"#  Welcome to the capture program  #")
    print(f"# This can capture traffic on your #")
    print(f"# network via Wireshark/tshark, or #")
    print(f"# tcpdump. Files are saved in txt. #")
    print(f"####################################")

def prompt_menu_action():
    """Print out menu prompt"""
    print(f"\n*** Please select an activity and then the number of capture files. ***")
    print(f"    1 - Capture with Wireshark")
    print(f"    2 - Capture with tcpdump")
    print(f"    x - Exit the program")

    return input("   What would you like to do? ")

def print_error(error_msg):
    """Print out error message"""
    print(f"*** Error: " + error_msg + ". Please try again.")

########################################################
# Main Program 1 functionality in a class for Program 2
########################################################

class Program1():

    def __init__(self):
        """Initializer for Program1 runs"""
        self.wireshark_file_count = 0
        self.tcpdump_file_count = 0
        self.num_files = 0

    def is_valid_input(self, user_input):
        """Check if the input is either '1' or '2'."""
        return user_input in ['1', '2']

    def check_num_files(self, num_files):
        """Check if number of files for captures is between 1 and MAX_FILES inclusive"""
        if num_files < 1 or num_files > MAX_FILES:
            print_error(f"Invalid number of files. The maximum number of files is {MAX_FILES}")
            return False

        return True
    
    def add_file_count(self, type, num_files):
        """
        Increment file_count with number of completed files for a particular log command.
        Primarily used to keep track of the file names and how many files were created.

        Args:
            type (char): "w" to indicate wireshark_file_count, "t" to indicate tcpdump_file_count
            num_files (int): Number of files to increment by
        """
        if type.lower() == "w":
            self.wireshark_file_count += num_files
        elif type.lower() == "t":
            self.tcpdump_file_count += num_files

    def set_num_files(self, num_files):
        """
        Updates number of files being worked on.
        Assumes that num_files has been already verified with check_num_files.

        Args:
            num_files (int): Number of files being run on this loop of Program1
        """
        self.num_files = num_files

    def capture_wireshark(self, count):
        """
        Capture network traffic using tshark with a maximum number of packets and saving 
        it to a txt file.

        Args:
            packet_count (int): The number of packets to capture (default is 10).
        """
        try:
            # Guarantee that output files are in the same directory
            program_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Define the output file path in the same directory as the script
            file_id = self.wireshark_file_count + count
            output_file = os.path.join(program_dir, f"w{file_id}.txt")

            # Capture MAX_PACKETS packets using tshark command
            command = f"tshark -c {MAX_PACKETS} -x > {output_file}"
            subprocess.run(command, shell=True, check=True)
            print(f"*** Traffic saved to w{file_id}.txt ***\n")
            
        except subprocess.CalledProcessError as e:
            print_error(f"Error occurred while capturing traffic: {e}")


    def capture_tcpdump(self, count):
        """
        Capture network traffic using tcpdump with a maximum number of packets and saving 
        it to a txt file.

        Args:
            packet_count (int): The number of packets to capture (default is 10).
        """
        try:
            # Guarantee that output files are in the same directory
            program_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Define the output file path in the same directory as the script
            file_id = self.tcpdump_file_count + count
            output_file = os.path.join(program_dir, f"t{file_id}.txt")

            # Capture MAX_PACKETS packets using tshark command
            command = f"sudo tcpdump -c {MAX_PACKETS} -X > {output_file}"
            subprocess.run(command, shell=True, check=True)
            print(f"*** Traffic saved to t{file_id}.txt ***\n")
            
        except subprocess.CalledProcessError as e:
            print_error(f"Error occurred while capturing traffic: {e}")

########################################################
# Program 1 functionality
########################################################

def main():
    """
    Main capture program. Executes main menu loop to prompt user for tshark or tcpdump
    traffic logging.
    """
    # Output system start message
    output_banner()

    # Initialize Program1 Object
    p1 = Program1()

    # Loop menu until quit message is received
    while True:
        user_input = prompt_menu_action().strip()

        # Check for quit command
        if user_input.lower() == "x":
            break
        
        # Check for valid commands
        try:
            if p1.is_valid_input(user_input):
                if user_input == "1":
                    # Run wireshark capture
                    num_files = int(input("*** Beginning Wireshark/tshark capture. How many files? "))

                    # Check for valid number of files
                    if (p1.check_num_files(num_files)):
                        # Save number of files
                        p1.set_num_files(num_files)

                        # Begin capture process
                        for i in range(num_files):
                            p1.capture_wireshark(i)

                        # Update Program1 Object's file_count for output file numbering
                        p1.add_file_count("w", num_files)

                        print(f"*** Finished Wireshark/tshark capture - returning to menu. ***")

                elif user_input == "2":
                    # Run tcpdump capture
                    num_files = int(input("*** Beginning tcpdump capture. How many files? "))

                    # Check for valid number of files
                    if (p1.check_num_files(num_files)):
                        # Save number of files
                        p1.set_num_files(num_files)

                        # Begin capture process
                        for i in range(num_files):
                            p1.capture_tcpdump(i)

                        # Update Program1 Object's file_count for output file numbering
                        p1.add_file_count("t", num_files)

                        print(f"*** Finished tcpdump capture - returning to menu. ***")
            else:
                print_error("Invalid input")
        except Exception as e:
            print_error("Invalid input")
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