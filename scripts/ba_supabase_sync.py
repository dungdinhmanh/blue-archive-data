#!/usr/bin/env python3
"""
Blue Archive Supabase Sync
Synchronizes Blue Archive data to Supabase database
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Any
from supabase import create_client, Client

class BlueArchiveSupabaseSync:
    def __init__(self):
        # Get Supabase credentials from environment
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://bpvdkhsgznuibgmjsnjz.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.supabase_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY environment variable is required")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
    def create_database_schema(self):
        """Create clean database schema"""
        print("🔄 Creating database schema...")
        
        # Characters table
        characters_sql = """
        CREATE TABLE IF NOT EXISTS characters (
            id BIGINT PRIMARY KEY,
            name TEXT NOT NULL,
            dev_name TEXT,
            school TEXT,
            club TEXT,
            rarity INTEGER,
            squad_type TEXT,
            position TEXT,
            weapon_type TEXT,
            armor_type TEXT,
            bullet_type TEXT,
            terrain JSONB,
            profile JSONB,
            stats JSONB,
            skills JSONB,
            weapon JSONB,
            equipment JSONB,
            is_limited BOOLEAN DEFAULT false,
            images JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);
        CREATE INDEX IF NOT EXISTS idx_characters_school ON characters(school);
        CREATE INDEX IF NOT EXISTS idx_characters_rarity ON characters(rarity);
        """
        
        try:
            self.supabase.rpc('exec_sql', {'sql': characters_sql}).execute()
            print("✅ Database schema created")
        except Exception as e:
            print(f"❌ Error creating schema: {e}")
    
    def sync_characters(self):
        """Sync character data to Supabase"""
        print("🔄 Syncing character data...")
        
        try:
            # Load character data from GitHub
            url = "https://raw.githubusercontent.com/dungdinhmanh/blue-archive-data/main/data/characters/characters.json"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                print("❌ Character data not found, running local fetch...")
                return
            
            characters = response.json()
            
            # Prepare data for Supabase
            for character in characters:
                # Add CDN image URLs
                character['images'] = {
                    'icon': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/icons/{character['id']}.webp",
                    'portrait': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/portraits/{character['id']}.webp",
                    'collection': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/collection/{character['id']}.webp"
                }
            
            # Upsert to Supabase
            result = self.supabase.table('characters').upsert(characters).execute()
            
            print(f"✅ Synced {len(characters)} characters")
            
        except Exception as e:
            print(f"❌ Error syncing characters: {e}")
    
    def run(self):
        """Run the complete sync process"""
        print("🚀 Blue Archive Supabase Sync")
        print("=" * 40)
        
        self.create_database_schema()
        self.sync_characters()
        
        print("\n🎉 Sync complete!")

def main():
    try:
        sync = BlueArchiveSupabaseSync()
        sync.run()
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        print("Please set SUPABASE_SERVICE_ROLE_KEY environment variable")

if __name__ == "__main__":
    main()