#!/usr/bin/env python3
"""
Fetch correct and complete character data from SchaleDB
"""

import json
import requests
from typing import Dict, List, Any, Optional

def fetch_schaledb_data() -> List[Dict[str, Any]]:
    """Fetch raw character data from SchaleDB GitHub repository"""
    url = "https://raw.githubusercontent.com/SchaleDB/SchaleDB/main/data/en/students.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching SchaleDB data: {str(e)}")
        return []

def map_schaledb_to_supabase_format(schale_student: Dict[str, Any]) -> Dict[str, Any]:
    """Map SchaleDB student data to Supabase character format"""
    
    char_id = schale_student.get("Id")
    if not char_id:
        return None
    
    # Extract basic info
    name = schale_student.get("Name")
    
    # Extract profile data
    profile_data = {
        "age": schale_student.get("ProfileAge"),
        "birthday": schale_student.get("ProfileBirthday"),
        "height": schale_student.get("ProfileHeight"),
        "hobby": schale_student.get("ProfileHobby"),
        "school_year": schale_student.get("SchoolYear"),
        "ssr_quote": schale_student.get("CharacterSSRNew")
    }
    
    # Extract stats data
    stats_data = {
        "attack_power_1": schale_student.get("AttackPower1"),
        "attack_power_100": schale_student.get("AttackPower100"),
        "max_hp_1": schale_student.get("MaxHP1"),
        "max_hp_100": schale_student.get("MaxHP100"),
        "def_power_1": schale_student.get("DefensePower1"),
        "def_power_100": schale_student.get("DefensePower100"),
        "heal_power_1": schale_student.get("HealPower1"),
        "heal_power_100": schale_student.get("HealPower100"),
        "stability_point": schale_student.get("StabilityPoint"),
        "dodge_point": schale_student.get("DodgePoint"),
        "accuracy_point": schale_student.get("AccuracyPoint"),
        "critical_point": schale_student.get("CriticalPoint"),
        "critical_damage": schale_student.get("CriticalDamageRate")
    }
    
    # Extract terrain data
    terrain_data = {
        "street": schale_student.get("StreetBattleAdaptation"),
        "outdoor": schale_student.get("OutdoorBattleAdaptation"),
        "indoor": schale_student.get("IndoorBattleAdaptation")
    }
    
    # Extract weapon data
    weapon_data = {
        "name": schale_student.get("WeaponName"),
        "image": schale_student.get("WeaponImg"),
        "description": schale_student.get("WeaponDesc")
    }
    
    # Extract skills data - only include fields that exist in SchaleDB
    skills_data = []
    skills_raw = schale_student.get("Skills", [])
    
    for skill in skills_raw:
        if not skill:
            continue
            
        skill_obj = {
            "skill_type": skill.get("SkillType"),
            "name": skill.get("Name"),
            "desc": skill.get("Desc"),
            "icon": skill.get("Icon")
        }
        
        # Only add optional fields if they exist and are not null
        if skill.get("Parameters"):
            skill_obj["parameters"] = skill.get("Parameters")
        if skill.get("Cost"):
            skill_obj["cost"] = skill.get("Cost")
        if skill.get("Duration"):
            skill_obj["duration"] = skill.get("Duration")
        if skill.get("Range"):
            skill_obj["range"] = skill.get("Range")
        if skill.get("Radius"):
            skill_obj["radius"] = skill.get("Radius")
        if skill.get("Effects"):
            skill_obj["effects"] = skill.get("Effects")
            
        skills_data.append(skill_obj)
    
    # Extract equipment data
    equipment_data = schale_student.get("Equipment", [])
    
    # Extract images data
    images_data = {
        "collection": schale_student.get("CollectionBG"),
        "portrait": schale_student.get("PortraitImg"),
        "lobby": schale_student.get("LobbyImg")
    }
    
    return {
        "id": char_id,
        "name": name,
        "dev_name": schale_student.get("DevName"),
        "character_voice": schale_student.get("CharacterVoice"),
        "illustrator": schale_student.get("Illustrator"),
        "designer": schale_student.get("Designer"),
        "collection_bg": schale_student.get("CollectionBG"),
        "school_year": schale_student.get("SchoolYear"),
        "is_limited": schale_student.get("IsLimited", False),
        "source": "schaledb",
        "profile": profile_data,
        "stats": stats_data,
        "terrain": terrain_data,
        "weapon": weapon_data,
        "skills": skills_data,
        "equipment": equipment_data,
        "images": images_data,
        # Foreign key mappings - will need lookup functions
        "school_name": schale_student.get("School"),
        "club_name": schale_student.get("Club"),
        "rarity_stars": schale_student.get("StarGrade"),
        "squad_type": schale_student.get("SquadType"),
        "position": schale_student.get("Position"),
        "weapon_type": schale_student.get("WeaponType"),
        "armor_type": schale_student.get("ArmorType"),
        "bullet_type": schale_student.get("BulletType"),
        "tactic_role": schale_student.get("TacticRole")
    }

def process_and_save_data():
    """Fetch, process and save corrected SchaleDB data"""
    print("Fetching character data from SchaleDB...")
    
    # Fetch raw data
    raw_students = fetch_schaledb_data()
    if not raw_students:
        print("No data fetched from SchaleDB")
        return
    
    print(f"Fetched {len(raw_students)} characters from SchaleDB")
    
    # Process data
    processed_characters = []
    for student in raw_students:
        mapped_char = map_schaledb_to_supabase_format(student)
        if mapped_char:
            processed_characters.append(mapped_char)
    
    print(f"Processed {len(processed_characters)} characters successfully")
    
    # Save to file
    with open('corrected_schaledb_data.json', 'w', encoding='utf-8') as f:
        json.dump(processed_characters, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved corrected data to corrected_schaledb_data.json")
    
    # Print sample for verification
    if processed_characters:
        sample = processed_characters[0]
        print(f"\nSample character: {sample.get('name')} (ID: {sample.get('id')})")
        print(f"Skills count: {len(sample.get('skills', []))}")
        if sample.get('skills'):
            print(f"First skill: {sample['skills'][0].get('name')} ({sample['skills'][0].get('skill_type')})")

def main():
    """Main function"""
    process_and_save_data()

if __name__ == "__main__":
    main()