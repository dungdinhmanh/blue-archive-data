# Blue Archive Data Pipeline

Automated data extraction and synchronization pipeline for Blue Archive game data with Supabase integration.

## 🎯 Features

- **SchaleDB Integration**: Direct fetch from official SchaleDB repository
- **Schema-Compatible Sync**: Proper foreign key mapping for Supabase database
- **Automated Pipeline**: Monthly GitHub Actions workflow for data updates
- **Data Integrity**: Skills extraction with proper field validation
- **Normalized Database**: Foreign key relationships and JSONB fields

## 📁 Repository Structure

```
blue-archive-data/
├── .github/workflows/      # GitHub Actions automation
│   └── auto-update.yml    # Monthly data update workflow
├── data/                  # Processed character data
│   ├── characters/        # Character data (JSON)
│   ├── enhanced/         # Enhanced character datasets
│   ├── events/           # Event data
│   ├── items/            # Item data
│   ├── localization/     # Localization data
│   └── raids/            # Raid data
├── scripts/              # Data processing scripts
│   ├── fetch_correct_schaledb.py  # Fetch corrected SchaleDB data
│   ├── sync_corrected_data.py     # Sync to Supabase with FK mapping
│   ├── ba_enhanced_fetcher.py     # Enhanced data fetching
│   ├── ba_supabase_sync.py        # Basic Supabase sync
│   └── [other scripts]           # Additional processing tools
└── requirements.txt      # Python dependencies
```

## 🚀 Usage

### Supabase Sync Pipeline

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export SUPABASE_URL=your_supabase_project_url
   export SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   ```

3. **Fetch corrected SchaleDB data:**
   ```bash
   python scripts/fetch_correct_schaledb.py
   ```

4. **Sync to Supabase with proper schema mapping:**
   ```bash
   python scripts/sync_corrected_data.py
   ```

### Alternative Data Processing

1. **Fetch from community APIs:**
   ```bash
   python scripts/ba_enhanced_fetcher.py
   ```

2. **Basic Supabase sync:**
   ```bash
   python scripts/ba_supabase_sync.py
   ```

## 📊 Data Sources

- **Primary**: SchaleDB official repository (https://github.com/SchaleDB/SchaleDB)
- **Secondary**: Community APIs and GitHub repositories
- **Database**: Supabase with normalized schema and foreign key relationships

## 🔧 Configuration

### Environment Variables
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key for database operations

### Supabase Schema
The pipeline supports normalized database schema with:
- Foreign key relationships (schools, clubs, rarities, etc.)
- JSONB fields for complex data (skills, stats, profile, terrain, weapon)
- Proper data type mapping and validation

## 🤖 Automation

Monthly GitHub Actions workflow automatically:
- Checks for Blue Archive version updates
- Fetches latest character data from SchaleDB
- Processes and validates data
- Updates repository with new information

## 📈 Data Statistics

- **Characters**: 300+ processed characters with complete data
- **Data Categories**: Students, weapons, equipment, events, raids
- **Data Integrity**: Schema-validated with proper foreign key relationships
- **Update Frequency**: Monthly automated updates

## 🛠️ Schema Compatibility

The pipeline ensures full compatibility with Supabase database schema:
- ✅ Proper foreign key ID mapping
- ✅ JSONB field validation
- ✅ Skills data with conditional field inclusion
- ✅ No fabricated or invalid fields
- ✅ Normalized lookup tables support

---

**Blue Archive Data Pipeline** - Schema-compatible, automated, and reliable! 🎯