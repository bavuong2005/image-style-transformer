from PIL import Image, ImageEnhance, ImageOps
import numpy as np

# Helper functions
def adjust_rgb_channels(img, r_factor=1.0, g_factor=1.0, b_factor=1.0):
    r, g, b = img.split()
    r = r.point(lambda i: min(i * r_factor, 255))
    g = g.point(lambda i: min(i * g_factor, 255))
    b = b.point(lambda i: min(i * b_factor, 255))
    return Image.merge("RGB", (r, g, b))

def add_noise(img, intensity=15):
    arr = np.array(img).astype(np.int16)
    noise = np.random.randint(-intensity, intensity + 1, arr.shape, dtype=np.int16)
    noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)

def gamma_correct(img, gamma=1.0):
    arr = np.array(img).astype(np.float32) / 255.0
    arr = np.power(arr, gamma)
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype("uint8"))

def shift_hue(img, shift=2):
    h, s, v = img.convert('HSV').split()
    h = h.point(lambda i: (i + shift) % 255)
    return Image.merge('HSV', (h, s, v)).convert('RGB')

# Main filter functions
def apply_vintage(img):
    """Hiệu ứng cổ điển, màu hơi ngả vàng và tương phản thấp."""
    img = ImageEnhance.Color(img).enhance(0.6)
    img = ImageEnhance.Contrast(img).enhance(0.8)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = adjust_rgb_channels(img, 1.05, 1.02, 0.9)
    return img

def apply_film_analog(img):
    """Hiệu ứng film analog: tương phản mạnh và thêm hạt nhiễu."""
    img = ImageEnhance.Contrast(img).enhance(1.15)
    return add_noise(img, intensity=18)

def apply_teal_orange_cinematic(img):
    """Hiệu ứng teal-orange phong cách điện ảnh: da cam - xanh lam."""
    img = adjust_rgb_channels(img, r_factor=1.08, g_factor=0.95, b_factor=1.1)
    return ImageEnhance.Contrast(img).enhance(1.1)

def apply_black_white(img):
    """Chuyển ảnh sang trắng đen cổ điển."""
    return img.convert("L")

def apply_sepia(img):
    """Tạo tone nâu ấm kiểu ảnh cũ."""
    gray = img.convert("L")
    return ImageOps.colorize(gray, black="#4B382A", white="#F5ECD0")

def apply_pastel(img):
    """Tone sáng, màu nhạt nhẹ kiểu pastel."""
    img = ImageEnhance.Contrast(img).enhance(0.7)
    img = ImageEnhance.Brightness(img).enhance(1.15)
    img = ImageEnhance.Color(img).enhance(1.1)
    return img

def apply_hdr_boost(img):
    """Tăng tương phản và độ sắc nét kiểu HDR."""
    img = ImageEnhance.Contrast(img).enhance(1.7)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    return img

def apply_moody_dark(img):
    """Tone tối, cảm xúc, tương phản cao."""
    img = ImageEnhance.Brightness(img).enhance(0.85)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = adjust_rgb_channels(img, 1.02, 1.0, 0.95)
    return img

def apply_warm_tone(img):
    """Tăng tone ấm (đỏ, vàng), giảm xanh lam."""
    return adjust_rgb_channels(img, r_factor=1.15, g_factor=1.05, b_factor=0.9)

def apply_cool_tone(img):
    """Tăng tone lạnh (xanh lam), giảm đỏ."""
    return adjust_rgb_channels(img, r_factor=0.9, g_factor=1.0, b_factor=1.15)

# Ume style functions
def apply_ume_style_soft(img):
    """Ume style nhẹ nhàng, sáng, tự nhiên."""
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.3)
    img = ImageEnhance.Sharpness(img).enhance(1.1)
    img = shift_hue(img, 2)
    return gamma_correct(img, 0.95)

def apply_ume_style_natural(img):
    """Ume style trung tính, hơi ấm, tươi màu."""
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Color(img).enhance(1.6)
    img = ImageEnhance.Sharpness(img).enhance(1.2)
    img = shift_hue(img, 3)
    return gamma_correct(img, 0.9)

def apply_ume_style_strong(img):
    """Ume style mạnh mẽ, đậm màu, tương phản cao."""
    img = ImageEnhance.Brightness(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.8)
    img = ImageEnhance.Color(img).enhance(1.8)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    img = shift_hue(img, 4)
    return gamma_correct(img, 0.85)


# Map of style names to functions

STYLE_FUNCTIONS = {
    "ume_soft": apply_ume_style_soft,
    "ume_natural": apply_ume_style_natural,
    "ume_strong": apply_ume_style_strong,
    "vintage": apply_vintage,
    "film": apply_film_analog,
    "cinematic": apply_teal_orange_cinematic,
    "bw": apply_black_white,
    "sepia": apply_sepia,
    "pastel": apply_pastel,
    "hdr": apply_hdr_boost,
    "moody": apply_moody_dark,
    "warm": apply_warm_tone,
    "cool": apply_cool_tone,
}
