from collections import defaultdict
import pandas as pd
import lxml.html

def transform_table_to_list(table):
    dct = transform_table_to_dict(table)
    return list(dict_iter(dct))

def transform_table_to_dict(table):
    result = defaultdict(lambda : defaultdict(unicode))
    for row_i, row in enumerate(table.xpath('./tr')):
        for col_i, col in enumerate(row.xpath('./td|./th')):
            colspan = int(col.get('colspan', 1))
            rowspan = int(col.get('rowspan', 1))
            col_data = col.text_content()
            while row_i in result and col_i in result[row_i]:
                col_i += 1
            for i in range(row_i, row_i + rowspan):
                for j in range(col_i, col_i + colspan):
                    result[i][j] = col_data
    return result


def dict_iter(dct):
    for i, row in sorted(dct.items()):
        cols = []
        for j, col in sorted(row.items()):
            cols.append(col)
        yield cols


if __name__ == '__main__':
    
    doc = lxml.html.parse('table.html')
    for table_el in doc.xpath('//table'):
        table = transform_table_to_list(table_el)

        #print table
        pd.set_option('display.width', 1000)

        print "{:-^100}".format("-")
        df = pd.DataFrame(table[1:], columns=table[0])
        print df
        print "{:-^100}".format("-")

        

