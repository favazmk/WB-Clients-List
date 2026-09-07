import json
import os

def update_clients():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    json_path = os.path.join(script_dir, 'clients_data.json')
    js_path = os.path.join(project_root, 'js', 'clients-data.js')

    with open(json_path, 'r', encoding='utf-8') as f:
        clients = json.load(f)

    # 1. Update client-22 to Rashidali Cafeteria
    for c in clients:
        if c['id'] == 'client-22':
            c['name'] = 'Rashidali Cafeteria'
            c['tags'] = ['Cafeteria', 'Dining', 'Beverages', 'Food', 'Staging']
            print("Renamed client-22 to 'Rashidali Cafeteria'")

    # Check if 73, 74, 75 already exist
    existing_domains = {c['domain'] for c in clients}

    new_entries = [
        {
            "id": "client-73",
            "name": "Docmate",
            "domain": "docmate.ae",
            "url": "https://docmate.ae",
            "type": "custom",
            "category": "Health, Fitness & Wellness",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Doctor Booking", "Healthcare", "Medical", "Appointments", "UAE", "Custom Domain"]
        },
        {
            "id": "client-74",
            "name": "Netex Freight",
            "domain": "netexfreight.com",
            "url": "https://netexfreight.com",
            "type": "custom",
            "category": "Industrial, Trading & Engineering",
            "platform": "WordPress",
            "status": "Active",
            "tags": ["Freight Forwarding", "Logistics", "Cargo", "Shipping", "Custom Domain"]
        },
        {
            "id": "client-75",
            "name": "Mice Media",
            "domain": "mice-media.vercel.app",
            "url": "https://mice-media.vercel.app",
            "type": "custom",
            "category": "Events & Event Planning",
            "platform": "HTML / Web App",
            "status": "Active",
            "tags": ["Event Planning", "Events", "Conferences", "MICE", "Exhibitions", "Custom Domain"]
        }
    ]

    for entry in new_entries:
        if entry['domain'] not in existing_domains:
            clients.append(entry)
            print(f"Added new client: {entry['name']} ({entry['domain']})")

    # Write JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)

    # Write JS
    js_content = """/**
 * Clients Database for Sales Team Directory
 * Extracted and curated from Hostinger hPanel Client Roster
 * Verified & Updated with Approved Client Additions
 */

const CLIENTS_DATA = """ + json.dumps(clients, indent=2, ensure_ascii=False) + """;
"""
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\nTotal clients in database now: {len(clients)}")

    from collections import Counter
    counts = Counter(c['category'] for c in clients)
    print(f"Total business categories: {len(counts)}")
    for cat, cnt in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {cnt:2d} | {cat}")

if __name__ == '__main__':
    update_clients()
