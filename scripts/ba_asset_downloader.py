#!/usr/bin/env python3
"""
Blue Archive Asset Downloader
Downloads character images and creates organized directory structure for GitHub CDN
"""

import os
import json
import requests
from pathlib import Path
import time
from urllib.parse import urlparse

def create_directory_structure():
    """Create organized directory structure for assets"""
    directories = [
        "images/characters/icons",
        "images/characters/portraits", 
        "images/characters/collection",
        "images/characters/lobby",
        "images/weapons",
        "images/equipment",
        "images/skills"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def download_image(url, filepath, retries=3):
    """Download image with retry logic"""
    for attempt in range(retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    
    return False

def get_schaledb_images():
    """Download character images from SchaleDB"""
    print("🔄 Fetching character list from SchaleDB...")
    
    try:
        # Get character list
        response = requests.get("https://schaledb.com/data/students.json")
        response.raise_for_status()
        characters = response.json()
        
        print(f"📊 Found {len(characters)} characters")
        
        downloaded = 0
        failed = 0
        
        for char in characters:
            char_id = char.get('Id')
            name = char.get('Name', 'Unknown')
            
            if not char_id:
                continue
                
            print(f"🔄 Processing {name} (ID: {char_id})")
            
            # Define image URLs and paths
            image_types = {
                'icon': f"https://schaledb.com/images/student/icon/{char_id}.webp",
                'portrait': f"https://schaledb.com/images/student/portrait/{char_id}.webp",
                'collection': f"https://schaledb.com/images/student/collection/{char_id}.webp",
                'lobby': f"https://schaledb.com/images/student/lobby/{char_id}.webp"
            }
            
            for img_type, url in image_types.items():
                filepath = f"images/characters/{img_type}s/{char_id}.webp"
                
                if os.path.exists(filepath):
                    print(f"⏭️  Skipping existing: {filepath}")
                    continue
                
                if download_image(url, filepath):
                    downloaded += 1
                else:
                    failed += 1
                
                # Rate limiting
                time.sleep(0.5)
        
        print(f"📈 Download complete: {downloaded} success, {failed} failed")
        
    except Exception as e:
        print(f"❌ Error fetching SchaleDB data: {e}")

def create_cdn_manifest():
    """Create manifest file for CDN URLs"""
    manifest = {
        "base_url": "https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main",
        "version": "1.0.0",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "directories": {
            "character_icons": "/images/characters/icons/",
            "character_portraits": "/images/characters/portraits/",
            "character_collection": "/images/characters/collection/",
            "character_lobby": "/images/characters/lobby/",
            "weapons": "/images/weapons/",
            "equipment": "/images/equipment/",
            "skills": "/images/skills/"
        },
        "url_format": {
            "character_icon": "{base_url}/images/characters/icons/{id}.webp",
            "character_portrait": "{base_url}/images/characters/portraits/{id}.webp",
            "weapon": "{base_url}/images/weapons/{id}.webp"
        }
    }
    
    with open('cdn_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("✅ Created CDN manifest")

def main():
    """Main function"""
    print("🚀 Blue Archive Asset Downloader")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Download images
    get_schaledb_images()
    
    # Create CDN manifest
    create_cdn_manifest()
    
    print("\n🎉 Asset download complete!")
    print("📁 Directory structure created")
    print("🌐 CDN manifest generated")
    print("\nNext steps:")
    print("1. Upload images to GitHub repository")
    print("2. Update character data with CDN URLs")
    print("3. Test CDN access via jsdelivr")

if __name__ == "__main__":
    main()