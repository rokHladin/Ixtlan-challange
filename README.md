# Koledar

**Enostaven in eleganten grafičen koledarček z podporo za praznike.**

## Opis

Koledar je moderna grafična aplikacija, napisana v Pythonu z uporabo Tkinter knjižnice. Aplikacija prikazuje koledarski prikaz za poljuben mesec in leto z naprednimi funkcionalnostmi za navigacijo in označevanje posebnih dni.

## Funkcionalnosti

### Osnovne funkcionalnosti
- **Prikaz koledarja** po mesecih z jasno razporeditvijo dni po tednih
- **Navigacija** po mesecih in letih z intuitivnim vmesnikom
- **Skok na datum** - možnost direktnega skoka na poljuben datum

### Vizualne oznake
- **Nedelje** - označene z **rumeno** barvo
- **Prazniki** - označeni z **rdečo** barvo  
- **Današnji dan** - označen z **modro** barvo

### Prazniki
- **Samodejno nalaganje** praznikov iz datoteke
- **Ponavljajoči prazniki** (npr. Novo leto, Božič)
- **Enkratni prazniki** (npr. Velikonočni ponedeljki za določena leta)

## Hitri začetek

### Zahteve
- Python 3.6 ali novejši
- Tkinter (običajno vključen v Python)

### Zagon aplikacije
```bash
python main.py
```

### Gradnja executable datoteke
Za ustvarjanje neodvisne .exe/.bin datoteke:
```bash
python build_exe.py
```

## 📂 Struktura projekta

```
Koledar/
├── app/
│   ├── calendar_app.py      # Glavna aplikacija
│   ├── holiday_store.py     # Upravljanje praznikov  
│   └── utils.py            # Pomožne funkcije
├── assets/
│   └── holidays.txt        # Datoteka s prazniki
├── main.py                 # Vstopna točka
├── build_exe.py           # Skript za gradnjo exe
├── requirements.txt       # Python odvisnosti
└── README.md             # Ta datoteka
```

## Format datoteke s prazniki

Datoteka `assets/holidays.txt` uporablja preprost format:

```
# Komentar
DD.MM|Y    # Ponavljajoči praznik (vsako leto)
DD.MM.YYYY|N  # Enkratni praznik
```

## Uporaba aplikacije

### Navigacija
1. **Izbira meseca**: Uporabi padajoči meni za izbiro meseca
2. **Vpis leta**: Klikni v polje leta in vnesi željeno leto
3. **Skok na datum**: Vnesi datum v formatu DD.MM.YYYY in klikni "Pojdi"

### Barvne oznake
- 🟡 **Rumeno** = Nedelja
- 🔴 **Rdeče** = Praznik  
- 🔵 **Modro** = Današnji dan
- ⚪ **Belo** = Običajen delovnik


## Gradnja distribucije

Skript `build_exe.py` samodejno:
1. Preveri in namesti PyInstaller
2. Zgradi samostojno executable datoteko
3. Očisti začasne datoteke
4. Poroča o velikosti in lokaciji datoteke

Executable datoteka bo ustvarjena v `dist/` mapi.
