# Ghid de utilizare Admin Panel - Răsfățul Pescarului

## Introducere
Acest ghid te va ajuta să folosești panoul de administrare pentru site-ul Răsfățul Pescarului. Toate câmpurile și instrucțiunile sunt acum în limba română.

## Accesarea Admin Panel-ului
1. Deschide browser-ul și navighează la: `http://127.0.0.1:8000/admin/`
2. Introdu numele de utilizator și parola
3. Vei vedea panoul principal de administrare

## Secțiuni disponibile

### 1. Județe
**Locație:** Main → Județe

**Ce poți face:**
- Adaugă județe noi din România
- Modifică județele existente
- Organizează județele pe regiuni

**Câmpuri importante:**
- **Nume județ:** Numele complet (ex: Argeș, Brașov, Cluj)
- **URL slug:** Se generează automat din nume
- **Regiune:** Alege regiunea istorică corespunzătoare

### 2. Lacuri de pescuit
**Locație:** Main → Lacuri de pescuit

**Ce poți face:**
- Adaugă lacuri noi de pescuit
- Modifică informațiile lacurilor existente
- Activează/dezactivează lacurile

**Câmpuri importante:**
- **Numele lacului:** Numele complet al lacului
- **Descriere:** Descrierea detaliată cu facilități și condiții
- **Adresa:** Adresa completă (ex: Comuna X, Județul Y)
- **Județul:** Selectează din lista de județe
- **Coordonate GPS:**
  - **Latitudine/Longitudine:** Găsește coordonatele pe Google Maps:
    1. Deschide Google Maps
    2. Fă click dreapta pe locația lacului
    3. Selectează coordonatele care apar (ex: 45.39189813235069, 24.62707585690222)
    4. Copiază și lipește în câmpuri - prima cifră este latitudinea, a doua longitudinea
  - **Cod embed Google Maps:** Alternativă la coordonate - copiază codul iframe complet de la Google Maps
- **Tipul bălții:** Selectează tipul corespunzător (privată, publică, competiții, etc.)
- **Tipuri de pești:** Separate prin virgulă (ex: Crap, Șalău, Știucă, Caras)
- **Facilități:** Separate prin spații (ex: parcare cazare restaurant toalete)
- **Program de funcționare:** Programul detaliat de lucru (ex: Luni-Vineri: 06:00-22:00)
- **Preț pe zi:** În lei românești (ex: 50.00)
- **Reguli de pescuit:** Regulile și restricțiile pentru pescuit (ex: Permis obligatoriu, Program: 06:00-22:00)
- **Imagine:** Format recomandat JPG/PNG, max 2MB
- **Activ:** Bifează pentru a afișa pe site

### 3. Videoclipuri
**Locație:** Main → Videoclipuri

**Ce poți face:**
- Adaugă videoclipuri noi
- Marchează videoclipuri ca recomandate
- Activează/dezactivează videoclipurile

**Câmpuri importante:**
- **Titlul videoclipului:** Titlu descriptiv
- **Descriere:** Descrierea conținutului
- **Link video:** URL complet (ex: https://youtube.com/watch?v=...)
- **Imagine de previzualizare:** Opțional, se poate genera automat
- **Activ:** Pentru afișare pe site
- **Video recomandat:** Pentru secțiunea de recomandări

### 4. Setări Site
**Locație:** Main → Setări Site

**Ce poți face:**
- Modifică informațiile generale ale site-ului
- Actualizează link-urile către rețelele sociale

**Secțiuni:**
- **Informații generale:** Nume site, email, telefon, adresă
- **Rețele sociale:** Link-uri Facebook, Instagram, YouTube
- **Conținut:** Text despre companie

### 5. Setări Footer
**Locație:** Main → Setări Footer

**Ce poți face:**
- Modifică informațiile din footer-ul site-ului

**Câmpuri:**
- **Informații contact:** Titlu secțiune
- **Adresa completă:** Adresa fizică
- **Telefon:** Cu prefixul țării (ex: +40 123 456 789)
- **Email:** Adresa de email
- **Program de lucru:** (ex: Luni - Vineri: 09:00 - 18:00)

### 6. Secțiune Hero
**Locație:** Main → Secțiune Hero

**Ce poți face:**
- Modifică textul și link-urile din secțiunea principală

**Câmpuri:**
- **Textul butonului principal:** Text pe buton
- **Link buton principal:** URL către care duce butonul
- **Link Facebook/TikTok:** Link-uri către rețelele sociale

## Sfaturi pentru utilizare

### Pentru Lacuri:
1. **Coordonate GPS:** Folosește Google Maps pentru precizie
2. **Google Maps Embed:** Pentru hărți personalizate, copiază codul iframe de la Google Maps
3. **Tipul bălții:** Alege tipul corect pentru a ajuta pescarii să înțeleagă regulamentul
4. **Program de funcționare:** Specifică orele exacte și condițiile speciale
5. **Imagini:** Folosește imagini de calitate, landscape orientation
6. **Descriere:** Fii descriptiv - include informații despre adâncime, specii, reguli
7. **Facilități:** Folosește termenii standard: parcare, cazare, restaurant, toalete

### Pentru Videoclipuri:
1. **Link-uri YouTube:** Copiază link-ul complet din bara de adrese
2. **Titluri:** Fă-le descriptive și atractive
3. **Recomandări:** Nu marca prea multe videoclipuri ca recomandate

### Pentru Imagini:
1. **Format:** JPG sau PNG
2. **Dimensiune:** Max 2MB
3. **Rezoluție:** Minim 800x600 pixeli
4. **Conținut:** Imagini clare, bine iluminate

## Funcții utile

### Filtrare și căutare:
- Folosește filtrele din dreapta pentru a găsi rapid înregistrări
- Bara de căutare funcționează pentru nume, descrieri, tipuri de pești

### Editare în masă:
- Selectează mai multe înregistrări
- Folosește acțiunile din dropdown pentru modificări în masă

### Previzualizare:
- Folosește "Vezi pe site" pentru a vedea cum arată pe site-ul public

## Probleme comune și soluții

### Cum să obții cod embed Google Maps:
1. Deschide Google Maps în browser
2. Caută locația lacului
3. Click pe "Share" (Partajează)
4. Selectează "Embed a map" (Încorporează o hartă)
5. Alege dimensiunea dorită
6. Copiază codul iframe complet
7. Lipește în câmpul "Cod embed Google Maps"

### Coordonatele nu sunt corecte:
- Verifică că ai copiat ambele coordonate (latitudine și longitudine)
- Asigură-te că folosești punctul (.) ca separator zecimal, nu virgula

### Imaginea nu se încarcă:
- Verifică dimensiunea (max 2MB)
- Folosește format JPG sau PNG
- Redenumește fișierul fără caractere speciale

### Lacul nu apare pe site:
- Verifică că câmpul "Activ" este bifat
- Asigură-te că toate câmpurile obligatorii sunt completate

## Contact pentru suport
Pentru probleme tehnice sau întrebări despre utilizarea admin panel-ului, contactează administratorul site-ului.
