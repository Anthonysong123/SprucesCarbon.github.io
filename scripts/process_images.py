"""
Normalize uploaded images to exact frame sizes for the website.

Drop originals into assets/images/incoming/ (same filenames as in HTML),
then run:  python website/scripts/process_images.py

Every output fills its target frame completely (no empty green bands).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "assets" / "images"
INCOMING = OUT / "incoming"

GREEN = (11, 61, 46)

# All image slots referenced in HTML → (width, height)
IMAGE_FRAMES: dict[str, tuple[int, int]] = {
    "home-hero.jpg": (1920, 1080),
    "home-trust-bg.jpg": (2100, 900),
    "home-pillar-1.jpg": (1200, 900),
    "home-pillar-2.jpg": (1200, 900),
    "home-pillar-3.jpg": (1200, 900),
    "home-projects.jpg": (1600, 900),
    "home-singapore.jpg": (1600, 900),
    "solutions-hero.jpg": (1600, 900),
    "solutions-dmrv-flow.jpg": (1600, 900),
    "solutions-integrity.jpg": (1200, 900),
    "solutions-standards.jpg": (1600, 900),
    "projects-solar.jpg": (1600, 900),
    "projects-cookstove.jpg": (1200, 900),
    "projects-platform.jpg": (1600, 900),
    "about-mission.jpg": (1600, 900),
    "about-governance.jpg": (1200, 900),
    "about-principles.jpg": (1600, 900),
    "contact.jpg": (1600, 900),
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INCOMING.mkdir(parents=True, exist_ok=True)


def load_image(path: Path) -> Image.Image:
    im = Image.open(path)
    return ImageOps.exif_transpose(im)


def detect_focal(im: Image.Image) -> tuple[float, float]:
    """Estimate subject centre from edge density (0–1, 0–1)."""
    w, h = im.size
    sample_w = 400
    sample_h = max(1, int(h * (sample_w / w)))
    small = im.convert("L").resize(
        (sample_w, sample_h), Image.Resampling.BILINEAR
    )
    edges = small.filter(ImageFilter.FIND_EDGES)
    px = edges.load()
    sw, sh = small.size
    sum_x = sum_y = weight = 0.0
    for y in range(sh):
        for x in range(sw):
            v = px[x, y]
            if v < 18:
                continue
            sum_x += x * v
            sum_y += y * v
            weight += v
    if weight < 1:
        return (0.5, 0.5)
    return (sum_x / weight / sw, sum_y / weight / sh)


def _ratios_close(src_ratio: float, target_ratio: float, tolerance: float = 0.14) -> bool:
    return abs(src_ratio - target_ratio) / max(target_ratio, 1e-6) < tolerance


def smart_fill_frame(
    im: Image.Image,
    target_w: int,
    target_h: int,
    *,
    focal: tuple[float, float] | None = None,
) -> Image.Image:
    """
    Fill (target_w × target_h) with no empty areas.

    - Similar aspect ratios → centre-weighted cover crop.
    - Different ratios → blurred cover background + sharp foreground
      (contain) so the full subject stays visible while the frame stays full.
    """
    im = load_image(im) if not isinstance(im, Image.Image) else ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    focal = focal or detect_focal(im)

    tw, th = target_w, target_h
    tr = tw / th
    sr = im.width / im.height

    resample = Image.Resampling.LANCZOS
    centering = (max(0.0, min(1.0, focal[0])), max(0.0, min(1.0, focal[1])))

    if _ratios_close(sr, tr):
        return ImageOps.fit(im, (tw, th), method=resample, centering=centering)

    # Full-bleed blurred backdrop from a cover crop
    radius = max(14, min(tw, th) // 35)
    backdrop = ImageOps.fit(im, (tw, th), method=resample, centering=centering)
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(radius))
    backdrop = ImageEnhance.Brightness(backdrop).enhance(0.78)
    backdrop = ImageEnhance.Color(backdrop).enhance(0.72)

    # Sharp foreground: fit entire image inside the frame
    scale = min(tw / im.width, th / im.height)
    # If letterbox bands would be very thin, nudge scale up slightly (still inside frame)
    cover_scale = max(tw / im.width, th / im.height)
    if cover_scale / scale < 1.18:
        scale = cover_scale * 0.98

    fw = max(1, int(im.width * scale))
    fh = max(1, int(im.height * scale))
    foreground = im.resize((fw, fh), resample)

    canvas = backdrop.copy()
    ox = (tw - fw) // 2
    oy = (th - fh) // 2
    canvas.paste(foreground, (ox, oy))
    return canvas


def crop_cookstove_monitor_region(im: Image.Image) -> Image.Image:
    """Optional preset: IoT module from community clean-cooking source photo."""
    w, h = im.size
    if h > w * 1.5:
        box = (int(w * 0.51), int(h * 0.53), int(w * 0.90), int(h * 0.69))
    else:
        box = (int(w * 0.55), int(h * 0.45), int(w * 0.92), int(h * 0.78))
    return im.crop(box)


def crop_solar_monitor_interior(im: Image.Image) -> Image.Image:
    """Optional preset: open enclosure interior from solar D-MRV source photo."""
    w, h = im.size
    return im.crop((int(w * 0.38), int(h * 0.42), w, h))


def resolve_source(name: str) -> Path | None:
    for candidate in (INCOMING / name, OUT / name):
        if candidate.is_file():
            return candidate
    # Legacy project-root sources
    aliases = {
        "projects-cookstove.jpg": ROOT / "Community clean cooking & device monitoring.jpg",
        "projects-solar.jpg": ROOT / "Distributed Solar D-MRV Initiative.jpg",
    }
    path = aliases.get(name)
    if path and path.is_file():
        return path
    return None


def preprocess(name: str, im: Image.Image) -> Image.Image:
    src = resolve_source(name)
    if name == "projects-cookstove.jpg" and src and "clean cooking" in src.name.lower():
        return crop_cookstove_monitor_region(im)
    if name == "projects-solar.jpg" and src and "solar" in src.name.lower():
        return crop_solar_monitor_interior(im)
    return im


def save_jpg(im: Image.Image, name: str, quality: int = 88) -> None:
    path = OUT / name
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)
    print(f"  ok {path.name}  {im.size[0]}x{im.size[1]}")


def process_one(name: str, size: tuple[int, int]) -> bool:
    src = resolve_source(name)
    if not src:
        return False
    im = load_image(src)
    im = preprocess(name, im)
    focal = detect_focal(im)
    out = smart_fill_frame(im, size[0], size[1], focal=focal)
    save_jpg(out, name)
    return True


def propagate_derived() -> None:
    """When only project images exist, fill related slots from the same assets."""
    solar = OUT / "projects-solar.jpg"
    cook = OUT / "projects-cookstove.jpg"
    if not solar.is_file() or not cook.is_file():
        return
    pairs = [
        ("home-pillar-1.jpg", solar),
        ("home-pillar-3.jpg", solar),
        ("solutions-integrity.jpg", cook),
    ]
    for target, source in pairs:
        if (INCOMING / target).is_file():
            continue
        if target in IMAGE_FRAMES:
            tw, th = IMAGE_FRAMES[target]
            im = load_image(source)
            save_jpg(smart_fill_frame(im, tw, th, focal=detect_focal(im)), target)
            print(f"  -> derived {target} from {source.name}")


def main() -> None:
    ensure_dirs()
    print(f"Incoming folder: {INCOMING}")
    print(f"Output folder:   {OUT}\n")

    done = 0
    skipped = 0
    for name, size in IMAGE_FRAMES.items():
        if process_one(name, size):
            done += 1
        else:
            skipped += 1

    propagate_derived()

    print(f"\nProcessed {done} image(s), skipped {skipped} (no source file).")
    if skipped:
        print("Add files to incoming/ — see assets/images/README.md for filenames.")


if __name__ == "__main__":
    main()
