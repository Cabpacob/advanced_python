from astdrawercabpacob import medium
from easy import table, get_table_tex, get_document_tex
from pdflatex import PDFLaTeX


def get_graphics_tex(graphics_path):
    return '\n\t\\includegraphics[width=80mm]' + f'{{{graphics_path}}}\n'


if __name__ == '__main__':
    medium.draw_tree('fib.py', 'artifacts/tree.png')

    graphics_tex = get_graphics_tex('artifacts/tree.png')
    table_tex = get_table_tex(table)

    with open('artifacts/medium.tex', 'w') as f:
        t = get_document_tex(graphics_tex + table_tex).encode()
        f.write(get_document_tex(graphics_tex + table_tex))

    pdfl = PDFLaTeX.from_binarystring(t, 'artifacts/medium')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
