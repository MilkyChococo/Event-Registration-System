import argparse
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET


TARGET_WIDTH = 1880
TARGET_HEIGHT = 1253
IMAGE_DIR = Path(__file__).resolve().parents[1] / "app" / "static" / "images"
SVG_NS = "http://www.w3.org/2000/svg"
SUPPORTED_RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def parse_view_box(root: ET.Element) -> tuple[float, float, float, float]:
    raw_view_box = (root.get("viewBox") or "").replace(",", " ").split()
    if len(raw_view_box) == 4:
        try:
            return tuple(float(value) for value in raw_view_box)  # type: ignore[return-value]
        except ValueError:
            pass

    width = parse_dimension(root.get("width")) or TARGET_WIDTH
    height = parse_dimension(root.get("height")) or TARGET_HEIGHT
    return 0.0, 0.0, float(width), float(height)


def parse_dimension(value: str | None) -> float | None:
    if not value:
        return None
    cleaned = value.strip().lower().replace("px", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def backup_file(path: Path) -> None:
    backup_path = path.with_suffix(f"{path.suffix}.bak")
    if not backup_path.exists():
        shutil.copy2(path, backup_path)


def scale_svg(path: Path, dry_run: bool) -> str:
    ET.register_namespace("", SVG_NS)
    tree = ET.parse(path)
    root = tree.getroot()
    min_x, min_y, source_width, source_height = parse_view_box(root)

    scale_x = TARGET_WIDTH / source_width
    scale_y = TARGET_HEIGHT / source_height
    children = list(root)

    if not dry_run:
        backup_file(path)
        for child in children:
            root.remove(child)

        group = ET.Element(f"{{{SVG_NS}}}g")
        group.set("transform", f"translate({-min_x * scale_x:.6g} {-min_y * scale_y:.6g}) scale({scale_x:.6g} {scale_y:.6g})")
        group.extend(children)

        root.set("width", str(TARGET_WIDTH))
        root.set("height", str(TARGET_HEIGHT))
        root.set("viewBox", f"0 0 {TARGET_WIDTH} {TARGET_HEIGHT}")
        root.set("preserveAspectRatio", "none")
        root.append(group)
        tree.write(path, encoding="utf-8", xml_declaration=False)

    return f"{path.name}: SVG {source_width:g}x{source_height:g} -> {TARGET_WIDTH}x{TARGET_HEIGHT}"


def scale_raster(path: Path, dry_run: bool) -> str:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required to resize PNG/JPG/WEBP files. Install it with: pip install pillow") from exc

    with Image.open(path) as image:
        source_size = image.size
        if not dry_run:
            backup_file(path)
            resized = image.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
            resized.save(path)
    return f"{path.name}: raster {source_size[0]}x{source_size[1]} -> {TARGET_WIDTH}x{TARGET_HEIGHT}"


def iter_image_files(image_dir: Path) -> list[Path]:
    supported_extensions = {".svg", *SUPPORTED_RASTER_EXTENSIONS}
    return sorted(
        path
        for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in supported_extensions
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Scale images in app/static/images to 1880x1253.")
    parser.add_argument("--image-dir", type=Path, default=IMAGE_DIR, help="Directory containing images to resize.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be resized without changing files.")
    args = parser.parse_args()

    image_dir = args.image_dir.resolve()
    if not image_dir.exists():
        raise SystemExit(f"Image directory does not exist: {image_dir}")

    image_files = iter_image_files(image_dir)
    if not image_files:
        print(f"No supported images found in {image_dir}")
        return

    for path in image_files:
        if path.suffix.lower() == ".svg":
            print(scale_svg(path, args.dry_run))
        else:
            print(scale_raster(path, args.dry_run))


if __name__ == "__main__":
    main()
