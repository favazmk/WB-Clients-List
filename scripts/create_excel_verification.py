import json
import os
import xlsxwriter

def create_pm_verification_sheet():
    # Resolve project root and data path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_file = os.path.join(script_dir, 'clients_data.json')
    excel_path = os.path.join(project_root, 'Client_Categories_Verification_Sheet.xlsx')

    # Load clients data
    with open(data_file, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    workbook = xlsxwriter.Workbook(excel_path)

    # -------------------------------------------------------------
    # Formats & Styles
    # -------------------------------------------------------------
    font_family = 'Segoe UI'

    title_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 16,
        'bold': True,
        'font_color': '#1e293b',
        'valign': 'vcenter'
    })

    subtitle_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'font_color': '#64748b',
        'valign': 'vcenter'
    })

    # KPI Summary Cards Formats
    kpi_card_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9,
        'bold': True,
        'font_color': '#475569',
        'bg_color': '#f8fafc',
        'border': 1,
        'border_color': '#cbd5e1',
        'align': 'center',
        'valign': 'vcenter'
    })

    kpi_val_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 13,
        'bold': True,
        'font_color': '#0f172a',
        'bg_color': '#f8fafc',
        'border': 1,
        'border_color': '#cbd5e1',
        'align': 'center',
        'valign': 'vcenter'
    })

    # Table Header Format
    th_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#ffffff',
        'bg_color': '#1e293b',
        'border': 1,
        'border_color': '#0f172a',
        'align': 'left',
        'valign': 'vcenter',
        'text_wrap': True
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

    # Action required header (Highlighted)
    th_highlight_fmt = workbook.add_format({
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

    # Row Data Formats
    cell_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    cell_bold_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'bold': True,
        'color': '#0f172a',
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    cell_center_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'align': 'center',
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    link_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'color': '#2563eb',
        'underline': True,
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    category_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'color': '#334155',
        'bg_color': '#f8fafc',
        'border': 1,
        'border_color': '#e2e8f0',
        'valign': 'vcenter'
    })

    dropdown_cell_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'border': 1,
        'border_color': '#cbd5e1',
        'bg_color': '#ffffff',
        'valign': 'vcenter'
    })

    status_dropdown_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'align': 'center',
        'border': 1,
        'border_color': '#cbd5e1',
        'bg_color': '#fffbeb',
        'font_color': '#b45309',
        'valign': 'vcenter'
    })

    # -------------------------------------------------------------
    # Sheet 1: Client Verification
    # -------------------------------------------------------------
    ws_main = workbook.add_worksheet('Client Verification')
    ws_main.set_tab_color('#4f46e5')
    ws_main.hide_gridlines(0)

    # Title & Subtitle
    ws_main.set_row(0, 26)
    ws_main.set_row(1, 18)
    ws_main.write('A1', 'Agency Website Client Directory — Category Verification Sheet', title_fmt)
    ws_main.write('A2', 'For Project Manager: Review assigned categories below. If correct, keep/mark "Approved". If incorrect, set "Needs Correction" and choose the right category in column F.', subtitle_fmt)

    # KPI Summary Row
    ws_main.set_row(3, 16)
    ws_main.set_row(4, 22)
    ws_main.write('B4', 'Total Clients', kpi_card_fmt)
    ws_main.write('B5', len(clients), kpi_val_fmt)

    ws_main.write('D4', 'Pending Review', kpi_card_fmt)
    ws_main.write_formula('D5', '=COUNTIF(E7:E78, "Pending Review")', kpi_val_fmt)

    ws_main.write('E4', 'Approved', kpi_card_fmt)
    ws_main.write_formula('E5', '=COUNTIF(E7:E78, "Approved")', kpi_val_fmt)

    ws_main.write('F4', 'Needs Correction', kpi_card_fmt)
    ws_main.write_formula('F5', '=COUNTIF(E7:E78, "Needs Correction")', kpi_val_fmt)

    # Table Column Headers (Row 6, index 5)
    headers = [
        ('#', 5, th_center_fmt),
        ('Client Name', 24, th_fmt),
        ('Website Domain (Clickable)', 32, th_fmt),
        ('Current Assigned Category', 32, th_fmt),
        ('PM Verification Status ▼', 22, th_highlight_fmt),
        ('Corrected Category (Dropdown) ▼', 34, th_highlight_fmt),
        ('PM Notes / Instructions', 32, th_fmt),
        ('Domain Type', 16, th_center_fmt),
        ('Platform', 16, th_center_fmt),
        ('Hosting Status', 22, th_center_fmt)
    ]

    header_row = 5
    ws_main.set_row(header_row, 28)

    for col_idx, (header_text, width, fmt) in enumerate(headers):
        ws_main.write(header_row, col_idx, header_text, fmt)
        ws_main.set_column(col_idx, col_idx, width)

    # Populate Data
    start_row = 6
    end_row = start_row + len(clients) - 1

    for i, client in enumerate(clients):
        row = start_row + i
        ws_main.set_row(row, 21)

        # Col 0: #
        ws_main.write(row, 0, i + 1, cell_center_fmt)

        # Col 1: Client Name
        ws_main.write(row, 1, client['name'], cell_bold_fmt)

        # Col 2: Website Domain (Clickable URL)
        ws_main.write_url(row, 2, client['url'], link_fmt, client['domain'])

        # Col 3: Current Category
        ws_main.write(row, 3, client['category'], category_fmt)

        # Col 4: PM Status (Default: Pending Review)
        ws_main.write(row, 4, 'Pending Review', status_dropdown_fmt)

        # Col 5: Corrected Category (Blank by default)
        ws_main.write(row, 5, '', dropdown_cell_fmt)

        # Col 6: PM Notes
        ws_main.write(row, 6, '', cell_fmt)

        # Col 7: Domain Type
        domain_label = 'Custom Domain' if client['type'] == 'custom' else 'Staging Subdomain'
        ws_main.write(row, 7, domain_label, cell_center_fmt)

        # Col 8: Platform
        ws_main.write(row, 8, client['platform'], cell_center_fmt)

        # Col 9: Status
        ws_main.write(row, 9, client['status'], cell_center_fmt)

    # -------------------------------------------------------------
    # Sheet 2: Categories Master List (Lookup Sheet)
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
        ('Other (Specify in Notes)', 'New category not listed above — specify in Column G')
    ]

    ws_cat.set_row(0, 24)
    ws_cat.write('A1', 'Category Name', cat_th_fmt)
    ws_cat.write('B1', 'Category Scope & Examples', cat_th_fmt)
    ws_cat.write('C1', 'Current Count', cat_th_fmt)

    ws_cat.set_column('A:A', 35)
    ws_cat.set_column('B:B', 65)
    ws_cat.set_column('C:C', 16)

    for idx, (cat_name, cat_desc) in enumerate(categories_list):
        r = idx + 1
        ws_cat.set_row(r, 20)
        ws_cat.write(r, 0, cat_name, cell_bold_fmt)
        ws_cat.write(r, 1, cat_desc, cell_fmt)
        # Count formula
        ws_cat.write_formula(r, 2, f'=COUNTIF(\'Client Verification\'!D$7:D$78, "{cat_name}")', cell_center_fmt)

    # -------------------------------------------------------------
    # Data Validation Rules
    # -------------------------------------------------------------
    # 1. PM Status Dropdown (Column E, Col 4)
    ws_main.data_validation(start_row, 4, end_row, 4, {
        'validate': 'list',
        'source': ['Approved', 'Needs Correction', 'Pending Review'],
        'input_title': 'Verification Status',
        'input_message': 'Choose "Approved" if category is accurate, or "Needs Correction" to change it.',
        'error_title': 'Invalid Selection',
        'error_message': 'Please select Approved, Needs Correction, or Pending Review.'
    })

    # 2. Corrected Category Dropdown (Column F, Col 5)
    ws_main.data_validation(start_row, 5, end_row, 5, {
        'validate': 'list',
        'source': '=Categories!$A$2:$A$16',
        'input_title': 'Select Category',
        'input_message': 'Pick the correct category from the master list if Column D is incorrect.',
        'error_title': 'Invalid Category',
        'error_message': 'Please select a valid category from the dropdown.'
    })

    # -------------------------------------------------------------
    # Conditional Formatting for Visual Clarity
    # -------------------------------------------------------------
    # Column E: Approved (Green)
    fmt_approved = workbook.add_format({
        'bg_color': '#dcfce7',
        'font_color': '#15803d',
        'bold': True
    })
    ws_main.conditional_format(start_row, 4, end_row, 4, {
        'type': 'cell',
        'criteria': '==',
        'value': '"Approved"',
        'format': fmt_approved
    })

    # Column E: Needs Correction (Red)
    fmt_correction = workbook.add_format({
        'bg_color': '#fee2e2',
        'font_color': '#b91c1c',
        'bold': True
    })
    ws_main.conditional_format(start_row, 4, end_row, 4, {
        'type': 'cell',
        'criteria': '==',
        'value': '"Needs Correction"',
        'format': fmt_correction
    })

    # Column E: Pending Review (Yellow)
    fmt_pending = workbook.add_format({
        'bg_color': '#fef3c7',
        'font_color': '#b45309',
        'bold': False
    })
    ws_main.conditional_format(start_row, 4, end_row, 4, {
        'type': 'cell',
        'criteria': '==',
        'value': '"Pending Review"',
        'format': fmt_pending
    })

    # Column F: Highlighted when filled
    fmt_corrected_val = workbook.add_format({
        'bg_color': '#ede9fe',
        'font_color': '#6d28d9',
        'bold': True
    })
    ws_main.conditional_format(start_row, 5, end_row, 5, {
        'type': 'no_blanks',
        'format': fmt_corrected_val
    })

    # Freeze panes at row 6 so header stays pinned while scrolling
    ws_main.freeze_panes(6, 0)

    # -------------------------------------------------------------
    # Sheet 3: How to Use Guide
    # -------------------------------------------------------------
    ws_help = workbook.add_worksheet('Instructions for PM')
    ws_help.set_tab_color('#3b82f6')
    ws_help.hide_gridlines(0)

    guide_title = workbook.add_format({
        'font_name': font_family,
        'font_size': 14,
        'bold': True,
        'font_color': '#1e293b'
    })
    guide_head = workbook.add_format({
        'font_name': font_family,
        'font_size': 11,
        'bold': True,
        'font_color': '#4f46e5'
    })
    guide_text = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'font_color': '#334155'
    })

    ws_help.set_column('A:A', 80)
    ws_help.write('A1', 'Project Manager Category Verification Guide', guide_title)
    ws_help.write('A3', 'Purpose of this Document:', guide_head)
    ws_help.write('A4', 'This workbook contains all 72 client websites extracted from the Hostinger hPanel. The sales portal categorizes each client to help the sales team prospect and explore sites by industry. Please verify each category.', guide_text)

    ws_help.write('A6', 'Step-by-Step Instructions:', guide_head)
    ws_help.write('A7', '1. Go to the "Client Verification" tab.', guide_text)
    ws_help.write('A8', '2. Review the Client Name in Column B and the Current Assigned Category in Column D.', guide_text)
    ws_help.write('A9', '3. You can click the Website Domain in Column C to open and inspect the live website.', guide_text)
    ws_help.write('A10', '4. In Column E ("PM Verification Status"), click the dropdown arrow and select:', guide_text)
    ws_help.write('A11', '    • "Approved" — If the assigned category is accurate.', guide_text)
    ws_help.write('A12', '    • "Needs Correction" — If the category is incorrect or needs improvement.', guide_text)
    ws_help.write('A13', '5. If you selected "Needs Correction", click the dropdown in Column F ("Corrected Category") and choose the right category.', guide_text)
    ws_help.write('A14', '6. If you need a new category or want to add context, write in Column G ("PM Notes / Instructions").', guide_text)
    ws_help.write('A15', '7. Save and return this file. The engineering team will update the portal immediately.', guide_text)

    workbook.close()
    print(f'Successfully created {excel_path}!')

if __name__ == '__main__':
    create_pm_verification_sheet()
