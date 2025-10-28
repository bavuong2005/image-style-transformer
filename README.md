# **Style Change \- Streamlit Image Filter App**

A simple web application built with Streamlit that allows users to upload an image and quickly apply various stylistic filters. The app is fully internationalized with support for English, Vietnamese, and Japanese for both the UI and filter descriptions.

## **Demo**

![Demo](https://raw.githubusercontent.com/bavuong2005/image-style-transformer/refs/heads/main/demo.gif)

## **Features**

* Simple drag-and-drop file uploader.  
* Side-by-side comparison of the original and processed image.  
* Download button for the resulting image.  
* **Multi-language Support:** 🇬🇧 English, 🇻🇳 Vietnamese, and 🇯🇵 Japanese.  
* Detailed descriptions for each style so users understand the effect before applying it.

### **Available Styles**

The application includes a wide range of popular filters:

1. **Vintage / Retro:** Creates an old, nostalgic look.  
2. **Film / Analog:** Simulates a film camera look with added grain.  
3. **Cinematic / Teal & Orange:** The famous blockbuster movie style.  
4. **Black & White:** Classic monochrome filter.  
5. **Sepia:** A nostalgic reddish-brown tone.  
6. **Pastel / Soft tone:** A light, dreamy, and soft color palette.  
7. **HDR / High Contrast:** Enhances details and contrast.  
8. **Moody / Dark tone:** A deep, atmospheric, and shadowy look.  
9. **Warm tone:** Adds warm yellow and orange hues.  
10. **Cool tone:** Adds cool blue and teal hues.  
11. **⭐ Ume Style (Custom):** A unique, custom-defined style featuring very high contrast and saturation for a powerful color punch.

## **Project Structure**

The project is split into two main files for better organization:

* app.py: Handles the entire Streamlit user interface (UI), state management, and language selection logic.  
* image\_filters.py: Contains all the PIL/NumPy image processing functions (e.g., apply\_...) and the function mapping dictionary.  
* requirements.txt: A list of all necessary Python dependencies.  
* README.md: This instruction file.

## **Installation and Usage**

### **Prerequisites**

* Python 3.8+

### **Instructions**

1. Get the code:  
   (Ensure you have app.py, image\_filters.py, and requirements.txt in the same directory).  
2. **(Recommended) Create a virtual environment:**  
   python \-m venv venv  
   source venv/bin/activate  \# On Windows: venv\\Scripts\\activate

3. Install the required libraries:  
   Open a terminal in the project directory and run:  
   pip install \-r requirements.txt

4. **Run the application:**  
   streamlit run app.py

5. Open your web browser and navigate to the local URL provided (usually http://localhost:8501).
