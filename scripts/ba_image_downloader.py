#!/usr/bin/env python3
"""
Blue Archive Image Downloader
Downloads all images from SchaleDB structure and uploads to GitHub
"""

import os
import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Any

class BlueArchiveImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.base_url = "https://raw.githubusercontent.com/SchaleDB/SchaleDB/main/images"
        self.images_dir = Path('images')
        
    def get_character_ids(self):
        """Get character IDs from our data"""
        try:
            with open('data/characters/characters.json', 'r', encoding='utf-8') as f:
                characters = json.load(f)
            return [char['id'] for char in characters]
        except:
            # Fallback character IDs
            return list(range(10000, 10100))  # Common character ID range
    
    def download_student_images(self):
        """Download student images from SchaleDB"""
        print("🔄 Downloading student images...")
        
        char_ids = self.get_character_ids()
        image_types = {
            'icon': 'images/student/icon',
            'portrait': 'images/student/portrait',
            'collection': 'images/student/collection',
            'lobby': 'images/student/lobby'
        }
        
        downloaded = 0
        
        for char_id in char_ids:
            print(f"🔄 Processing character {char_id}")
            
            for img_type, local_path in image_types.items():
                # Create local directory
                local_dir = Path(local_path)
                local_dir.mkdir(parents=True, exist_ok=True)
                
                # Download image
                img_file = local_dir / f"{char_id}.webp"
                
                if img_file.exists():
                    continue
                
                url = f"{self.base_url}/student/{img_type}/{char_id}.webp"
                
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        with open(img_file, 'wb') as f:
                            f.write(response.content)
                        print(f"✅ Downloaded {img_type}: {char_id}")
                        downloaded += 1
                    else:
                        print(f"❌ Not found {img_type}: {char_id}")
                except Exception as e:
                    print(f"❌ Error downloading {img_type} {char_id}: {e}")
                
                time.sleep(0.2)  # Rate limiting
        
        print(f"📈 Downloaded {downloaded} student images")
    
    def download_weapon_images(self):
        """Download weapon images"""
        print("🔄 Downloading weapon images...")
        
        # Create directory
        weapon_dir = Path('images/weapon')
        weapon_dir.mkdir(parents=True, exist_ok=True)
        
        # Common weapon IDs (based on character IDs)
        char_ids = self.get_character_ids()
        downloaded = 0
        
        for weapon_id in char_ids:
            img_file = weapon_dir / f"{weapon_id}.webp"
            
            if img_file.exists():
                continue
            
            url = f"{self.base_url}/weapon/{weapon_id}.webp"
            
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    with open(img_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Downloaded weapon: {weapon_id}")
                    downloaded += 1
            except Exception as e:
                print(f"❌ Error downloading weapon {weapon_id}: {e}")
            
            time.sleep(0.2)
        
        print(f"📈 Downloaded {downloaded} weapon images")
    
    def download_equipment_images(self):
        """Download equipment images"""
        print("🔄 Downloading equipment images...")
        
        # Create directory
        equipment_dir = Path('images/equipment')
        equipment_dir.mkdir(parents=True, exist_ok=True)
        
        # Common equipment IDs
        equipment_ids = list(range(1, 100))  # Equipment typically 1-99
        downloaded = 0
        
        for eq_id in equipment_ids:
            img_file = equipment_dir / f"{eq_id}.webp"
            
            if img_file.exists():
                continue
            
            url = f"{self.base_url}/equipment/{eq_id}.webp"
            
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    with open(img_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Downloaded equipment: {eq_id}")
                    downloaded += 1
            except Exception as e:
                continue  # Skip missing equipment
            
            time.sleep(0.1)
        
        print(f"📈 Downloaded {downloaded} equipment images")
    
    def download_ui_images(self):
        """Download UI and misc images"""
        print("🔄 Downloading UI images...")
        
        ui_categories = {
            'schoolicon': list(range(1, 20)),  # School icons
            'currency': list(range(1, 10)),    # Currency icons
            'item': list(range(1, 50))         # Item icons
        }
        
        total_downloaded = 0
        
        for category, ids in ui_categories.items():
            # Create directory
            category_dir = Path(f'images/{category}')
            category_dir.mkdir(parents=True, exist_ok=True)
            
            downloaded = 0
            
            for item_id in ids:
                img_file = category_dir / f"{item_id}.webp"
                
                if img_file.exists():
                    continue
                
                url = f"{self.base_url}/{category}/{item_id}.webp"
                
                try:
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        with open(img_file, 'wb') as f:
                            f.write(response.content)
                        print(f"✅ Downloaded {category}: {item_id}")
                        downloaded += 1
                except:
                    continue
                
                time.sleep(0.1)
            
            print(f"📈 Downloaded {downloaded} {category} images")
            total_downloaded += downloaded
        
        return total_downloaded
    
    def create_image_manifest(self):
        """Create manifest of all downloaded images"""
        print("🔄 Creating image manifest...")
        
        manifest = {
            "base_url": "https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main",
            "categories": {},
            "total_images": 0
        }
        
        # Count images in each category
        for category_path in self.images_dir.rglob('*'):
            if category_path.is_dir():
                images = list(category_path.glob('*.webp'))
                if images:
                    relative_path = category_path.relative_to(self.images_dir)
                    manifest["categories"][str(relative_path)] = {
                        "count": len(images),
                        "url_pattern": f"{manifest['base_url']}/images/{relative_path}/{{id}}.webp"
                    }
                    manifest["total_images"] += len(images)
        
        # Save manifest
        with open('image_manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created manifest: {manifest['total_images']} total images")
    
    def run(self):
        """Run complete image download process"""
        print("🚀 Blue Archive Image Downloader")
        print("=" * 50)
        
        # Download all image categories
        self.download_student_images()
        self.download_weapon_images()
        self.download_equipment_images()
        ui_count = self.download_ui_images()
        
        # Create manifest
        self.create_image_manifest()
        
        print("\n🎉 Image download complete!")
        print("📁 All images organized by category")
        print("📊 Manifest created for CDN usage")
        print("\nNext: Upload to GitHub repository")

def main():
    downloader = BlueArchiveImageDownloader()
    downloader.run()

if __name__ == "__main__":
    main()