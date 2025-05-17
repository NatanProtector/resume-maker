import utils.PDFwrite as PDFwrite
template_pdf_address_default = "./resourses/template.pdf"
result_address_default = "./result.pdf"

def applyName(name_addres, pdf_address, result_address):
    with open(name_addres, 'r', encoding='utf-8') as file:
        content = file.read()
        
        x = 200
        y = 725
        width = 180
        height = 50
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)

def applyDetails(details_addres, pdf_address, result_address):
    with open(details_addres, 'r', encoding='utf-8') as file:
        content = file.read()

        x = 10
        y = 610        
        width = 170
        height = 170
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)
        
def applySkills(skills_addres, pdf_address, result_address):
    with open(skills_addres, 'r', encoding='utf-8') as file:
        content = file.read()
        
        x = 10
        y = 400
        width = 170
        height = 200
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)
        
def applyLanguages(skills_addres, pdf_address, result_address):
    
    with open(skills_addres, 'r', encoding='utf-8') as file:
        content = file.read()
        
        x = 10
        y = 230
        width = 170
        height = 150
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)
        
def applyBody(body_addres, pdf_address, result_address):
    with open(body_addres, 'r', encoding='utf-8') as file:
        content = file.read()
        
        x = 200
        y = 10
        width = 400
        height = 650
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)
        
def applyBio(bio_addres, pdf_address, result_address):
    with open(bio_addres, 'r', encoding='utf-8') as file:
        content = file.read()
        
        x = 200
        y = 665
        width = 400
        height = 50
        
        PDFwrite.write_content_to_area(x, y, width, height, content, pdf_address, result_address)
        
        
if __name__ == "__main__":
    applySkills("./info/skills.txt", template_pdf_address_default, result_address_default)
    applyLanguages("./info/languages.txt", result_address_default, result_address_default)
    applyBody("./info/body.txt", result_address_default, result_address_default)
    applyName("./info/name.txt", result_address_default, result_address_default)
    applyBio("./info/bio.txt", result_address_default, result_address_default)
    applyDetails("./info/details.txt", result_address_default, result_address_default)
    