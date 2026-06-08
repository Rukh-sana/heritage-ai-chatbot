"""
Image Generation for Mohenjo-Daro Heritage Chatbot
Generates rich, styled heritage images using PIL — no internet required.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ImageGenerator:
    def __init__(self):
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)

    # ──────────────────────────────────────────────
    #  Internal drawing helpers
    # ──────────────────────────────────────────────

    def _font(self, size):
        """Load a system font with graceful fallback."""
        candidates = [
            "arial.ttf", "Arial.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arial.ttf",
        ]
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        return ImageFont.load_default()

    def _bold_font(self, size):
        candidates = [
            "arialbd.ttf", "Arial Bold.ttf", "Arial-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arialbd.ttf",
        ]
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        return ImageFont.load_default()

    def _draw_gradient(self, draw, width, height, top_color, bottom_color):
        """Vertical gradient fill."""
        r1, g1, b1 = top_color
        r2, g2, b2 = bottom_color
        for y in range(height):
            t = y / height
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

    def _draw_stars(self, draw, width, height, count=80):
        """Scatter small star dots."""
        import random
        rng = random.Random(42)
        for _ in range(count):
            x = rng.randint(0, width)
            y = rng.randint(0, height // 2)
            r = rng.randint(1, 2)
            alpha = rng.randint(150, 255)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, alpha))

    def _draw_border(self, draw, width, height, color=(255, 215, 0), thickness=4):
        """Decorative double-line border."""
        for i, w in enumerate([thickness, 1]):
            offset = 12 + i * 10
            draw.rectangle(
                [(offset, offset), (width - offset, height - offset)],
                outline=color, width=w,
            )

    def _centered_text(self, draw, text, y, font, color, width):
        """Draw horizontally centred text."""
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
        except AttributeError:
            tw, _ = draw.textsize(text, font=font)
        x = (width - tw) // 2
        draw.text((x, y), text, fill=color, font=font)

    # ──────────────────────────────────────────────
    #  Image 1 — The Great Bath
    # ──────────────────────────────────────────────

    def _create_great_bath(self):
        W, H = 800, 500
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)

        # Deep-blue sky gradient
        self._draw_gradient(draw, W, H // 2, (10, 20, 60), (30, 60, 120))
        # Sandy ground
        self._draw_gradient(
            ImageDraw.Draw(img), W, H,
            (120, 90, 50), (80, 55, 25),
        )
        # Re-draw sky (gradient helper fills whole image so do ground second)
        draw2 = ImageDraw.Draw(img)
        for y in range(H // 2):
            t = y / (H // 2)
            r = int(10 + (30 - 10) * t)
            g = int(20 + (60 - 20) * t)
            b = int(60 + (120 - 60) * t)
            draw2.line([(0, y), (W, y)], fill=(r, g, b))
        for y in range(H // 2, H):
            t = (y - H // 2) / (H // 2)
            r = int(120 + (80 - 120) * t)
            g = int(90 + (55 - 90) * t)
            b = int(50 + (25 - 50) * t)
            draw2.line([(0, y), (W, y)], fill=(r, g, b))

        self._draw_stars(draw2, W, H, count=60)

        # ── Bath pool ──
        bx1, by1, bx2, by2 = 160, 200, 640, 390
        # Pool surround (stone)
        draw2.rectangle([bx1 - 20, by1 - 20, bx2 + 20, by2 + 20],
                        fill=(140, 110, 70), outline=(90, 70, 40), width=3)
        # Water surface — blue with shimmer
        draw2.rectangle([bx1, by1, bx2, by2], fill=(20, 80, 140))
        # Shimmer lines
        for i in range(6):
            y_sh = by1 + 30 + i * 25
            draw2.line([(bx1 + 20, y_sh), (bx2 - 20, y_sh)],
                       fill=(80, 160, 220), width=2)

        # ── Brick columns / walls ──
        brick_color = (160, 120, 70)
        mortar = (200, 175, 140)
        for cx in [bx1 - 40, bx2 + 20]:
            for row in range(5):
                ry = by1 - 80 + row * 22
                draw2.rectangle([cx, ry, cx + 18, ry + 18],
                                fill=brick_color, outline=mortar, width=1)

        # ── Steps ──
        for s in range(4):
            draw2.rectangle(
                [bx1 + s * 18, by2 - s * 10, bx1 + (s + 1) * 18, by2 + 5],
                fill=(130, 100, 60), outline=(90, 70, 40), width=1,
            )

        # ── Brick floor texture ──
        for row in range(3):
            for col in range(8):
                fx = bx1 - 50 + col * 90
                fy = by2 + 20 + row * 14
                draw2.rectangle([fx, fy, fx + 85, fy + 12],
                                fill=brick_color, outline=mortar, width=1)

        self._draw_border(draw2, W, H)

        # ── Labels ──
        f_title = self._bold_font(42)
        f_sub   = self._font(20)
        f_small = self._font(15)
        gold = (255, 215, 0)
        white = (255, 255, 255)
        silver = (200, 200, 200)

        self._centered_text(draw2, "THE GREAT BATH", 30, f_title, gold, W)
        self._centered_text(draw2, "Ancient Ritual Pool  •  12m × 7m  •  2500 BCE", 85, f_sub, white, W)
        self._centered_text(draw2, "Mohenjo-Daro  •  UNESCO World Heritage  •  Sindh, Pakistan", 420, f_small, silver, W)
        self._centered_text(draw2, "One of the earliest public water structures in human history", 445, f_small, gold, W)

        path = os.path.join(self.output_dir, "mohenjo_daro_great_bath.jpg")
        img.save(path, quality=95)
        print(f"✅ Created: mohenjo_daro_great_bath.jpg")
        return path

    # ──────────────────────────────────────────────
    #  Image 2 — Urban Architecture & Grid Streets
    # ──────────────────────────────────────────────

    def _create_architecture(self):
        W, H = 800, 500
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)

        # Warm desert sky
        for y in range(H):
            t = y / H
            r = int(210 + (140 - 210) * t)
            g = int(170 + (100 - 170) * t)
            b = int(100 + (60 - 100) * t)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        brick  = (160, 115, 65)
        mortar = (190, 155, 110)
        shadow = (110, 75, 35)
        road   = (180, 155, 110)

        # ── Main north-south street ──
        draw.rectangle([370, 80, 430, H - 20], fill=road)
        # ── East-west cross street ──
        draw.rectangle([0, 250, W, 290], fill=road)
        # Street edge lines
        for x in [370, 430]:
            draw.line([(x, 80), (x, H - 20)], fill=(150, 120, 80), width=2)
        for y in [250, 290]:
            draw.line([(0, y), (W, y)], fill=(150, 120, 80), width=2)

        def brick_building(x1, y1, x2, y2, height_rows=6, window=True):
            """Draw a brick building block."""
            draw.rectangle([x1, y1, x2, y2], fill=brick, outline=shadow, width=2)
            bh = (y2 - y1) // height_rows
            bw = 40
            for row in range(height_rows):
                offset = (row % 2) * (bw // 2)
                for col in range(-1, (x2 - x1) // bw + 2):
                    bx = x1 + col * bw + offset
                    by = y1 + row * bh
                    draw.rectangle([bx, by, bx + bw - 2, by + bh - 2],
                                   fill=brick, outline=mortar, width=1)
            if window:
                # Simple square windows
                wx = (x1 + x2) // 2 - 12
                wy = y1 + 20
                draw.rectangle([wx, wy, wx + 24, wy + 24],
                               fill=(80, 120, 160), outline=shadow, width=1)

        # Left-side buildings
        brick_building(30,  90, 340, 240)
        brick_building(30, 300, 340, 450)
        brick_building(80, 160, 200, 240, height_rows=4, window=False)

        # Right-side buildings
        brick_building(460,  90, 760, 240)
        brick_building(460, 300, 760, 450)
        brick_building(550, 140, 700, 240, height_rows=4)

        # ── Drainage channel along street ──
        draw.rectangle([368, 90, 375, H - 20], fill=(50, 80, 120))
        draw.rectangle([428, 90, 435, H - 20], fill=(50, 80, 120))
        draw.rectangle([0, 248, W, 253],   fill=(50, 80, 120))
        draw.rectangle([0, 288, W, 293],   fill=(50, 80, 120))

        self._draw_border(draw, W, H)

        f_title = self._bold_font(36)
        f_sub   = self._font(19)
        f_small = self._font(14)
        gold  = (255, 215, 0)
        white = (255, 255, 255)
        dark  = (40, 25, 10)

        self._centered_text(draw, "URBAN ARCHITECTURE & GRID STREETS", 18, f_title, gold, W)
        self._centered_text(draw, "Standardised Fired Bricks  •  Covered Drainage  •  Planned Grid Layout", 62, f_sub, white, W)
        self._centered_text(draw, "Mohenjo-Daro  •  2500–1900 BCE  •  Larkana, Sindh", 460, f_small, gold, W)
        self._centered_text(draw, "Advanced urban planning — 4,000 years before modern city grids", 478, f_small, (220, 190, 140), W)

        path = os.path.join(self.output_dir, "mohenjo_daro_architecture.jpg")
        img.save(path, quality=95)
        print(f"✅ Created: mohenjo_daro_architecture.jpg")
        return path

    # ──────────────────────────────────────────────
    #  Image 3 — City Overview / Aerial at Sunset
    # ──────────────────────────────────────────────

    def _create_overview(self):
        W, H = 800, 500
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)

        # Dramatic sunset sky
        sky_colors = [
            (20, 10, 40), (60, 20, 60), (140, 50, 30),
            (200, 100, 30), (230, 160, 60), (245, 200, 100),
        ]
        band = H // 2 // len(sky_colors)
        for i, col in enumerate(sky_colors):
            nxt = sky_colors[i + 1] if i + 1 < len(sky_colors) else col
            for dy in range(band):
                t = dy / band
                r = int(col[0] + (nxt[0] - col[0]) * t)
                g = int(col[1] + (nxt[1] - col[1]) * t)
                b = int(col[2] + (nxt[2] - col[2]) * t)
                draw.line([(0, i * band + dy), (W, i * band + dy)], fill=(r, g, b))

        # Desert floor
        for y in range(H // 2, H):
            t = (y - H // 2) / (H // 2)
            r = int(130 + (70 - 130) * t)
            g = int(95  + (45 - 95)  * t)
            b = int(45  + (20 - 45)  * t)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        # ── Sun disc ──
        sun_x, sun_y = W // 2, H // 2 - 10
        for radius in range(55, 5, -5):
            alpha = int(80 + (55 - radius) * 3)
            col = (245, 200, 80, alpha)
            draw.ellipse(
                [sun_x - radius, sun_y - radius, sun_x + radius, sun_y + radius],
                fill=(245, 200, 80),
            )
        draw.ellipse([sun_x - 28, sun_y - 28, sun_x + 28, sun_y + 28],
                     fill=(255, 230, 120))

        # ── City silhouette (aerial perspective rows) ──
        brick = (110, 80, 40)
        dark  = (70, 50, 20)
        light = (160, 120, 65)

        # Far background buildings (small)
        for i in range(18):
            bx = 30 + i * 42
            bh = 18 + (i % 4) * 8
            by = H // 2 - bh
            draw.rectangle([bx, by, bx + 36, H // 2 + 5], fill=(80, 60, 30))

        # Mid-ground buildings
        for i in range(10):
            bx = 40 + i * 72
            bh = 35 + (i % 3) * 15
            by = H // 2 + 10
            draw.rectangle([bx, by, bx + 65, by + bh], fill=brick, outline=dark, width=1)
            # Brick rows
            for row in range(bh // 10):
                draw.line([(bx, by + row * 10), (bx + 65, by + row * 10)],
                           fill=dark, width=1)

        # Foreground large blocks
        fg_buildings = [
            (20, H // 2 + 80, 180, H - 30),
            (200, H // 2 + 65, 380, H - 25),
            (400, H // 2 + 75, 570, H - 35),
            (590, H // 2 + 60, 770, H - 20),
        ]
        for x1, y1, x2, y2 in fg_buildings:
            draw.rectangle([x1, y1, x2, y2], fill=light, outline=dark, width=2)
            # Horizontal brick lines
            for row in range((y2 - y1) // 14):
                draw.line([(x1, y1 + row * 14), (x2, y1 + row * 14)],
                           fill=dark, width=1)
            # Vertical mortar lines (staggered)
            for row in range((y2 - y1) // 14):
                offset = (row % 2) * 28
                for col in range((x2 - x1) // 55 + 1):
                    vx = x1 + col * 55 + offset
                    draw.line([(vx, y1 + row * 14), (vx, y1 + (row + 1) * 14)],
                               fill=dark, width=1)

        # ── Granary / citadel mound (prominent structure left) ──
        draw.polygon(
            [(60, H // 2 + 55), (160, H // 2 + 20), (260, H // 2 + 55)],
            fill=(130, 95, 45), outline=dark,
        )
        draw.rectangle([90, H // 2 + 25, 230, H // 2 + 55],
                       fill=(110, 80, 35), outline=dark, width=1)

        # ── Street grid lines (top-down) ──
        for sx in [190, 395, 585]:
            draw.line([(sx, H // 2 + 5), (sx, H - 20)], fill=(170, 140, 90), width=3)
        draw.line([(20, H // 2 + 100), (W - 20, H // 2 + 100)],
                   fill=(170, 140, 90), width=3)

        self._draw_stars(draw, W, H // 2, count=40)
        self._draw_border(draw, W, H)

        f_title = self._bold_font(44)
        f_sub   = self._font(20)
        f_small = self._font(14)
        gold   = (255, 215, 0)
        white  = (255, 255, 255)
        silver = (210, 190, 150)

        self._centered_text(draw, "MOHENJO-DARO", 22, f_title, gold, W)
        self._centered_text(draw, "Indus Valley Civilisation  •  Archaeological Reconstruction at Sunset", 76, f_sub, white, W)
        self._centered_text(draw, "UNESCO World Heritage Site  •  Est. 2500 BCE  •  Pop. ~35,000–40,000", 455, f_small, gold, W)
        self._centered_text(draw, "Larkana District, Sindh, Pakistan  •  Discovered 1922", 475, f_small, silver, W)

        path = os.path.join(self.output_dir, "mohenjo_daro_overview.jpg")
        img.save(path, quality=95)
        print(f"✅ Created: mohenjo_daro_overview.jpg")
        return path

    # ──────────────────────────────────────────────
    #  Public API
    # ──────────────────────────────────────────────

    def generate_project_images(self):
        """
        Generate all 3 Mohenjo-Daro project images.

        Returns
        -------
        generated_files : list[str]   — ordered list of file paths
        image_map       : dict[str, str] — key → file path
            Keys: 'great_bath', 'architecture', 'overview'
        """
        print("\n" + "=" * 60)
        print("🎨  GENERATING MOHENJO-DARO IMAGES")
        print("=" * 60 + "\n")

        creators = [
            ("great_bath",   self._create_great_bath),
            ("architecture", self._create_architecture),
            ("overview",     self._create_overview),
        ]

        image_map = {}
        generated_files = []

        for key, fn in creators:
            try:
                path = fn()
                image_map[key] = path
                generated_files.append(path)
            except Exception as e:
                print(f"⚠️  Failed to create '{key}': {e}")

        print("\n" + "=" * 60)
        print(f"✅  TOTAL: {len(generated_files)}/3 images ready")
        print(f"   Folder: {self.output_dir}/")
        print("=" * 60 + "\n")

        return generated_files, image_map
