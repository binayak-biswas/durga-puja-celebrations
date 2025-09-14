import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image

# ====== Config ======
destination_url = "https://binayak-biswas.github.io/durga-puja-celebrations/"
durga_maa_icon_path = "durga-maa.png"
output_filename = "durga_puja_qr_durga_maa.png"
# ====================

# Build QR with high error correction
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4,
)
qr.add_data(destination_url)
qr.make(fit=True)

# Generate QR with radial gradient fill (purple → maroon) on white background
img = qr.make_image(
    image_factory=StyledPilImage,
    color_mask=RadialGradiantColorMask(
        back_color=(255, 255, 255),   # white background
        center_color=(128, 0, 128),   # purple
        edge_color=(128, 0, 0)        # maroon
    )
).convert("RGB")

# Load Dhaki icon
try:
    icon = Image.open(durga_maa_icon_path).convert("RGBA")
except FileNotFoundError:
    raise FileNotFoundError("Maa Durga icon not found")

# Resize icon (~20% of QR width max)
img_w, img_h = img.size
icon_size = img_w // 5
icon.thumbnail((icon_size, icon_size), Image.LANCZOS)

# Center position
icon_w, icon_h = icon.size
x = (img_w - icon_w) // 2
y = (img_h - icon_h) // 2

# --- White background below the icon ---
white_bg = Image.new("RGB", icon.size, (255, 255, 255))
img.paste(white_bg, (x, y))

# Paste Dhaki icon in center on top of white background
img.paste(icon, (x, y), mask=icon)


# Save final QR
img.save(output_filename)
print(f"Festive QR code saved as {output_filename}")
