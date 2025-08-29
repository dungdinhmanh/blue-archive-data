# Blue Archive Data Pipeline

Automated data extraction and synchronization pipeline for Blue Archive game data.

## 🎯 Features

- **Character Data Extraction**: Fetch comprehensive character data from multiple sources
- **Image Assets**: Complete SchaleDB image collection with CDN delivery
- **Supabase Integration**: Automated database synchronization
- **Clean Data Pipeline**: Processed and normalized character datasets

## 📁 Repository Structure

```
blue-archive-data/
├── data/
│   ├── characters/          # Processed character data (JSON)
│   └── README.md           # Data documentation
├── images/                 # SchaleDB image assets
│   ├── student/           # Character images (icon, portrait, collection, lobby)
│   ├── weapon/            # Weapon images
│   ├── equipment/         # Equipment images
│   └── [other categories] # UI, background, etc.
├── scripts/               # Data processing scripts
│   ├── ba_community_fetcher.py
│   ├── ba_sync_complete.py
│   ├── clean_characters_data.py
│   └── create_final_characters_json.py
└── requirements.txt       # Python dependencies
```

## 🌐 CDN Usage

Images are available via jsdelivr CDN:

```
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/student/icon/{character_id}.webp
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/weapon/{weapon_id}.webp
```

## 🚀 Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Fetch character data:**
   ```bash
   python scripts/ba_community_fetcher.py
   ```

3. **Process and clean data:**
   ```bash
   python scripts/clean_characters_data.py
   python scripts/create_final_characters_json.py
   ```

4. **Sync to Supabase:**
   ```bash
   python scripts/ba_sync_complete.py
   ```

## 📊 Data Sources

- **Character Data**: Community APIs and GitHub repositories
- **Images**: SchaleDB official repository
- **Database**: Supabase with Row Level Security

## 🔧 Configuration

Set environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key for database operations

## 📈 Data Statistics

- **Characters**: 300+ processed characters
- **Images**: 1000+ game assets
- **Categories**: Students, weapons, equipment, UI elements
- **Formats**: JSON data, WebP images

---

**Blue Archive Data Pipeline** - Automated, clean, and efficient! 🎯