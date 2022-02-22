def get_tex_row(row):
    return ' & '.join(map(str, row))


def get_table_tex(table):
    return '''
    \\begin{{center}}
        \\begin{{tabular}}{{{cs}}}
            \\hline
            {rows} \\\\
            \\hline
        \\end{{tabular}}
    \\end{{center}}
    '''.format(
        cs = ' ' + len(table[0]) * '|c' + '| ',
        rows = ' \\\\ \n\t\t\t\\hline \n\t\t\t'.join(map(get_tex_row, table))
        )


def get_document_tex(content):
    return '''\\documentclass{{letter}}
\\usepackage{{graphicx}}
\\begin{{document}}
{content}
\\end{{document}}
'''.format(content=content)


table = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


if __name__ == '__main__':
    rows = len(table)
    columns = len(table[0])

    def equal_len(row):
        return len(row) == columns

    if not all(map(equal_len, table)):
        raise KeyError(f'wrong table with {columns} columns and {rows} rows')

    document_tex = get_document_tex(get_table_tex(table))
    with open('artifacts/easy.tex', 'w') as f:
        f.write(document_tex)
