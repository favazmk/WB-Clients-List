import os
import sys
import json
import re
import ssl
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import xlsxwriter

# Category Keyword Profiles
CATEGORY_PROFILES = {
    'E-Commerce & Retail': [
        'shop', 'store', 'cart', 'checkout', 'add to cart', 'price', 'product', 'products',
        'sale', 'retail', 'buy', 'order', 'shipping', 'delivery', 'cosmetics', 'watches',
        'ecommerce', 'e-commerce', 'skincare', 'groceries', 'supermarket'
    ],
    'Food & Beverage / Dining': [
        'restaurant', 'cafe', 'cafeteria', 'food', 'dining', 'menu', 'tea', 'karak',
        'coffee', 'sweets', 'bakery', 'confectionery', 'halwa', 'snacks', 'dishes',
        'dine-in', 'takeaway', 'cookies', 'catering', 'kitchen', 'taste', 'cuisine'
    ],
    'Industrial, Trading & Engineering': [
        'engineering', 'industrial', 'trading', 'maintenance', 'construction', 'contracting',
        'logistics', 'freight', 'cargo', 'shipping', 'forwarding', 'marine', 'ship', 'offshore',
        'machinery', 'equipment', 'fabrication', 'technical', 'general trading', 'distribution',
        'appliances', 'wholesale'
    ],
    'Fashion, Apparel & Textiles': [
        'fashion', 'abaya', 'abayas', 'modest', 'saree', 'sarees', 'silk', 'dress', 'apparel',
        'clothing', 'textile', 'textiles', 'designer', 'boutique', 'ethnic wear', 'fabrics'
    ],
    'Health, Fitness & Wellness': [
        'health', 'clinic', 'hospital', 'doctor', 'ayurveda', 'ayurvedic', 'wellness',
        'fitness', 'gym', 'workout', 'physiotherapy', 'skincare', 'treatment', 'salon',
        'beauty', 'spa', 'panchakarma', 'medical', 'appointment', 'booking', 'unani'
    ],
    'Corporate & Business Services': [
        'business setup', 'corporate', 'pro services', 'accounting', 'audit', 'tax',
        'consulting', 'consultancy', 'advisory', 'trade license', 'tasheel', 'typing center',
        'directory', 'business directory'
    ],
    'Real Estate & Interior Design': [
        'real estate', 'property', 'properties', 'apartment', 'villa', 'broker', 'brokerage',
        'leasing', 'rent', 'rental', 'sale', 'interior design', 'architecture', 'architects',
        'interior', 'decor', 'residential', 'commercial'
    ],
    'Portfolios & Personal Brands': [
        'portfolio', 'about me', 'resume', 'founder', 'ceo', 'profile', 'personal brand',
        'achievements', 'projects', 'works', 'biography', 'consultant'
    ],
    'Creative Agency & Media': [
        'creative agency', 'advertising', 'branding', 'marketing', 'printing', 'sign printing',
        'videography', 'photography', 'media production', 'graphic design', 'visual', 'studio'
    ],
    'Technology & IT Solutions': [
        'software', 'it solutions', 'technology', 'tech', 'development', 'erp', 'pos',
        'mobile app', 'networking', 'cctv', 'security', 'hardware', 'power conversion',
        'electronics'
    ],
    'Education & Community': [
        'school', 'college', 'academy', 'education', 'islamic', 'learning', 'courses',
        'students', 'kids', 'community', 'institute', 'donations', 'charity', 'tharbiya'
    ],
    'Luxury, Jewelry & Perfumes': [
        'jewelry', 'jewellery', 'gold', 'diamond', 'luxury', 'perfumes', 'fragrance',
        'oud', 'gems', 'expo', 'precious stones', 'watches & jewelry'
    ],
    'Travel, Tourism & Hospitality': [
        'tours', 'travels', 'travel', 'tourism', 'vacation', 'holidays', 'packages',
        'hostel', 'accommodation', 'living spaces', 'booking', 'hotel', 'flight'
    ],
    'Gifts & Floral': [
        'flowers', 'floral', 'bouquet', 'bouquets', 'roses', 'florist', 'flower delivery', 'gifts'
    ],
    'Events & Event Planning': [
        'events', 'event planning', 'conference', 'conferences', 'exhibition', 'exhibitions',
        'mice', 'event management', 'wedding planning'
    ]
}

PARKED_PATTERNS = [
    r'parking\.hostinger',
    r'there\'?s nothing here yet',
    r'domain parked',
    r'default web site page',
    r'account suspended',
    r'website under construction',
    r'under maintenance',
    r'buy this domain',
    r'domain is pending',
    r'cpanel',
    r'welcome to nginx'
]

def check_single_domain(client):
    domain = client['domain']
    url = client.get('url', f"https://{domain}")
    assigned_cat = client.get('category', 'Unknown')
    client_name = client.get('name', domain)

    res = {
        'id': client.get('id', ''),
        'name': client_name,
        'domain': domain,
        'url': url,
        'assigned_cat': assigned_cat,
        'http_status': None,
        'final_url': None,
        'title': '',
        'meta_desc': '',
        'headings': '',
        'detected_cat': None,
        'verification_status': 'UNKNOWN',
        'confidence': 'LOW',
        'notes': '',
        'error_detail': ''
    }

    # Custom SSL context to allow inspecting sites with minor SSL handshake/cert issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close'
    }

    # Try HTTPS first, then HTTP fallback
    target_urls = [url]
    if url.startswith('https://'):
        target_urls.append(url.replace('https://', 'http://'))

    html_text = ""
    for target in target_urls:
        req = urllib.request.Request(target, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=8, context=ctx) as response:
                res['http_status'] = response.status
                res['final_url'] = response.geturl()
                content_bytes = response.read(150000) # read first 150KB
                try:
                    html_text = content_bytes.decode('utf-8', errors='ignore')
                except Exception:
                    html_text = str(content_bytes)
                break
        except urllib.error.HTTPError as e:
            res['http_status'] = e.code
            try:
                html_text = e.read(50000).decode('utf-8', errors='ignore')
            except Exception:
                pass
            res['error_detail'] = f"HTTP {e.code}"
            break
        except urllib.error.URLError as e:
            res['error_detail'] = str(e.reason)
        except Exception as e:
            res['error_detail'] = str(e)

    if not html_text:
        # Site offline or DNS failed
        res['verification_status'] = 'OFFLINE / UNREACHABLE'
        res['notes'] = f"Could not establish connection: {res['error_detail'] or 'Timeout'}"
        return res

    # Extract Title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_text, re.IGNORECASE | re.DOTALL)
    if title_match:
        res['title'] = re.sub(r'\s+', ' ', title_match.group(1)).strip()

    # Extract Meta Description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html_text, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']', html_text, re.IGNORECASE)
    if desc_match:
        res['meta_desc'] = re.sub(r'\s+', ' ', desc_match.group(1)).strip()

    # Extract H1/H2
    headings = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', html_text, re.IGNORECASE | re.DOTALL)
    clean_headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings if h.strip()]
    res['headings'] = " | ".join(clean_headings[:4])

    # Check for Parked / Under Construction / Hostinger Placeholder
    search_corpus = f"{res['title']} {res['meta_desc']} {res['headings']} {html_text[:5000]}".lower()
    for pattern in PARKED_PATTERNS:
        if re.search(pattern, search_corpus):
            res['verification_status'] = 'PARKED / PLACEHOLDER'
            res['notes'] = 'Hosting placeholder, parked page, or under construction'
            return res

    # Semantic Keyword Scoring
    cat_scores = {cat: 0 for cat in CATEGORY_PROFILES}
    for cat, keywords in CATEGORY_PROFILES.items():
        for kw in keywords:
            # check title (weight 4)
            if kw in res['title'].lower():
                cat_scores[cat] += 4
            # check meta desc (weight 3)
            if kw in res['meta_desc'].lower():
                cat_scores[cat] += 3
            # check headings (weight 2)
            if kw in res['headings'].lower():
                cat_scores[cat] += 2
            # check first 5k HTML (weight 1)
            if kw in search_corpus:
                cat_scores[cat] += 1

    sorted_scores = sorted(cat_scores.items(), key=lambda x: x[1], reverse=True)
    best_cat, best_score = sorted_scores[0]
    assigned_score = cat_scores.get(assigned_cat, 0)

    res['detected_cat'] = best_cat

    # Evaluation
    if assigned_score > 0 and (best_cat == assigned_cat or (best_score - assigned_score) <= 2):
        res['verification_status'] = 'VERIFIED MATCH'
        res['confidence'] = 'HIGH' if assigned_score >= 4 else 'MODERATE'
        res['notes'] = f"Content keywords strongly match assigned category ({assigned_score} pts)."
    elif assigned_score == 0 and best_score >= 5 and best_cat != assigned_cat:
        res['verification_status'] = 'POSSIBLE MISMATCH'
        res['confidence'] = 'HIGH'
        res['notes'] = f"Content signals '{best_cat}' ({best_score} pts) rather than '{assigned_cat}'."
    elif assigned_score > 0:
        res['verification_status'] = 'VERIFIED MATCH'
        res['confidence'] = 'MODERATE'
        res['notes'] = f"Relevant keywords found for assigned category ({assigned_score} pts)."
    else:
        # Minimal keywords detected (e.g. sparse splash page or heavy JS rendering)
        res['verification_status'] = 'NEEDS MANUAL CHECK'
        res['confidence'] = 'LOW'
        res['notes'] = f"Limited metadata found. Page Title: '{res['title'][:50]}'"

    return res

def run_audit():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    json_path = os.path.join(script_dir, 'clients_data.json')
    report_xlsx = os.path.join(project_root, 'Domain_Live_Verification_Report_Updated.xlsx')

    with open(json_path, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    print(f"============================================================")
    print(f"Starting Live Domain & Category Audit for {len(clients)} Websites...")
    print(f"============================================================")

    results = []
    # 12 concurrent threads for fast execution
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_client = {executor.submit(check_single_domain, c): c for c in clients}
        completed_count = 0
        for future in as_completed(future_to_client):
            r = future.result()
            results.append(r)
            completed_count += 1
            status_icon = "MATCH" if r['verification_status'] == 'VERIFIED MATCH' else ("MISMATCH" if r['verification_status'] == 'POSSIBLE MISMATCH' else ("PARKED" if r['verification_status'] == 'PARKED / PLACEHOLDER' else "OFFLINE"))
            print(f"[{completed_count:2d}/{len(clients)}] [{status_icon:<8}] {r['domain'][:26]:<26} | HTTP {str(r['http_status']):<3} | Cat: {r['assigned_cat'][:25]}")

    # Sort results by original client ID order
    def extract_id(item):
        try:
            return int(item['id'].replace('client-', ''))
        except:
            return 999
    results.sort(key=extract_id)

    # Breakdown Stats
    verified_matches = [r for r in results if r['verification_status'] == 'VERIFIED MATCH']
    mismatches = [r for r in results if r['verification_status'] == 'POSSIBLE MISMATCH']
    parked = [r for r in results if r['verification_status'] == 'PARKED / PLACEHOLDER']
    offline = [r for r in results if r['verification_status'] == 'OFFLINE / UNREACHABLE']
    manual = [r for r in results if r['verification_status'] == 'NEEDS MANUAL CHECK']

    print(f"\n============================================================")
    print(f"Audit Summary for {len(results)} Domains:")
    print(f"  Verified Matches:        {len(verified_matches):2d}")
    print(f"  Potential Mismatches:     {len(mismatches):2d}")
    print(f"  Needs Manual Check:      {len(manual):2d}")
    print(f"  Parked / Placeholder:     {len(parked):2d}")
    print(f"  Offline / Unreachable:    {len(offline):2d}")
    print(f"============================================================\n")

    # Generate Professional Excel Workbook
    wb = xlsxwriter.Workbook(report_xlsx)
    ws = wb.add_worksheet('Verification Audit')
    ws.views = [{'show_grid_lines': True}]

    # Formatting
    font_name = 'Segoe UI'
    hdr_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 10, 'bold': True,
        'bg_color': '#1e293b', 'font_color': '#ffffff',
        'border': 1, 'border_color': '#cbd5e1', 'valign': 'vcenter'
    })
    cell_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5,
        'border': 1, 'border_color': '#e2e8f0', 'valign': 'vcenter'
    })
    link_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5,
        'font_color': '#2563eb', 'underline': True,
        'border': 1, 'border_color': '#e2e8f0', 'valign': 'vcenter'
    })
    verified_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5, 'bold': True,
        'bg_color': '#ecfdf5', 'font_color': '#047857',
        'border': 1, 'border_color': '#a7f3d0', 'valign': 'vcenter', 'align': 'center'
    })
    mismatch_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5, 'bold': True,
        'bg_color': '#fef2f2', 'font_color': '#b91c1c',
        'border': 1, 'border_color': '#fecaca', 'valign': 'vcenter', 'align': 'center'
    })
    parked_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5,
        'bg_color': '#fffbeb', 'font_color': '#b45309',
        'border': 1, 'border_color': '#fde68a', 'valign': 'vcenter', 'align': 'center'
    })
    offline_fmt = wb.add_format({
        'font_name': font_name, 'font_size': 9.5,
        'bg_color': '#f1f5f9', 'font_color': '#64748b',
        'border': 1, 'border_color': '#cbd5e1', 'valign': 'vcenter', 'align': 'center'
    })

    headers = [
        '#', 'Client Name', 'Website Domain', 'HTTP', 'Live Page Title',
        'Meta Description / Snippet', 'Assigned Category', 'Detected Signals',
        'Audit Status', 'Notes / Analysis'
    ]
    ws.set_row(0, 26)
    for col_idx, h in enumerate(headers):
        ws.write(0, col_idx, h, hdr_fmt)

    ws.set_column(0, 0, 5)   # #
    ws.set_column(1, 1, 26)  # Name
    ws.set_column(2, 2, 28)  # Domain
    ws.set_column(3, 3, 7)   # HTTP
    ws.set_column(4, 4, 34)  # Title
    ws.set_column(5, 5, 40)  # Description
    ws.set_column(6, 6, 28)  # Assigned
    ws.set_column(7, 7, 26)  # Detected
    ws.set_column(8, 8, 20)  # Status
    ws.set_column(9, 9, 45)  # Notes

    for row_idx, r in enumerate(results, start=1):
        ws.set_row(row_idx, 22)
        idx_num = int(r['id'].replace('client-', '')) if 'client-' in r['id'] else row_idx
        ws.write(row_idx, 0, idx_num, cell_fmt)
        ws.write(row_idx, 1, r['name'], cell_fmt)
        ws.write_url(row_idx, 2, r['url'], link_fmt, string=r['domain'])
        ws.write(row_idx, 3, r['http_status'] if r['http_status'] else 'ERR', cell_fmt)
        ws.write(row_idx, 4, r['title'][:60] if r['title'] else '-', cell_fmt)
        ws.write(row_idx, 5, r['meta_desc'][:80] if r['meta_desc'] else (r['headings'][:80] if r['headings'] else '-'), cell_fmt)
        ws.write(row_idx, 6, r['assigned_cat'], cell_fmt)
        ws.write(row_idx, 7, r['detected_cat'] if r['detected_cat'] else '-', cell_fmt)

        stat = r['verification_status']
        if stat == 'VERIFIED MATCH':
            fmt = verified_fmt
        elif stat == 'POSSIBLE MISMATCH':
            fmt = mismatch_fmt
        elif stat == 'PARKED / PLACEHOLDER':
            fmt = parked_fmt
        else:
            fmt = offline_fmt
        ws.write(row_idx, 8, stat, fmt)
        ws.write(row_idx, 9, r['notes'], cell_fmt)

    wb.close()
    print(f"Generated Live Audit Workbook: {report_xlsx}")

    # Also save structured JSON results for analysis
    results_json = os.path.join(script_dir, 'audit_results.json')
    with open(results_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    run_audit()
