# Image assets

## Upload workflow

1. Place your **original** photos in `incoming/` (this folder’s subfolder), using the **exact filenames** listed below.
2. Run from the project root:

   ```bash
   python website/scripts/process_images.py
   ```

3. Processed files are written to `website/assets/images/` (same names). Refresh the browser.

The script uses **`smart_fill_frame`**: every output matches the HTML frame size and **fills the box completely**—no half-empty green bands. When your photo’s aspect ratio differs from the frame, it uses a soft blurred backdrop plus a sharp centred foreground so the whole subject stays visible.

Optional: drop files directly in `assets/images/` (without `incoming/`) and run the script again to re-normalize them.

## Filenames & frame sizes

| File | Frame (px) | HTML aspect |
|------|----------------|-------------|
| `home-hero.jpg` | 1920×1080 | hero 16∶9 |
| `home-trust-bg.jpg` | 2100×900 | 21∶9 |
| `home-pillar-1.jpg` | 1200×900 | 4∶3 |
| `home-pillar-2.jpg` | 1200×900 | 4∶3 |
| `home-pillar-3.jpg` | 1200×900 | 4∶3 |
| `home-projects.jpg` | 1600×900 | 16∶9 |
| `home-singapore.jpg` | 1600×900 | 16∶9 |
| `solutions-hero.jpg` | 1600×900 | 16∶9 |
| `solutions-dmrv-flow.jpg` | 1600×900 | 16∶9 |
| `solutions-integrity.jpg` | 1200×900 | 4∶3 |
| `solutions-standards.jpg` | 1600×900 | 16∶9 |
| `projects-solar.jpg` | 1600×900 | 16∶9 |
| `projects-cookstove.jpg` | 1200×900 | 4∶3 |
| `projects-platform.jpg` | 1600×900 | 16∶9 |
| `about-mission.jpg` | 1600×900 | 16∶9 |
| `about-governance.jpg` | 1200×900 | 4∶3 |
| `about-principles.jpg` | 1600×900 | 16∶9 |
| `contact.jpg` | 1600×900 | 16∶9 |

Use `.jpg` or `.png` sources; outputs are always `.jpg`.

## Tips for best results

- Prefer photos close to the target aspect ratio (e.g. 16∶9 for hero and project banners).
- Avoid heavy borders or letterboxing in the source file—the script will fill the frame, but a clean crop uploads faster.
- `projects-cookstove.jpg` / `projects-solar.jpg`: if you use the legacy root-level source photos, the script still applies the IoT-module / enclosure-interior crops before filling the frame.
