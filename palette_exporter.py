import io
import json
import csv
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import List, Dict, Any

class PaletteExporter:
    """Export color palettes in various formats"""
    
    def __init__(self):
        self.swatch_width = 100
        self.swatch_height = 100
        self.text_height = 40
        
    def create_palette_image(self, colors: List[Dict], image_name: str = "palette", 
                           layout: str = "horizontal") -> bytes:
        """
        Create a visual palette image from extracted colors
        
        Args:
            colors: List of color dictionaries with rgb, hex, percentage
            image_name: Name for the palette
            layout: 'horizontal' or 'grid' layout
            
        Returns:
            Bytes of the PNG image
        """
        num_colors = len(colors)
        
        if layout == "horizontal":
            # Horizontal strip layout
            total_width = num_colors * self.swatch_width
            total_height = self.swatch_height + self.text_height
            
            # Create image
            img = Image.new('RGB', (total_width, total_height), 'white')
            draw = ImageDraw.Draw(img)
            
            for i, color in enumerate(colors):
                x = i * self.swatch_width
                rgb = color['rgb']
                hex_color = color['hex']
                percentage = color['percentage']
                
                # Draw color swatch
                draw.rectangle(
                    [(x, 0), (x + self.swatch_width, self.swatch_height)],
                    fill=rgb
                )
                
                # Add text labels
                try:
                    # Try to use a better font if available
                    font = ImageFont.truetype("arial.ttf", 12)
                except (OSError, IOError):
                    try:
                        font = ImageFont.load_default()
                    except AttributeError:
                        # Fallback for newer Pillow versions
                        font = ImageFont.load_default(size=12)
                
                # Color info text
                text_y = self.swatch_height + 5
                draw.text((x + 5, text_y), hex_color, fill='black', font=font)
                draw.text((x + 5, text_y + 15), f"{percentage:.1f}%", fill='black', font=font)
                
        else:  # grid layout
            # Calculate grid dimensions
            cols = min(4, num_colors)
            rows = (num_colors + cols - 1) // cols
            
            total_width = cols * self.swatch_width
            total_height = rows * (self.swatch_height + self.text_height)
            
            # Create image
            img = Image.new('RGB', (total_width, total_height), 'white')
            draw = ImageDraw.Draw(img)
            
            for i, color in enumerate(colors):
                row = i // cols
                col = i % cols
                
                x = col * self.swatch_width
                y = row * (self.swatch_height + self.text_height)
                
                rgb = color['rgb']
                hex_color = color['hex']
                percentage = color['percentage']
                
                # Draw color swatch
                draw.rectangle(
                    [(x, y), (x + self.swatch_width, y + self.swatch_height)],
                    fill=rgb
                )
                
                # Add text labels
                try:
                    font = ImageFont.truetype("arial.ttf", 12)
                except (OSError, IOError):
                    try:
                        font = ImageFont.load_default()
                    except AttributeError:
                        # Fallback for newer Pillow versions
                        font = ImageFont.load_default(size=12)
                
                text_y = y + self.swatch_height + 5
                draw.text((x + 5, text_y), hex_color, fill='black', font=font)
                draw.text((x + 5, text_y + 15), f"{percentage:.1f}%", fill='black', font=font)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    def export_as_json(self, colors: List[Dict], metadata: Dict = None) -> str:
        """
        Export palette as JSON format
        
        Args:
            colors: List of color dictionaries
            metadata: Additional information about the palette
            
        Returns:
            JSON string
        """
        palette_data = {
            'palette_info': metadata or {},
            'colors': [],
            'export_format': 'json',
            'total_colors': len(colors)
        }
        
        for i, color in enumerate(colors):
            color_data = {
                'index': i,
                'hex': color['hex'],
                'rgb': {
                    'r': int(color['rgb'][0]),
                    'g': int(color['rgb'][1]),
                    'b': int(color['rgb'][2])
                },
                'hsl': self._rgb_to_hsl(color['rgb']),
                'percentage': round(color['percentage'], 2),
                'brightness': round(color.get('brightness', 0), 2)
            }
            palette_data['colors'].append(color_data)
        
        return json.dumps(palette_data, indent=2)
    
    def export_as_csv(self, colors: List[Dict], metadata: Dict = None) -> str:
        """
        Export palette as CSV format
        
        Args:
            colors: List of color dictionaries
            metadata: Additional information about the palette
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Index', 'Hex', 'R', 'G', 'B', 'Percentage', 'Brightness'])
        
        # Color data
        for i, color in enumerate(colors):
            writer.writerow([
                i,
                color['hex'],
                int(color['rgb'][0]),
                int(color['rgb'][1]),
                int(color['rgb'][2]),
                round(color['percentage'], 2),
                round(color.get('brightness', 0), 2)
            ])
        
        return output.getvalue()
    
    def export_as_adobe_swatch(self, colors: List[Dict], palette_name: str = "Custom Palette") -> str:
        """
        Export palette in Adobe Swatch Exchange (.ase) compatible format (simplified)
        Returns a text representation that can be imported into design software
        """
        ase_text = f"Adobe Swatch Exchange - {palette_name}\n"
        ase_text += "=" * 50 + "\n\n"
        
        for i, color in enumerate(colors):
            rgb = color['rgb']
            hex_color = color['hex']
            
            # Convert RGB to 0-1 range for Adobe compatibility
            r_norm = rgb[0] / 255.0
            g_norm = rgb[1] / 255.0
            b_norm = rgb[2] / 255.0
            
            ase_text += f"Color {i+1}: {hex_color}\n"
            ase_text += f"  RGB: ({rgb[0]}, {rgb[1]}, {rgb[2]})\n"
            ase_text += f"  RGB Normalized: ({r_norm:.3f}, {g_norm:.3f}, {b_norm:.3f})\n"
            ase_text += f"  Percentage: {color['percentage']:.1f}%\n\n"
        
        return ase_text
    
    def export_as_css(self, colors: List[Dict], class_prefix: str = "color") -> str:
        """
        Export palette as CSS variables and classes
        """
        css_output = "/* Color Palette CSS */\n"
        css_output += ":root {\n"
        
        # CSS custom properties
        for i, color in enumerate(colors):
            css_output += f"  --{class_prefix}-{i+1}: {color['hex']};\n"
        
        css_output += "}\n\n"
        
        # CSS classes
        for i, color in enumerate(colors):
            css_output += f".{class_prefix}-{i+1} {{\n"
            css_output += f"  color: {color['hex']};\n"
            css_output += "}\n\n"
            
            css_output += f".bg-{class_prefix}-{i+1} {{\n"
            css_output += f"  background-color: {color['hex']};\n"
            css_output += "}\n\n"
        
        return css_output
    
    def export_as_scss(self, colors: List[Dict], variable_prefix: str = "color") -> str:
        """
        Export palette as SCSS variables
        """
        scss_output = "// Color Palette SCSS Variables\n\n"
        
        for i, color in enumerate(colors):
            scss_output += f"${variable_prefix}-{i+1}: {color['hex']};\n"
        
        scss_output += "\n// Color map for easy iteration\n"
        scss_output += f"$palette-colors: (\n"
        
        for i, color in enumerate(colors):
            scss_output += f"  '{variable_prefix}-{i+1}': {color['hex']}"
            if i < len(colors) - 1:
                scss_output += ","
            scss_output += "\n"
        
        scss_output += ");\n"
        
        return scss_output
    
    def export_for_figma(self, colors: List[Dict]) -> str:
        """
        Export palette in Figma-compatible format (JSON for plugins)
        """
        figma_data = {
            "version": "1.0",
            "type": "color-palette",
            "colors": []
        }
        
        for i, color in enumerate(colors):
            # Figma uses 0-1 range for RGB values
            figma_color = {
                "name": f"Color {i+1}",
                "hex": color['hex'],
                "rgb": {
                    "r": color['rgb'][0] / 255.0,
                    "g": color['rgb'][1] / 255.0,
                    "b": color['rgb'][2] / 255.0,
                    "a": 1.0
                },
                "percentage": color['percentage']
            }
            figma_data["colors"].append(figma_color)
        
        return json.dumps(figma_data, indent=2)
    
    def export_for_affinity(self, colors: List[Dict]) -> str:
        """Export palette in Affinity apps-compatible .afpalette format (XML)"""
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<palette name="Extracted Color Palette" version="2.0">')
        xml_content.append('  <colors>')
        
        for i, color in enumerate(colors):
            r, g, b = color['rgb']
            # Affinity uses 0-1 range for RGB values
            r_norm = r / 255.0
            g_norm = g / 255.0
            b_norm = b / 255.0
            
            xml_content.append(f'    <color name="Color {i+1}" model="rgb">')
            xml_content.append(f'      <component id="red" value="{r_norm:.6f}"/>')
            xml_content.append(f'      <component id="green" value="{g_norm:.6f}"/>')
            xml_content.append(f'      <component id="blue" value="{b_norm:.6f}"/>')
            xml_content.append(f'      <component id="alpha" value="1.0"/>')
            xml_content.append('    </color>')
        
        xml_content.append('  </colors>')
        xml_content.append('</palette>')
        
        return '\n'.join(xml_content)
    
    def export_for_photopea(self, colors: List[Dict]) -> str:
        """Export palette in Photopea-compatible .aco format (Adobe Color format as JSON)"""
        # Photopea can import Adobe Color Table (.aco) files
        # We'll create a JSON representation that can be imported
        photopea_colors = []
        
        for i, color in enumerate(colors):
            r, g, b = color['rgb']
            
            # Convert RGB to HSV for better color management
            r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
            max_val = max(r_norm, g_norm, b_norm)
            min_val = min(r_norm, g_norm, b_norm)
            diff = max_val - min_val
            
            # Calculate HSV
            if diff == 0:
                h = 0
            elif max_val == r_norm:
                h = (60 * ((g_norm - b_norm) / diff) + 360) % 360
            elif max_val == g_norm:
                h = (60 * ((b_norm - r_norm) / diff) + 120) % 360
            else:
                h = (60 * ((r_norm - g_norm) / diff) + 240) % 360
            
            s = 0 if max_val == 0 else diff / max_val
            v = max_val
            
            photopea_color = {
                "name": f"Color_{i+1}",
                "rgb": {
                    "r": r,
                    "g": g,
                    "b": b
                },
                "hsv": {
                    "h": round(h, 2),
                    "s": round(s * 100, 2),
                    "v": round(v * 100, 2)
                },
                "hex": color['hex'],
                "percentage": color['percentage']
            }
            photopea_colors.append(photopea_color)
        
        photopea_palette = {
            "name": "Extracted_Color_Palette",
            "type": "photopea_palette",
            "version": "1.0",
            "colors": photopea_colors,
            "usage_note": "Import this JSON into Photopea via Window > Swatches > Load Swatches"
        }
        
        safe_palette = self._sanitize_json_types(photopea_palette)
        return json.dumps(safe_palette, indent=2)
    
    def _rgb_to_hsl(self, rgb):
        """Convert RGB to HSL"""
        r, g, b = [x/255.0 for x in rgb]
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2
        
        if diff == 0:
            h = s = 0  # achromatic
        else:
            # Saturation
            s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
            
            # Hue
            if max_val == r:
                h = (g - b) / diff + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / diff + 2
            else:
                h = (r - g) / diff + 4
            h /= 6
        
        return {
            'h': round(h * 360, 1),
            's': round(s * 100, 1),
            'l': round(l * 100, 1)
        }
    
    def create_pencil_shopping_list(self, pencil_matches: List[Dict], format_type: str = "text") -> str:
        """
        Create a shopping list of recommended pencils
        
        Args:
            pencil_matches: List of pencil match dictionaries
            format_type: 'text', 'csv', or 'json'
        """
        # Remove duplicates and sort by quality
        unique_pencils = {}
        for match in pencil_matches:
            key = f"{match['brand']}_{match['code']}"
            if key not in unique_pencils or match['color_difference'] < unique_pencils[key]['color_difference']:
                unique_pencils[key] = match
        
        sorted_pencils = sorted(unique_pencils.values(), key=lambda x: x['color_difference'])
        
        if format_type == "text":
            output = "COLORED PENCIL SHOPPING LIST\n"
            output += "=" * 40 + "\n\n"
            
            prismacolor = [p for p in sorted_pencils if p['brand'] == 'Prismacolor']
            faber_castell = [p for p in sorted_pencils if p['brand'] == 'Faber Castell']
            
            if prismacolor:
                output += "PRISMACOLOR PENCILS:\n"
                output += "-" * 20 + "\n"
                for pencil in prismacolor[:10]:  # Top 10
                    output += f"• {pencil['name']} ({pencil['code']}) - Match Quality: {self._get_quality_text(pencil['color_difference'])}\n"
                output += "\n"
            
            if faber_castell:
                output += "FABER CASTELL PENCILS:\n"
                output += "-" * 25 + "\n"
                for pencil in faber_castell[:10]:  # Top 10
                    output += f"• {pencil['name']} ({pencil['code']}) - Match Quality: {self._get_quality_text(pencil['color_difference'])}\n"
                output += "\n"
            
            return output
            
        elif format_type == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow(['Brand', 'Name', 'Code', 'Color Difference', 'Match Quality'])
            
            for pencil in sorted_pencils:
                writer.writerow([
                    pencil['brand'],
                    pencil['name'],
                    pencil['code'],
                    round(pencil['color_difference'], 2),
                    self._get_quality_text(pencil['color_difference'])
                ])
            
            return output.getvalue()
            
        else:  # json
            shopping_data = {
                'shopping_list': [],
                'total_pencils': len(sorted_pencils),
                'brands': list(set(p['brand'] for p in sorted_pencils))
            }
            
            for pencil in sorted_pencils:
                shopping_data['shopping_list'].append({
                    'brand': pencil['brand'],
                    'name': pencil['name'],
                    'code': pencil['code'],
                    'color_difference': round(pencil['color_difference'], 2),
                    'match_quality': self._get_quality_text(pencil['color_difference']),
                    'rgb': pencil['pencil_rgb']
                })
            
            return json.dumps(shopping_data, indent=2)
    def _sanitize_json_types(self, obj):
        """Recursively convert NumPy types to native Python types for JSON serialization"""
        import numpy as np

        if isinstance(obj, dict):
            return {k: self._sanitize_json_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize_json_types(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(self._sanitize_json_types(i) for i in obj)
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj        
    
    def _get_quality_text(self, color_difference: float) -> str:
        """Convert color difference to quality text"""
        if color_difference < 3:
            return "Excellent"
        elif color_difference < 6:
            return "Very Good"
        elif color_difference < 12:
            return "Good"
        elif color_difference < 25:
            return "Acceptable"
        else:
            return "Poor"