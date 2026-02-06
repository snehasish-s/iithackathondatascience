#!/usr/bin/env python3
"""Test API endpoints"""
import requests
import sys

print('\n🔍 Testing API Endpoints...\n')

endpoints = [
    ('Stats', 'http://localhost:5000/api/stats'),
    ('Causes', 'http://localhost:5000/api/causes'),
    ('Signals', 'http://localhost:5000/api/signals'),
    ('Warnings', 'http://localhost:5000/api/warnings'),
    ('Domains', 'http://localhost:5000/api/domains'),
    ('Intents', 'http://localhost:5000/api/intents'),
]

success_count = 0
for name, url in endpoints:
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                print(f'✅ {name}: OK')
                success_count += 1
            else:
                error = data.get('error', 'Unknown error')
                print(f'⚠️  {name}: {error}')
        else:
            print(f'❌ {name}: HTTP {r.status_code}')
    except Exception as e:
        print(f'❌ {name}: {str(e)[:60]}')

print(f'\n✨ Results: {success_count}/{len(endpoints)} endpoints working')
print(f'🌐 Dashboard: http://localhost:5000\n')

sys.exit(0 if success_count == len(endpoints) else 1)
