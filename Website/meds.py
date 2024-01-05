import PyPDF2
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


pdf_data = PdfReader("C:\\Users\\ritaf\\Documents\\ESTUDOS\\NOVA IMS\\3º Ano\\Capstone Project\\Projeto\\meds.pdf")
pdf_text = ""

for i, page in enumerate(pdf_data.pages):
    text = page.extract_text()
    if text:
        pdf_text += text

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 700,
    chunk_overlap = 100
)

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()
meds_data = text_splitter.split_text(pdf_text)
enablePrint()

