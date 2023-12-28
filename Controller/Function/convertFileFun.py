from pypdf import PdfReader , PdfMerger
from ArabicOcr import arabicocr
from werkzeug.utils import secure_filename
from datetime import datetime
import pypandoc
from pypandoc.pandoc_download import download_pandoc
download_pandoc()
import os
from flask import current_app
from docx import Document
from bs4 import BeautifulSoup
from io import BytesIO

def pdfToText(reader):
    # reader = PdfReader(file,'utf-8')
    reader = PdfReader(reader, "utf-8")
    number_of_pages = len(reader.pages)
    i=0
    f=open("outputPdf.txt",'wb')
    while i<=number_of_pages-1:
        page = reader.pages[i]  
        text = page.extract_text().encode("utf-8")
        i+=1
        print(text)
        f.write(text) 
    f.close()  
    f1=open("outputPdf.txt", "rb")
    result = f1.read().decode("utf-8")
    print(result)
    return result

def imageToText(image,out_image):
    image_path='Files/Temp/{}'.format(image)
    # out_image='Files/Images/out.jpg'
    results=arabicocr.arabic_ocr(image_path,out_image)
    print(results)
    words=[]
    for i in range(len(results)):	
            word=results[i][1]
            words.append(word)
    with open ('file.txt','w',encoding='utf-8') as myfile:
        myfile.write(" ".join(words))
    f1=open("file.txt", "r", encoding="utf-8")
    text = f1.read()
    print(text)
    return text

def wordSum(data):
    filename = os.path.join(current_app.config['UPLOAD_FOLDER_WORD'], secure_filename(str(datetime.now())+" "+"sum.docx"))
    with open("tempText.txt", 'w', encoding="utf-8") as f:
        f.write("الوصف :")
        f.write("\n\n")
        f.write(data["abs"])
        f.write("\n\n")
        f.write("التلخيص :")
        f.write("\n\n")
        f.write(data["ex"])
    pypandoc.convert_file('tempText.txt', 'rst', format='md',outputfile="tempMd.md")
    pypandoc.convert_file('tempMd.md', 'docx', outputfile=filename)
    return filename

def wordExam(data):
    filename = os.path.join(current_app.config['UPLOAD_FOLDER_WORD'], secure_filename(str(datetime.now())+" "+"exam.docx"))
    with open("tempText.txt", 'w', encoding="utf-8") as f:
        f.write("1- اختر الإجابة الصحيحة مما يلي:")
        f.write("\n\n")
        for x in data["q"]:
            f.write("\t\t")
            f.write("-")
            f.write(x["text"])
            f.write("\n\n")
            for y in x["option"]:
                f.write("\t\t\t")
                f.write(y["text"])
                f.write("\n\n")
        f.write("\n\n")
        f.write("2- اجب عن الأسئلة التالية :")
        f.write("\n\n")
        for x in data["qs"]:
            f.write("\t\t")
            f.write("-")
            f.write(x)
            f.write("\n\n")
        f.write("\n\n")
        f.write("3- إملأ الفراغات التالية :")
        f.write("\n\n")
        for x in data["wi"]:
            f.write("\t\t")
            f.write("-")
            f.write(x)
            f.write("\n\n")
    pypandoc.convert_file('tempText.txt', 'rst', format='md',outputfile="tempMd.md")
    pypandoc.convert_file('tempMd.md', 'docx', outputfile=filename)
    return filename

# from docx2html import convert

# def convert_word_to_html(file_path):
#     # document = Document(file_path)
#     # output = BytesIO()
#     # document.save(output)
#     # soup = BeautifulSoup(output.getvalue(), 'html.parser')
#     # html = soup.prettify()
#     html = convert(file_path)
#     return html