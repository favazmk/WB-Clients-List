import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_path = os.path.join(script_dir, 'clients_data.json')
js_path = os.path.join(project_root, 'js', 'clients-data.js')

with open(json_path, 'r', encoding='utf-8') as f:
    clients = json.load(f)

# Apply all findings from Domain Live Audit:
# 1. 360new.hashirnisam.com -> Health, Fitness & Wellness (360 Wellness Pools & Hydrotherm)
# 2. 360.hashirnisam.com -> Health, Fitness & Wellness (360 Wellness & Spa - Sauna / Hammam)
# 3. safeway.hashirnisam.com -> Industrial, Trading & Engineering (Elictrix Electrical Solutions)
# 4. newbinsbay.hashirnisam.com -> Creative Agency & Media (Binsbay Staging)
# 5. binsbay.hashirnisam.com -> Creative Agency & Media (Binsbay Staging)

audit_updates = {
    'client-03': {
        'name': 'Elictrix (Safeway)',
        'category': 'Industrial, Trading & Engineering',
        'tags': ['Electrical Solutions', 'Equipment', 'Supplies', 'Trading', 'Staging']
    },
    'client-12': {
        'name': 'Binsbay (New Staging)',
        'category': 'Creative Agency & Media',
        'tags': ['Sign Printing', 'Branding', 'Advertising', 'Staging']
    },
    'client-17': {
        'name': '360 Wellness (New)',
        'category': 'Health, Fitness & Wellness',
        'tags': ['Hydrotherapy', 'Pools & Spas', 'Wellness', 'Staging']
    },
    'client-21': {
        'name': '360 Wellness & Spa',
        'category': 'Health, Fitness & Wellness',
        'tags': ['Sauna & Spa', 'Hammam', 'Thermal Baths', 'Wellness', 'Staging']
    },
    'client-48': {
        'name': 'Binsbay Staging',
        'category': 'Creative Agency & Media',
        'tags': ['Sign Printing', 'Branding', 'Advertising', 'Staging']
    }
}

updated_count = 0
for c in clients:
    cid = c['id']
    if cid in audit_updates:
        u = audit_updates[cid]
        c['name'] = u['name']
        c['category'] = u['category']
        c['tags'] = u['tags']
        print(f"Applied finding to [{cid}] {c['domain']} -> {c['name']} | {c['category']}")
        updated_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(clients, f, indent=2, ensure_ascii=False)

js_content = """/**
 * Clients Database for Sales Team Directory
 * Verified & Updated via Live Domain Audit
 */

const CLIENTS_DATA = """ + json.dumps(clients, indent=2, ensure_ascii=False) + """;
"""

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\nSuccessfully synchronized {updated_count} client updates across JSON and JS database!")

from collections import Counter
counts = Counter(c['category'] for c in clients)
print(f"\nUpdated Business Category Distribution ({len(counts)} industries):")
for cat, cnt in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
    print(f"  {cnt:2d} | {cat}")
