def compareTextFiles(file1_path, file2_path):
    """
    Compares two text files line by line, identifies differences, and shows differing characters.

    Args:
        file1_path: Path to the first file.
        file2_path: Path to the second file.

    Returns:
        A list of tuples, where each tuple contains:
        (row, column, char1, char2) for character differences, or
        (row, column, None, char) for extra characters in a line, or
        None if there's an error opening the files.
        Returns an empty list if files are identical.
    """
    try:
        with open(file1_path, 'r', encoding='latin-1') as file1, open(file2_path, 'r', encoding='latin-1') as file2:
            differences = []
            row_num = 1
            for line1, line2 in zip(file1, file2):
                col_num = 1
                for char1, char2 in zip(line1, line2):
                    if char1 != char2:
                        differences.append((row_num, col_num, char1, char2))
                    col_num += 1
                # Handle different line lengths:
                len_diff = abs(len(line1) - len(line2))
                start_diff_col = min(len(line1), len(line2)) + 1
                if len_diff > 0 and not (line1.strip() == "" and line2.strip() == ""):
                    if len(line1) > len(line2):
                        for i in range(len_diff):
                            differences.append((row_num, start_diff_col + i, line1[start_diff_col + i-1], None))
                    else:
                        for i in range(len_diff):
                            differences.append((row_num, start_diff_col + i, None, line2[start_diff_col + i-1]))

                row_num += 1

            # Check for extra lines in either file
            remaining_lines1 = file1.readlines()
            remaining_lines2 = file2.readlines()
            if remaining_lines1:
                for line in remaining_lines1:
                    col_num = 1
                    for char in line:
                        differences.append((row_num, col_num, char, None))
                        col_num += 1
                    row_num += 1
            if remaining_lines2:
                for line in remaining_lines2:
                    col_num = 1
                    for char in line:
                        differences.append((row_num, col_num, None, char))
                        col_num += 1
                    row_num += 1
            # return differences
            if differences is None:
                pass # Error already handled
            elif not differences:
                print("The files are identical.")
            else:
                print("The files differ at the following positions:")
                for row, col, char1, char2 in differences:
                    if char1 is not None and char2 is not None:
                        print(f"Row: {row}, Column: {col}: File1: '{char1}', File2: '{char2}'")
                    elif char1 is None:
                        print(f"Row: {row}, Column: {col}: File1: (Missing), File2: '{char2}'")
                    else:
                        print(f"Row: {row}, Column: {col}: File1: '{char1}', File2: (Missing)")


    except FileNotFoundError:
        print("Error: One or both files not found.")
        return None
    except Exception as e: #Catching other potential errors
        print(f"An error occurred: {e}")
        return None


# # Example usage:
# file1_path = "file1.txt"  # Replace with your file paths
# file2_path = "file2.txt"

# differences = compare_text_files(file1_path, file2_path)

# if differences is None:
#     pass #Error already handled in the function
# elif not differences:
#     print("The files are identical.")
# else:
#     print("The files differ at the following positions:")
#     for row, col in differences:
#         print(f"Row: {row}, Column: {col}")
