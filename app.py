import streamlit as st
from PIL import Image
import io

# Import the dictionary of processing functions from image_filters.py
try:
    from image_filters import STYLE_FUNCTIONS
except ImportError:
    st.error("Error: `image_filters.py` not found. Please make sure both files are in the same directory.")
    st.stop()

# TRANSLATION DATA

# Internal keys (same as in image_filters.py)
STYLE_KEYS = list(STYLE_FUNCTIONS.keys())

# Dictionary containing style names and descriptions
STYLE_DETAILS = {
    # "ume": {
    #     "vi": {
    #         "name": "⭐ Ume Style",
    #         "desc": "Phong cách chỉnh ảnh nổi bật với độ bão hòa và tương phản cao, mang lại cảm giác sống động và ấn tượng."
    #     },
    #     "en": {
    #         "name": "⭐ Ume Style",
    #         "desc": "A photo style featuring strong contrast and saturation for a vivid, impactful look."
    #     },
    #     "ja": {
    #         "name": "⭐ Umeスタイル",
    #         "desc": "高いコントラストと彩度が特徴で、鮮やかで印象的な仕上がりになります。"
    #     },
    # },

    "ume_soft": {
        "vi": {
            "name": "⭐ Ume Style (Mềm)",
            "desc": "Tăng nhẹ độ bão hòa và tương phản để làm ảnh rực rỡ hơn mà vẫn tự nhiên, phù hợp cho chân dung và phong cảnh sáng."
        },
        "en": {
            "name": "⭐ Ume Style (Soft)",
            "desc": "Gently enhances saturation and contrast for a lively yet natural look — ideal for portraits and bright scenes."
        },
        "ja": {
            "name": "⭐ Umeスタイル（ソフト）",
            "desc": "彩度とコントラストを控えめに強調し、自然で明るい印象に仕上げます。ポートレートや明るい風景に最適です。"
        },
    },

    "ume_natural": {
        "vi": {
            "name": "⭐ Ume Style (Tự nhiên)",
            "desc": "Cân bằng giữa độ tương phản và màu sắc sống động, giúp ảnh nổi bật mà vẫn giữ được cảm giác hài hòa, giống các bộ lọc Instagram cao cấp."
        },
        "en": {
            "name": "⭐ Ume Style (Natural)",
            "desc": "Balances strong contrast and vibrant colors for a vivid yet harmonious look, similar to premium Instagram filters."
        },
        "ja": {
            "name": "⭐ Umeスタイル（ナチュラル）",
            "desc": "コントラストと鮮やかさのバランスを取り、印象的でありながら調和のとれた仕上がりにします。"
        },
    },

    "ume_strong": {
        "vi": {
            "name": "⭐ Ume Style (Mạnh)",
            "desc": "Tăng mạnh độ tương phản và bão hòa, mang lại hiệu ứng ấn tượng và sống động — phù hợp cho ảnh phong cảnh hoặc đường phố."
        },
        "en": {
            "name": "⭐ Ume Style (Strong)",
            "desc": "Applies strong contrast and high saturation for a bold, dynamic look — great for landscapes or street photography."
        },
        "ja": {
            "name": "⭐ Umeスタイル（ストロング）",
            "desc": "コントラストと彩度を強く高め、力強くダイナミックな印象を与えます。風景写真やストリート写真に最適です。"
        },
    },

    "vintage": {
        "vi": {"name": "Vintage / Retro", "desc": "Tạo vẻ cũ kỹ, hoài cổ với màu sắc phai nhạt và tông màu ấm."},
        "en": {"name": "Vintage / Retro", "desc": "Creates an old, nostalgic look with faded colors and warm tones."},
        "ja": {"name": "ヴィンテージ / レトロ", "desc": "色あせた暖色系の色調で、古くノスタルジックな外観を作り出します。"},
    },
    "film": {
        "vi": {"name": "Film / Analog (Thêm hạt)", "desc": "Giả lập ảnh chụp từ máy phim, thường có thêm nhiễu hạt (grain) để tăng độ chân thực."},
        "en": {"name": "Film / Analog (Add grain)", "desc": "Simulates photos from a film camera, often with added grain for authenticity."},
        "ja": {"name": "フィルム / アナログ (グレイン追加)", "desc": "フィルムカメラで撮影した写真をシミュレートし、しばしば本物らしさのためにグレイン（粒子）を追加します。"},
    },
    "cinematic": {
        "vi": {"name": "Cinematic / Teal & Orange", "desc": "Phong cách điện ảnh phổ biến, đẩy tông màu tối sang Xanh (Teal) và tông màu da/sáng sang Cam (Orange)."},
        "en": {"name": "Cinematic / Teal & Orange", "desc": "A popular cinematic style that pushes shadows towards Teal and skin/highlights towards Orange."},
        "ja": {"name": "シネマティック / ティール＆オレンジ", "desc": "影をティール（青緑）に、肌やハイライトをオレンジに寄せる、人気のある映画風のスタイルです。"},
    },
    "bw": {
        "vi": {"name": "Black & White / Monochrome", "desc": "Chuyển ảnh sang thang độ xám (trắng đen), tập trung vào hình khối, ánh sáng và tương phản."},
        "en": {"name": "Black & White / Monochrome", "desc": "Converts the image to grayscale, focusing on shape, light, and contrast."},
        "ja": {"name": "白黒 / モノクローム", "desc": "画像をグレースケール（白黒）に変換し、形、光、コントラストに焦点を当てます。"},
    },
    "sepia": {
        "vi": {"name": "Sepia (Tông nâu)", "desc": "Tạo tông màu nâu đỏ ấm áp, giống như các bức ảnh cũ từ thế kỷ 19."},
        "en": {"name": "Sepia (Brown tone)", "desc": "Creates a warm reddish-brown tone, resembling old photographs from the 19th century."},
        "ja": {"name": "セピア (ブラウン調)", "desc": "19世紀の古い写真のような、暖かみのある赤褐色の色調を作り出します。"},
    },
    "pastel": {
        "vi": {"name": "Pastel / Soft tone", "desc": "Làm dịu màu sắc, giảm tương phản và tăng độ sáng, tạo cảm giác nhẹ nhàng, mơ mộng."},
        "en": {"name": "Pastel / Soft tone", "desc": "Softens colors, reduces contrast, and increases brightness for a light, dreamy feel."},
        "ja": {"name": "パステル / ソフトトーン", "desc": "色を和らげ、コントラストを下げ、明るさを上げて、軽やかで夢のような雰囲気にします。"},
    },
    "hdr": {
        "vi": {"name": "HDR / High Contrast", "desc": "Tăng cường độ tương phản và độ sắc nét, làm nổi bật chi tiết ở cả vùng sáng và vùng tối."},
        "en": {"name": "HDR / High Contrast", "desc": "Enhances contrast and sharpness, bringing out details in both bright and dark areas."},
        "ja": {"name": "HDR / ハイコントラスト", "desc": "コントラストとシャープネスを強調し、明るい領域と暗い領域の両方のディテールを引き出します。"},
    },
    "moody": {
        "vi": {"name": "Moody / Dark tone", "desc": "Tạo cảm giác sâu lắng, tâm trạng bằng cách giảm nhẹ độ sáng tổng thể và tăng tương phản ở vùng tối."},
        "en": {"name": "Moody / Dark tone", "desc": "Creates a deep, atmospheric feel by slightly reducing overall brightness and increasing contrast in the shadows."},
        "ja": {"name": "ムーディー / ダークトーン", "desc": "全体の明るさをわずかに下げ、影のコントラストを上げることで、深みのある雰囲気を作り出します。"},
    },
    "warm": {
        "vi": {"name": "Warm tone (Tông ấm)", "desc": "Thêm tông màu vàng và cam vào ảnh, tạo cảm giác ấm áp, thân thiện hoặc hoài niệm (như hoàng hôn)."},
        "en": {"name": "Warm tone", "desc": "Adds yellow and orange hues to the image, creating a cozy, friendly, or nostalgic (like sunset) feel."},
        "ja": {"name": "暖色系", "desc": "画像に黄色やオレンジの色合いを加え、居心地の良い、親しみやすい、またはノスタルジックな（夕焼けのような）雰囲気を作り出します。"},
    },
    "cool": {
        "vi": {"name": "Cool tone (Tông lạnh)", "desc": "Thêm tông màu xanh dương vào ảnh, tạo cảm giác mát mẻ, yên tĩnh hoặc hiện đại, công nghệ."},
        "en": {"name": "Cool tone", "desc": "Adds blue hues to the image, creating a calm, quiet, or modern, technological feel."},
        "ja": {"name": "寒色系", "desc": "画像に青系の色合いを加え、落ち着いた、静かな、またはモダンで技術的な雰囲気を作り出します。"},
    }
}

# Dictionary for UI strings (buttons, titles, etc.)
TRANSLATED_UI = {
    "vi": {
        "lang_selector": "Chọn ngôn ngữ:",
        "title": "Style Change - Chuyển đổi Phong cách Ảnh",
        "upload_header": "1. Tải ảnh lên",
        "upload_prompt": "Chọn một file ảnh (JPG, PNG)",
        "original_caption": "Ảnh gốc",
        "result_header": "2. Chọn Style & Tải về",
        "select_style": "Chọn phong cách bạn muốn:",
        "apply_button": "Áp dụng style",
        "processing": "Đang xử lý...",
        "processed_caption": "Ảnh đã xử lý:",
        "download_button": "Tải ảnh đã xử lý",
        "info_start": "Vui lòng tải ảnh lên ở cột bên trái để bắt đầu.",
        "resize_info": "Ảnh gốc quá lớn. Đã tự động giảm kích thước (chiều rộng tối đa {max_width}px) để xử lý nhanh hơn.",
    },
    "en": {
        "lang_selector": "Select Language:",
        "title": "Style Change - Image Style Transfer",
        "upload_header": "1. Upload Image",
        "upload_prompt": "Choose an image file (JPG, PNG)",
        "original_caption": "Original Image",
        "result_header": "2. Select Style & Download",
        "select_style": "Select your desired style:",
        "apply_button": "Apply Style",
        "processing": "Processing...",
        "processed_caption": "Processed Image:",
        "download_button": "Download Processed Image",
        "info_start": "Please upload an image on the left to start.",
        "resize_info": "Original image is too large. It has been automatically resized (max width {max_width}px) for faster processing.",
    },
    "ja": {
        "lang_selector": "言語を選択:",
        "title": "スタイル変更 - 画像スタイル変換",
        "upload_header": "1. 画像をアップロード",
        "upload_prompt": "画像ファイルを選択 (JPG, PNG)",
        "original_caption": "元の画像",
        "result_header": "2. スタイルを選択 & ダウンロード",
        "select_style": "ご希望のスタイルを選択してください：",
        "apply_button": "スタイルを適用",
        "processing": "処理中...",
        "processed_caption": "処理後の画像：",
        "download_button": "処理済み画像をダウンロード",
        "info_start": "開始するには、左側で画像をアップロードしてください。",
        "resize_info": "元の画像が大きすぎるため、処理を高速化するために自動的にリサイズされました（最大幅 {max_width}px）。",
    }
}

# APP INTERFACE

st.set_page_config(layout="wide")

# 1. LANGUAGE SELECTOR
lang_code = st.radio(
    label="Chọn ngôn ngữ / Select Language / 言語を選択:",
    options=["vi", "en", "ja"],
    format_func=lambda code: {"vi": "Tiếng Việt", "en": "English", "ja": "日本語"}[code],
    horizontal=True,
)

# Get the corresponding UI strings for the selected language
ui = TRANSLATED_UI[lang_code]

# Set the page title according to the selected language
st.title(ui["title"])

# 2. TWO-COLUMN LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.header(ui["upload_header"])
    uploaded_file = st.file_uploader(
        ui["upload_prompt"], 
        type=["jpg", "jpeg", "png"]
    )
    
    original_image = None
    if uploaded_file is not None:
        original_image = Image.open(uploaded_file).convert('RGB')
        
        # Resize large images to improve performance
        MAX_WIDTH = 1200
        if original_image.width > MAX_WIDTH:
            try:
                aspect_ratio = original_image.height / original_image.width
                new_height = int(MAX_WIDTH * aspect_ratio)
                
                # Use RESAMPLING.LANCZOS for high-quality downsampling
                original_image = original_image.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                st.info(ui["resize_info"].format(max_width=MAX_WIDTH))
            except Exception as e:
                st.error(f"Lỗi khi giảm kích thước ảnh: {e}")
        
        st.image(original_image, caption=ui["original_caption"], width='stretch')

with col2:
    st.header(ui["result_header"])
    
    if original_image is not None:
        # Style selection box
        selected_key = st.selectbox(
            label=ui["select_style"],
            options=STYLE_KEYS,  # Use internal key list
            # Display translated names for users
            format_func=lambda key: STYLE_DETAILS[key][lang_code]["name"]
        )
        
        # Display the selected style’s description
        st.info(STYLE_DETAILS[selected_key][lang_code]["desc"])

        # Get the translated style name to show on the button
        selected_style_name = STYLE_DETAILS[selected_key][lang_code]["name"]
        
        # Image processing button (uses selected language)
        if st.button(f"{ui['apply_button']} \"{selected_style_name}\""):
            with st.spinner(ui["processing"]):
                # Retrieve the corresponding processing function using the internal key
                process_function = STYLE_FUNCTIONS[selected_key]
                # Apply the filter
                processed_image = process_function(original_image)
                
                st.image(
                    processed_image, 
                    caption=f"{ui['processed_caption']} {selected_style_name}", 
                    width='stretch'
                )
                
                # Prepare file for download
                buf = io.BytesIO()
                save_format = 'PNG' if selected_key == "bw" else 'JPEG'
                if save_format == 'PNG':
                    processed_image.save(buf, format="PNG")
                else:
                    processed_image.save(buf, format="JPEG", quality=95)
                
                byte_im = buf.getvalue()

                # Download button (uses selected language)
                st.download_button(
                    label=ui["download_button"],
                    data=byte_im,
                    file_name=f"{selected_key}_{uploaded_file.name}",  # Use internal key to avoid errors
                    mime=f"image/{save_format.lower()}"
                )
    else:
        # Display info message (uses selected language)
        st.info(ui["info_start"])
