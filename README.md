# tibber_traffic_light
Tibber Traffic Light Integration for Home Assistant
# Tibber Traffic Light Integration für Home Assistant

Eine Home Assistant Integration, die eine farbige "Ampel" anzeigt, basierend auf den aktuellen Strompreisen von Tibber.

## 🎨 Features

- 🟢 **Grün**: Günstiger Preis (unter dem Durchschnitt - 20%)
- 🟡 **Gelb**: Durchschnittlicher Preis (zwischen den Grenzen)
- 🔴 **Rot**: Teurer Preis (über dem Durchschnitt + 20%)

## 📋 Voraussetzungen

- Home Assistant 2024.1.0 oder höher
- Tibber-Integration oder ein existierender Strompreis-Sensor
- Zwei Sensoren:
  - `sensor.keksi_strompreis` (aktueller Preis)
  - `sensor.tibber_average_price` (Tagespreis-Durchschnitt)

## 📥 Installation

### Methode 1: Manuelle Installation

1. Klone dieses Repository oder lade es als ZIP herunter:
```bash
   git clone https://github.com/rdaxer/tibber_traffic_light.git
```

2. Kopiere den Ordner `custom_components/tibber_traffic_light/` in dein Home Assistant `custom_components/` Verzeichnis

3. Starte Home Assistant neu:
   - **Einstellungen → System → Neustarten**

4. Füge die Integration hinzu:
   - **Einstellungen → Geräte & Dienste → + Integrationen**
   - Suche nach "Tibber Traffic Light"
   - Klicke auf "Erstellen"
   - Passe ggf. den Preisoffset an (Standard: 20%)

### Methode 2: HACS (wird noch hinzugefügt)
