#!/usr/bin/env python3
"""
Startup script for Causal Chat Analysis Dashboard
Starts the Flask API backend and automatically opens the dashboard in browser
"""

import webbrowser
import time
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("🎯 Causal Chat Analysis Dashboard")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not Path('api.py').exists():
        print("❌ Error: api.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    required_modules = ['flask', 'flask_cors', 'pandas', 'nltk']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            missing.append(module)
            print(f"  ✗ {module} (missing)")
    
    if missing:
        print()
        print("⚠️  Missing dependencies. Install with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        print("Or install all dependencies with:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("✅ All dependencies satisfied!")
    print()
    
    # Start Flask API
    print("🚀 Starting Flask API server...")
    print("   http://localhost:5000")
    print()
    
    try:
        # Start Flask app
        api_process = subprocess.Popen(
            [sys.executable, 'api.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("✅ Server is running!")
                print()
        except:
            print("⚠️  Server may not be responding. Continuing anyway...")
            print()
        
        # Open dashboard in browser
        dashboard_url = 'http://localhost:5000'
        print(f"🌐 Opening dashboard in browser...")
        print(f"   {dashboard_url}")
        print()
        
        webbrowser.open(dashboard_url)
        
        # Keep the process running
        print("=" * 60)
        print("Dashboard is running!")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        api_process.wait()
        
    except KeyboardInterrupt:
        print()
        print()
        print("🛑 Shutting down...")
        api_process.terminate()
        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
        print("✅ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
