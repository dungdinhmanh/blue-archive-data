# Blue Archive Data

Comprehensive Blue Archive character data and assets with jsDelivr CDN support for fast global access.

## 🚀 Quick Start

### Character Images via jsDelivr CDN
```javascript
// Character portrait
const characterImage = `https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/${devName}.png`

// School icon
const schoolIcon = `https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/schools/${school.toLowerCase()}.png`

// Examples
const aruImage = "https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/aru.png"
const gehennaIcon = "https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/schools/gehenna.png"
```

### Character Data API
```javascript
// All characters
const characters = await fetch('https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/characters.json')

// Characters by school
const bySchool = await fetch('https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/characters_by_school.json')

// Statistics
const stats = await fetch('https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/character_statistics.json')
```

## 📁 Repository Structure

```
blue-archive-data/
├── images/
│   ├── characters/          # Character portraits (266x266px)
│   │   ├── aru.png
│   │   ├── shiroko.png
│   │   └── ...
│   ├── schools/             # School icons (50x50px)
│   │   ├── gehenna.png
│   │   ├── millennium.png
│   │   └── ...
│   └── weapons/             # Weapon type icons
├── data/
│   ├── characters.json      # Complete character data
│   ├── characters_basic.json
│   ├── characters_by_school.json
│   ├── characters_by_rarity.json
│   └── character_statistics.json
└── .github/workflows/       # Auto-update workflows
```

## 📊 Data Statistics

- **Total Characters:** 309
- **Complete Data:** 221 characters (71.5%)
- **Schools:** Millennium (50), Trinity (44), Gehenna (43), Abydos (16), etc.
- **Rarities:** SSR (161), SR (25), R (35)

## 🔄 Auto-Updates

This repository automatically updates monthly when new Blue Archive versions are detected via:
- Game version monitoring API
- Community data source polling
- Automated image validation and sync

## 🌐 jsDelivr CDN Benefits

- ✅ **Global CDN** - Fast access worldwide
- ✅ **No rate limits** - Unlimited requests
- ✅ **Version control** - Access specific commits via `@commit-hash`
- ✅ **Caching** - Automatic browser caching
- ✅ **HTTPS** - Secure delivery

### CDN URL Patterns
```
# Latest version (main branch)
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/path/to/file

# Specific version (commit hash)
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@abc123/path/to/file

# Minified JSON (automatic)
https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/characters.min.json
```

## 🛠️ Usage Examples

### React/Vue Component
```jsx
function CharacterCard({ character }) {
  const imageUrl = `https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/characters/${character.dev_name}.png`
  const schoolIcon = `https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/images/schools/${character.school.toLowerCase()}.png`
  
  return (
    <div className="character-card">
      <img src={imageUrl} alt={character.name} />
      <img src={schoolIcon} alt={character.school} className="school-icon" />
      <h3>{character.name}</h3>
      <p>{character.school} - {character.rarity}</p>
    </div>
  )
}
```

### Python/API Usage
```python
import requests

# Load character data
response = requests.get('https://cdn.jsdelivr.net/gh/dungdinhmanh/blue-archive-data@main/data/characters.json')
characters = response.json()

# Find character by name
aru = next(char for char in characters if char['name'] == 'Aru')
print(f"Aru's image: {aru['image_url']}")
```

## 📝 Data Sources

- **Community APIs:** BlueArchiveData Repository, BlueArchive API
- **Official Sources:** Game assets and version monitoring
- **Data Validation:** Multi-source verification and cleaning

## 🤝 Contributing

This repository is automatically maintained. For issues or suggestions, please open an issue.

## 📄 License

Data is sourced from public community APIs. Images are property of Nexon/NEXON Games Co., Ltd.
Used under Fair Use for educational and development purposes.

---

**Last Updated:** Auto-updated monthly via GitHub Actions
**CDN Status:** ✅ Active via jsDelivr
**Total Files:** Updated automatically