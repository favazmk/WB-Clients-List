import zipfile
import xml.etree.ElementTree as ET

def parse_excel_corrections():
    excel_file = 'Client_Category_Verification_CORRECTED.xlsx'
    with zipfile.ZipFile(excel_file) as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            sst_xml = z.read('xl/sharedStrings.xml')
            sst_root = ET.fromstring(sst_xml)
            for si in sst_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                t_elems = si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                shared_strings.append(''.join(t.text or '' for t in t_elems))

        sheet_xml = z.read('xl/worksheets/sheet1.xml')
        sheet_root = ET.fromstring(sheet_xml)

        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        rows = sheet_root.findall('.//ns:row', ns)

        corrections = []
        all_rows = []

        for row in rows:
            r_idx = int(row.get('r'))
            cells = {}
            for c in row.findall('ns:c', ns):
                ref = c.get('r')
                col_letter = ''.join(filter(str.isalpha, ref))
                cell_type = c.get('t')
                val_elem = c.find('ns:v', ns)
                val = val_elem.text if val_elem is not None else None

                if cell_type == 's' and val is not None:
                    val = shared_strings[int(val)]
                elif cell_type == 'inlineStr':
                    is_elem = c.find('.//ns:t', ns)
                    val = is_elem.text if is_elem is not None else ''

                cells[col_letter] = val

            if r_idx > 5 and 'B' in cells:
                col_a = cells.get('A', '')
                col_b = cells.get('B', '')
                col_c = cells.get('C', '')
                col_d = cells.get('D', '')
                all_rows.append((r_idx, col_a, col_b, col_c, col_d))
                if col_d and str(col_d).strip():
                    corrections.append((r_idx, col_a, col_b, col_c, col_d))

        print(f"Total client rows: {len(all_rows)}")
        print(f"Total corrections from PM: {len(corrections)}\n")
        for r_idx, num, domain, old_cat, new_cat in corrections:
            print(f"#{num} | Domain: {domain} | Old: '{old_cat}' -> NEW: '{new_cat}'")

if __name__ == '__main__':
    parse_excel_corrections()
