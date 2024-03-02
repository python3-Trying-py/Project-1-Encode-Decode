# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 21:49:06 2024

@author: payta
"""

import CryptographJUPYTER as CJ

CJ.Encrypt("Plaintext.txt")

fileOrigin = open("original.txt")
contentsOrigin = fileOrigin.read()
print(contentsOrigin)