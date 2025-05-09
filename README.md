# TrendTrace : Fashion Trend & Suspect Identification

This project focuses on the integration of advanced machine learning models and data management systems to enhance the process of **human detection**, **clothing parsing**, and **trend analysis** from video feeds.

## Key Technologies and Approaches

- **YOLOv8 for Human Detection**  
  The system uses YOLOv8 to detect humans in video feeds. It assigns bounding boxes and tracks individuals to avoid duplicate captures. To improve relevance, it focuses on a **Region of Interest (ROI)** and keypoints from **shoulder to knee**, ensuring only useful images are captured.

- **High Performance with Multiprocessing**  
  Captured frames are processed in parallel using Python's **multiprocessing** module to maintain system performance and handle real-time video data efficiently.

- **Clothing Parsing with U²-Net**  
  A pre-trained **U²-Net model** is used for clothes segmentation. Based on the **iMaterialist (Fashion) 2019 dataset**, clothing is categorized into:
  - Upper body
  - Lower body
  - Full body

  Precise bounding boxes are generated for each clothing region.

- **Attribute Extraction via Google AI Studio API**  
  Segmented clothing regions are analyzed using the **Google AI Studio API**, extracting detailed clothing attributes such as:
  - Type
  - Color
  - Pattern
  - Texture
  - Brand
  - Style
  - Season
  - Gender
  - Usage

## Data Management System

- **Dynamic Database with Gspread**  
  The project uses **Gspread**, a Python library for Google Sheets, to build a dynamic and real-time database. This setup allows:
  - Storing collected clothing data
  - Performing real-time updates
  - Enabling trend analysis
  - Supporting traceability and history tracking

## User Interface

- **Kivy and KivyMD UI**  
  A user-friendly interface is built using **Kivy** and **KivyMD**, offering:
  - Smooth navigation
  - Interactive controls
  - Real-time feedback for operations

## Applications

This robust solution can be applied in several domains, including:

- 👗 **Retail** – Customer behavior tracking, trend identification  
- 🔐 **Security** – Suspicious clothing detection, identification support  
- 🧵 **Fashion** – Style analysis, brand detection, seasonal recommendations  

---

Overall, the project demonstrates the **effective use of machine learning and data management technologies** to enable intelligent human detection, clothing analysis, and actionable insights from video data.
