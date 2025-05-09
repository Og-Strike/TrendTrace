# 🔧 Setup Instructions for Google Gemini & Gspread Integration

Follow the steps below to set up the Gemini API and Google Sheets (Gspread) integration for your project.

---

## 📌 Step 1: Configure Gemini API

1. **Obtain your Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open the file `universal.py`.
3. Paste your **Gemini API key** into the appropriate variable, typically defined like:
   ```python
   API_KEY = "your-api-key-here"
   ```

---

## 📌 Step 2: Enable Google Sheets API (Gspread)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Drive API** and **Google Sheets API**.
4. Navigate to **APIs & Services > Credentials**.
5. Click on **"Create Credentials"** > choose **Service Account**.
6. After creating, **download the credentials file** in **JSON format** (e.g., `project_name.json`).

---

## 📌 Step 3: Share Google Drive Access

1. Open the downloaded `project_name.json` file.
2. Copy the `"client_email"` value.
3. Go to your Google Sheet > **Share** it with that email.
4. Give **Editor** permission to allow reading, writing, and updating.

---

## 📌 Step 4: Update JSON Credential Path in Code

1. **Locate** the following files:
   - `main.py`
   - `database.py`
2. In both files, **search for** the section where the **credential JSON path** is defined.
3. Replace it with your actual file path:
   ```python
   cred = ServiceAccountCredentials.from_json_keyfile_name("path/to/project_name.json", scope)
   ```

## 📌 Step 5: Run the Application from the Correct Directory

1. Before running the project, make sure you are in the correct directory where your project files are saved.
2. Open your terminal or command prompt.
3. Use the `cd` (change directory) command to navigate to the folder containing your project. For example:

   ```bash
   cd path/to/your/project

---

✅ **You're all set!** The system should now be able to read from and write to your Google Sheets using the configured APIs.
