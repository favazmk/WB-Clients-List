import os
import xlsxwriter

def create_new_16_verification_sheet():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(project_root, 'New_16_Clients_Category_Verification.xlsx')

    workbook = xlsxwriter.Workbook(excel_path)

    # -------------------------------------------------------------
    # Styling & Formats
    # -------------------------------------------------------------
    font_family = 'Segoe UI'

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

    # Header formats
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

    # Data cells
    cell_num_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0',
        'font_color': '#64748b'
    })

    cell_name_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9.5,
        'bold': True,
        'font_color': '#0f172a',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
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

    cell_desc_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 9,
        'font_color': '#475569',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#e2e8f0'
    })

    cell_cat_fmt = workbook.add_format({
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

    section_header_fmt = workbook.add_format({
        'font_name': font_family,
        'font_size': 10,
        'bold': True,
        'font_color': '#475569',
        'bg_color': '#e2e8f0',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#cbd5e1'
    })

    # -------------------------------------------------------------
    # Sheet 1: Category Verification
    # -------------------------------------------------------------
    ws_main = workbook.add_worksheet('New Clients Verification')
    ws_main.set_tab_color('#4f46e5')
    ws_main.hide_gridlines(0)

    # Title block
    ws_main.set_row(0, 24)
    ws_main.set_row(1, 18)
    ws_main.set_row(2, 18)
    ws_main.write('A1', 'New Website Client Additions — Category Verification (16 Sites)', title_fmt)
    ws_main.write('A2', 'Total New Clients: 16  |  Click any website domain to inspect the live site if needed.', subtitle_fmt)
    ws_main.write('A3', '👉 If the Proposed Category in Column E is correct, leave Column F blank. If wrong, pick the correct category from the dropdown in Column F.', instruction_fmt)

    header_row = 4
    ws_main.set_row(header_row, 28)

    headers = [
        ('#', 6, th_center_fmt),
        ('Client Name', 25, th_fmt),
        ('Website Domain (Clickable)', 26, th_fmt),
        ('Business Description / Scope', 46, th_fmt),
        ('Proposed Category', 32, th_fmt),
        ('Correct Category (Select If Wrong) ▼', 34, th_action_fmt)
    ]

    for col_idx, (text, width, fmt) in enumerate(headers):
        ws_main.write(header_row, col_idx, text, fmt)
        ws_main.set_column(col_idx, col_idx, width)

    # 16 New Clients Data
    new_clients = [
        ("Al Wifaq Online", "alwifaqonline.com", "https://alwifaqonline.com", "UAE Based Casio Watch Exclusive Partner B2C with Payment Gateway", "E-Commerce & Retail"),
        ("Cedar Cosmetics", "cedarcosmetics.com", "https://cedarcosmetics.com", "UAE Based Korean Skincare (SKIN1004 Authorized Seller) B2C E-Commerce", "E-Commerce & Retail"),
        ("La Fille Élégante", "lafille-elegante.com", "https://lafille-elegante.com", "UAE Based Abaya & Modest Fashion Brand E-Commerce with Payment Gateway", "Fashion, Apparel & Textiles"),
        ("Vogue Venue", "voguevenue.ae", "https://voguevenue.ae", "UAE Multi-Brand Watch & Clock E-Commerce (Casio, Tommy Hilfiger, Armani)", "E-Commerce & Retail"),
        ("Sunrise Arabia", "sunrisearabia.com", "https://sunrisearabia.com", "Middle East & Oman Electronics & Mobile Accessories E-Commerce Brand", "E-Commerce & Retail"),
        ("Ashal United", "ashalunited.com", "https://ashalunited.com", "KSA Based B2B Home Appliances Website without Payment Gateway", "Industrial, Trading & Engineering"),
        ("Careintco International", "careintco.com", "https://careintco.com", "KSA/Oman Based Firm, Product Listings Only without E-Commerce", "Corporate & Business Services"),
        ("1Point360", "1point360.com", "https://1point360.com", "Business & Corporate Services Website", "Corporate & Business Services"),
        ("Ayursiha Hospital", "ayursiha.com", "https://ayursiha.com", "Kochi Based Ayurveda, Unani & Physiotherapy Hospital (EN/AR)", "Health, Fitness & Wellness"),
        ("Al Zehra Tours & Travels", "alzehra.com", "https://alzehra.com", "Kerala Tour Operator Website", "Travel, Tourism & Hospitality"),
        ("Amigos Logistics", "amigoslogistics.com", "https://amigoslogistics.com", "Dubai Based Logistics & Freight Forwarding Company", "Industrial, Trading & Engineering"),
        ("Ultimate Tek Solutions", "ultimatetek.in", "https://ultimatetek.in", "KSA/India Software & App Development Firm", "Technology & IT Solutions"),
        ("Ajman Global Pvt Ltd", "ajmanglobal.com", "https://ajmanglobal.com", "General Trading & Distribution Company Website", "Industrial, Trading & Engineering"),
        ("Tormac Marine", "tormacmarine.com", "https://tormacmarine.com", "Marine Services & Ship Management Company Website", "Industrial, Trading & Engineering"),
        ("Al Jamiathul Kauzariyya", "kauzariyya.com", "https://kauzariyya.com", "Islamic Arabic College Website with Blog & Donations", "Education & Community"),
        ("Hashir Nisam", "hashirnisam.com", "https://hashirnisam.com", "Personal Branding Website – Founder & CEO Portfolio", "Portfolios & Personal Brands")
    ]

    start_row = 5
    for i, (name, dom, url, desc, cat) in enumerate(new_clients):
        row = start_row + i
        ws_main.set_row(row, 22)
        ws_main.write(row, 0, i + 1, cell_num_fmt)
        ws_main.write(row, 1, name, cell_name_fmt)
        ws_main.write_url(row, 2, url, cell_link_fmt, dom)
        ws_main.write(row, 3, desc, cell_desc_fmt)
        ws_main.write(row, 4, cat, cell_cat_fmt)
        ws_main.write(row, 5, '', cell_dropdown_fmt)

    # 2 Existing Clients to Update (Rows 22 & 23)
    existing_fixes_row = start_row + len(new_clients)
    ws_main.set_row(existing_fixes_row, 22)
    ws_main.merge_range(existing_fixes_row, 0, existing_fixes_row, 5, "▼ EXISTING PORTAL CLIENTS TO RECLASSIFY / RENAME (FOR VERIFICATION)", section_header_fmt)

    existing_fixes = [
        ("Jabal Almadina Real Estate (JAMRE)", "jamre.ae", "https://jamre.ae", "Dubai Based Real Estate Brokerage with Property Listings (Previously mislabeled as BBQ & Grill)", "Real Estate & Interior Design"),
        ("Bandhan Construction", "bcgmllc.com", "https://bcgmllc.com", "Construction Company Website (Currently labeled as BCGM LLC)", "Industrial, Trading & Engineering")
    ]

    for j, (name, dom, url, desc, cat) in enumerate(existing_fixes):
        row = existing_fixes_row + 1 + j
        ws_main.set_row(row, 22)
        ws_main.write(row, 0, f"Fix {j + 1}", cell_num_fmt)
        ws_main.write(row, 1, name, cell_name_fmt)
        ws_main.write_url(row, 2, url, cell_link_fmt, dom)
        ws_main.write(row, 3, desc, cell_desc_fmt)
        ws_main.write(row, 4, cat, cell_cat_fmt)
        ws_main.write(row, 5, '', cell_dropdown_fmt)

    total_data_rows = len(new_clients) + 1 + len(existing_fixes)
    end_row = start_row + total_data_rows - 1

    # Freeze panes at row 5
    ws_main.freeze_panes(5, 0)

    # Data Validation on Column F (Column Index 5)
    ws_main.data_validation(start_row, 5, end_row, 5, {
        'validate': 'list',
        'source': '=Categories!$A$2:$A$17',
        'input_title': 'Select Category',
        'input_message': 'Choose the correct category if Column E needs adjustment.',
        'error_title': 'Invalid Category',
        'error_message': 'Please pick a category from the dropdown.'
    })

    # Conditional format: Purple highlight when PM selects a category
    fmt_changed = workbook.add_format({
        'bg_color': '#ede9fe',
        'font_color': '#6d28d9',
        'bold': True,
        'border': 1,
        'border_color': '#8b5cf6'
    })
    ws_main.conditional_format(start_row, 5, end_row, 5, {
        'type': 'no_blanks',
        'format': fmt_changed
    })

    # -------------------------------------------------------------
    # Sheet 2: Master Categories List
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
        ('Events & Event Planning', 'Event management, MICE exhibitions, conferences, celebrations'),
        ('Fashion, Apparel & Textiles', 'Clothing brands, ethnic wear, sarees, textile manufacturing'),
        ('Food & Beverage / Dining', 'Restaurants, cafes, bakeries, confectionery, snacks, cookies'),
        ('Gifts & Floral', 'Flower shops, gift delivery, floral boutiques'),
        ('Health, Fitness & Wellness', 'Gyms, fitness coaching, beauty salons, ayurvedic clinics, hospitals'),
        ('Industrial, Trading & Engineering', 'Heavy engineering, valves, trading, logistics & freight, manufacturing'),
        ('Luxury, Jewelry & Perfumes', 'Gold, diamond jewelry, luxury exhibitions, oud & perfumes'),
        ('Portfolios & Personal Brands', 'Personal websites, executive portfolios, designer showcases'),
        ('Real Estate & Interior Design', 'Property brokerages, interior design, architecture, luxury stays'),
        ('Technology & IT Solutions', 'IT support, software development, networking, security hardware'),
        ('Travel, Tourism & Hospitality', 'Tour operators, holiday packages, hostels, accommodations'),
        ('Other (Specify in Notes)', 'New category not listed above')
    ]

    ws_cat.set_row(0, 24)
    ws_cat.write('A1', 'Category Name (Dropdown Options)', cat_th_fmt)
    ws_cat.write('B1', 'Category Description & Scope', cat_th_fmt)
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
    print(f"Successfully generated verification sheet at {excel_path}!")

if __name__ == '__main__':
    create_new_16_verification_sheet()
