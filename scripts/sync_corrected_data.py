#!/usr/bin/env python3
"""
Sync corrected SchaleDB data to Supabase database
"""

import json
import os
from typing import Dict, List, Any, Optional
from supabase import create_client, Client

def load_corrected_data() -> List[Dict[str, Any]]:
    """Load corrected SchaleDB character data"""
    try:
        with open('corrected_schaledb_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: corrected_schaledb_data.json not found")
        return []

def create_supabase_client() -> Client:
    """Create Supabase client using environment variables"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables must be set")
    
    return create_client(supabase_url, supabase_key)

def lookup_foreign_key_id(supabase: Client, table: str, name_field: str, name_value: str) -> Optional[int]:
    """Lookup foreign key ID by name"""
    if not name_value:
        return None
    
    try:
        result = supabase.table(table).select("id").eq(name_field, name_value).execute()
        if result.data:
            return result.data[0]['id']
    except Exception as e:
        print(f"Error looking up {table} for {name_value}: {str(e)}")
    
    return None

def prepare_character_for_sync(supabase: Client, char: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare character data with proper foreign key IDs"""
    sync_data = {
        "id": char.get("id"),
        "name": char.get("name"),
        "dev_name": char.get("dev_name"),
        "character_voice": char.get("character_voice"),
        "illustrator": char.get("illustrator"),
        "designer": char.get("designer"),
        "collection_bg": char.get("collection_bg"),
        "school_year": char.get("school_year"),
        "is_limited": char.get("is_limited", False),
        "source": char.get("source", "schaledb"),
        "profile": char.get("profile"),
        "stats": char.get("stats"),
        "terrain": char.get("terrain"),
        "weapon": char.get("weapon"),
        "skills": char.get("skills"),
        "equipment": char.get("equipment"),
        "images": char.get("images")
    }
    
    # Lookup foreign key IDs
    if char.get("school_name"):
        sync_data["school_id"] = lookup_foreign_key_id(supabase, "schools", "name", char.get("school_name"))
    
    if char.get("club_name"):
        sync_data["club_id"] = lookup_foreign_key_id(supabase, "clubs", "name", char.get("club_name"))
    
    if char.get("rarity_stars"):
        rarity_name = f"{char.get('rarity_stars')}★"
        sync_data["rarity_id"] = lookup_foreign_key_id(supabase, "rarities", "name", rarity_name)
    
    if char.get("squad_type"):
        sync_data["squad_type_id"] = lookup_foreign_key_id(supabase, "squad_types", "name", char.get("squad_type"))
    
    if char.get("position"):
        sync_data["position_id"] = lookup_foreign_key_id(supabase, "positions", "name", char.get("position"))
    
    if char.get("weapon_type"):
        sync_data["weapon_type_id"] = lookup_foreign_key_id(supabase, "weapon_types", "name", char.get("weapon_type"))
    
    if char.get("armor_type"):
        sync_data["armor_type_id"] = lookup_foreign_key_id(supabase, "armor_types", "name", char.get("armor_type"))
    
    if char.get("bullet_type"):
        sync_data["bullet_type_id"] = lookup_foreign_key_id(supabase, "bullet_types", "name", char.get("bullet_type"))
    
    if char.get("tactic_role"):
        sync_data["tactic_role_id"] = lookup_foreign_key_id(supabase, "tactic_roles", "name", char.get("tactic_role"))
    
    # Remove temporary lookup fields
    for key in ["school_name", "club_name", "rarity_stars", "squad_type", "position", 
                "weapon_type", "armor_type", "bullet_type", "tactic_role"]:
        sync_data.pop(key, None)
    
    return sync_data

def sync_characters_to_supabase(supabase: Client, characters: List[Dict[str, Any]], batch_size: int = 10):
    """Sync characters to Supabase in batches with proper foreign key mapping"""
    
    total_updated = 0
    total_chars = len(characters)
    
    for i in range(0, total_chars, batch_size):
        batch = characters[i:i + batch_size]
        
        try:
            for char in batch:
                char_id = char.get('id')
                if not char_id:
                    print(f"Skipping character without ID: {char.get('name', 'Unknown')}")
                    continue
                
                # Prepare character data with foreign key lookups
                sync_data = prepare_character_for_sync(supabase, char)
                
                # Update character in Supabase
                result = supabase.table('characters').update(sync_data).eq('id', char_id).execute()
                
                if result.data:
                    total_updated += 1
                    print(f"✓ Updated character {char_id}: {char.get('name', 'Unknown')}")
                else:
                    print(f"✗ Failed to update character {char_id}: {char.get('name', 'Unknown')}")
                    
        except Exception as e:
            print(f"Error updating batch {i//batch_size + 1}: {str(e)}")
            continue
    
    print(f"\nSync completed: {total_updated}/{total_chars} characters updated successfully")
    return total_updated

def main():
    """Main sync function"""
    print("Starting Blue Archive data sync to Supabase...")
    
    # Load corrected data
    characters = load_corrected_data()
    if not characters:
        print("No character data found to sync")
        return
    
    print(f"Loaded {len(characters)} characters from corrected data")
    
    # Create Supabase client
    try:
        supabase = create_supabase_client()
        print("✓ Connected to Supabase")
    except Exception as e:
        print(f"✗ Failed to connect to Supabase: {str(e)}")
        return
    
    # Sync data
    updated_count = sync_characters_to_supabase(supabase, characters)
    
    if updated_count > 0:
        print(f"✓ Successfully synced {updated_count} characters to Supabase")
    else:
        print("✗ No characters were synced")

if __name__ == "__main__":
    main()