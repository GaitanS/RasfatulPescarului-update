#!/usr/bin/env python
"""
Script pentru crearea unei imagini placeholder pentru profiluri
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_placeholder_avatar(size=(200, 200), filename="default-avatar.png"):
    """Creează o imagine placeholder pentru avatar"""
    
    # Creează directorul dacă nu există
    media_dir = Path("media/profiles/avatars")
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Creează imaginea
    img = Image.new('RGB', size, color='#198754')  # Verde ca tema site-ului
    draw = ImageDraw.Draw(img)
    
    # Adaugă un cerc alb în mijloc
    margin = 20
    circle_bbox = [margin, margin, size[0] - margin, size[1] - margin]
    draw.ellipse(circle_bbox, fill='white', outline='#198754', width=3)
    
    # Adaugă o iconiță de utilizator simplă
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Cap (cerc mic)
    head_radius = 25
    head_bbox = [
        center_x - head_radius, center_y - 40,
        center_x + head_radius, center_y + 10
    ]
    draw.ellipse(head_bbox, fill='#198754')
    
    # Corp (arc)
    body_radius = 45
    body_bbox = [
        center_x - body_radius, center_y + 10,
        center_x + body_radius, center_y + 100
    ]
    draw.arc(body_bbox, start=0, end=180, fill='#198754', width=15)
    
    # Salvează imaginea
    filepath = media_dir / filename
    img.save(filepath, 'PNG')
    print(f"✅ Imagine placeholder creată: {filepath}")
    
    return filepath

def create_multiple_placeholders():
    """Creează mai multe imagini placeholder"""
    placeholders = [
        "default-avatar.png",
        "Capture-removebg-preview.png",  # Pentru eroarea din consolă
        "user-placeholder.png",
        "profile-default.png"
    ]
    
    for placeholder in placeholders:
        create_placeholder_avatar(filename=placeholder)

if __name__ == "__main__":
    print("🖼️  Creare imagini placeholder pentru profiluri...")
    create_multiple_placeholders()
    print("🎉 Toate imaginile placeholder au fost create!")
