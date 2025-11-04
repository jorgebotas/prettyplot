from pathlib import Path
from matplotlib import font_manager


# Register custom fonts automatically on import
def _register_fonts():
    """
    Register custom fonts with matplotlib for automatic use.
    
    This function scans the fonts directory and registers all .ttf files
    with matplotlib's font manager using the addfont() method. The fonts
    will be immediately available for use in matplotlib plots.
    """
    
    # Get the directory containing this file
    package_dir = Path(__file__).parent
    fonts_dir = package_dir / "fonts"

    existing_fonts = list_registered_fonts()
    
    # Check if fonts directory exists
    if fonts_dir.exists():
        # Register all font files in the fonts directory
        for font_file in fonts_dir.glob("*.ttf"):
            # Skip if font already registered
            if font_file.stem in existing_fonts:
                continue

            try:
                # addfont() reads the font file and adds it to the font cache
                # It extracts font metadata (name, family, etc.) from the TTF file
                font_manager.fontManager.addfont(str(font_file))
            except Exception:
                # Silently ignore registration errors
                # (e.g., if the font is already registered or invalid)
                pass


def list_registered_fonts():
    """
    List all fonts that have been registered with matplotlib.
    
    Returns:
        list: List of font family names available.
    """
    
    # Get all font names from the manager
    font_names = [f.name for f in font_manager.fontManager.ttflist]
    
    return sorted(set(font_names))