# SLR Parser & Compiler Frontend

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python implementation of SLR(1) parser with GUI interface for compiler frontend development.

## Features ✨

- **SLR Parsing Table Generation** with conflict detection
- Interactive **Tkinter-based GUI** for grammar analysis
- Lexical analyzer with symbol table management
- Support for logical expressions (`AND/OR/NOT`)
- Automatic Excel report generation for:
  - Action/Goto parsing tables
  - Closure sets visualization
  - FIRST/FOLLOW sets
- Multi-window visualization system
- Thread-safe queue implementation for parsing operations

## Installation 🛠️

### bash 

git clone https://github.com/kcflexigbo/slr-parser-compiler-frontend.git

cd slr-parser-compiler-frontend 

pip install -r requirements.txt

## Requirements 📦

### python 

pandas

pandastable

mttkinter # For thread-safe 
Tkinter 

xlrd # Excel file handling

## Usage 🚀
### bash 

python main.py

1. **Input Grammar** in the main text editor
2. Use control buttons to:
   - Generate parsing tables
   - View closure sets
   - Analyze FIRST/FOLLOW sets
   - Detect conflicts
3. Save results to Excel/Text files through `Save Files` option

## Project Structure 📂

. ├── Course Project/ # Main implementation 

│ ├── analyzer.py # Lexical analysis core 

│ ├── slrgenerator.py # SLR table generator 

│ ├── filesbrowser.py # File I/O operations 

│ └── main.py # GUI entry point 

├── Question 1/ # Basic parser implementation 

├── Question 2/ # Enhanced version with tables 

├── run.bat # Windows launch script 

└── .gitignore # Python/Venv exclusion rules

## Example Outputs 📊
1. **Action Table** (Excel)  
   ![Action Table Example](docs/action_table.png)

2. **Closure Visualization**
    
    ### plaintext 
   
    Closure 0: 

    S -> •EXPR 

   EXPR -> •EXPR OR TERM 

   EXPR -> •TERM 

    ...

## Contributing 🤝
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request

## License 📄
MIT License - See [LICENSE](LICENSE) for details

Key elements included:
1. Matches .gitignore patterns for Python projects
2. Reflects multi-directory structure from codebase
3. Highlights SLR-specific features from parsing tables
4. Includes threading requirements from mttkinter usage
5. Documents Excel I/O functionality shown in code
6. Maintains Windows compatibility (run.bat reference)