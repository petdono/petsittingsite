#!/usr/bin/env python3
"""
Simple run script for the pet sitting website
"""

import os
from app import app

if __name__ == '__main__':
    print("🚀 Starting Pet Sitting Website...")
    print("📍 Access at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )