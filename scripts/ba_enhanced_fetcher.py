#!/usr/bin/env python3
"""
Blue Archive Enhanced Data Fetcher
Extracts comprehensive character data from multiple sources
"""

import os
import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Any

class BlueArchiveDataFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
    def fetch_character_data(self):
        """Fetch character data from torikushii repository"""
        print("🔄 Fetching character data...")
        
        try:
            url = "https://raw.githubusercontent.com/torikushiii/BlueArchiveData/master/global/characters.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            raw_data = response.json()
            characters = []
            
            for char_id, char_data in raw_data.items():
                if not char_data.get('Name'):
                    continue
                    
                character = {
                    'id': int(char_id),
                    'name': char_data.get('Name', ''),
                    'dev_name': char_data.get('DevName', ''),
                    'school': char_data.get('School', ''),
                    'club': char_data.get('Club', ''),
                    'rarity': char_data.get('StarGrade', 3),
                    'squad_type': char_data.get('SquadType', ''),
                    'position': char_data.get('Position', ''),
                    'weapon_type': char_data.get('WeaponType', ''),
                    'armor_type': char_data.get('ArmorType', ''),
                    'bullet_type': char_data.get('BulletType', ''),
                    'terrain': char_data.get('Terrain', {}),
                    'profile': char_data.get('Profile', {}),
                    'stats': char_data.get('Stat', {}),
                    'skills': char_data.get('Skills', []),
                    'weapon': char_data.get('Weapon', {}),
                    'equipment': char_data.get('Equipment', []),
                    'is_limited': char_data.get('IsLimited', False)
                }
                
                characters.append(character)
            
            # Save character data
            output_file = self.data_dir / 'characters' / 'characters.json'
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(characters)} characters to {output_file}")
            return characters
            
        except Exception as e:
            print(f"❌ Error fetching character data: {e}")
            return []
    
    def fetch_additional_data(self):
        """Fetch items, equipment, and other game data"""
        print("🔄 Fetching additional game data...")
        
        data_sources = {
            'items.json': 'https://raw.githubusercontent.com/torikushiii/BlueArchiveData/master/global/items.json',
            'equipment.json': 'https://raw.githubusercontent.com/torikushiii/BlueArchiveData/master/global/equipment.json',
            'events.json': 'https://raw.githubusercontent.com/torikushiii/BlueArchiveData/master/global/events.json'
        }
        
        for filename, url in data_sources.items():
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if filename == 'items.json' or filename == 'equipment.json':
                    output_dir = self.data_dir / 'items'
                else:
                    output_dir = self.data_dir / 'events'
                
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / filename
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Saved {filename}")
                
            except Exception as e:
                print(f"❌ Error fetching {filename}: {e}")
    
    def run(self):
        """Run the complete data fetching process"""
        print("🚀 Blue Archive Data Fetcher")
        print("=" * 40)
        
        characters = self.fetch_character_data()
        self.fetch_additional_data()
        
        print(f"\n🎉 Data extraction complete!")
        print(f"📊 {len(characters)} characters processed")
        print(f"📁 Data saved to {self.data_dir}")

def main():
    fetcher = BlueArchiveDataFetcher()
    fetcher.run()

if __name__ == "__main__":
    main()