#!/usr/bin/env python3
"""
Blue Archive Enhanced Data Fetcher
Fetches comprehensive game data similar to schaledb.com structure
"""

import requests
import json
import os
from typing import Dict, List, Any, Optional
import time
from datetime import datetime

class BlueArchiveEnhancedFetcher:
    def __init__(self):
        self.base_urls = {
            'schaledb': 'https://schaledb.com/data/en/',
            'torikushii_global': 'https://raw.githubusercontent.com/torikushiii/BlueArchiveData/main/global/',
            'torikushii_japan': 'https://raw.githubusercontent.com/torikushiii/BlueArchiveData/main/japan/',
            'bluearchive_api': 'https://api.ennead.cc/buruaka/'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BlueArchiveDataPipeline/1.0'
        })
    
    def fetch_schaledb_data(self) -> Dict[str, Any]:
        """Fetch comprehensive data from schaledb API endpoints"""
        endpoints = [
            'students.min.json',
            'equipment.min.json', 
            'items.min.json',
            'summons.min.json',
            'raids.min.json',
            'events.min.json',
            'enemies.min.json',
            'furniture.min.json',
            'currency.min.json',
            'localization.min.json'
        ]
        
        data = {}
        for endpoint in endpoints:
            try:
                url = self.base_urls['schaledb'] + endpoint
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                key = endpoint.replace('.min.json', '')
                data[key] = response.json()
                print(f"✅ Fetched {key}: {len(data[key]) if isinstance(data[key], list) else 'OK'}")
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"❌ Failed to fetch {endpoint}: {e}")
                data[key] = []
        
        return data
    
    def fetch_torikushii_data(self, region: str = 'global') -> Dict[str, Any]:
        """Fetch data from torikushii repository"""
        base_url = self.base_urls[f'torikushii_{region}']
        endpoints = [
            'characters.json',
            'items.json', 
            'events.json',
            'gacha.json',
            'furniture.json',
            'clubs.json',
            'schools.json',
            'armors.json',
            'bullets.json'
        ]
        
        data = {}
        for endpoint in endpoints:
            try:
                url = base_url + endpoint
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                key = endpoint.replace('.json', '')
                data[key] = response.json()
                print(f"✅ Fetched {region} {key}: {len(data[key]) if isinstance(data[key], list) else 'OK'}")
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Failed to fetch {region} {endpoint}: {e}")
                data[key] = []
        
        return data
    
    def enhance_character_data(self, schale_students: List[Dict], tori_characters: List[Dict]) -> List[Dict]:
        """Merge and enhance character data from multiple sources"""
        enhanced_characters = []
        
        # Create lookup for torikushii data
        tori_lookup = {char.get('Id', char.get('id')): char for char in tori_characters}
        
        for student in schale_students:
            char_id = student.get('Id')
            enhanced_char = {
                # Basic Info
                'id': char_id,
                'name': student.get('Name'),
                'dev_name': student.get('DevName'),
                'rarity': student.get('StarGrade'),
                'school': student.get('School'),
                'club': student.get('Club'),
                
                # Combat Stats
                'type': student.get('Role'),
                'position': student.get('Position'),
                'squad_type': student.get('SquadType'),
                'weapon_type': student.get('WeaponType'),
                'armor_type': student.get('ArmorType'), 
                'bullet_type': student.get('BulletType'),
                'range': student.get('Range'),
                
                # Detailed Stats
                'stats': {
                    'max_hp': student.get('MaxHP100'),
                    'attack': student.get('AttackPower100'),
                    'defense': student.get('DefensePower100'),
                    'heal_power': student.get('HealPower100'),
                    'accuracy': student.get('AccuracyPoint'),
                    'evasion': student.get('DodgePoint'),
                    'critical': student.get('CriticalPoint'),
                    'critical_resistance': student.get('CriticalChanceResistPoint'),
                    'critical_damage': student.get('CriticalDamageRate'),
                    'critical_damage_resistance': student.get('CriticalDamageResistRate'),
                    'stability': student.get('StabilityPoint'),
                    'range': student.get('Range'),
                    'cc_power': student.get('OppressionPower'),
                    'cc_resistance': student.get('OppressionResist'),
                    'defense_penetration': student.get('DefensePenetration'),
                    'ammo_count': student.get('AmmoCount'),
                    'ammo_cost': student.get('AmmoCost')
                },
                
                # Weapon Data
                'weapon': {
                    'name': student.get('WeaponName'),
                    'description': student.get('WeaponDesc'),
                    'stats': student.get('WeaponStatValue', []),
                    'passive_skill': student.get('WeaponPassiveSkill')
                },
                
                # Skills
                'skills': {
                    'ex_skill': student.get('ExSkill', []),
                    'normal_skill': student.get('NormalSkill', []),
                    'passive_skill': student.get('PassiveSkill', []),
                    'sub_skill': student.get('SubSkill', [])
                },
                
                # Equipment
                'equipment': student.get('Equipment', []),
                
                # Terrain Adaptation
                'terrain': {
                    'street': student.get('StreetBattleAdaptation'),
                    'outdoor': student.get('OutdoorBattleAdaptation'), 
                    'indoor': student.get('IndoorBattleAdaptation')
                },
                
                # Profile
                'profile': {
                    'age': student.get('CharacterAge'),
                    'birthday': student.get('Birthday'),
                    'height': student.get('CharacterHeight'),
                    'hobby': student.get('Hobby'),
                    'designer': student.get('Designer'),
                    'illustrator': student.get('Illustrator'),
                    'voice_actor': student.get('CharacterVoice')
                },
                
                # Images (will be populated by asset manager)
                'images': {
                    'icon': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/icons/{char_id}.webp",
                    'portrait': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/portraits/{char_id}.webp",
                    'collection': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/collection/{char_id}.webp",
                    'weapon': f"https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/weapons/{char_id}.webp"
                },
                
                # Metadata
                'source': 'schaledb',
                'last_updated': datetime.now().isoformat()
            }
            
            # Merge with torikushii data if available
            if char_id in tori_lookup:
                tori_data = tori_lookup[char_id]
                # Add any additional fields from torikushii
                enhanced_char['tori_data'] = tori_data
            
            enhanced_characters.append(enhanced_char)
        
        return enhanced_characters
    
    def create_enhanced_datasets(self) -> Dict[str, Any]:
        """Create comprehensive datasets with all game data"""
        print("🚀 Starting enhanced data collection...")
        
        # Fetch from all sources
        schale_data = self.fetch_schaledb_data()
        tori_global = self.fetch_torikushii_data('global')
        tori_japan = self.fetch_torikushii_data('japan')
        
        # Enhanced character data
        enhanced_characters = self.enhance_character_data(
            schale_data.get('students', []),
            tori_global.get('characters', [])
        )
        
        # Comprehensive datasets
        datasets = {
            'characters': enhanced_characters,
            'equipment': schale_data.get('equipment', []),
            'items': schale_data.get('items', []),
            'weapons': [char.get('weapon', {}) for char in enhanced_characters if char.get('weapon')],
            'skills': {
                'ex_skills': [char.get('skills', {}).get('ex_skill', []) for char in enhanced_characters],
                'normal_skills': [char.get('skills', {}).get('normal_skill', []) for char in enhanced_characters],
                'passive_skills': [char.get('skills', {}).get('passive_skill', []) for char in enhanced_characters]
            },
            'raids': schale_data.get('raids', []),
            'events': schale_data.get('events', []),
            'summons': schale_data.get('summons', []),
            'enemies': schale_data.get('enemies', []),
            'furniture': schale_data.get('furniture', []),
            'schools': tori_global.get('schools', []),
            'clubs': tori_global.get('clubs', []),
            'game_meta': {
                'armors': tori_global.get('armors', []),
                'bullets': tori_global.get('bullets', []),
                'currencies': schale_data.get('currency', []),
                'localization': schale_data.get('localization', {})
            },
            'statistics': {
                'total_characters': len(enhanced_characters),
                'by_school': self._count_by_field(enhanced_characters, 'school'),
                'by_rarity': self._count_by_field(enhanced_characters, 'rarity'),
                'by_weapon_type': self._count_by_field(enhanced_characters, 'weapon_type'),
                'by_role': self._count_by_field(enhanced_characters, 'type'),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        return datasets
    
    def _count_by_field(self, data: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences of field values"""
        counts = {}
        for item in data:
            value = item.get(field, 'Unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    def save_enhanced_data(self, datasets: Dict[str, Any], output_dir: str = 'enhanced_data'):
        """Save enhanced datasets to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save main datasets
        for key, data in datasets.items():
            if key != 'statistics':  # Save statistics separately
                filename = f"{output_dir}/{key}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"💾 Saved {filename}")
        
        # Save statistics
        stats_file = f"{output_dir}/statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(datasets['statistics'], f, ensure_ascii=False, indent=2)
        print(f"📊 Saved {stats_file}")
        
        # Create summary
        summary = {
            'datasets': list(datasets.keys()),
            'total_characters': datasets['statistics']['total_characters'],
            'data_sources': ['schaledb.com', 'torikushiii/BlueArchiveData'],
            'last_updated': datasets['statistics']['last_updated']
        }
        
        with open(f"{output_dir}/summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"📋 Saved {output_dir}/summary.json")

def main():
    fetcher = BlueArchiveEnhancedFetcher()
    datasets = fetcher.create_enhanced_datasets()
    fetcher.save_enhanced_data(datasets)
    
    print(f"\n✅ Enhanced data collection complete!")
    print(f"📊 Total characters: {datasets['statistics']['total_characters']}")
    print(f"🏫 Schools: {len(datasets['statistics']['by_school'])}")
    print(f"⭐ Rarities: {len(datasets['statistics']['by_rarity'])}")
    print(f"🔫 Weapon types: {len(datasets['statistics']['by_weapon_type'])}")

if __name__ == '__main__':
    main()