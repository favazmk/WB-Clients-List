import json
import os
import zipfile
import xml.etree.ElementTree as ET

def apply_pm_corrections():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    corrected_excel = os.path.join(project_root, 'Client_Category_Verification_CORRECTED.xlsx')
    clients_json_path = os.path.join(script_dir, 'clients_data.json')
    clients_js_path = os.path.join(project_root, 'js', 'clients-data.js')

    # 1. Parse Excel Corrections
    corrections = {}
    with zipfile.ZipFile(corrected_excel) as z:
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

        for row in rows:
            r_idx = int(row.get('r'))
            if r_idx <= 5:
                continue
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

            domain = (cells.get('B') or '').strip()
            new_cat = (cells.get('D') or '').strip()
            if domain and new_cat:
                corrections[domain] = new_cat

    print(f"Extracted {len(corrections)} PM category corrections from Excel:")
    for dom, cat in corrections.items():
        print(f"  • {dom} -> {cat}")

    # 2. Update JSON
    with open(clients_json_path, 'r', encoding='utf-8') as f:
        clients_data = json.load(f)

    # Tag updates for relevancy
    tag_updates = {
        'bcgmllc.com': ["Industrial", "Engineering", "Trading", "Custom Domain"],
        'miyayurway.com': ["Wellness", "Health", "Ayurway", "Lifestyle", "Custom Domain"],
        'thefinobel.com': ["Fashion", "Apparel", "Textiles", "Finobel", "Custom Domain"],
        'argserviceuae.com': ["Engineering", "Maintenance", "Industrial Services", "UAE", "Custom Domain"],
        'nearme888.com': ["Business Directory", "Services", "Corporate", "Custom Domain"],
        'sadisorg.com': ["Healthcare", "Wellness", "Community", "Organization", "Custom Domain"],
        'britlyliving.co.uk': ["Home Retail", "Furniture", "E-Commerce", "Decor", "UK", "Custom Domain"],
        'scottkids.com': ["Kids", "Education", "Learning", "Community", "Custom Domain"]
    }

    updated_count = 0
    for client in clients_data:
        d = client['domain']
        if d in corrections:
            old_cat = client['category']
            client['category'] = corrections[d]
            if d in tag_updates:
                client['tags'] = tag_updates[d]
            print(f"Applied to JSON: {d} | '{old_cat}' -> '{corrections[d]}'")
            updated_count += 1

    with open(clients_json_path, 'w', encoding='utf-8') as f:
        json.dump(clients_data, f, indent=2, ensure_ascii=False)

    # 3. Update js/clients-data.js
    # Re-format as JavaScript file
    js_content = """/**
 * Clients Database for Sales Team Directory
 * Extracted and curated from Hostinger hPanel Client Roster
 * Verified & Updated via Project Manager Review
 */

const CLIENTS_DATA = """ + json.dumps(clients_data, indent=2, ensure_ascii=False) + """;
"""
    with open(clients_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\nSuccessfully updated {updated_count} records in:")
    print(f"  1. {clients_json_path}")
    print(f"  2. {clients_js_path}")

    # Print summary of categories
    from collections import Counter
    counts = Counter(c['category'] for c in clients_data)
    print(f"\nUpdated Business Categories Distribution ({len(counts)} industries):")
    for cat, cnt in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {cnt:2d} | {cat}")

if __name__ == '__main__':
    apply_pm_corrections()
