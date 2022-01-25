import xlwt

class Fichero:
    
    def __init__(self, listaContactos):
        self.listaContactos = listaContactos
    
    def guardarExcel(self, nombreFichero):
        writeBook= xlwt.Workbook(encoding='utf-8')
        sheet = writeBook.add_sheet("document",cell_overwrite_ok=True)
        style = xlwt.XFStyle()

        sheet.write(0, 0, 'WEB')
        sheet.write(0, 1, 'EMAIL')
        cont=1
        for contacto in self.listaContactos:
            sheet.write(cont, 0, contacto.web)
            sheet.write(cont, 1, contacto.email)
            cont = cont + 1

        writeBook.save(nombreFichero)