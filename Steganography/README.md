# Steganography
Embedding data into images.

The tool is able to embed two different types of data into the pixels of an image:
- simple message strings
- whole files

It extracts these either into files or in case of a simple message string also to the command line.

# Usage  
1. Create a new python virtual environment. Then install the required packages:

    pip3 install -r requirements.txt

2. Execute the python script:

    python3 steganography.py <image file> (-e | -d) [-m MESSAGE | -f FILE] [-o OUTPUT] [-h] 

    -h, --help ................ show help message  
    -e, --encode .............. encode flag  
    -d, --decode .............. decode flag  
    -o, --output OUTPUT ....... output file name  
    -m, --message MESSAGE ..... string message to be embedded  
    -f, --file FILE ........... file to be embedded.  


# Examples:  

    # Encode a commandline message string into the image "image.png". The generated image "flower.png" is saved in the "outputs" directory:
    python3 steganography.py -e image.jpg -m "Hello world" -o flower.png
    # Decode it again:
    python3 steganography.py -d outputs/flower.png

    # Encode the file "file.txt" into the pixels of the image "image.jpg" and save it as "flower.png":
    python3 steganography.py -e image.jpg -f ../file.txt -o flower.png
    # Decode it again:
    python3 steganography.py -d myNewImage.png -o myfile.txt

# How the tool is structured

### steganography.py :
In the steganography.py the user input gets parsed and processed. All data is prepared for encoding/decoding. It then passes this data to the encode() and decode() methods written in PNGgraphy.py  

### PNGgraphy.py
The real binary encoding and decoding happens here. It's called "PNGgraphy" because it encodes only to png images. To encode data into a .jpg file a different encoding is necessary because of jpg-compression.  

### utils.py
Some useful helpers  
  

# How the tool works 
Each pixel consists of four bytes: the red value, green value, blue value and the alpha channel. Altering the least significant bit of one of the color values can't be recognized by the human eye.  

The tool splits each byte of a message or file into its bits and stores these at the least significant bit of the red channel of a pixel. Because todays cameras and smartphones produce high quality pictures in size of mega bytes a lot of data can be stored into one image.  

Hint: If sending an image containing embedded data make sure it does not get compressed otherwise the data is lost. In messanger apps send it as a "document" instead of an "image".  

Be aware: NEVER execute a received file if you don't know what it does. Always make sure it is not malicious!
