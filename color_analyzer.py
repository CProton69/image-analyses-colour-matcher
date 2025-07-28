import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

class ColorAnalyzer:
    """Analyzes images to extract dominant colors using K-means clustering"""
    
    def __init__(self):
        pass
    
    def extract_dominant_colors(self, image, num_colors=8, max_size=300):
        """
        Extract dominant colors from an image using K-means clustering
        
        Args:
            image: PIL Image object
            num_colors: Number of dominant colors to extract
            max_size: Maximum dimension to resize image to for faster processing
        
        Returns:
            List of dictionaries containing color information
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image for faster processing
            original_size = image.size
            if max(original_size) > max_size:
                ratio = max_size / max(original_size)
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
                try:
                    # Use LANCZOS for newer Pillow versions, fallback to BICUBIC for older versions
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                except AttributeError:
                    # Fallback for older Pillow versions
                    try:
                        from PIL.Image import Resampling
                        image = image.resize(new_size, Resampling.LANCZOS)
                    except (AttributeError, ImportError):
                        image = image.resize(new_size)
            
            # Convert image to numpy array
            img_array = np.array(image)
            
            # Reshape to list of pixels
            pixels = img_array.reshape(-1, 3)
            
            # Remove very dark and very light pixels (optional preprocessing)
            # This helps focus on meaningful colors
            brightness = np.mean(pixels, axis=1)
            mask = (brightness > 20) & (brightness < 235)
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) < num_colors:
                # If too few pixels after filtering, use all pixels
                filtered_pixels = pixels
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init='auto')
            kmeans.fit(filtered_pixels)
            
            # Get cluster centers (dominant colors)
            colors = kmeans.cluster_centers_.astype(int)
            
            # For location analysis, we need to predict labels for ALL pixels
            all_labels = kmeans.predict(pixels)
            
            # Calculate the percentage of each color using filtered pixels
            filtered_labels = kmeans.labels_
            total_pixels = len(filtered_labels) if filtered_labels is not None else 0
            
            color_info = []
            for i, color in enumerate(colors):
                # Count pixels in this cluster (from filtered pixels for percentage)
                count = np.sum(filtered_labels == i)
                percentage = (count / total_pixels) * 100
                
                # Convert to hex
                hex_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                
                # Calculate additional color properties
                hsv = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
                
                # Analyze where this color appears in the image using all pixels
                location_info = self._analyze_color_location(img_array, all_labels, i, color)
                
                color_info.append({
                    'rgb': tuple(color),
                    'hex': hex_color,
                    'percentage': percentage,
                    'hsv': hsv,
                    'brightness': np.mean(color),
                    'location_info': location_info
                })
            
            # Sort by percentage (most dominant first)
            color_info.sort(key=lambda x: x['percentage'], reverse=True)
            
            return color_info
            
        except Exception as e:
            print(f"Error in color extraction: {str(e)}")
            return []
    
    def rgb_to_lab(self, rgb):
        """
        Convert RGB to LAB color space for better color distance calculations
        """
        # Normalize RGB values
        rgb = np.array(rgb) / 255.0
        
        # Apply gamma correction
        rgb = np.where(rgb > 0.04045, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
        
        # Convert to XYZ
        xyz_matrix = np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041]
        ])
        
        xyz = np.dot(xyz_matrix, rgb)
        
        # Normalize by D65 illuminant
        xyz = xyz / np.array([0.95047, 1.00000, 1.08883])
        
        # Convert to LAB
        xyz = np.where(xyz > 0.008856, xyz ** (1/3), (7.787 * xyz + 16/116))
        
        lab = np.array([
            116 * xyz[1] - 16,
            500 * (xyz[0] - xyz[1]),
            200 * (xyz[1] - xyz[2])
        ])
        
        return lab
    
    def calculate_color_difference(self, color1_rgb, color2_rgb):
        """
        Calculate Delta E (CIE76) color difference between two RGB colors
        """
        try:
            lab1 = self.rgb_to_lab(color1_rgb)
            lab2 = self.rgb_to_lab(color2_rgb)
            
            # Calculate Delta E (CIE76)
            delta_e = np.sqrt(np.sum((lab1 - lab2) ** 2))
            
            return delta_e
        except Exception:
            # Fallback to simple Euclidean distance in RGB space
            return np.sqrt(np.sum((np.array(color1_rgb) - np.array(color2_rgb)) ** 2))
    
    def _analyze_color_location(self, img_array, labels, cluster_id, color):
        """
        Analyze where a specific color cluster appears in the image
        
        Args:
            img_array: Image as numpy array
            labels: K-means cluster labels for each pixel
            cluster_id: ID of the cluster to analyze
            color: RGB color of the cluster
            
        Returns:
            Dictionary with location information
        """
        try:
            height, width = img_array.shape[:2]
            
            # Reshape labels to match image dimensions
            label_image = labels.reshape(height, width)
            
            # Find all pixels belonging to this color cluster
            cluster_mask = (label_image == cluster_id)
            
            if not np.any(cluster_mask):
                return {
                    'regions': ['Not found'],
                    'distribution': 'scattered',
                    'primary_areas': [],
                    'coverage': {'top': 0, 'middle': 0, 'bottom': 0, 'left': 0, 'center': 0, 'right': 0}
                }
            
            # Get coordinates of pixels with this color
            y_coords, x_coords = np.where(cluster_mask)
            
            # Analyze distribution
            distribution = self._classify_distribution(y_coords, x_coords, height, width)
            
            # Analyze coverage by regions
            coverage = self._analyze_regional_coverage(y_coords, x_coords, height, width)
            
            # Find primary areas where this color appears
            primary_areas = self._find_primary_areas(coverage)
            
            # Create descriptive regions
            regions = self._describe_regions(coverage, primary_areas)
            
            return {
                'regions': regions,
                'distribution': distribution,
                'primary_areas': primary_areas,
                'coverage': coverage
            }
            
        except Exception as e:
            return {
                'regions': ['Analysis unavailable'],
                'distribution': 'unknown',
                'primary_areas': [],
                'coverage': {'top': 0, 'middle': 0, 'bottom': 0, 'left': 0, 'center': 0, 'right': 0}
            }
    
    def _classify_distribution(self, y_coords, x_coords, height, width):
        """Classify how the color is distributed across the image"""
        if len(y_coords) == 0:
            return 'none'
        
        # Calculate spread
        y_spread = (np.max(y_coords) - np.min(y_coords)) / height
        x_spread = (np.max(x_coords) - np.min(x_coords)) / width
        
        # Calculate concentration
        y_std = np.std(y_coords) / height
        x_std = np.std(x_coords) / width
        
        if y_spread > 0.7 and x_spread > 0.7:
            return 'widespread'
        elif y_std < 0.15 and x_std < 0.15:
            return 'concentrated'
        elif y_spread < 0.3 or x_spread < 0.3:
            return 'localized'
        else:
            return 'scattered'
    
    def _analyze_regional_coverage(self, y_coords, x_coords, height, width):
        """Analyze coverage in different regions of the image"""
        coverage = {
            'top': 0, 'middle': 0, 'bottom': 0,
            'left': 0, 'center': 0, 'right': 0
        }
        
        if len(y_coords) == 0:
            return coverage
        
        total_pixels = len(y_coords)
        
        # Vertical regions
        top_mask = y_coords < height / 3
        middle_mask = (y_coords >= height / 3) & (y_coords < 2 * height / 3)
        bottom_mask = y_coords >= 2 * height / 3
        
        coverage['top'] = np.sum(top_mask) / total_pixels * 100
        coverage['middle'] = np.sum(middle_mask) / total_pixels * 100
        coverage['bottom'] = np.sum(bottom_mask) / total_pixels * 100
        
        # Horizontal regions
        left_mask = x_coords < width / 3
        center_mask = (x_coords >= width / 3) & (x_coords < 2 * width / 3)
        right_mask = x_coords >= 2 * width / 3
        
        coverage['left'] = np.sum(left_mask) / total_pixels * 100
        coverage['center'] = np.sum(center_mask) / total_pixels * 100
        coverage['right'] = np.sum(right_mask) / total_pixels * 100
        
        return coverage
    
    def _find_primary_areas(self, coverage):
        """Find the primary areas where the color appears (threshold > 20%)"""
        primary = []
        
        # Vertical areas
        if coverage['top'] > 20:
            primary.append('top')
        if coverage['middle'] > 20:
            primary.append('middle')
        if coverage['bottom'] > 20:
            primary.append('bottom')
        
        # Horizontal areas (only if not already covered by vertical)
        if len(primary) == 0:
            if coverage['left'] > 20:
                primary.append('left')
            if coverage['center'] > 20:
                primary.append('center')
            if coverage['right'] > 20:
                primary.append('right')
        
        return primary if primary else ['scattered']
    
    def _describe_regions(self, coverage, primary_areas):
        """Create human-readable descriptions of where colors appear"""
        if not primary_areas or primary_areas == ['scattered']:
            return ['Throughout the image']
        
        regions = []
        
        # Map areas to descriptions
        area_descriptions = {
            'top': 'Upper portion',
            'middle': 'Middle section', 
            'bottom': 'Lower portion',
            'left': 'Left side',
            'center': 'Center area',
            'right': 'Right side'
        }
        
        for area in primary_areas:
            if area in area_descriptions:
                regions.append(area_descriptions[area])
        
        # Add specific combinations
        if 'top' in primary_areas and 'bottom' in primary_areas:
            if 'Top and bottom edges' not in regions:
                regions = ['Top and bottom edges']
        elif 'left' in primary_areas and 'right' in primary_areas:
            if 'Left and right sides' not in regions:
                regions = ['Left and right sides']
        
        return regions if regions else ['Various areas']
