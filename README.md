# Blue Archive Data Pipeline

Comprehensive Blue Archive game data extraction, processing, and synchronization system.

## Features

- **Data Extraction**: Fetch character data from multiple sources
- **Data Processing**: Clean and normalize game data
- **Asset Management**: Download and organize game assets
- **Database Sync**: Automated Supabase synchronization
- **CDN Integration**: Fast asset delivery via jsdelivr

## Structure

```
blue-archive-data/
├── data/
│   ├── characters/           # Character data files
│   ├── items/               # Item and equipment data
│   └── events/              # Event data
├── images/
│   ├── characters/          # Character images
│   │   ├── icons/
│   │   ├── portraits/
│   │   └── collection/
│   ├── weapons/             # Weapon images
│   └── equipment/           # Equipment images
├── scripts/
│   ├── ba_enhanced_fetcher.py    # Data extraction
│   ├── ba_supabase_sync.py       # Database sync
│   ├── ba_asset_manager.py       # Asset management
│   └── ba_sync_complete.py       # Complete sync process
└── requirements.txt
```

## Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Complete sync (recommended)**:
   ```bash
   python scripts/ba_sync_complete.py
   ```

3. **Individual operations**:
   ```bash
   # Extract data only
   python scripts/ba_enhanced_fetcher.py
   
   # Sync to database only
   python scripts/ba_supabase_sync.py
   
   # Manage assets only
   python scripts/ba_asset_manager.py
   ```

## API Access

**Supabase REST API**:
```
GET https://bpvdkhsgznuibgmjsnjz.supabase.co/rest/v1/characters
```

**CDN URLs**:
```
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/characters/characters.json
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/icons/{id}.webp
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/weapons/{id}.webp
```

## Environment Variables

```bash
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## License

MIT License - see LICENSE file for details.