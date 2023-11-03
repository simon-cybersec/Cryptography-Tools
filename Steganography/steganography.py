import sys
import os
import argparse
import pathlib
import base64
from PIL import Image
from PNGgraphy import *


#
# Process the parsed commandline arguments 
#
def process(args, parser):

    # Default output file name
    default_filename = "newFile"
    default_imagename = "newImage"

    # Calculate the number of bytes that can be embedded into the image
    image_byte_capacity = 0
    if args.image is not None:
        with Image.open(args.image) as image:
            width, height = image.size
            image_byte_capacity = width * height

            print(f'[+] Image: {image.filename}')
            print(f'[+] Format: {image.format}, Mode: {image.mode}')            
            print(f'[+] Width: {width}, Height: {height}')            
            print(f'[+] Byte capacity: {image_byte_capacity} \n')


    # ENCODING
    if args.encode is True:

        input_data = ''

        # If message is specified directly on commandline (no input file)
        if args.message is not None:

            # Check if the message length is too big. 1 byte of data needs 8 bytes of the image
            if len(args.message) * 8 > image_byte_capacity:
                print("ERROR: Message is too long!")
                exit(1)

            else:                
                # For the decoder to notice it's a cl message the input type is specified as 'm'
                input_type = 'm'

                # Input data is "m" + the message
                input_data = input_type + args.message

        # If input file is specified
        elif args.file is not None:

            # For the decoder to notice it's a file the input type is specified as 'f'
            input_type = 'f'

            # Check if file exists
            if pathlib.Path(args.file).is_file():
                print("[+] Check: file exists")

                # Check if the file size is too big. 1 byte of data needs 8 bytes of the image
                if pathlib.Path(args.file).stat().st_size * 8 > image_byte_capacity:
                    print("ERROR: Input file size is too big!")
                    exit(1)

                else:
                    # Open file in binary mode. Convert bytes to base64
                    with open(args.file, 'rb') as binary_file:
                        input_bytes = binary_file.read()
                        base64_encoded_bytes = base64.b64encode(input_bytes)
                        base64_message = base64_encoded_bytes.decode('utf-8')
                        # The input data is the data_type "f" + the above base64 string
                        input_data = input_type + base64_message

            # If file does not exist
            else:
                print("ERROR: Input file does not exist")
                exit(1)

        # If no message and no file is specified
        else:
            print("NOTE: Specify the data to embed into the image using -m or -f flag")
            exit(1)

        # Create output folder if not existing
        if not os.path.exists("./outputs/"):
            os.mkdir("./outputs/")

        # Encode the input data into the image
        with Image.open(args.image) as image:
            print("[+] Encoding ...")

            # If a output filename is specified
            if args.output is not None:
                encode(image, input_data, "./outputs/" + args.output)
            else:
                encode(image, input_data, "./outputs/" + default_imagename)

            print("[+] Done")

    # DECODING
    elif args.decode is True:

        decoded_data = ""
        with Image.open(args.image) as image:
            print("[+] Decoding ...")
            decoded_data = decode(image)            

        if decoded_data is not None:

            print("[+] Analysing ...")

            # We got a simple message
            if decoded_data[0] == "m":
                print("[+] Extracted a simple message")
                if args.output is not None:
                    print("[+] Writing message into file outputs/" + args.output + " ...")
                    print("[!] HINT: NEVER execute a file you don't know. Be sure it is not malicious ! ! !")
                    with open("outputs/" + args.output, 'a') as out:
                        out.write(decoded_data[1:] + '\n')
                    print("[+] Done")
                else:
                    print("[+] Message: " + decoded_data[1:])

            # We got a file
            elif decoded_data[0] == "f":
                print("[+] Extracted a file")

                # Convert base64 to binary
                base64_encoded_bytes = decoded_data[1:].encode('utf-8')
                decoded_bytes = base64.decodebytes(base64_encoded_bytes)

                # Create output folder if not existing
                if not os.path.exists("./outputs/"):
                    os.mkdir("./outputs/")

                # If output filename is specified
                if args.output is not None:
                    print("[+] Writing file outputs/" + args.output + " ...")
                    with open("outputs/" + args.output, 'wb') as file_to_save:
                        file_to_save.write(decoded_bytes)
                else:
                    print("[+] Writing file " + default_filename + " ... (no file extension)")
                    print("[!] HINT: NEVER execute a file you don't know. Be sure it is not malicious ! ! !")
                    with open("outputs/" + default_filename, 'wb') as file_to_save:
                        file_to_save.write(decoded_bytes)

                print("[+] Done")

            # If there is no messagetype found in the image (No 'm' or 'f')
            else:
                print("ERROR: No message type found in the image!")
                print("[+] Data gets dumped into error_log.txt ...")
                with open("outputs/error_log.txt", 'a') as out:
                    out.write(decoded_data + '\n')
                print("[+] Done")

    else:
        parser.print_help()

    return 0


#
# Main method
#
def main():
    # type () -> int
    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group(required=True)

    # image always required
    parser.add_argument("image",
                        type=str,
                        help="image file")

    # -e/-d one of them is required
    group1.add_argument("-e",
                        "--encode",
                        action='store_true',
                        help="encode")
    group1.add_argument("-d",
                        "--decode",
                        action='store_true',
                        help="decode")

    # -o not required
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="output image name or filepath")

    # -m/-f required
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-m",
                        "--message",
                        type=str,
                        help="message to be encoded.")
    group2.add_argument("-f",
                        "--file",
                        type=pathlib.Path,
                        help="file (name/path) to be encoded.")

    # Parse commandline arguments.
    args = parser.parse_args()

    return process(args, parser)


# --------- MAIN ---------
if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
