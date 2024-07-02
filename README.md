# Convert SSA results to DSS

This project modifies HEC-RAS unsteady flow files to quickly apply DSS data.

## 🧑🏽‍💻 Author
### Ned Santiago  📞+63 (917) 890 5173  ✉️ [nedsantiago@tutanota.com](mailto:nedsantiago@tutanota.com)

## 🎯 Purpose

This github project was made for Hydrologists working with SSA. Specifically, for acquaintances needing to move data from Autodesk Storm and Sanitary Analysis (SSA) to Hydrologic Engineering Center's River Analysis System (HEC-RAS).

Our Hydraulic models required 300+ timeseries data to be applied to its respective boundary condition line in HEC-RAS. Thus, to save time, this Python Script was made to quickly apply that data. This script is the successor to a GUI manipulation script using pyautogui. It was faster to manipulate the text file than the GUI of HEC-RAS; thus, this script succeeds the HEC-RAS GUI manipulator as a faster implementation.

## ⚡Usage
### For exporting flooding flow rate data
1) Run the file
2) Declare the HEC-RAS main directory
3) Declare Unsteady Flow file to manipulate
4) Select DSS file to apply to Unsteady Flow file
5) Done!

## 📖 Documentation
### How to create the executable

This package requires PyInstaller and a terminal. PyInstaller is responsible for creating an executable of `modify_unsteady.py`. First, install PyInstaller
```
py -m pip install pyinstaller
```
Second, locate the PyInstaller script. Using PyInstaller requires using the package itself (and not as a module). Thus, to compile the code:
```
pyinstaller ./src/modify_unsteady.py
```
The executable is located at 
```
./dist/modify_unsteady/modify_unsteady.exe
```