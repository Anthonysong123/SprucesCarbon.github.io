# Spruces Global Carbon — Local website preview

Static HTML/CSS site (English v1). No build step required.

## Quick start

**Option A — double-click (Windows)**

Run `preview.bat` in this folder. Your browser opens at [http://localhost:8080](http://localhost:8080).

**Option B — terminal**

```text
cd "c:\Users\AnthonySong\OneDrive\Desktop\Sprucees Carbon\website"
python -m http.server 8080
```

Then open **http://localhost:8080** in Chrome or Edge.

## Pages

| File | URL |
|------|-----|
| Home | `/` or `index.html` |
| Solutions | `solutions.html` |
| Projects | `projects.html` |
| About | `about.html` |
| Contact | `contact.html` |
| Privacy (stub) | `privacy.html` |
| Cookie (stub) | `cookie.html` |

## Images

Place generated photos in `assets/images/` using the filenames in [`assets/images/README.md`](assets/images/README.md). Refresh the browser after adding files.

`home-hero.png` is pre-copied from the project Gemini asset when available. Other slots show a green gradient placeholder until you add images.

## Contact form

Submit opens your default mail client with a pre-filled message to **Info@sprucesglobal.com** (no server backend).

## After approval

- Swap in final images per README prompts  
- Optional: migrate copy to Wix/Squarespace  
- Chinese translation: planned after English sign-off (not in v1)
