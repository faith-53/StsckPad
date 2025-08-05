# StackPad - Modern Text Editor

A feature-rich text editor built with Python and tkinter, designed for developers and writers who need a lightweight yet powerful editing environment.

## Overview

StackPad is a modern text editor that combines simplicity with powerful features. It offers a tabbed interface, file explorer sidebar, syntax highlighting support, and session management - all in a lightweight package that runs smoothly on any system.

## Features

### Core Features
- **Tabbed Interface**: Work with multiple files simultaneously using intuitive tabs
- **File Explorer**: Built-in sidebar for easy file and folder navigation
- **Auto-save**: Automatic saving prevents data loss
- **Session Management**: Restore your previous work environment on restart
- **Zoom Controls**: Adjustable font size for better readability

### Editing Features
- **Undo/Redo**: Full undo/redo support with keyboard shortcuts
- **Find & Replace**: Powerful search and replace functionality
- **Syntax Highlighting**: Support for various programming languages
- **Word Wrap**: Automatic text wrapping for better readability

### File Support
- **Multiple Formats**: Supports .txt, .py, .md, .json, and more
- **Large Files**: Efficient handling of large text files
- **Encoding**: UTF-8 support for international text

## Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Quick Start
1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:

```bash
python Editor.py
```

## Usage

### Starting the Application
Run `python Editor.py` to launch StackPad. The application will open with your last session restored (if available).

### Interface Overview
- **Sidebar**: File explorer on the left for easy navigation
- **Tabs**: Multiple documents can be opened simultaneously
- **Menu Bar**: Access to all features and settings

### Keyboard Shortcuts
- **Ctrl+N**: New tab
- **Ctrl+O**: Open file
- **Ctrl+S**: Save file
- **Ctrl+Shift+S**: Save as
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+F**: Find and replace
- **Ctrl++**: Zoom in
- **Ctrl+-**: Zoom out

## Technical Details

### Architecture
- **Language**: Python 3.x
- **GUI Framework**: tkinter
- **File Handling**: JSON for session management

### Dependencies
- **Standard Library**: Uses only Python standard library modules
- **No External Dependencies**: Zero additional package requirements

## Configuration

### Session Management
The application automatically saves your session to `.session.json`. This includes:
- Open files and their content
- File paths
- Tab positions

## Contributing
We welcome contributions! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License
This project is open source and available under the MIT License.
