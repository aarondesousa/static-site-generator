# Static Site Generator

A lightweight static site generator written in Python. It recursively processes Markdown (`.md`) files from a `content/` directory, converts them into HTML, and copies static assets to a `docs/` directory for deployment.

This project was built as part of a guided course on Boot.dev to practice file I/O, directory traversal, and Markdown parsing.

## 🚀 How to Run

> 📦 Prerequisite: Python **3.10 or higher** must be installed on your system.

### 🔹 Set Up the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/aarondesousa/static-site-generator.git
   cd static-site-generator
   ```

### 🔹 For Local Development

1. Run the script: `./main.sh`
2. Open your browser at [http://localhost:8888](http://localhost:8888)

### 🔹 For GitHub Pages Deployment

1. Ensure GitHub Pages is set to serve from the `docs/` folder.
2. Run the build script: `./build.sh`
   > If your repository name is different, update the base path in `build.sh`.
3. Push the generated `docs/` folder to GitHub.

📁 **Note:** If your GitHub Pages setup uses a different output directory or base path, you can adjust it in `src/main.py` by modifying:

```python
destination_public_dir = os.path.join(".", "docs")
```
