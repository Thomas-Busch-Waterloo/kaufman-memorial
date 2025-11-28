# Bryan Kaufman Memorial PDF Generator

A Python-based PDF generator that creates a beautiful memorial tribute document from JSON data, featuring customizable backgrounds, profile images, and paginated comments.

## Overview

This project generates a memorial PDF for Bryan Daniel Kaufman (1947-2025), a beloved math, physics and science teacher, props master and friend. The PDF includes memories and tributes from the Eastwood Arts Alumni Facebook group.

## Features

- **Dynamic PDF Generation**: Converts JSON data and HTML templates into professionally formatted PDFs
- **Customizable Backgrounds**: Supports per-page background images with configurable sizing and positioning
- **Smart Pagination**: Automatically groups comments across multiple pages based on character count and comment limits
- **Profile Images**: Displays author profile pictures alongside their memories
- **Debug Mode**: Generates an HTML file for preview and debugging before PDF creation

## Project Structure

```
kaufman/
├── render_pdf.py           # Main Python script for PDF generation
├── template.html           # Jinja2 HTML template
├── data.json              # Configuration and content data
├── requirements.txt       # Python dependencies
├── images/                # Image assets
│   ├── backgrounds/       # Background images for pages
│   └── profiles/          # Profile pictures for contributors
├── bryan-memories.pdf     # Generated PDF output
└── bryan-memories-debug.html  # Debug HTML output
```

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - `jinja2==3.1.2` - HTML templating engine
   - `weasyprint==61.2` - PDF generation from HTML/CSS

3. **System Dependencies** (for WeasyPrint):
   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
     ```
   - On macOS:
     ```bash
     brew install pango
     ```
   - On Windows: WeasyPrint will install necessary dependencies automatically

## Usage

### Generate the PDF

Simply run the main script:

```bash
python render_pdf.py
```

This will:
1. Load data from `data.json`
2. Paginate comments intelligently
3. Render the HTML template with Jinja2
4. Generate `bryan-memories-debug.html` for preview
5. Create `bryan-memories.pdf` as the final output

### Customize Content

Edit `data.json` to customize:

- **Person information**: Name, subtitle, date range, profile image
- **Background images**: Cover page and per-page backgrounds with custom sizing
- **Comments**: Author names, messages, profile images, and text heights

#### Background Configuration

The `backgrounds` section supports flexible configuration:

```json
{
  "backgrounds": {
    "cover": {
      "image": "images/backgrounds/vintage theater stage.png",
      "size": "cover",
      "position": "center"
    },
    "pages": {
      "image": "images/backgrounds/moon sky.png",
      "size": "cover",
      "position": "center"
    },
    "pages_list": [
      {
        "image": "images/backgrounds/drawn space.png",
        "size": "100% 100%",
        "position": "center"
      }
    ]
  }
}
```

**Size options**:
- `"cover"` - Scale to fill page while maintaining aspect ratio (may crop)
- `"100% 100%"` - Stretch to fill page completely (may distort)
- `"contain"` - Scale to fit within page (no cropping)

### Pagination Settings

The pagination algorithm in `render_pdf.py` can be adjusted:

```python
pages = paginate_comments(comments, max_chars=2400, max_per_page=2)
```

- `max_chars`: Maximum characters per page (default: 2400)
- `max_per_page`: Maximum number of comments per page (default: 2)

## Contributing

We welcome additional memories and tributes to Bryan Kaufman from the Eastwood Arts Alumni community and anyone whose life he touched.

### How to Add Your Memory

#### Option 1: Submit via GitHub Issue (Non-Technical Users)

If you're not familiar with Git, you can submit your memory through a GitHub issue:

1. Go to the [Issues page](https://github.com/Thomas-Busch-Waterloo/kaufman-memorial/issues)
2. Click "New Issue"
3. Provide the following information:
   - Your full name
   - Your message/memory of Bryan
   - A profile picture (optional, but encouraged)
4. Submit the issue and we'll add it to the PDF for you

#### Option 2: Submit a Pull Request (Technical Users)

If you're comfortable with Git and GitHub:

1. **Fork this repository**

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/kaufman-memorial.git
   cd kaufman-memorial
   ```

3. **Create a new branch**:
   ```bash
   git checkout -b add-my-memory
   ```

4. **Add your profile image** (optional):
   - Add your profile picture to `images/profiles/`
   - Supported formats: JPG, PNG, WebP
   - Recommended size: 300x300px or similar square dimensions
   - File name: Use your full name in lowercase with spaces (e.g., `john smith.jpg`)

5. **Edit `data.json`**:
   - Add your comment to the `comments` array
   - Follow the format shown below

6. **Test your changes** (optional):
   ```bash
   pip install -r requirements.txt
   python render_pdf.py
   ```
   - Check the generated PDF to ensure your entry looks correct

7. **Commit and push**:
   ```bash
   git add data.json images/profiles/
   git commit -m "Add memory from [Your Name]"
   git push origin add-my-memory
   ```

8. **Create a Pull Request**:
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Provide a brief description
   - Submit for review

### Comment Format

Add your entry to the `comments` array in `data.json`:

```json
{
  "author": "Your Full Name",
  "message": "Your memory or tribute to Bryan. Share a story, a lesson learned, or how he impacted your life.",
  "profile_image": "images/profiles/your name.jpg",
  "height": "120px"
}
```

**Field descriptions**:
- `author` (required): Your full name as you'd like it to appear
- `message` (required): Your memory or tribute (recommended 50-200 words)
- `profile_image` (optional): Path to your profile picture in the `images/profiles/` directory
- `height` (optional): Text height in pixels - leave as "120px" for average-length messages; adjust if your message is significantly longer or shorter

**Example**:

```json
{
  "author": "Jane Doe",
  "message": "Mr. Kaufman had a remarkable ability to make physics come alive. I'll never forget the day he demonstrated centrifugal force using a bucket of water on a rope. His enthusiasm was contagious and inspired me to pursue engineering.",
  "profile_image": "images/profiles/jane doe.jpg",
  "height": "140px"
}
```

### Guidelines

- **Be respectful**: This is a memorial tribute
- **Be authentic**: Share genuine memories and feelings
- **Length**: Aim for 50-200 words for optimal layout
- **Profile images**: Square images work best; will be displayed as circles
- **Testing**: If possible, generate the PDF locally to preview your addition

### Questions?

If you have any questions about contributing, please [open an issue](https://github.com/Thomas-Busch-Waterloo/kaufman-memorial/issues) or reach out to the repository maintainer.

## Development

### Debug HTML Output

The script generates `bryan-memories-debug.html` which can be opened in a browser to preview the layout before PDF generation. This is useful for:
- Testing CSS styles
- Checking layout and spacing
- Verifying image paths
- Troubleshooting rendering issues

### Modify Template

Edit `template.html` to customize:
- Page layout and structure
- CSS styles
- Font choices
- Spacing and margins

## Output

- **bryan-memories.pdf**: The final memorial PDF document
- **bryan-memories-debug.html**: HTML preview for debugging

## License

This project is for personal memorial use.

## Acknowledgments

Created in loving memory of Bryan Daniel Kaufman, with contributions from the Eastwood Arts Alumni community.
