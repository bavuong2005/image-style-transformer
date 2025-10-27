from PIL import Image, ImageEnhance, ImageOps
import numpy as np

# Image Processing Functions (Image Filter Functions)

def apply_vintage(img):
    img_color = ImageEnhance.Color(img).enhance(0.6)
    img_contrast = ImageEnhance.Contrast(img_color).enhance(0.8)
    img_brightness = ImageEnhance.Brightness(img_contrast).enhance(1.1)
    r, g, b = img_brightness.split()
    r = r.point(lambda i: i * 1.05)
    g = g.point(lambda i: i * 1.02)
    b = b.point(lambda i: i * 0.9)
    return Image.merge('RGB', (r, g, b))

def apply_film_analog(img):
    img_contrast = ImageEnhance.Contrast(img).enhance(1.15)
    img_array = np.array(img_contrast)
    noise = np.random.randint(-18, 18, img_array.shape, dtype='int16')
    img_noisy = np.clip(img_array.astype('int16') + noise, 0, 255).astype('uint8')
    return Image.fromarray(img_noisy)

def apply_cinematic_teal_orange(img):
    r, g, b = img.split()
    r = r.point(lambda i: i * 1.1 if i > 120 else i * 0.9)
    g = g.point(lambda i: i * 0.95)
    b = b.point(lambda i: i * 1.1 if i < 150 else i * 0.9)
    return Image.merge('RGB', (r, g, b))

def apply_bw(img):
    return img.convert('L')

def apply_sepia(img):
    img_l = img.convert('L')
    return ImageOps.colorize(img_l, black="#4E3629", white="#FDF8E8")

def apply_pastel(img):
    img_contrast = ImageEnhance.Contrast(img).enhance(0.7)
    img_bright = ImageEnhance.Brightness(img_contrast).enhance(1.1)
    return img_bright

def apply_hdr_contrast(img):
    img_contrast = ImageEnhance.Contrast(img).enhance(1.7)
    img_sharp = ImageEnhance.Sharpness(img_contrast).enhance(1.2)
    return img_sharp

def apply_moody_dark(img):
    img_bright = ImageEnhance.Brightness(img).enhance(0.85)
    img_contrast = ImageEnhance.Contrast(img_bright).enhance(1.25)
    return img_contrast

def apply_warm_tone(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(i * 1.15, 255))
    b = b.point(lambda i: i * 0.9)
    return Image.merge('RGB', (r, g, b))

def apply_cool_tone(img):
    r, g, b = img.split()
    r = r.point(lambda i: i * 0.9)
    b = b.point(lambda i: min(i * 1.15, 255))
    return Image.merge('RGB', (r, g, b))

def apply_ume_style_soft(img):
    from PIL import ImageEnhance, Image
    import numpy as np

    img_enh = ImageEnhance.Brightness(img).enhance(1.03)
    img_enh = ImageEnhance.Contrast(img_enh).enhance(1.3)
    img_enh = ImageEnhance.Color(img_enh).enhance(1.3)
    img_enh = ImageEnhance.Sharpness(img_enh).enhance(1.1)

    # Hue shift nhẹ
    h, s, v = img_enh.convert('HSV').split()
    h_new = h.point(lambda i: (i + 2) % 255)
    img_hue = Image.merge('HSV', (h_new, s, v)).convert('RGB')

    # Nâng sáng bóng nhẹ bằng gamma
    data = np.array(img_hue, dtype=np.float32) / 255.0
    data = np.power(data, 0.95)
    return Image.fromarray(np.clip(data * 255, 0, 255).astype('uint8'))

def apply_ume_style_natural(img):
    from PIL import ImageEnhance, Image
    import numpy as np

    img_enh = ImageEnhance.Brightness(img).enhance(1.05)
    img_enh = ImageEnhance.Contrast(img_enh).enhance(1.5)
    img_enh = ImageEnhance.Color(img_enh).enhance(1.6)
    img_enh = ImageEnhance.Sharpness(img_enh).enhance(1.2)

    h, s, v = img_enh.convert('HSV').split()
    h_new = h.point(lambda i: (i + 3) % 255)
    img_hue = Image.merge('HSV', (h_new, s, v)).convert('RGB')

    data = np.array(img_hue, dtype=np.float32) / 255.0
    data = np.power(data, 0.9)  # nâng sáng vùng tối nhẹ
    return Image.fromarray(np.clip(data * 255, 0, 255).astype('uint8'))

def apply_ume_style_strong(img):
    from PIL import ImageEnhance, Image
    import numpy as np

    img_enh = ImageEnhance.Brightness(img).enhance(1.08)
    img_enh = ImageEnhance.Contrast(img_enh).enhance(1.8)
    img_enh = ImageEnhance.Color(img_enh).enhance(1.8)
    img_enh = ImageEnhance.Sharpness(img_enh).enhance(1.3)

    h, s, v = img_enh.convert('HSV').split()
    h_new = h.point(lambda i: (i + 4) % 255)
    img_hue = Image.merge('HSV', (h_new, s, v)).convert('RGB')

    data = np.array(img_hue, dtype=np.float32) / 255.0
    data = np.power(data, 0.85)
    return Image.fromarray(np.clip(data * 255, 0, 255).astype('uint8'))


# Map (Dictionary) linking style names to processing functions

STYLE_FUNCTIONS = {
    "ume_soft": apply_ume_style_soft,
    "ume_natural": apply_ume_style_natural,
    "ume_strong": apply_ume_style_strong,
    "vintage": apply_vintage,
    "film": apply_film_analog,
    "cinematic": apply_cinematic_teal_orange,
    "bw": apply_bw,
    "sepia": apply_sepia,
    "pastel": apply_pastel,
    "hdr": apply_hdr_contrast,
    "moody": apply_moody_dark,
    "warm": apply_warm_tone,
    "cool": apply_cool_tone,
}
