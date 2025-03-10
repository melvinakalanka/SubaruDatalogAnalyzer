# Subaru WRX STI ECU Log Analyzer

## Overview
The **Subaru WRX STI ECU Log Analyzer** is a GUI-based tool for analyzing ECU logs, ROM files, and ROM definition files. It allows users to visualize important engine parameters such as **boost pressure, knock correction, and injector duty cycle**.

## Features
- Load and analyze **ECU log files (CSV)**.
- Load **ROM files (BIN)**.
- Load **ROM definition files (XML)**.
- Extract key performance parameters:
  - Boost pressure
  - Knock correction
  - Injector duty cycle
- Visualize data with interactive plots.
- Simple GUI interface built with Tkinter.

## Prerequisites
- **Python 3.x** installed
- Required Python libraries:
  ```sh
  pip install pandas matplotlib
  ```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/subaru-log-analyzer.git
   cd subaru-log-analyzer
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Run the script:
   ```sh
   python subaru_log_analyzer.py
   ```
2. Use the GUI to upload:
   - **ECU Log (CSV)**
   - **ROM File (BIN)**
   - **ROM Definition File (XML)**
3. Click **Analyze Data** to process the logs and visualize key parameters.

## Error Handling
- **Missing Files**: Ensure all required files are uploaded before analysis.
- **Incorrect File Format**: Only CSV, BIN, and XML files are supported.
- **Permissions**: Ensure the script has read access to the selected files.

## Notes
- This tool is designed specifically for Subaru WRX STI ECU logs.
- The XML definition file must contain address mappings for correct analysis.
- The script can be modified to support additional Subaru models.

## License
This project is licensed under the MIT License.

