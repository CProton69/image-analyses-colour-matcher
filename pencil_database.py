import pandas as pd

class PencilDatabase:
    """Database of Prismacolor and Faber Castell colored pencil colors"""
    
    def __init__(self):
        self.prismacolor_pencils = self._create_prismacolor_database()
        self.faber_castell_pencils = self._create_faber_castell_database()
        self.caran_dache_pencils = self._create_caran_dache_database()
        self.derwent_pencils = self._create_derwent_database()
        self.staedtler_pencils = self._create_staedtler_database()
        self.koh_i_noor_pencils = self._create_koh_i_noor_database()
        
    def _get_purchase_urls(self):
        """Get purchase URLs for different brands and retailers by country"""
        return {
            'UK': {
                'prismacolor': {
                    'Amazon UK': 'https://www.amazon.co.uk/s?k=prismacolor+colored+pencils',
                    'Hobbycraft': 'https://www.hobbycraft.co.uk/search?q=prismacolor+pencils',
                    'The Works': 'https://www.theworks.co.uk/search?q=prismacolor',
                    'Currys PC World': 'https://www.currys.co.uk/search?q=prismacolor'
                },
                'faber_castell': {
                    'Amazon UK': 'https://www.amazon.co.uk/s?k=faber+castell+polychromos',
                    'Jackson\'s Art': 'https://www.jacksonsart.com/en-gb/faber-castell-polychromos-pencils',
                    'Hobbycraft': 'https://www.hobbycraft.co.uk/search?q=faber+castell+polychromos',
                    'WHSmith': 'https://www.whsmith.co.uk/search?q=faber+castell'
                }
            },
            'US': {
                'prismacolor': {
                    'Amazon US': 'https://www.amazon.com/s?k=prismacolor+colored+pencils',
                    'Blick Art Materials': 'https://www.dickblick.com/products/prismacolor-premier-colored-pencils/',
                    'Michaels': 'https://www.michaels.com/search?q=prismacolor%20colored%20pencils',
                    'Jerry\'s Artarama': 'https://www.jerrysartarama.com/prismacolor-colored-pencils'
                },
                'faber_castell': {
                    'Amazon US': 'https://www.amazon.com/s?k=faber+castell+polychromos+colored+pencils',
                    'Blick Art Materials': 'https://www.dickblick.com/products/faber-castell-polychromos-artists-colored-pencils/',
                    'Michaels': 'https://www.michaels.com/search?q=faber%20castell%20colored%20pencils',
                    'Jerry\'s Artarama': 'https://www.jerrysartarama.com/faber-castell-polychromos-colored-pencils'
                }
            },
            'Canada': {
                'prismacolor': {
                    'Amazon Canada': 'https://www.amazon.ca/s?k=prismacolor+colored+pencils',
                    'Curry\'s Art Store': 'https://www.currys.com/catalogsearch/result/?q=prismacolor',
                    'Michaels Canada': 'https://michaels.com/search?q=prismacolor',
                    'DeSerres': 'https://www.deserres.ca/en/search/?q=prismacolor'
                },
                'faber_castell': {
                    'Amazon Canada': 'https://www.amazon.ca/s?k=faber+castell+polychromos',
                    'Curry\'s Art Store': 'https://www.currys.com/catalogsearch/result/?q=faber+castell',
                    'Michaels Canada': 'https://michaels.com/search?q=faber+castell',
                    'DeSerres': 'https://www.deserres.ca/en/search/?q=faber+castell'
                }
            },
            'Australia': {
                'prismacolor': {
                    'Amazon Australia': 'https://www.amazon.com.au/s?k=prismacolor+colored+pencils',
                    'Officeworks': 'https://www.officeworks.com.au/shop/search?q=prismacolor&searchTerm=prismacolor',
                    'Art Materials Australia': 'https://www.artmaterialsaustralia.com.au/search?q=prismacolor',
                    'Riot Art & Craft': 'https://www.riotart.com.au/search?q=prismacolor'
                },
                'faber_castell': {
                    'Amazon Australia': 'https://www.amazon.com.au/s?k=faber+castell+polychromos',
                    'Officeworks': 'https://www.officeworks.com.au/shop/search?q=faber+castell&searchTerm=faber+castell',
                    'Art Materials Australia': 'https://www.artmaterialsaustralia.com.au/search?q=faber+castell',
                    'Riot Art & Craft': 'https://www.riotart.com.au/search?q=faber+castell'
                }
            },
            'Germany': {
                'prismacolor': {
                    'Amazon Germany': 'https://www.amazon.de/s?k=prismacolor+buntstifte',
                    'Idee Creativmarkt': 'https://www.idee-shop.com/search?q=prismacolor',
                    'Boesner': 'https://www.boesner.com/search?q=prismacolor',
                    'Gerstaecker': 'https://www.gerstaecker.de/search?q=prismacolor'
                },
                'faber_castell': {
                    'Amazon Germany': 'https://www.amazon.de/s?k=faber+castell+polychromos',
                    'Faber-Castell Official': 'https://www.faber-castell.de/produkte/kunst-grafik/buntstifte/polychromos',
                    'Boesner': 'https://www.boesner.com/search?q=faber+castell+polychromos',
                    'Gerstaecker': 'https://www.gerstaecker.de/search?q=faber+castell+polychromos'
                }
            }
        }
    
    def _create_prismacolor_database(self):
        """Create comprehensive Prismacolor pencil database"""
        pencils = [
            # Reds
            {"name": "Crimson Red", "code": "PC924", "rgb": (220, 20, 60)},
            {"name": "Scarlet Lake", "code": "PC923", "rgb": (255, 36, 0)},
            {"name": "True Red", "code": "PC922", "rgb": (237, 28, 36)},
            {"name": "Magenta", "code": "PC930", "rgb": (255, 0, 255)},
            {"name": "Hot Pink", "code": "PC993", "rgb": (255, 105, 180)},
            {"name": "Process Red", "code": "PC994", "rgb": (237, 28, 36)},
            {"name": "Mulberry", "code": "PC995", "rgb": (197, 75, 140)},
            {"name": "Raspberry", "code": "PC1030", "rgb": (227, 11, 92)},
            {"name": "Pink Rose", "code": "PC1016", "rgb": (255, 182, 193)},
            {"name": "Blush Pink", "code": "PC928", "rgb": (255, 192, 203)},
            
            # Oranges
            {"name": "Orange", "code": "PC918", "rgb": (255, 165, 0)},
            {"name": "Poppy Red", "code": "PC922", "rgb": (255, 99, 71)},
            {"name": "Pale Vermillion", "code": "PC921", "rgb": (255, 160, 122)},
            {"name": "Peach", "code": "PC939", "rgb": (255, 218, 185)},
            {"name": "Apricot", "code": "PC1003", "rgb": (251, 206, 177)},
            {"name": "Light Peach", "code": "PC927", "rgb": (255, 239, 213)},
            
            # Yellows
            {"name": "Canary Yellow", "code": "PC916", "rgb": (255, 255, 153)},
            {"name": "Lemon Yellow", "code": "PC915", "rgb": (255, 255, 0)},
            {"name": "Yellow Ochre", "code": "PC942", "rgb": (238, 203, 173)},
            {"name": "Goldenrod", "code": "PC1034", "rgb": (218, 165, 32)},
            {"name": "Cream", "code": "PC914", "rgb": (255, 253, 208)},
            {"name": "Pale Yellow", "code": "PC1011", "rgb": (255, 255, 224)},
            
            # Greens
            {"name": "True Green", "code": "PC910", "rgb": (50, 205, 50)},
            {"name": "Grass Green", "code": "PC909", "rgb": (124, 252, 0)},
            {"name": "Kelly Green", "code": "PC908", "rgb": (76, 187, 23)},
            {"name": "Forest Green", "code": "PC946", "rgb": (34, 139, 34)},
            {"name": "Olive Green", "code": "PC911", "rgb": (128, 128, 0)},
            {"name": "Jade Green", "code": "PC1021", "rgb": (0, 168, 107)},
            {"name": "Apple Green", "code": "PC912", "rgb": (141, 182, 0)},
            {"name": "Limepeel", "code": "PC1005", "rgb": (191, 255, 0)},
            {"name": "Spring Green", "code": "PC913", "rgb": (0, 255, 127)},
            
            # Blues
            {"name": "True Blue", "code": "PC903", "rgb": (0, 123, 191)},
            {"name": "Ultramarine", "code": "PC902", "rgb": (65, 105, 225)},
            {"name": "Cerulean Blue", "code": "PC901", "rgb": (0, 123, 167)},
            {"name": "Sky Blue Light", "code": "PC904", "rgb": (135, 206, 235)},
            {"name": "Light Blue", "code": "PC906", "rgb": (173, 216, 230)},
            {"name": "Powder Blue", "code": "PC1087", "rgb": (176, 224, 230)},
            {"name": "Periwinkle", "code": "PC1025", "rgb": (204, 204, 255)},
            {"name": "Non-Photo Blue", "code": "PC919", "rgb": (164, 221, 237)},
            
            # Purples
            {"name": "Violet", "code": "PC932", "rgb": (138, 43, 226)},
            {"name": "Purple", "code": "PC931", "rgb": (128, 0, 128)},
            {"name": "Lavender", "code": "PC934", "rgb": (230, 230, 250)},
            {"name": "Lilac", "code": "PC956", "rgb": (200, 162, 200)},
            {"name": "Orchid", "code": "PC1009", "rgb": (218, 112, 214)},
            {"name": "Plum", "code": "PC1026", "rgb": (221, 160, 221)},
            
            # Browns
            {"name": "Dark Brown", "code": "PC947", "rgb": (101, 67, 33)},
            {"name": "Light Brown", "code": "PC1001", "rgb": (205, 133, 63)},
            {"name": "Burnt Ochre", "code": "PC943", "rgb": (204, 119, 34)},
            {"name": "Raw Sienna", "code": "PC945", "rgb": (160, 82, 45)},
            {"name": "Burnt Sienna", "code": "PC948", "rgb": (138, 54, 15)},
            {"name": "Van Dyke Brown", "code": "PC949", "rgb": (94, 38, 18)},
            {"name": "Sepia", "code": "PC948", "rgb": (112, 66, 20)},
            {"name": "Tan", "code": "PC942", "rgb": (210, 180, 140)},
            
            # Grays and Blacks
            {"name": "Black", "code": "PC935", "rgb": (0, 0, 0)},
            {"name": "Cool Grey 90%", "code": "PC1063", "rgb": (51, 51, 51)},
            {"name": "Cool Grey 70%", "code": "PC1061", "rgb": (102, 102, 102)},
            {"name": "Cool Grey 50%", "code": "PC1059", "rgb": (153, 153, 153)},
            {"name": "Cool Grey 30%", "code": "PC1057", "rgb": (179, 179, 179)},
            {"name": "Cool Grey 10%", "code": "PC1055", "rgb": (230, 230, 230)},
            {"name": "Warm Grey 90%", "code": "PC1070", "rgb": (68, 63, 58)},
            {"name": "Warm Grey 70%", "code": "PC1068", "rgb": (128, 120, 111)},
            {"name": "Warm Grey 50%", "code": "PC1066", "rgb": (153, 146, 138)},
            {"name": "White", "code": "PC938", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def _create_faber_castell_database(self):
        """Create comprehensive Faber Castell pencil database"""
        pencils = [
            # Reds
            {"name": "Alizarin Crimson", "code": "FC226", "rgb": (227, 38, 54)},
            {"name": "Deep Red", "code": "FC223", "rgb": (196, 30, 58)},
            {"name": "Middle Cadmium Red", "code": "FC217", "rgb": (231, 65, 69)},
            {"name": "Pale Geranium Lake", "code": "FC121", "rgb": (239, 100, 108)},
            {"name": "Pink Carmine", "code": "FC127", "rgb": (221, 101, 134)},
            {"name": "Pink Madder Lake", "code": "FC129", "rgb": (221, 108, 158)},
            {"name": "Rose Carmine", "code": "FC126", "rgb": (217, 87, 125)},
            {"name": "Magenta", "code": "FC133", "rgb": (202, 52, 120)},
            
            # Oranges
            {"name": "Orange Glaze", "code": "FC113", "rgb": (237, 118, 66)},
            {"name": "Cadmium Orange", "code": "FC115", "rgb": (245, 128, 37)},
            {"name": "Dark Cadmium Orange", "code": "FC118", "rgb": (218, 102, 46)},
            {"name": "Burnt Orange", "code": "FC117", "rgb": (191, 91, 44)},
            {"name": "Light Orange", "code": "FC109", "rgb": (252, 177, 102)},
            {"name": "Peach", "code": "FC132", "rgb": (245, 189, 156)},
            
            # Yellows
            {"name": "Cadmium Yellow", "code": "FC107", "rgb": (254, 221, 45)},
            {"name": "Light Cadmium Yellow", "code": "FC105", "rgb": (254, 242, 97)},
            {"name": "Dark Cadmium Yellow", "code": "FC108", "rgb": (250, 200, 45)},
            {"name": "Naples Ochre", "code": "FC131", "rgb": (241, 194, 125)},
            {"name": "Raw Ochre", "code": "FC179", "rgb": (206, 160, 102)},
            {"name": "Chrome Yellow", "code": "FC100", "rgb": (255, 231, 79)},
            
            # Greens
            {"name": "Sap Green", "code": "FC170", "rgb": (102, 140, 55)},
            {"name": "Permanent Green", "code": "FC166", "rgb": (76, 136, 74)},
            {"name": "Permanent Green Olive", "code": "FC167", "rgb": (124, 144, 70)},
            {"name": "Chrome Oxide Green", "code": "FC176", "rgb": (102, 128, 83)},
            {"name": "Hookers Green", "code": "FC159", "rgb": (50, 102, 74)},
            {"name": "Viridian", "code": "FC156", "rgb": (64, 130, 109)},
            {"name": "May Green", "code": "FC171", "rgb": (145, 189, 135)},
            {"name": "Leaf Green", "code": "FC112", "rgb": (119, 176, 71)},
            {"name": "Grass Green", "code": "FC166", "rgb": (108, 171, 98)},
            
            # Blues
            {"name": "Ultramarine", "code": "FC120", "rgb": (63, 105, 170)},
            {"name": "Prussian Blue", "code": "FC246", "rgb": (45, 82, 129)},
            {"name": "Phthalo Blue", "code": "FC110", "rgb": (43, 108, 166)},
            {"name": "Sky Blue", "code": "FC146", "rgb": (125, 178, 219)},
            {"name": "Light Blue", "code": "FC140", "rgb": (149, 194, 222)},
            {"name": "Cobalt Blue", "code": "FC143", "rgb": (83, 141, 195)},
            {"name": "Delft Blue", "code": "FC141", "rgb": (97, 156, 204)},
            
            # Purples
            {"name": "Red Violet", "code": "FC194", "rgb": (154, 71, 131)},
            {"name": "Blue Violet", "code": "FC137", "rgb": (121, 104, 172)},
            {"name": "Manganese Violet", "code": "FC160", "rgb": (145, 95, 150)},
            {"name": "Mauve", "code": "FC249", "rgb": (168, 132, 172)},
            {"name": "Light Magenta", "code": "FC119", "rgb": (216, 108, 174)},
            
            # Browns
            {"name": "Burnt Sienna", "code": "FC283", "rgb": (158, 79, 49)},
            {"name": "Raw Umber", "code": "FC280", "rgb": (130, 102, 68)},
            {"name": "Burnt Umber", "code": "FC280", "rgb": (123, 63, 44)},
            {"name": "Van Dyke Brown", "code": "FC176", "rgb": (102, 51, 43)},
            {"name": "Sepia", "code": "FC175", "rgb": (115, 74, 48)},
            {"name": "Caput Mortuum Violet", "code": "FC263", "rgb": (127, 70, 65)},
            {"name": "Light Ochre", "code": "FC177", "rgb": (204, 153, 102)},
            
            # Grays and Blacks
            {"name": "Black", "code": "FC199", "rgb": (0, 0, 0)},
            {"name": "Payne's Grey", "code": "FC181", "rgb": (77, 93, 108)},
            {"name": "Neutral Tint", "code": "FC235", "rgb": (102, 102, 102)},
            {"name": "Warm Grey I", "code": "FC270", "rgb": (204, 194, 179)},
            {"name": "Warm Grey II", "code": "FC271", "rgb": (179, 166, 149)},
            {"name": "Warm Grey III", "code": "FC272", "rgb": (153, 138, 119)},
            {"name": "Warm Grey IV", "code": "FC273", "rgb": (128, 111, 93)},
            {"name": "Cold Grey I", "code": "FC230", "rgb": (204, 204, 204)},
            {"name": "Cold Grey II", "code": "FC231", "rgb": (179, 179, 179)},
            {"name": "Cold Grey III", "code": "FC232", "rgb": (153, 153, 153)},
            {"name": "Cold Grey IV", "code": "FC233", "rgb": (128, 128, 128)},
            {"name": "White", "code": "FC101", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def _create_caran_dache_database(self):
        """Create comprehensive Caran d'Ache pencil database"""
        pencils = [
            # Reds
            {"name": "Scarlet", "code": "070", "rgb": (237, 28, 36)},
            {"name": "Vermillion", "code": "060", "rgb": (227, 66, 52)},
            {"name": "Light Cadmium Red", "code": "061", "rgb": (255, 99, 71)},
            {"name": "Permanent Red", "code": "065", "rgb": (220, 20, 60)},
            {"name": "Carmine", "code": "080", "rgb": (150, 0, 24)},
            {"name": "Bordeaux Red", "code": "075", "rgb": (111, 30, 43)},
            {"name": "Anthraquinoid Pink", "code": "081", "rgb": (255, 105, 180)},
            {"name": "Rose Pink", "code": "481", "rgb": (255, 182, 193)},
            
            # Oranges
            {"name": "Orange", "code": "030", "rgb": (255, 165, 0)},
            {"name": "Apricot", "code": "041", "rgb": (251, 206, 177)},
            {"name": "Flesh", "code": "040", "rgb": (255, 218, 185)},
            {"name": "Light Flesh", "code": "042", "rgb": (255, 239, 213)},
            {"name": "Burnt Orange", "code": "051", "rgb": (204, 85, 0)},
            
            # Yellows
            {"name": "Lemon Yellow", "code": "240", "rgb": (255, 255, 0)},
            {"name": "Cadmium Yellow", "code": "010", "rgb": (255, 237, 0)},
            {"name": "Middle Cadmium Yellow", "code": "020", "rgb": (255, 215, 0)},
            {"name": "Golden Yellow", "code": "021", "rgb": (255, 193, 7)},
            {"name": "Yellow Ochre", "code": "025", "rgb": (238, 203, 173)},
            {"name": "Raw Sienna", "code": "036", "rgb": (160, 82, 45)},
            
            # Greens
            {"name": "Light Green", "code": "470", "rgb": (144, 238, 144)},
            {"name": "Grass Green", "code": "461", "rgb": (124, 252, 0)},
            {"name": "Green", "code": "210", "rgb": (0, 128, 0)},
            {"name": "Emerald Green", "code": "200", "rgb": (80, 200, 120)},
            {"name": "Veronese Green", "code": "201", "rgb": (0, 179, 152)},
            {"name": "Bluish Green", "code": "202", "rgb": (0, 150, 136)},
            {"name": "Forest Green", "code": "229", "rgb": (34, 139, 34)},
            {"name": "Olive Green", "code": "019", "rgb": (128, 128, 0)},
            
            # Blues
            {"name": "Light Blue", "code": "161", "rgb": (173, 216, 230)},
            {"name": "Sky Blue", "code": "171", "rgb": (135, 206, 235)},
            {"name": "Cobalt Blue", "code": "140", "rgb": (0, 71, 171)},
            {"name": "Ultramarine", "code": "120", "rgb": (65, 105, 225)},
            {"name": "Prussian Blue", "code": "159", "rgb": (0, 49, 83)},
            {"name": "Night Blue", "code": "155", "rgb": (25, 25, 112)},
            {"name": "Periwinkle Blue", "code": "141", "rgb": (204, 204, 255)},
            
            # Purples
            {"name": "Violet", "code": "100", "rgb": (138, 43, 226)},
            {"name": "Purple", "code": "110", "rgb": (128, 0, 128)},
            {"name": "Magenta", "code": "090", "rgb": (255, 0, 255)},
            {"name": "Light Magenta", "code": "191", "rgb": (255, 119, 255)},
            {"name": "Lilac", "code": "192", "rgb": (200, 162, 200)},
            
            # Browns
            {"name": "Burnt Sienna", "code": "037", "rgb": (138, 54, 15)},
            {"name": "Van Dyke Brown", "code": "076", "rgb": (94, 38, 18)},
            {"name": "Burnt Umber", "code": "049", "rgb": (138, 51, 36)},
            {"name": "Raw Umber", "code": "048", "rgb": (115, 74, 18)},
            {"name": "Sepia", "code": "407", "rgb": (112, 66, 20)},
            {"name": "Brown Ochre", "code": "035", "rgb": (150, 113, 23)},
            
            # Grays and Blacks
            {"name": "Black", "code": "009", "rgb": (0, 0, 0)},
            {"name": "Payne's Grey", "code": "508", "rgb": (83, 104, 120)},
            {"name": "Neutral Tint", "code": "007", "rgb": (102, 102, 102)},
            {"name": "French Grey 10%", "code": "002", "rgb": (230, 230, 230)},
            {"name": "French Grey 30%", "code": "003", "rgb": (179, 179, 179)},
            {"name": "French Grey 50%", "code": "004", "rgb": (128, 128, 128)},
            {"name": "French Grey 70%", "code": "005", "rgb": (77, 77, 77)},
            {"name": "White", "code": "001", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def _create_derwent_database(self):
        """Create comprehensive Derwent pencil database"""
        pencils = [
            # Reds
            {"name": "Crimson Lake", "code": "20", "rgb": (220, 20, 60)},
            {"name": "Deep Cadmium", "code": "15", "rgb": (227, 38, 54)},
            {"name": "Geranium Lake", "code": "17", "rgb": (231, 84, 128)},
            {"name": "Rose Pink", "code": "23", "rgb": (255, 182, 193)},
            {"name": "Flesh Pink", "code": "24", "rgb": (255, 218, 185)},
            {"name": "Magenta", "code": "28", "rgb": (255, 0, 255)},
            {"name": "Imperial Purple", "code": "26", "rgb": (102, 2, 60)},
            
            # Oranges
            {"name": "Spectrum Orange", "code": "11", "rgb": (255, 165, 0)},
            {"name": "Deep Chrome", "code": "12", "rgb": (255, 140, 0)},
            {"name": "Middle Chrome", "code": "13", "rgb": (255, 185, 15)},
            {"name": "Orange Chrome", "code": "14", "rgb": (255, 117, 24)},
            {"name": "Flesh", "code": "132", "rgb": (255, 203, 164)},
            
            # Yellows
            {"name": "Lemon Cadmium", "code": "01", "rgb": (255, 255, 0)},
            {"name": "Deep Cadmium", "code": "04", "rgb": (255, 215, 0)},
            {"name": "Naples Yellow", "code": "16", "rgb": (250, 218, 94)},
            {"name": "Straw Yellow", "code": "02", "rgb": (227, 207, 87)},
            {"name": "Gold", "code": "22", "rgb": (255, 215, 0)},
            {"name": "Raw Sienna", "code": "58", "rgb": (160, 82, 45)},
            
            # Greens
            {"name": "May Green", "code": "42", "rgb": (145, 189, 135)},
            {"name": "Grass Green", "code": "51", "rgb": (124, 252, 0)},
            {"name": "Sap Green", "code": "49", "rgb": (48, 128, 20)},
            {"name": "Cedar Green", "code": "50", "rgb": (72, 120, 88)},
            {"name": "Olive Green", "code": "52", "rgb": (128, 128, 0)},
            {"name": "Bottle Green", "code": "44", "rgb": (0, 106, 78)},
            {"name": "Emerald Green", "code": "46", "rgb": (80, 200, 120)},
            {"name": "Viridian", "code": "47", "rgb": (64, 130, 109)},
            
            # Blues
            {"name": "Sky Blue", "code": "33", "rgb": (135, 206, 235)},
            {"name": "Smalt Blue", "code": "35", "rgb": (0, 123, 167)},
            {"name": "Ultramarine", "code": "32", "rgb": (65, 105, 225)},
            {"name": "Prussian Blue", "code": "36", "rgb": (0, 49, 83)},
            {"name": "Indigo", "code": "38", "rgb": (75, 0, 130)},
            {"name": "Delft Blue", "code": "37", "rgb": (97, 156, 204)},
            {"name": "Kingfisher Blue", "code": "31", "rgb": (0, 139, 208)},
            
            # Purples
            {"name": "Blue Violet Lake", "code": "27", "rgb": (138, 43, 226)},
            {"name": "Violet", "code": "29", "rgb": (148, 0, 211)},
            {"name": "Purple", "code": "25", "rgb": (128, 0, 128)},
            {"name": "Red Violet", "code": "21", "rgb": (199, 21, 133)},
            {"name": "Mauve", "code": "30", "rgb": (224, 176, 255)},
            
            # Browns
            {"name": "Burnt Sienna", "code": "61", "rgb": (158, 79, 49)},
            {"name": "Light Sienna", "code": "60", "rgb": (205, 133, 63)},
            {"name": "Burnt Umber", "code": "54", "rgb": (138, 51, 36)},
            {"name": "Raw Umber", "code": "55", "rgb": (115, 74, 18)},
            {"name": "Vandyke Brown", "code": "56", "rgb": (94, 38, 18)},
            {"name": "Chocolate", "code": "57", "rgb": (123, 63, 0)},
            {"name": "Copper Beech", "code": "62", "rgb": (141, 102, 57)},
            
            # Grays and Blacks
            {"name": "Ivory Black", "code": "67", "rgb": (0, 0, 0)},
            {"name": "Lamp Black", "code": "66", "rgb": (25, 25, 25)},
            {"name": "Gunmetal", "code": "68", "rgb": (77, 93, 108)},
            {"name": "French Grey", "code": "70", "rgb": (150, 150, 150)},
            {"name": "Silver Grey", "code": "71", "rgb": (192, 192, 192)},
            {"name": "Dove Grey", "code": "69", "rgb": (128, 128, 128)},
            {"name": "Chinese White", "code": "72", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def _create_staedtler_database(self):
        """Create Staedtler Ergosoft pencil database"""
        pencils = [
            # Reds
            {"name": "Carmine", "code": "29", "rgb": (227, 38, 54)},
            {"name": "Scarlet Red", "code": "28", "rgb": (237, 28, 36)},
            {"name": "Red", "code": "21", "rgb": (208, 2, 27)},
            {"name": "Pink", "code": "23", "rgb": (255, 182, 193)},
            {"name": "Magenta", "code": "25", "rgb": (255, 0, 255)},
            {"name": "Rose", "code": "26", "rgb": (255, 0, 127)},
            
            # Oranges
            {"name": "Orange", "code": "4", "rgb": (255, 165, 0)},
            {"name": "Light Orange", "code": "54", "rgb": (255, 200, 124)},
            {"name": "Peach", "code": "405", "rgb": (255, 218, 185)},
            
            # Yellows
            {"name": "Lemon Yellow", "code": "1", "rgb": (255, 255, 0)},
            {"name": "Yellow", "code": "12", "rgb": (255, 237, 0)},
            {"name": "Light Yellow", "code": "11", "rgb": (255, 255, 153)},
            {"name": "Yellow Orange", "code": "14", "rgb": (255, 185, 15)},
            {"name": "Yellow Ochre", "code": "17", "rgb": (238, 203, 173)},
            
            # Greens
            {"name": "Light Green", "code": "5", "rgb": (144, 238, 144)},
            {"name": "Green", "code": "53", "rgb": (0, 128, 0)},
            {"name": "Dark Green", "code": "57", "rgb": (0, 100, 0)},
            {"name": "Leaf Green", "code": "51", "rgb": (119, 176, 71)},
            {"name": "Pine Green", "code": "59", "rgb": (34, 139, 34)},
            
            # Blues
            {"name": "Light Blue", "code": "30", "rgb": (173, 216, 230)},
            {"name": "Sky Blue", "code": "31", "rgb": (135, 206, 235)},
            {"name": "Blue", "code": "3", "rgb": (0, 123, 191)},
            {"name": "Dark Blue", "code": "33", "rgb": (0, 0, 139)},
            {"name": "Ultramarine", "code": "37", "rgb": (65, 105, 225)},
            
            # Purples
            {"name": "Violet", "code": "6", "rgb": (138, 43, 226)},
            {"name": "Purple", "code": "62", "rgb": (128, 0, 128)},
            {"name": "Light Violet", "code": "61", "rgb": (221, 160, 221)},
            
            # Browns
            {"name": "Brown", "code": "76", "rgb": (165, 42, 42)},
            {"name": "Light Brown", "code": "77", "rgb": (205, 133, 63)},
            {"name": "Van Dyke Brown", "code": "75", "rgb": (94, 38, 18)},
            {"name": "Burnt Sienna", "code": "74", "rgb": (138, 54, 15)},
            
            # Grays and Blacks
            {"name": "Black", "code": "9", "rgb": (0, 0, 0)},
            {"name": "Grey", "code": "90", "rgb": (128, 128, 128)},
            {"name": "Light Grey", "code": "91", "rgb": (192, 192, 192)},
            {"name": "White", "code": "0", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def _create_koh_i_noor_database(self):
        """Create Koh-I-Noor Polycolor pencil database"""
        pencils = [
            # Reds
            {"name": "Carmine", "code": "3720", "rgb": (220, 20, 60)},
            {"name": "Scarlet", "code": "3700", "rgb": (237, 28, 36)},
            {"name": "Vermillion", "code": "3710", "rgb": (227, 66, 52)},
            {"name": "Pink", "code": "3730", "rgb": (255, 182, 193)},
            {"name": "Rose", "code": "3740", "rgb": (255, 20, 147)},
            {"name": "Magenta", "code": "3760", "rgb": (255, 0, 255)},
            
            # Oranges
            {"name": "Orange", "code": "3800", "rgb": (255, 165, 0)},
            {"name": "Light Orange", "code": "3810", "rgb": (255, 200, 124)},
            {"name": "Peach", "code": "3820", "rgb": (255, 218, 185)},
            {"name": "Apricot", "code": "3830", "rgb": (251, 206, 177)},
            
            # Yellows
            {"name": "Lemon", "code": "3000", "rgb": (255, 255, 0)},
            {"name": "Yellow", "code": "3010", "rgb": (255, 237, 0)},
            {"name": "Golden Yellow", "code": "3020", "rgb": (255, 215, 0)},
            {"name": "Yellow Ochre", "code": "3070", "rgb": (238, 203, 173)},
            {"name": "Naples Yellow", "code": "3030", "rgb": (250, 218, 94)},
            
            # Greens
            {"name": "Light Green", "code": "3340", "rgb": (144, 238, 144)},
            {"name": "Green", "code": "3360", "rgb": (0, 128, 0)},
            {"name": "Dark Green", "code": "3380", "rgb": (0, 100, 0)},
            {"name": "Emerald Green", "code": "3350", "rgb": (80, 200, 120)},
            {"name": "Olive Green", "code": "3390", "rgb": (128, 128, 0)},
            {"name": "Forest Green", "code": "3370", "rgb": (34, 139, 34)},
            
            # Blues
            {"name": "Light Blue", "code": "3150", "rgb": (173, 216, 230)},
            {"name": "Sky Blue", "code": "3140", "rgb": (135, 206, 235)},
            {"name": "Blue", "code": "3130", "rgb": (0, 123, 191)},
            {"name": "Dark Blue", "code": "3100", "rgb": (0, 0, 139)},
            {"name": "Ultramarine", "code": "3120", "rgb": (65, 105, 225)},
            {"name": "Prussian Blue", "code": "3110", "rgb": (0, 49, 83)},
            
            # Purples
            {"name": "Violet", "code": "3900", "rgb": (138, 43, 226)},
            {"name": "Purple", "code": "3910", "rgb": (128, 0, 128)},
            {"name": "Light Violet", "code": "3920", "rgb": (221, 160, 221)},
            {"name": "Red Violet", "code": "3930", "rgb": (199, 21, 133)},
            
            # Browns
            {"name": "Brown", "code": "3460", "rgb": (165, 42, 42)},
            {"name": "Light Brown", "code": "3470", "rgb": (205, 133, 63)},
            {"name": "Dark Brown", "code": "3450", "rgb": (101, 67, 33)},
            {"name": "Burnt Sienna", "code": "3440", "rgb": (138, 54, 15)},
            {"name": "Raw Sienna", "code": "3430", "rgb": (160, 82, 45)},
            {"name": "Van Dyke Brown", "code": "3420", "rgb": (94, 38, 18)},
            
            # Grays and Blacks
            {"name": "Black", "code": "3999", "rgb": (0, 0, 0)},
            {"name": "Grey", "code": "3990", "rgb": (128, 128, 128)},
            {"name": "Light Grey", "code": "3980", "rgb": (192, 192, 192)},
            {"name": "Dark Grey", "code": "3970", "rgb": (64, 64, 64)},
            {"name": "White", "code": "3000", "rgb": (255, 255, 255)},
        ]
        
        return pd.DataFrame(pencils)
    
    def get_all_pencils(self):
        """Get all pencils from all brands"""
        all_dfs = []
        
        # Add existing brands
        prismacolor_df = self.prismacolor_pencils.copy()
        prismacolor_df['brand'] = 'Prismacolor'
        all_dfs.append(prismacolor_df)
        
        faber_castell_df = self.faber_castell_pencils.copy()
        faber_castell_df['brand'] = 'Faber Castell'
        all_dfs.append(faber_castell_df)
        
        # Add new brands
        caran_dache_df = self.caran_dache_pencils.copy()
        caran_dache_df['brand'] = 'Caran d\'Ache'
        all_dfs.append(caran_dache_df)
        
        derwent_df = self.derwent_pencils.copy()
        derwent_df['brand'] = 'Derwent'
        all_dfs.append(derwent_df)
        
        staedtler_df = self.staedtler_pencils.copy()
        staedtler_df['brand'] = 'Staedtler'
        all_dfs.append(staedtler_df)
        
        koh_i_noor_df = self.koh_i_noor_pencils.copy()
        koh_i_noor_df['brand'] = 'Koh-I-Noor'
        all_dfs.append(koh_i_noor_df)
        
        return pd.concat(all_dfs, ignore_index=True)
    
    def get_purchase_links(self, brand, country='UK'):
        """Get purchase links for a specific brand and country"""
        urls = self._get_purchase_urls()
        if country not in urls:
            country = 'UK'  # Default to UK
            
        brand_lower = brand.lower()
        if brand_lower == 'prismacolor':
            return urls[country]['prismacolor']
        elif brand_lower == 'faber castell':
            return urls[country]['faber_castell']
        elif brand_lower in ['caran d\'ache', 'caran dache']:
            return urls[country].get('caran_dache', {})
        elif brand_lower == 'derwent':
            return urls[country].get('derwent', {})
        elif brand_lower == 'staedtler':
            return urls[country].get('staedtler', {})
        elif brand_lower in ['koh-i-noor', 'koh i noor']:
            return urls[country].get('koh_i_noor', {})
        else:
            return {}
    
    def get_available_countries(self):
        """Get list of available countries for shopping"""
        return list(self._get_purchase_urls().keys())
    
    def get_prismacolor_pencils(self):
        """Get only Prismacolor pencils"""
        df = self.prismacolor_pencils.copy()
        df['brand'] = 'Prismacolor'
        return df
    
    def get_faber_castell_pencils(self):
        """Get only Faber Castell pencils"""
        df = self.faber_castell_pencils.copy()
        df['brand'] = 'Faber Castell'
        return df
    
    def get_caran_dache_pencils(self):
        """Get only Caran d'Ache pencils"""
        df = self.caran_dache_pencils.copy()
        df['brand'] = 'Caran d\'Ache'
        return df
    
    def get_derwent_pencils(self):
        """Get only Derwent pencils"""
        df = self.derwent_pencils.copy()
        df['brand'] = 'Derwent'
        return df
    
    def get_staedtler_pencils(self):
        """Get only Staedtler pencils"""
        df = self.staedtler_pencils.copy()
        df['brand'] = 'Staedtler'
        return df
    
    def get_koh_i_noor_pencils(self):
        """Get only Koh-I-Noor pencils"""
        df = self.koh_i_noor_pencils.copy()
        df['brand'] = 'Koh-I-Noor'
        return df
    
    def get_available_brands(self):
        """Get list of all available brands"""
        return ['Prismacolor', 'Faber Castell', 'Caran d\'Ache', 'Derwent', 'Staedtler', 'Koh-I-Noor']
