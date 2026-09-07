import json
import os
import xlsxwriter

def create_pm_verification_sheet():
    # Resolve project root and data path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_file = os.path.join(script_dir, 'clients_data.json')
    excel_path = os.path.join(project_root, 'Client_Category_Verification.xlsx')

    # Load clients data
    with open(data_file, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    workbook = xlsxwriter.Workbook(excel_path)

    # -------------------------------------------------------------
    # Styling & Formats (Modern, Professional, Clean)
    # -------------------------------------------------------------
    font_family = 'Segoe UI'

    # Title & Subtitle Formats
    title_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 15,
        'bold': True,
        'font_color': '#0f172a',
        'valign': 'vcenter'
    })

    subtitle_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'font_color': '#64748b',
        'valign': 'vcenter'
    })

    instruction_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'bold': True,
        'font_color': '#4f46e5',
        'valign': 'vcenter'
    })

    # Header Formats
    th_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#ffffff',
        'bg_color': '#1e293b',
        'border': 1,
        'border_color': '#0f172a',
        'align': 'left',
        'valign': 'vcenter'
    })

    th_center_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#ffffff',
        'bg_color': '#1e293b',
        'border': 1,
        'border_color': '#0f172a',
        'align': 'center',
        'valign': 'vcenter'
    })

    # Action Column Header (Highlighted Indigo)
    th_action_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#ffffff',
        'bg_color': '#4f46e5',
        'border': 1,
        'border_color': '#3730a3',
        'align': 'center',
        'valign': 'vcenter'
    })

    # Cell Data Formats
    cell_num_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0',
        'font_color': '#64748b'
    })

    cell_link_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'font_color': '#2563eb',
        'underline': True,
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })

    cell_category_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'font_color': '#1e293b',
        'bg_color': '#f8fafc',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })

    cell_dropdown_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#cbd5e1',
        'bg_color': '#ffffff'
    })

    # -------------------------------------------------------------
    # Sheet 1: Category Verification (Main 4-Column Sheet)
    # -------------------------------------------------------------
    ws_main = workbook.add_worksheet('Category Verification')
    ws_main.set_tab_color('#4f46e5')
    ws_main.hide_gridlines(0)

    # Title & Instructions block
    ws_main.set_row(0, 24)
    ws_main.set_row(1, 18)
    ws_main.set_row(2, 18)
    ws_main.write('A1', 'Agency Website Clients — Category Verification', title_fmt)
    ws_main.write('A2', 'Total Clients: 72  |  Click any domain to view the live website if needed.', subtitle_fmt)
    ws_main.write('A3', '👉 Review Column C: If the category is correct, leave Column D blank. If wrong, choose the correct one from the dropdown in Column D.', instruction_fmt)

    # 4 Table Columns (Row index 4 = Excel Row 5)
    header_row = 4
    ws_main.set_row(header_row, 28)

    headers = [
        ('#', 6, th_center_fmt),
        ('Domain', 34, th_fmt),
        ('Current Assigned Category', 34, th_fmt),
        ('Correct Category (Select If Wrong) ▼', 36, th_action_fmt)
    ]

    for col_idx, (text, width, fmt) in enumerate(headers):
        ws_main.write(header_row, col_idx, text, fmt)
        ws_main.set_column(col_idx, col_idx, width)

    # Data Rows
    start_row = 5
    end_row = start_row + len(clients) - 1

    for i, client in enumerate(clients):
        row = start_row + i
        ws_main.set_row(row, 22)

        # 1. #
        ws_main.write(row, 0, i + 1, cell_num_fmt)

        # 2. Domain (Clickable Link)
        ws_main.write_url(row, 1, client['url'], cell_link_fmt, client['domain'])

        # 3. Current Assigned Category
        ws_main.write(row, 2, client['category'], cell_category_fmt)

        # 4. Correct Category (Dropdown - blank by default)
        ws_main.write(row, 3, '', cell_dropdown_fmt)

    # Freeze panes so header row 5 stays visible on scroll
    ws_main.freeze_panes(header_row + 1, 0)

    # Data Validation (Dropdown on Column D, rows 6 to 77)
    ws_main.data_validation(start_row, 3, end_row, 3, {
        'validate': 'list',
        'source': '=Categories!$A$2:$A$16',
        'input_title': 'Select Correct Category',
        'input_message': 'Pick the correct category here only if the current category in Column C is wrong.',
        'error_title': 'Invalid Category',
        'error_message': 'Please select a valid category from the dropdown.'
    })

    # Conditional Formatting: Highlight in soft purple when the PM makes a correction!
    fmt_changed = workbook.add_format({
        'bg_color': '#ede9fe',
        'font_color': '#6d28d9',
        'bold': True,
        'border': 1,
        'border_color': '#8b5cf6'
    })
    ws_main.conditional_format(start_row, 3, end_row, 3, {
        'type': 'no_blanks',
        'format': fmt_changed
    })

    # -------------------------------------------------------------
    # Sheet 2: Categories (Master Category Reference for Dropdown)
    # -------------------------------------------------------------
    ws_cat = workbook.add_worksheet('Categories')
    ws_cat.set_tab_color('#059669')
    ws_cat.hide_gridlines(0)

    cat_th_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#ffffff',
        'bg_color': '#059669',
        'border': 1,
        'valign': 'vcenter'
    })

    categories_list = [
        ('Corporate & Business Services', 'Legal, HR, PRO, business setup, consulting, and finance'),
        ('Creative Agency & Media', 'Branding, advertising, digital studios, media production'),
        ('E-Commerce & Retail', 'Online retail stores, supermarkets, eyewear, electronics'),
        ('Education & Community', 'Schools, academies, non-profit institutions, community orgs'),
        ('Fashion, Apparel & Textiles', 'Clothing brands, ethnic wear, sarees, textile manufacturing'),
        ('Food & Beverage / Dining', 'Restaurants, cafes, bakeries, confectionery, snacks, cookies'),
        ('Gifts & Floral', 'Flower shops, gift delivery, floral boutiques'),
        ('Health, Fitness & Wellness', 'Gyms, fitness coaching, beauty salons, ayurvedic clinics'),
        ('Industrial, Trading & Engineering', 'Heavy engineering, valves, trading, paper hygiene manufacturing'),
        ('Luxury, Jewelry & Perfumes', 'Gold, diamond jewelry, luxury exhibitions, oud & perfumes'),
        ('Portfolios & Personal Brands', 'Personal websites, executive portfolios, designer showcases'),
        ('Real Estate & Interior Design', 'Property brokerages, interior design, architecture, luxury stays'),
        ('Technology & IT Solutions', 'IT support, software development, networking, security hardware'),
        ('Travel, Tourism & Hospitality', 'Tour operators, holiday packages, hostels, accommodations'),
        ('Other (Specify in Notes)', 'New category not listed above')
    ]

    ws_cat.set_row(0, 24)
    ws_cat.write('A1', 'Category Name (Dropdown List)', cat_th_fmt)
    ws_cat.write('B1', 'Category Description & Examples', cat_th_fmt)

    ws_cat.set_column('A:A', 35)
    ws_cat.set_column('B:B', 70)

    cat_bold_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'bold': True,
        'font_color': '#0f172a',
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    cat_desc_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'font_color': '#475569',
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    for idx, (cat_name, cat_desc) in enumerate(categories_list):
        r = idx + 1
        ws_cat.set_row(r, 20)
        ws_cat.write(r, 0, cat_name, cat_bold_fmt)
        ws_cat.write(r, 1, cat_desc, cat_desc_fmt)

    workbook.close()
    print(f'Successfully generated simplified Excel sheet at {excel_path}!')

if __name__ == '__main__':
    create_pm_verification_sheet()
