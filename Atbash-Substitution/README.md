# Atbash-Substituion  
The Atbash-substitution replaces an 'a' with a 'z' and so on.  
Encoding and decoding are done by the same method.  
Plaintext:  
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z  
Replacement:  
Z Y X W V U T S R Q P O N M L K J I H G F E D C B A  
  
# Usage

    atbash.py [-h] [-i INPUT | -m MESSAGE] [-o OUTPUT] [-g]

Arguments:  
  -h, --help: Show this help message and exit  
  
  -i, --input <file.txt>: Input text file  
  -m, --message <message>: Message from commandline  
  
  -o, --output <output.txt>: Output file. Otherwise write to commandline  
  -g, --group: Group the output in groupts of five  

  
