import json
import os
import sys

def apply_all_updates():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    json_path = os.path.join(script_dir, 'clients_data.json')
    js_path = os.path.join(project_root, 'js', 'clients-data.js')

    with open(json_path, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    # 1. Apply Verified Corrections to Existing Clients
    corrections_map = {
        'rijuss.hashirnisam.com': {
            'name': "Riju's Natural Skincare",
            'category': 'Health, Fitness & Wellness',
            'tags': ['Skincare', 'Soaps', 'Natural Wellness', 'Handcrafted', 'Staging']
        },
        'shaistafathima.com': {
            'category': 'Portfolios & Personal Brands',
            'tags': ['Data Analytics', 'AI / ML', 'Software Testing', 'Portfolio', 'Custom Domain']
        },
        'bcgmllc.com': {
            'name': 'Bandhan Construction',
            'category': 'Industrial, Trading & Engineering',
            'tags': ['Construction', 'Contracting', 'General Maintenance', 'UAE', 'Custom Domain']
        },
        'binsbay.com': {
            'category': 'Creative Agency & Media',
            'tags': ['Sign Printing', 'Branding', 'Advertising', 'Videography', 'Web Dev', 'Custom Domain']
        },
        'dvice.uk': {
            'category': 'Technology & IT Solutions',
            'tags': ['Electronics', 'Power Conversion', 'Hardware Manufacturing', 'UK', 'Custom Domain']
        },
        'halavanew.hashirnisam.com': {
            'name': 'Halava Sweets',
            'category': 'Food & Beverage / Dining',
            'tags': ['Halwa', 'Traditional Sweets', 'F&B', 'Staging']
        },
        'raysportsuae.com': {
            'category': 'Health, Fitness & Wellness',
            'tags': ['Gym Equipment', 'Fitness', 'Sports Flooring', 'Maintenance', 'UAE', 'Custom Domain']
        },
        'jamre.ae': {
            'name': 'Jabal Almadina Real Estate (JAMRE)',
            'category': 'Real Estate & Interior Design',
            'tags': ['Real Estate Brokerage', 'Property Sales & Leasing', 'Dubai', 'Custom Domain']
        },
        'bettermarknew.hashirnisam.com': {
            'name': 'Bettermark Groceries',
            'category': 'E-Commerce & Retail',
            'tags': ['Online Grocery', 'Fresh Produce', 'Fruits & Vegetables', 'Delivery', 'Staging']
        }
    }

    updated_existing = 0
    for c in clients:
        d = c['domain']
        if d in corrections_map:
            c_update = corrections_map[d]
            if 'name' in c_update:
                c['name'] = c_update['name']
            c['category'] = c_update['category']
            if 'tags' in c_update:
                c['tags'] = c_update['tags']
            print(f"Updated existing client: {d} -> {c['name']} | {c['category']}")
            updated_existing += 1

    # 2. Add 16 New Verified Clients
    existing_domains = {c['domain'].lower() for c in clients}

    new_16 = [
        {
            "id": "client-76",
            "name": "Al Wifaq Online",
            "domain": "alwifaqonline.com",
            "url": "https://alwifaqonline.com",
            "type": "custom",
            "category": "E-Commerce & Retail",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Watches", "Casio Partner", "G-SHOCK", "E-Commerce", "UAE", "Custom Domain"]
        },
        {
            "id": "client-77",
            "name": "Cedar Cosmetics",
            "domain": "cedarcosmetics.com",
            "url": "https://cedarcosmetics.com",
            "type": "custom",
            "category": "E-Commerce & Retail",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Cosmetics", "Skincare", "SKIN1004", "K-Beauty", "E-Commerce", "UAE", "Custom Domain"]
        },
        {
            "id": "client-78",
            "name": "La Fille Élégante",
            "domain": "lafille-elegante.com",
            "url": "https://lafille-elegante.com",
            "type": "custom",
            "category": "Fashion, Apparel & Textiles",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Abayas", "Modest Fashion", "Designer Apparel", "E-Commerce", "UAE", "Custom Domain"]
        },
        {
            "id": "client-79",
            "name": "Vogue Venue",
            "domain": "voguevenue.ae",
            "url": "https://voguevenue.ae",
            "type": "custom",
            "category": "E-Commerce & Retail",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Watches", "Clocks", "Multi-Brand Retail", "E-Commerce", "UAE", "Custom Domain"]
        },
        {
            "id": "client-80",
            "name": "Sunrise Arabia",
            "domain": "sunrisearabia.com",
            "url": "https://sunrisearabia.com",
            "type": "custom",
            "category": "E-Commerce & Retail",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Electronics", "Mobile Accessories", "Headphones", "E-Commerce", "Oman", "Custom Domain"]
        },
        {
            "id": "client-81",
            "name": "Ashal United",
            "domain": "ashalunited.com",
            "url": "https://ashalunited.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Home Appliances", "B2B Trading", "Multimedia", "Distribution", "KSA", "Custom Domain"]
        },
        {
            "id": "client-82",
            "name": "Careintco International",
            "domain": "careintco.com",
            "url": "https://careintco.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Electronics Trading", "Distribution", "Sourcing", "KSA", "Oman", "Custom Domain"]
        },
        {
            "id": "client-83",
            "name": "1Point360",
            "domain": "1point360.com",
            "url": "https://1point360.com",
            "type": "custom",
            "category": "Corporate & Business Services",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Accounting", "Audit", "Tax", "PRO Services", "Business Setup", "Custom Domain"]
        },
        {
            "id": "client-84",
            "name": "Ayursiha Hospital",
            "domain": "ayursiha.com",
            "url": "https://ayursiha.com",
            "type": "custom",
            "category": "Health, Fitness & Wellness",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Ayurveda Hospital", "Physiotherapy", "Unani", "Healthcare", "Kochi", "Custom Domain"]
        },
        {
            "id": "client-85",
            "name": "Al Zehra Tours & Travels",
            "domain": "alzehra.com",
            "url": "https://alzehra.com",
            "type": "custom",
            "category": "Travel, Tourism & Hospitality",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Tours & Travels", "Kerala Tourism", "Vacation Packages", "Holidays", "Custom Domain"]
        },
        {
            "id": "client-86",
            "name": "Amigos Logistics",
            "domain": "amigoslogistics.com",
            "url": "https://amigoslogistics.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Freight Forwarding", "Logistics", "Air Freight", "Sea Freight", "Dubai", "Custom Domain"]
        },
        {
            "id": "client-87",
            "name": "Ultimate Tek Solutions",
            "domain": "ultimatetek.in",
            "url": "https://ultimatetek.in",
            "type": "custom",
            "category": "Technology & IT Solutions",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Software Development", "ERP", "POS Solutions", "Mobile Apps", "Custom Domain"]
        },
        {
            "id": "client-88",
            "name": "Ajman Global Pvt Ltd",
            "domain": "ajmanglobal.com",
            "url": "https://ajmanglobal.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["General Trading", "Wholesale Trade", "Commodities", "Distribution", "Custom Domain"]
        },
        {
            "id": "client-89",
            "name": "Tormac Marine",
            "domain": "tormacmarine.com",
            "url": "https://tormacmarine.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Marine Services", "Ship Management", "Offshore", "Crewing", "Shipping", "Custom Domain"]
        },
        {
            "id": "client-90",
            "name": "Al Jamiathul Kauzariyya",
            "domain": "kauzariyya.com",
            "url": "https://kauzariyya.com",
            "type": "custom",
            "category": "Education & Community",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Arabic College", "Education", "Islamic Academy", "Community", "Donations", "Custom Domain"]
        },
        {
            "id": "client-91",
            "name": "Hashir Nisam",
            "domain": "hashirnisam.com",
            "url": "https://hashirnisam.com",
            "type": "custom",
            "category": "Portfolios & Personal Brands",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Founder", "CEO Portfolio", "Personal Branding", "Executive", "Custom Domain"]
        }
    ]

    added_new = 0
    for entry in new_16:
        if entry['domain'].lower() not in existing_domains:
            clients.append(entry)
            print(f"Added new verified client: [{entry['id']}] {entry['name']} ({entry['domain']}) -> {entry['category']}")
            added_new += 1
            existing_domains.add(entry['domain'].lower())

    # Save to JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)

    # Save to JS
    js_content = """/**
 * Clients Database for Sales Team Directory
 * Verified & Updated from Client_Category_Verification_FULLY_VERIFIED_FIXED.xlsx
 * and Client_Category_Verification_16_WEBSITES_VERIFIED.xlsx
 */

const CLIENTS_DATA = """ + json.dumps(clients, indent=2, ensure_ascii=False) + """;
"""
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\n==========================================")
    print(f"Existing Clients Corrected: {updated_existing}")
    print(f"New Verified Clients Added: {added_new}")
    print(f"Total Clients in Database:  {len(clients)}")
    print(f"==========================================\n")

    from collections import Counter
    counts = Counter(c['category'] for c in clients)
    print(f"Updated Business Distribution ({len(counts)} industries):")
    for cat, cnt in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {cnt:2d} | {cat}")

if __name__ == '__main__':
    apply_all_updates()
