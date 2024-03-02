# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:53:35 2024

@author: payta
"""

"""
Pseudocode:
    Copy and paste my encryption program into the encryption function with a few tweaks
    1. change the code so the user can input a file name
    2. move the encryption dictionary out side the function just so the function looks cleaner when written
    3. add an exception for the case in which a user inputs their own key and it is unable to encrypt specific characters
    
    Luckily I thought ahead and coded a decrypter about 2 weeks ago
    I'll just copy and paste that as well but I'll include the pseudo code for that below
        "1. Read encrypted.txt and convert to string
         2. run through every two digits in the new string and convert the two digit segments to their
            corresponding character
         3. Write that string to a decrypted.txt"
    Obviously I'll need to change this a bit
    1. I'll add an excpetion for the case in which the decryption key provided cannot decrypt a peice of given text
       This exception will insert an error into the string and when write to the original.txt will do 3 things
           1. Write the decrypted text w/o any error signals
           2. Write the decrypted text w/ error signals
           3. Write a warning that the text couldn't be properly decrypted
    2. It will write to original.txt, not decrypted.txt
    3. I'll need to make the function except a custom file name and key
    
    Finally I'll write a Encrypt/Decrypt function that does both of these to make testing and using much easier
    
    For the purpose of needing only one key I will also be adding a function to invert a dictionary
"""

#This function inverts a dictionary. This saves me time and makes the program cleaner
def inv_dict(key):
    return key.__class__(map(reversed, key.items()))

#dictionary with a 2 digit number corresponding to each lowercase letter, uppercase letter, number, and special character
#This is the default encryption dictionary
EncryptKeyDefault = {"a":"01","b":"02","c":"03","d":"04","e":"05","f":"06","g":"07","h":"08","i":"09",
                     "j":"10","k":"11","l":"12","m":"13","n":"14","o":"15","p":"16","q":"17","r":"18",
                     "s":"19","t":"20","u":"21","v":"22","w":"23","x":"24","y":"25","z":"26","0":"27",
                     "1":"28","2":"29","3":"30","4":"31","5":"32","6":"33","7":"34","8":"35","9":"36",
                     ".":"37",",":"38"," ":"39","A":"40","B":"41","C":"42","D":"43","E":"44","F":"45",
                     "G":"46","H":"47","I":"48","J":"49","K":"50","L":"51","M":"52","N":"53","O":"54",
                     "P":"55","Q":"56","R":"57","S":"58","T":"59","U":"60","V":"61","W":"62","X":"63",
                     "Y":"64","Z":"65","\n":"66"}

#This is the Decryption key for the default encryption key. It is just the inverse of the encryption key,
#using the inverse function define at the beginning of the program
DecryptKeyDefault = inv_dict(EncryptKeyDefault)


#This is the encryption function. It takes the file name and a dictionary for encryption
#The encryption dictionary is set to default to the dictionary at the beginning of the program if no
#encryption dictionary is provided
def Encrypt(FileName, encryptDict = EncryptKeyDefault):
    #Reads from file, and puts file contents into string
    filePlain = open(FileName,"r")
    stringPlain = filePlain.read()

    #creates a string that will store encrypted text
    stringEncrypt = ""

    #measures the length of the to-be-encrypted text
    stringLength = int(len(stringPlain))
    n = range(0,stringLength)

    #runs though each letter in the plain text and places its corresponding digit pair in the encrypted string
    #The function will attempt to convert a character into its corresponding encryption character(s)
    #if unsuccessful it will simply print error in that characters place
    for i in n:
        try:
            stringEncrypt += str(encryptDict[stringPlain[i]])
        
        except:
            stringEncrypt += "[ERROR]"
        
    #opens and writes the contents of the encrypted string into the encrypted file
    fileEncrypt = open(r"encrypted.txt","w")
    fileEncrypt.write(stringEncrypt)
    
#This is the decryption function. It takes a decryption key in the form of a dictionary, though it will
#default to DecryptKeyDefault, which is created at the beginning of the program
#keyLength defines how much space is between encrypted characters(e.g the default encryption key converts
#characters to 2 digit combinations, such as 01 and 34, so the keyLength is 2. Another key which might
#convert characters into 4 character combinations, such as 27H! and 7#j9, would have a keyLength of 4)
def Decrypt(decryptDict = DecryptKeyDefault, keyLength = 2):
    
    #opens the encrypted file and reads the text from it
    fileEncrypted = open(r"encrypted.txt","r")
    stringEncrypted = fileEncrypted.read()
    
    #creates an empty string that will be filled with the decrypted text
    stringDecrypt = ""

    #finds the length of the encrypted text
    stringLength = int(len(stringEncrypted))
    
    #error is used to track if there are any errors when decryptign the encrypted text. This will be used
    #to determine if a new "error version" of the string needs to be created and if said string needs to be
    #printed into the original.txt
    error = False

    #creates a basic counter for the coming while loop
    i = 0
    #I use a while loop here because I can't figure out how to modify the index of a for loop
    #The loop will look at the number of characters defined by keyLength(Default of 2) and then compare those
    #characters to the decryption dictionary and insert the corresponding character into stringDecrypt
    #The loop while iterate over each group of characters until it has iterated over the entirety of stringEncrypted
    #If the program comes upon a character it cannot decrypt it will create a copy string that will have
    #[ERROR] inserted at the points where a character could not be decrypted. If the program comes across a previous
    #error in the program it will replace it with [PREVIOUS ERROR]
    #the temp string is used for copying the stringDecrypt
    temp = ""
    while (i < stringLength):
        
        #First we try to decrypt a group of characters
        #check is used to temporarily store the number of characters within the keyLength
        #This is done using another while loop which just inserts the needed characters into check
        #Then we insert the whatever character corresponds to check using our decrption dictionary into 
        #stringDecrypt and do the same for temp. Then we increase the counter by the keyLength
        try:
            check = ""
            j = i
            while (j <= i + keyLength):
                check += stringEncrypted[j]
            stringDecrypt += decryptDict[check]
            temp += decryptDict[check]
            i += keyLength  
     
        #if check cannot be decrypted then we move to the error section below
        except:
            
            #Here we create a new string to store our decrypted string with errors and we update it to match
            #our current string
            stringDecryptError = ""
            stringDecryptError += temp
            
            #This if statement checks if it is the first time we have an error, and if we do it flips error
            #from being false to being true. We use this later to decide how we print the output into original.txt
            if (error == False):
                error = True
            
            #The following try and except statements check to see if the next bit of text was a previous error
            #If this is checking within the last 6 characters of the encrypted string, then the except statement
            #ensures that the program deos not get stuck tryign to read characters that aren't there
            try:
                #Test stores the next 7 characters of the encrypted string into a temporary variable and then
                #checks to see if it reads [ERROR] which would signify it was a previous error from encrypting
                #if it was a previous error, then we insert a different error sign that signifies that it is
                #a previous error.
                #the else statement just inserts a normal error signifier if it is not a previous error
                test = stringEncrypted[i] + stringEncrypted[i + 1] + stringEncrypted[i + 2] + stringEncrypted[i + 3] + stringEncrypted[i + 4] + stringEncrypted[i + 5] + stringEncrypted[i + 6]
                if (test == "[ERROR]"):
                    stringDecryptError += "[PREVIOUS ERROR]"
                    temp = ""
                    i += 7
                
                else:
                   stringDecryptError += "[ERROR]"
                   temp = ""
                   i += keyLength 
            
            #This except statement just catches the program in case test attempts to read past the end of the encrypted string
            except:             
                stringDecryptError += "[ERROR]"
                temp = ""
                i += keyLength
    
    #If there was an error then the final bit of stringDecryptError will be updated
    if (error == True):
        stringDecryptError += temp
    
    #if there was an error then we will print the decrypted text without errors and with errors, along with
    #a notice that there were errors in the decryption process.
    fileDencrypt = open(r"original.txt","w")
    if (error == True):
        errorString = "Decrypted Text(Errors omitted):\n" + stringDecrypt + "\n\n\nDecrypted Text(Errors included):\n" + stringDecryptError + "\n\n\n[Text could not be properly encrypted or decrypted]"
        fileDencrypt.write(errorString)
    else:
        fileDencrypt.write(stringDecrypt)

#This function just runs both Encrypt and Decrypt. Nice and tidy
def EncryptAndDecrypt(FileName, encryptDict = EncryptKeyDefault, decryptDict = DecryptKeyDefault):  
    Encrypt(FileName, encryptDict)
    Decrypt(decryptDict)

#This is all of that code in a nice tidy line. Using the default parameters.
EncryptAndDecrypt("Plaintext.txt")

"""
Author Note:
    This was actually a really fun one to write. I feel like I got a lot of chances to make things more
    efficient and plenty more to overcomplicate things. But hey, I like a flexible program.
"""
