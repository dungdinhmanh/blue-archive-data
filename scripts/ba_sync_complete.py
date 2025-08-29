#!/usr/bin/env python3
"""
Blue Archive Complete Sync
Fetches data and syncs to Supabase in one script
"""

import os
import json
import requests
from pathlib import Path
import time
from typing import Dict, List, Any
from supabase import create_client, Client

class BlueArchiveCompleteSync:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Supabase setup
        self.supabase_url = "https://bpvdkhsgznuibgmjsnjz.supabase.co"
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'sbp_5cde0efc3712bcd2082effbe37ae4d649a1d8f93')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
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
                    'is_limited': char_data.get('IsLimited', False),
                    'images': {
                        'icon': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/icons/{char_id}.webp",
                        'portrait': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/portraits/{char_id}.webp",
                        'collection': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/collection/{char_id}.webp"
                    }
                }
                
                characters.append(character)
            
            print(f"✅ Fetched {len(characters)} characters")
            return characters
            
        except Exception as e:
            print(f"❌ Error fetching character data: {e}")
            return []
    
    def sync_to_supabase(self, characters):
        """Sync character data to Supabase"""
        print("🔄 Syncing to Supabase...")
        
        try:
            # Batch insert/upsert characters
            batch_size = 50
            total_synced = 0
            
            for i in range(0, len(characters), batch_size):
                batch = characters[i:i + batch_size]
                
                result = self.supabase.table('characters').upsert(batch).execute()
                total_synced += len(batch)
                
                print(f"✅ Synced batch {i//batch_size + 1}: {len(batch)} characters")
                time.sleep(0.5)  # Rate limiting
            
            print(f"✅ Total synced: {total_synced} characters")
            
        except Exception as e:
            print(f"❌ Error syncing to Supabase: {e}")
    
    def upload_to_github(self, characters):
        """Save character data to local file for GitHub upload"""
        print("🔄 Saving data for GitHub...")
        
        try:
            # Create data directory
            data_dir = Path('data/characters')
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Save character data
            output_file = data_dir / 'characters.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(characters, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(characters)} characters to {output_file}")
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def run(self):
        """Run complete sync process"""
        print("🚀 Blue Archive Complete Sync")
        print("=" * 40)
        
        # Step 1: Fetch character data
        characters = self.fetch_character_data()
        
        if not characters:
            print("❌ No character data fetched, aborting sync")
            return
        
        # Step 2: Save to local file
        self.upload_to_github(characters)
        
        # Step 3: Sync to Supabase
        self.sync_to_supabase(characters)
        
        print("\n🎉 Complete sync finished!")
        print(f"📊 {len(characters)} characters processed")
        print("📁 Data saved locally")
        print("🗄️ Data synced to Supabase")

def main():
    sync = BlueArchiveCompleteSync()
    sync.run()

if __name__ == "__main__":
    main()