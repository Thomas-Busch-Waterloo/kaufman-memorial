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
