#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomožen skript za ustvarjanje executable datoteke koledarja
"""

import subprocess
import sys
import os
from pathlib import Path


def check_pyinstaller():
    """Preveri, ali je PyInstaller nameščen"""
    try:
        import PyInstaller
        print("✓ PyInstaller je nameščen")
        return True
    except ImportError:
        print("✗ PyInstaller ni nameščen")
        return False


def install_pyinstaller():
    """Namesti PyInstaller"""
    try:
        print("Nameščanje PyInstaller-ja...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller uspešno nameščen")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Napaka pri nameščanju PyInstaller-ja: {e}")
        return False


def build_executable():
    """Zgradi executable datoteko"""
    try:
        print("Gradnja executable datoteke...")
        
        # Parametri za PyInstaller
        cmd = [
            "pyinstaller",
            "--onefile",        # Ena datoteka
            "--windowed",       # Brez konzole (GUI aplikacija)
            "--name=Koledar",   # Ime executable datoteke
            "--clean",          # Počisti pred gradnjo
            "main.py"
        ]
        
        subprocess.check_call(cmd)
        print("✓ Executable datoteka uspešno ustvarjena!")
        
        # Preveri, ali datoteka obstaja
        if os.name == 'nt':  # Windows
            exe_path = Path("dist") / "Koledar.exe"
        else:  # Linux/macOS
            exe_path = Path("dist") / "Koledar"
            
        if exe_path.exists():
            print(f"✓ Datoteka je na voljo: {exe_path.absolute()}")
            print(f"✓ Velikost datoteke: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("✗ Executable datoteka ni bila najdena")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Napaka pri gradnji: {e}")
        return False
    except Exception as e:
        print(f"✗ Neznana napaka: {e}")
        return False


def clean_build_files():
    """Počisti začasne datoteke gradnje"""
    try:
        import shutil
        
        # Počisti mape
        for dir_name in ["build", "__pycache__"]:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"✓ Počiščeno: {dir_name}/")
        
        # Počisti .spec datoteko
        spec_file = "Koledar.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"✓ Počiščeno: {spec_file}")
            
    except Exception as e:
        print(f"Opozorilo: Napaka pri čiščenju: {e}")


def main():
    """Glavna funkcija"""
    print("=== Gradnja executable datoteke koledarja ===\n")
    
    # Preveri, ali glavna datoteka obstaja
    if not os.path.exists("main.py"):
        print("✗ Datoteka main.py ni najdena!")
        print("Prepričaj se, da si v pravi mapi.")
        return False
    
    # Preveri PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False
    
    # Zgradi executable
    success = build_executable()
    
    # Počisti začasne datoteke
    clean_build_files()
    
    if success:
        print("\n=== Gradnja uspešna! ===")
        print("Executable datoteko najdeš v 'dist/' mapi.")
        print("Zaženi jo lahko neodvisno brez nameščenega Python-a.")
    else:
        print("\n=== Gradnja neuspešna! ===")
        print("Preveri napake zgoraj in poskusi znova.")
    
    return success


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
