import numpy as np
from color_analyzer import ColorAnalyzer

class ColorMatcher:
    """Matches extracted colors to colored pencil collections"""
    
    def __init__(self, pencil_database):
        self.pencil_db = pencil_database
        self.color_analyzer = ColorAnalyzer()
    
    def find_matches(self, target_rgb, max_matches=5, max_difference=50):
        """
        Find the closest matching pencils for a given RGB color
        
        Args:
            target_rgb: Tuple of (R, G, B) values
            max_matches: Maximum number of matches to return per brand
            max_difference: Maximum color difference to consider a match
        
        Returns:
            List of dictionaries containing match information
        """
        all_pencils = self.pencil_db.get_all_pencils()
        matches = []
        
        for _, pencil in all_pencils.iterrows():
            pencil_rgb = pencil['rgb']
            
            # Calculate color difference
            color_diff = self.color_analyzer.calculate_color_difference(
                target_rgb, pencil_rgb
            )
            
            # Only consider matches within the difference threshold
            if color_diff <= max_difference:
                match_info = {
                    'brand': pencil['brand'],
                    'name': pencil['name'],
                    'code': pencil['code'],
                    'pencil_rgb': pencil_rgb,
                    'target_rgb': target_rgb,
                    'color_difference': color_diff
                }
                matches.append(match_info)
        
        # Sort by color difference (closest first)
        matches.sort(key=lambda x: x['color_difference'])
        
        # Limit matches per brand
        prismacolor_matches = [m for m in matches if m['brand'] == 'Prismacolor'][:max_matches]
        faber_castell_matches = [m for m in matches if m['brand'] == 'Faber Castell'][:max_matches]
        
        return prismacolor_matches + faber_castell_matches
    
    def find_best_match(self, target_rgb, brand=None):
        """
        Find the single best matching pencil for a color
        
        Args:
            target_rgb: Tuple of (R, G, B) values
            brand: Optional brand filter ('Prismacolor' or 'Faber Castell')
        
        Returns:
            Dictionary containing the best match information
        """
        if brand:
            if brand == 'Prismacolor':
                pencils = self.pencil_db.get_prismacolor_pencils()
            elif brand == 'Faber Castell':
                pencils = self.pencil_db.get_faber_castell_pencils()
            else:
                pencils = self.pencil_db.get_all_pencils()
        else:
            pencils = self.pencil_db.get_all_pencils()
        
        best_match = None
        min_difference = float('inf')
        
        for _, pencil in pencils.iterrows():
            pencil_rgb = pencil['rgb']
            color_diff = self.color_analyzer.calculate_color_difference(
                target_rgb, pencil_rgb
            )
            
            if color_diff < min_difference:
                min_difference = color_diff
                brand_name = pencil.get('brand', brand if brand else 'Unknown')
                best_match = {
                    'brand': brand_name,
                    'name': pencil['name'],
                    'code': pencil['code'],
                    'pencil_rgb': pencil_rgb,
                    'target_rgb': target_rgb,
                    'color_difference': color_diff
                }
        
        return best_match
    
    def get_color_palette_matches(self, color_palette, max_matches_per_color=3):
        """
        Find matches for an entire color palette
        
        Args:
            color_palette: List of RGB tuples
            max_matches_per_color: Maximum matches to find per color
        
        Returns:
            Dictionary with color index as key and matches as values
        """
        palette_matches = {}
        
        for i, color_rgb in enumerate(color_palette):
            matches = self.find_matches(
                color_rgb, 
                max_matches=max_matches_per_color
            )
            palette_matches[i] = matches
        
        return palette_matches
    
    def calculate_match_quality(self, color_difference):
        """
        Categorize match quality based on color difference
        
        Args:
            color_difference: Delta E color difference value
        
        Returns:
            String describing match quality
        """
        if color_difference < 3:
            return "Excellent match"
        elif color_difference < 6:
            return "Very good match"
        elif color_difference < 12:
            return "Good match"
        elif color_difference < 25:
            return "Acceptable match"
        else:
            return "Poor match"
    
    def get_complementary_colors(self, target_rgb):
        """
        Find pencils that would work well as complementary colors
        
        Args:
            target_rgb: Tuple of (R, G, B) values
        
        Returns:
            List of complementary color matches
        """
        # Calculate complementary color (opposite on color wheel)
        r, g, b = target_rgb
        
        # Convert to HSV, rotate hue by 180 degrees, convert back
        import colorsys
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        comp_h = (h + 0.5) % 1.0  # Add 180 degrees (0.5 in normalized space)
        comp_r, comp_g, comp_b = colorsys.hsv_to_rgb(comp_h, s, v)
        
        complementary_rgb = (
            int(comp_r * 255), 
            int(comp_g * 255), 
            int(comp_b * 255)
        )
        
        # Find matches for the complementary color
        return self.find_matches(complementary_rgb, max_matches=3)
