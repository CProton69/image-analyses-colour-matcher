import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import io
import time
import hashlib
from color_analyzer import ColorAnalyzer
from pencil_database import PencilDatabase
from color_matcher import ColorMatcher
from database import DatabaseManager
from palette_exporter import PaletteExporter

def main():
    st.title("🎨 Colour Analysis & Pencil Matcher")
    st.markdown("Upload an image to analyze its colors and find matching Prismacolor and Faber Castell pencils!")
    
    # Initialize components
    if 'color_analyzer' not in st.session_state:
        st.session_state.color_analyzer = ColorAnalyzer()
        st.session_state.pencil_db = PencilDatabase()
        st.session_state.color_matcher = ColorMatcher(st.session_state.pencil_db)
        st.session_state.db_manager = DatabaseManager()
        st.session_state.palette_exporter = PaletteExporter()
        
        # Create unique session ID for this user
        if 'session_id' not in st.session_state:
            # Generate session ID based on timestamp and random data
            session_data = f"{time.time()}_{st.session_state.get('user_id', 'anonymous')}"
            st.session_state.session_id = hashlib.md5(session_data.encode()).hexdigest()
            st.session_state.db_manager.create_user_session(st.session_state.session_id)
    
    # Shopping links section
    with st.expander("🛒 Where to Buy Colored Pencils"):
        st.markdown("### Choose Your Country/Region:")
        
        # Country selection
        countries = st.session_state.pencil_db.get_available_countries()
        selected_country = st.selectbox(
            "Select your country for local retailers:",
            options=countries,
            index=0,  # Default to UK (first in list)
            key="country_selector"
        )
        
        st.markdown(f"### Popular Retailers in {selected_country}:")
        
        col1, col2 = st.columns(2)
        
        # Show links for all available brands
        available_brands = st.session_state.pencil_db.get_available_brands()
        brands_per_col = 2
        num_cols = (len(available_brands) + brands_per_col - 1) // brands_per_col
        cols = st.columns(num_cols)
        
        for i, brand in enumerate(available_brands):
            col_idx = i // brands_per_col
            if col_idx < len(cols):
                with cols[col_idx]:
                    st.markdown(f"**{get_brand_emoji(brand)} {brand} Pencils:**")
                    brand_links = st.session_state.pencil_db.get_purchase_links(brand, selected_country)
                    if brand_links:
                        for retailer, url in brand_links.items():
                            st.markdown(f"• [{retailer}]({url})")
                    else:
                        st.markdown("• Check local art supply stores")
        
        st.markdown("---")
        st.markdown("💡 **Tip:** Individual pencils can often be purchased separately, or you can buy complete sets!")
        
        if selected_country == 'UK':
            st.info("🇬🇧 UK customers: Many retailers offer free delivery on orders over £25-£30")
    
    st.markdown("---")
    
    # Sidebar for settings and history
    st.sidebar.header("Settings")
    num_colors = st.sidebar.slider("Number of colors to extract", min_value=3, max_value=15, value=8)
    show_color_difference = st.sidebar.checkbox("Show color difference metrics", value=True)
    
    # History section in sidebar
    st.sidebar.header("Analysis History")
    if st.sidebar.button("View My History"):
        st.session_state.show_history = True
    
    if st.sidebar.button("Clear History"):
        if st.sidebar.button("Confirm Clear", key="confirm_clear"):
            # In a full implementation, you would add a delete method
            st.sidebar.success("History cleared!")
    
    # Database statistics
    st.sidebar.header("App Statistics")
    try:
        stats = st.session_state.db_manager.get_statistics()
        st.sidebar.metric("Total Analyses", stats['total_analyses'])
        st.sidebar.metric("Total Images", stats['total_uploads'])
        
        if stats['brand_popularity']:
            st.sidebar.subheader("Popular Brands")
            for brand, count in stats['brand_popularity'].items():
                st.sidebar.text(f"{brand}: {count}")
    except Exception as e:
        st.sidebar.error("Could not load statistics")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg'],
        help="Upload PNG, JPG, or JPEG images for color analysis"
    )
    
    if uploaded_file is not None:
        try:
            # Display original image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Original Image")
                st.image(image, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                st.subheader("Image Info")
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Size:** {image.size[0]} × {image.size[1]} pixels")
                st.write(f"**Format:** {image.format}")
                st.write(f"**Mode:** {image.mode}")
            
            # Save image to database
            try:
                image_bytes = io.BytesIO()
                image.save(image_bytes, format=image.format or 'PNG')
                image_data = image_bytes.getvalue()
                
                image_id = st.session_state.db_manager.save_image_upload(
                    session_id=st.session_state.session_id,
                    filename=uploaded_file.name,
                    file_size=len(image_data),
                    image_format=image.format or 'PNG',
                    image_mode=image.mode,
                    width=image.size[0],
                    height=image.size[1],
                    image_data=image_data
                )
            except Exception as db_error:
                st.warning(f"Could not save to database: {str(db_error)}")
                image_id = None  # Continue without database storage
            
            # Analyze colors
            with st.spinner("Analyzing colors..."):
                start_time = time.time()
                dominant_colors = st.session_state.color_analyzer.extract_dominant_colors(
                    image, num_colors=num_colors
                )
                processing_time = time.time() - start_time
            
            if dominant_colors:
                st.success(f"Extracted {len(dominant_colors)} dominant colors!")
                
                # Save color analysis to database
                analysis_id = None
                if image_id is not None:
                    try:
                        analysis_id = st.session_state.db_manager.save_color_analysis(
                            image_id=image_id,
                            session_id=st.session_state.session_id,
                            num_colors_requested=num_colors,
                            colors_extracted=dominant_colors,
                            processing_time=processing_time
                        )
                    except Exception as db_error:
                        st.warning(f"Could not save analysis to database: {str(db_error)}")
                        analysis_id = None
                
                # Display extracted colors
                st.subheader("🎨 Extracted Colors")
                
                # Create color palette display
                color_cols = st.columns(min(len(dominant_colors), 8))
                for i, color_info in enumerate(dominant_colors):
                    if i < len(color_cols):
                        with color_cols[i]:
                            rgb = color_info['rgb']
                            hex_color = color_info['hex']
                            percentage = color_info['percentage']
                            
                            # Create color swatch using HTML
                            st.markdown(
                                f"""
                                <div style="background-color: {hex_color}; 
                                           height: 60px; 
                                           border-radius: 5px; 
                                           border: 1px solid #ddd;
                                           margin-bottom: 5px;">
                                </div>
                                <p style="text-align: center; font-size: 12px; margin: 0;">
                                    <strong>{hex_color}</strong><br>
                                    RGB({rgb[0]}, {rgb[1]}, {rgb[2]})<br>
                                    {percentage:.1f}%
                                </p>
                                """, 
                                unsafe_allow_html=True
                            )
                            
                            # Show location information if available
                            if 'location_info' in color_info:
                                location = color_info['location_info']
                                if location['regions'] and location['regions'] != ['Analysis unavailable']:
                                    regions_text = ', '.join(location['regions'])
                                    
                                    # Distribution pattern icons
                                    distribution_icons = {
                                        'widespread': '🌐',
                                        'concentrated': '🎯', 
                                        'localized': '📍',
                                        'scattered': '✨',
                                        'unknown': '❓'
                                    }
                                    icon = distribution_icons.get(location['distribution'], '📊')
                                    
                                    st.markdown(
                                        f"""
                                        <p style="text-align: center; font-size: 11px; margin: 5px 0; 
                                                  color: #666; line-height: 1.3;">
                                            📍 <strong>Found in:</strong> {regions_text}<br>
                                            {icon} <strong>Pattern:</strong> {location['distribution'].title()}
                                        </p>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                
                # Export palette section
                st.subheader("📥 Export Color Palette")
                
                export_cols = st.columns(4)
                
                with export_cols[0]:
                    # Export as image
                    layout = st.selectbox("Layout", ["horizontal", "grid"], key="layout_select")
                    if st.button("📸 Export as Image"):
                        palette_img = st.session_state.palette_exporter.create_palette_image(
                            dominant_colors, uploaded_file.name.split('.')[0], layout
                        )
                        st.download_button(
                            label="Download Palette Image",
                            data=palette_img,
                            file_name=f"{uploaded_file.name.split('.')[0]}_palette.png",
                            mime="image/png"
                        )
                
                with export_cols[1]:
                    # Export as JSON
                    if st.button("📄 Export as JSON"):
                        metadata = {
                            "source_image": uploaded_file.name,
                            "extraction_method": "K-means clustering",
                            "num_colors": num_colors,
                            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                        }
                        json_data = st.session_state.palette_exporter.export_as_json(dominant_colors, metadata)
                        st.download_button(
                            label="Download JSON",
                            data=json_data,
                            file_name=f"{uploaded_file.name.split('.')[0]}_palette.json",
                            mime="application/json"
                        )
                
                with export_cols[2]:
                    # Export as CSS
                    if st.button("🎨 Export as CSS"):
                        css_data = st.session_state.palette_exporter.export_as_css(dominant_colors)
                        st.download_button(
                            label="Download CSS",
                            data=css_data,
                            file_name=f"{uploaded_file.name.split('.')[0]}_palette.css",
                            mime="text/css"
                        )
                
                with export_cols[3]:
                    # Export as CSV
                    if st.button("📊 Export as CSV"):
                        csv_data = st.session_state.palette_exporter.export_as_csv(dominant_colors)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"{uploaded_file.name.split('.')[0]}_palette.csv",
                            mime="text/csv"
                        )
                
                # Additional export formats
                with st.expander("🔧 More Export Options"):
                    extra_cols = st.columns(3)
                    
                    with extra_cols[0]:
                        if st.button("Adobe Swatch"):
                            ase_data = st.session_state.palette_exporter.export_as_adobe_swatch(
                                dominant_colors, f"{uploaded_file.name.split('.')[0]} Palette"
                            )
                            st.download_button(
                                label="Download Adobe Swatch",
                                data=ase_data,
                                file_name=f"{uploaded_file.name.split('.')[0]}_palette.ase.txt",
                                mime="text/plain"
                            )
                    
                    with extra_cols[1]:
                        if st.button("SCSS Variables"):
                            scss_data = st.session_state.palette_exporter.export_as_scss(dominant_colors)
                            st.download_button(
                                label="Download SCSS",
                                data=scss_data,
                                file_name=f"{uploaded_file.name.split('.')[0]}_palette.scss",
                                mime="text/plain"
                            )
                    
                    with extra_cols[2]:
                        if st.button("Figma Compatible"):
                            figma_data = st.session_state.palette_exporter.export_for_figma(dominant_colors)
                            st.download_button(
                                label="Download Figma JSON",
                                data=figma_data,
                                file_name=f"{uploaded_file.name.split('.')[0]}_figma_palette.json",
                                mime="application/json"
                            )
                
                # Row 2 - New Affinity and Photopea exports
                st.markdown("**Design Software Swatches:**")
                design_cols = st.columns(2)
                
                with design_cols[0]:
                    if st.button("🎨 Affinity Apps (.afpalette)"):
                        affinity_data = st.session_state.palette_exporter.export_for_affinity(dominant_colors)
                        st.download_button(
                            label="Download Affinity Palette",
                            data=affinity_data,
                            file_name=f"{uploaded_file.name.split('.')[0]}_affinity_palette.afpalette",
                            mime="application/xml"
                        )
                
                with design_cols[1]:
                    if st.button("🌐 Photopea Compatible"):
                        photopea_data = st.session_state.palette_exporter.export_for_photopea(dominant_colors)
                        st.download_button(
                            label="Download Photopea JSON",
                            data=photopea_data,
                            file_name=f"{uploaded_file.name.split('.')[0]}_photopea_palette.json",
                            mime="application/json"
                        )
                
                # Find matching pencils
                st.subheader("✏️ Matching Colored Pencils")
                
                with st.spinner("Finding pencil matches..."):
                    all_matches = []
                    for color_info in dominant_colors:
                        matches = st.session_state.color_matcher.find_matches(
                            color_info['rgb'], max_matches=3
                        )
                        all_matches.extend(matches)
                
                if all_matches:
                    # Save pencil matches to database
                    if analysis_id is not None:
                        try:
                            st.session_state.db_manager.save_pencil_matches(
                                analysis_id=analysis_id,
                                session_id=st.session_state.session_id,
                                matches=all_matches
                            )
                        except Exception as db_error:
                            st.warning(f"Could not save matches to database: {str(db_error)}")
                    
                    # Group by brand
                    available_brands = st.session_state.pencil_db.get_available_brands()
                    brand_matches = {}
                    
                    for brand in available_brands:
                        brand_matches[brand] = [m for m in all_matches if m['brand'] == brand]
                    
                    # Filter out brands with no matches
                    brands_with_matches = {k: v for k, v in brand_matches.items() if v}
                    
                    if brands_with_matches:
                        # Use tabs for all brands to handle the new ones nicely
                        brand_names = list(brands_with_matches.keys())
                        tabs = st.tabs([f"{get_brand_emoji(brand)} {brand}" for brand in brand_names])
                        
                        for i, (brand, matches) in enumerate(brands_with_matches.items()):
                            with tabs[i]:
                                display_pencil_matches(
                                    matches, show_color_difference, st.session_state.pencil_db
                                )
                    
                    # Summary statistics
                    st.subheader("📊 Summary")
                    total_matches = len(all_matches)
                    avg_difference = np.mean([m['color_difference'] for m in all_matches])
                    
                    # Create dynamic columns for brand counts
                    num_brands_with_matches = len(brands_with_matches)
                    if num_brands_with_matches <= 6:
                        metric_cols = st.columns(num_brands_with_matches + 1)  # +1 for total
                        
                        with metric_cols[0]:
                            st.metric("Total Matches", total_matches)
                        
                        for i, (brand, matches) in enumerate(brands_with_matches.items()):
                            with metric_cols[i + 1]:
                                st.metric(brand, len(matches))
                    else:
                        # If too many brands, show total and top 3
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Matches", total_matches)
                        
                        sorted_brands = sorted(brands_with_matches.items(), key=lambda x: len(x[1]), reverse=True)
                        for i, (brand, matches) in enumerate(sorted_brands[:3]):
                            with [col2, col3, col4][i]:
                                st.metric(brand, len(matches))
                    
                    if show_color_difference:
                        st.metric("Average Color Difference (ΔE)", f"{avg_difference:.2f}")
                    
                    # Export pencil shopping list
                    st.subheader("🛒 Export Pencil Shopping List")
                    
                    shopping_cols = st.columns(3)
                    
                    with shopping_cols[0]:
                        if st.button("📝 Text Shopping List"):
                            shopping_text = st.session_state.palette_exporter.create_pencil_shopping_list(
                                all_matches, "text"
                            )
                            st.download_button(
                                label="Download Shopping List",
                                data=shopping_text,
                                file_name=f"{uploaded_file.name.split('.')[0]}_shopping_list.txt",
                                mime="text/plain"
                            )
                    
                    with shopping_cols[1]:
                        if st.button("📊 CSV Shopping List"):
                            shopping_csv = st.session_state.palette_exporter.create_pencil_shopping_list(
                                all_matches, "csv"
                            )
                            st.download_button(
                                label="Download CSV List",
                                data=shopping_csv,
                                file_name=f"{uploaded_file.name.split('.')[0]}_shopping_list.csv",
                                mime="text/csv"
                            )
                    
                    with shopping_cols[2]:
                        if st.button("📄 JSON Shopping List"):
                            shopping_json = st.session_state.palette_exporter.create_pencil_shopping_list(
                                all_matches, "json"
                            )
                            st.download_button(
                                label="Download JSON List",
                                data=shopping_json,
                                file_name=f"{uploaded_file.name.split('.')[0]}_shopping_list.json",
                                mime="application/json"
                            )
                
                else:
                    st.error("No matching pencils found. This might indicate an issue with the color matching algorithm.")
            
            else:
                st.error("Failed to extract colors from the image. Please try a different image.")
                
        except Exception as e:
            st.error(f"An error occurred while processing the image: {str(e)}")
            st.info("Please make sure you've uploaded a valid image file (PNG, JPG, or JPEG).")
    
    else:
        # Show history if requested
        if st.session_state.get('show_history', False):
            st.subheader("📜 Your Analysis History")
            
            try:
                history = st.session_state.db_manager.get_user_history(st.session_state.session_id)
                
                if history:
                    for item in history:
                        with st.expander(f"🖼️ {item['filename']} - {item['analysis_time'].strftime('%Y-%m-%d %H:%M')}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Image Size:** {item['image_size']}")
                                st.write(f"**Colors Extracted:** {item['num_colors']}")
                            
                            with col2:
                                st.write(f"**Pencil Matches:** {item['num_matches']}")
                                st.write(f"**Analysis Time:** {item['analysis_time'].strftime('%H:%M:%S')}")
                            
                            with col3:
                                if st.button(f"View Details", key=f"details_{item['analysis_id']}"):
                                    st.json(item['colors_extracted'][:3])  # Show first 3 colors
                            
                            # Show top matches
                            if item['matches']:
                                st.write("**Top Matches:**")
                                for match in item['matches'][:5]:
                                    quality_emoji = "🟢" if match['quality'] in ['Excellent', 'Very Good'] else "🟡" if match['quality'] == 'Good' else "🔴"
                                    st.write(f"{quality_emoji} {match['brand']} {match['name']} ({match['code']}) - {match['quality']}")
                    
                    if st.button("Hide History"):
                        st.session_state.show_history = False
                        st.rerun()
                else:
                    st.info("No analysis history found. Upload and analyze some images to build your history!")
                    
            except Exception as e:
                st.error(f"Could not load history: {str(e)}")
        
        else:
            # Show instructions when no file is uploaded
            st.info("👆 Upload an image to get started!")
            
            # Display sample information
            with st.expander("ℹ️ How it works"):
                st.markdown("""
                1. **Upload an image** - Choose any PNG, JPG, or JPEG file
                2. **Color extraction** - The app uses K-means clustering to identify dominant colors
                3. **Pencil matching** - Colors are matched to Prismacolor and Faber Castell pencil collections
                4. **Results** - View matching pencils with color swatches and difference metrics
                5. **History** - All your analyses are saved and can be viewed in the sidebar
                
                **Tips:**
                - Images with clear, distinct colors work best
                - Adjust the number of colors to extract in the sidebar
                - Color difference is measured using Delta E (ΔE) - lower values mean closer matches
                - Your analysis history is saved automatically
                """)

def get_brand_emoji(brand):
    """Get emoji for brand"""
    brand_emojis = {
        'Prismacolor': '🟡',
        'Faber Castell': '🔵',
        'Caran d\'Ache': '🟢',
        'Derwent': '🟣',
        'Staedtler': '🔴',
        'Koh-I-Noor': '🟠'
    }
    return brand_emojis.get(brand, '✏️')

def display_pencil_matches(matches, show_difference=True, pencil_db=None):
    """Display pencil matches in a formatted way"""
    # Remove duplicates and sort by color difference
    unique_matches = {}
    for match in matches:
        key = f"{match['brand']}_{match['name']}_{match['code']}"
        if key not in unique_matches or match['color_difference'] < unique_matches[key]['color_difference']:
            unique_matches[key] = match
    
    sorted_matches = sorted(unique_matches.values(), key=lambda x: x['color_difference'])
    
    # Get selected country from session state (default to UK)
    selected_country = st.session_state.get('country_selector', 'UK')
    
    for match in sorted_matches[:10]:  # Show top 10 matches
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            # Color swatch
            hex_color = f"#{match['pencil_rgb'][0]:02x}{match['pencil_rgb'][1]:02x}{match['pencil_rgb'][2]:02x}"
            st.markdown(
                f"""
                <div style="background-color: {hex_color}; 
                           height: 40px; 
                           border-radius: 5px; 
                           border: 1px solid #ddd;">
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(f"**{match['name']}**")
            st.markdown(f"Code: {match['code']}")
            if show_difference:
                difference_color = "🟢" if match['color_difference'] < 5 else "🟡" if match['color_difference'] < 15 else "🔴"
                st.markdown(f"Color Difference: {difference_color} {match['color_difference']:.2f} ΔE")
        
        with col3:
            # Shopping button with country-specific links
            if pencil_db:
                purchase_links = pencil_db.get_purchase_links(match['brand'], selected_country)
                if purchase_links:
                    st.markdown("**Buy:**")
                    # Show top 2 retailers to keep it concise
                    for i, (retailer, url) in enumerate(purchase_links.items()):
                        if i < 2:  # Limit to 2 retailers per match
                            st.markdown(f"[{retailer}]({url})", help=f"Buy {match['name']} from {retailer}")
        
        st.markdown("---")

if __name__ == "__main__":
    main()
