#!/usr/bin/env python3
"""
Blue Archive Asset Manager
Downloads and manages game assets
"""

import os
import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Any

class BlueArchiveAssetManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.images_dir = Path('images')
        
    def download_character_images(self):
        """Download character images from SchaleDB"""
        print("🔄 Downloading character images...")
        
        try:
            # Load character data
            with open('data/characters/characters.json', 'r', encoding='utf-8') as f:
                characters = json.load(f)
            
            image_types = ['icons', 'portraits', 'collection']
            downloaded = 0
            
            for character in characters:
                char_id = character['id']
                name = character['name']
                
                print(f"🔄 Processing {name} (ID: {char_id})")
                
                for img_type in image_types:
                    # Create directory
                    img_dir = self.images_dir / 'characters' / img_type
                    img_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Download image
                    img_file = img_dir / f"{char_id}.webp"
                    
                    if img_file.exists():
                        continue
                    
                    # Try multiple sources
                    urls = [
                        f"https://schaledb.com/images/student/{img_type[:-1]}/{char_id}.webp",
                        f"https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/{img_type[:-1]}/{char_id}.webp"
                    ]
                    
                    for url in urls:
                        try:
                            response = self.session.get(url, timeout=30)
                            if response.status_code == 200:
                                with open(img_file, 'wb') as f:
                                    f.write(response.content)
                                print(f"✅ Downloaded {img_type}: {char_id}")
                                downloaded += 1
                                break
                        except:
                            continue
                    
                    time.sleep(0.2)  # Rate limiting
            
            print(f"📈 Downloaded {downloaded} images")
            
        except Exception as e:
            print(f"❌ Error downloading images: {e}")
    
    def create_cdn_manifest(self):
        """Create CDN manifest for asset URLs"""
        manifest = {
            "base_url": "https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main",
            "version": "1.0.0",
            "directories": {
                "character_icons": "/images/characters/icons/",
                "character_portraits": "/images/characters/portraits/",
                "character_collection": "/images/characters/collection/",
                "weapons": "/images/weapons/",
                "equipment": "/images/equipment/"
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
    
    def run(self):
        """Run the complete asset management process"""
        print("🚀 Blue Archive Asset Manager")
        print("=" * 40)
        
        self.download_character_images()
        self.create_cdn_manifest()
        
        print("\n🎉 Asset management complete!")

def main():
    manager = BlueArchiveAssetManager()
    manager.run()

if __name__ == "__main__":
    main()