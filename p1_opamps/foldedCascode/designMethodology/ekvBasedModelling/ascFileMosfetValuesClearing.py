
# This script is used to remove SYMATTR Value2 lines and add WINDOW lines in LTSpice .asc files.
import shutil

def process_asc_file_inplace(input_filename):
    """
    Processes an LTSpice .asc file in-place to remove SYMATTR Value2 lines and add WINDOW lines.

    Args:
        input_filename: Path to the input .asc file.
    """

    try:
        # Create a temporary file
        temp_filename = input_filename + ".tmp"
        with open(input_filename, 'r') as infile, open(temp_filename, 'w') as outfile:
            for line in infile:
                # Remove SYMATTR Value2 lines
                if "SYMATTR Value2" in line:
                    continue  # Skip this line

                outfile.write(line)

                # Add WINDOW line after SYMBOL lines for mosfets (nmosb or pmosb)
                if line.startswith("SYMBOL nmosb") or line.startswith("SYMBOL pmosb"):
                    outfile.write("WINDOW 3 63 27 Invisible 2\n")

        # Replace the original file with the temporary file
        shutil.move(temp_filename, input_filename)  # Overwrites the original

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_asc_file(input_filename, output_filename):
    """
    Processes an LTSpice .asc file to remove SYMATTR Value2 lines and add WINDOW lines.

    Args:
        input_filename: Path to the input .asc file.
        output_filename: Path to the output .asc file.
    """

    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                # Remove SYMATTR Value2 lines
                if "SYMATTR Value2" in line:
                    continue  # Skip this line

                outfile.write(line)

                # Add WINDOW line after SYMBOL lines for mosfets (nmosb or pmosb)
                if line.startswith("SYMBOL nmosb") or line.startswith("SYMBOL pmosb"):
                    outfile.write("WINDOW 3 63 27 Invisible 2\n")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
