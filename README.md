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
│   └── ba_asset_manager.py       # Asset management
└── requirements.txt
```

## Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Extract data**:
   ```bash
   python scripts/ba_enhanced_fetcher.py
   ```

3. **Sync to database**:
   ```bash
   python scripts/ba_supabase_sync.py
   ```

## CDN URLs

Assets are available via jsdelivr CDN:
```
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/icons/{id}.webp
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/weapons/{id}.webp
```

## License

MIT License - see LICENSE file for details.