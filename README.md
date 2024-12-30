## Carousell_Auto_Selling_Textbooks

This project automates the process of selling textbooks on Carousell, addressing common challenges such as manual listing and photo uploads. 

The script uses Selenium WebDriver to simpllify the posting process, ensuring that users can efficiently sell their textbooks without tedious manual entry.

### Prerequisites
Python 3.x

### Setup Instructions
#### Step 1: Export Cookies
```
Use the EditThisCookie extension to export your cookies from Carousell. Save this as cookie.txt in the project directory.
```
#### Step 2: Clone this repository using Git and 
```
git clone https://github.com/RaymondRaman/Carousell_Auto_Selling_Textbooks
```
#### Step 3: Navigate into the project directory and install required libraries
```
Open terminal and run follow command
cd Carousell_Auto_Selling_Textbooks
pip install -r requirements.txt
```
#### Step 4: Export Cookies
```
Use the EditThisCookie extension to export your cookies from Carousell. Save this as `cookie.txt` in the project directory.
```
#### Step 5: Prepare Excel File
```
Modify Excel file named `items_to_sell.xlsx` containing the following columns:
- `Listing Title`
- `Condition`
- `Price`
- `Description`
```
#### Step 6: Organize Photos
```
Create a folder named `photos` in the same directory as the script. Inside, create subfolders for each textbook using the exact title from the Excel file. Place all relevant images in these subfolders. 

Tips: Assume there are n photos, name cover img as n, remaining img as n-1, n-2, ...
```
### Step 7: Run the script using
```
python auto_sell_script.py
```





