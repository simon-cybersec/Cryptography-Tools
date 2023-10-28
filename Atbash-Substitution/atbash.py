##
## Encoding/decoding text using the atbash-substitution
##
## Atbash replaces an 'a' by 'z' and so on.
## Encoding and decoding are done by the same method.
##      a b c d e f g h i j k l m n o p q r s t u v w x y z  
##      Z Y X W V U T S R Q P O N M L K J I H G F E D C B A
import argparse
import sys
import re

# Atbash lookup-table
lookup = {
    "a": "z",
    "b": "y",
    "c": "x",
    "d": "w",
    "e": "v",
    "f": "u",
    "g": "t",
    "h": "s",
    "i": "r",
    "j": "q",
    "k": "p",
    "l": "o",
    "m": "n",
    "n": "m",
    "o": "l",
    "p": "k",
    "q": "j",
    "r": "i",
    "s": "h",
    "t": "g",
    "u": "f",
    "v": "e",
    "w": "d",
    "x": "c",
    "y": "b",
    "z": "a",
    " ": " ",
    "\n": "\n",
    ".": ".",
    "!": "!",
    ",": ","
}


#
# Atbash substitution
#
def atbash(text):

    # Convert text to lower case
    text = text.lower()

    # Replace special characters (withou '\n', '.', '!', ',')
    text = re.sub('[^a-zA-Z0-9 \n\.\!\,]', '', text)

    # Keep numbers
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    # Replace each character by the one in the lookup table
    atbash_text = ""    
    for t in text:
        
        # Keep numbers
        if t in numbers:
            atbash_text += t

        # Otherwise take the lookup value
        else:
            atbash_text += lookup[t]

    return atbash_text


#
# Process the parsed commandline arguments
#
def process(args, parser):  

    # List conataining the resulting atbash-strings
    atbash_lines = []

    # If an input file is specified
    if args.input is not None:
        try:
            print("[Input ] " + args.input.name )

            # Read all lines into a list
            lines = args.input.readlines()
            
            # Process each line:
            for line in lines:
                atbash_lines.append( atbash(line) )

        # Close file
        finally:
            if args.input: args.input.close()

    # If instead a message is given on the commandline
    elif args.message is not None:
        message = args.message
        print("[Input] ")
        print(message)

        # Execute atbash substitution
        atbash_lines.append( atbash(message) + "\n" )


    # If flag is set to group the output in groups of five characters
    if args.group is True:
        
        # Remove newline character   
        for i in range(0, len(atbash_lines)):
            atbash_lines[i] = atbash_lines[i].strip("\n")
        
        # Join all lines together
        big_string = ""
        for i in range(0, len(atbash_lines)):
            big_string += atbash_lines[i].strip("\n")
        
        # Replace all whitespaces
        big_string = big_string.replace(" ", "")
        print("Big string: " + big_string)

        # Group into groups of five
        group_string = ""
        g = 0 # group counter
        for i in range(0, len(big_string)):
            group_string += big_string[i]
            g += 1

            # If group is fullhouse reset
            if g == 5:
                g = 0
                group_string += " "

        print("Group string: " + group_string)



    # If an output file is specified write to it
    if args.output is not None:
        try:
            print("[Output] " + args.output.name )

            # If option "-g" not specified write non-grouped output
            if args.group is False:
                for line in atbash_lines:
                    args.output.write( line )

            # Otherwise write groupted output
            else:

                # Create list of grouped words
                words = group_string.split(" ")
                line  = ""

                # If number of grouped words is not bigger than 5 write string directly
                if len(words) <= 5:
                    args.output.write( group_string + "\n" )

                # Otherwise create lines of 5 words and write those
                else:
                    counter = 0
                    for word in words:
                        line += word + " "
                        counter += 1
                        if counter == 5:
                            args.output.write( line + "\n" )
                            line = ""
                            counter = 0
                    # Write the remaining words (block of less than 5 words)
                    if len(line) != 0:
                        args.output.write( line + "\n")

        # Close file
        finally:
            if args.output: args.output.close()

    # If no outputfile is specified write to commandline
    else:
        print("\n[Output] ")

        # If option "-g" not specified write non-grouped output
        if args.group is False:
            for line in atbash_lines:
                print( line.strip("\n") )

        # Otherwise write groupted output
        else:

            # Create list of grouped words
            words = group_string.split(" ")
            line  = ""

            # If number of grouped words is not bigger than 5 write string directly
            if len(words) <= 5:
                print( group_string )

            # Otherwise create lines of 5 words and write those
            else:
                counter = 0
                for word in words:
                    line += word + " "
                    counter += 1
                    if counter == 5:
                        print( line )
                        line = ""
                        counter = 0
                # Write the remaining words (block of less than 5 words)
                if len(line) != 0:
                    print( line + "\n")

    return 0


#
# Main method. Parse the commandline arguments
#
def main():
    print(":: ATBASH CONVERTER ::")

    parser = argparse.ArgumentParser()

    # Input either as file or as commandline string
    input_group = parser.add_mutually_exclusive_group()

    input_group.add_argument(
        '-i', '--input',
        help='Text input file',
        type=argparse.FileType('r'),
    )

    input_group.add_argument(
        '-m', '--message',
        help='Message from commandline',
        type=str
    )
    
    # Output either to file or on commanline
    parser.add_argument(
        '-o', '--output',
        help='Output file. Otherwise write to commandline',
        type=argparse.FileType('w'),
    )

    # Optional specify to group output in groups of five characters
    parser.add_argument(
        '-g', '--group',
        help='Group the output in groupts of five',
        action='store_true')  # on/off flag

    # Parse commandline arguments
    args = parser.parse_args()

    return process(args, parser)


if __name__ == '__main__':
    # Execute main method
    ret = main()
    sys.exit(ret)
    