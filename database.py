import os
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Float, LargeBinary, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class UserSession(Base):
    """Table to store user sessions"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

class ImageUpload(Base):
    """Table to store uploaded images and metadata"""
    __tablename__ = 'image_uploads'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer)
    image_format = Column(String(50))
    image_mode = Column(String(50))
    width = Column(Integer)
    height = Column(Integer)
    upload_time = Column(DateTime, default=datetime.utcnow)
    image_data = Column(LargeBinary)  # Store actual image data

class ColorAnalysis(Base):
    """Table to store color analysis results"""
    __tablename__ = 'color_analysis'
    
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, nullable=False)
    session_id = Column(String(255), nullable=False)
    num_colors_requested = Column(Integer)
    colors_extracted = Column(JSON)  # Store color data as JSON
    analysis_time = Column(DateTime, default=datetime.utcnow)
    processing_time_seconds = Column(Float)

class PencilMatch(Base):
    """Table to store pencil matching results"""
    __tablename__ = 'pencil_matches'
    
    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, nullable=False)
    session_id = Column(String(255), nullable=False)
    brand = Column(String(100))
    pencil_name = Column(String(255))
    pencil_code = Column(String(100))
    target_rgb = Column(JSON)  # RGB values of target color
    pencil_rgb = Column(JSON)  # RGB values of pencil color
    color_difference = Column(Float)
    match_quality = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """Database manager for color analysis app"""

    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')

        if not self.database_url:
            self.database_url = 'sqlite:///mydata.db'
            print("⚠️  DATABASE_URL not found. Using default: sqlite:///mydata.db")

        print(f"[DEBUG] Using database URL: {self.database_url}")

        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Auto-create tables
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def create_user_session(self, session_id):
        """Create or update a user session"""
        db = self.get_session()
        try:
            # Check if session exists
            existing_session = db.query(UserSession).filter(UserSession.session_id == session_id).first()
            
            if existing_session:
                # Update last activity
                db.query(UserSession).filter(UserSession.session_id == session_id).update(
                    {"last_activity": datetime.utcnow()}
                )
                db.commit()
                return existing_session.id
            else:
                # Create new session
                new_session = UserSession(session_id=session_id)
                db.add(new_session)
                db.commit()
                return new_session.id
        finally:
            db.close()
    
    def save_image_upload(self, session_id, filename, file_size, image_format, image_mode, width, height, image_data):
        """Save uploaded image information"""
        db = self.get_session()
        try:
            image_upload = ImageUpload(
                session_id=session_id,
                filename=filename,
                file_size=file_size,
                image_format=image_format,
                image_mode=image_mode,
                width=width,
                height=height,
                image_data=image_data
            )
            db.add(image_upload)
            db.commit()
            return image_upload.id
        finally:
            db.close()
    
    def save_color_analysis(self, image_id, session_id, num_colors_requested, colors_extracted, processing_time):
        """Save color analysis results"""
        db = self.get_session()
        try:
            # Convert numpy types to Python native types for JSON serialization
            colors_json = self._convert_numpy_types(colors_extracted)
            
            analysis = ColorAnalysis(
                image_id=image_id,
                session_id=session_id,
                num_colors_requested=num_colors_requested,
                colors_extracted=colors_json,
                processing_time_seconds=float(processing_time)
            )
            db.add(analysis)
            db.commit()
            return analysis.id
        finally:
            db.close()
    
    def _convert_numpy_types(self, obj):
        """Convert numpy types to Python native types for JSON serialization"""
        import numpy as np
        
        if isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_numpy_types(item) for item in obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    def save_pencil_matches(self, analysis_id, session_id, matches):
        """Save pencil matching results"""
        db = self.get_session()
        try:
            for match in matches:
                # Calculate match quality
                diff = float(match['color_difference'])
                if diff < 3:
                    quality = "Excellent"
                elif diff < 6:
                    quality = "Very Good"
                elif diff < 12:
                    quality = "Good"
                elif diff < 25:
                    quality = "Acceptable"
                else:
                    quality = "Poor"
                
                # Convert numpy types to Python types
                target_rgb = [int(x) for x in match['target_rgb']]
                pencil_rgb = [int(x) for x in match['pencil_rgb']]
                
                pencil_match = PencilMatch(
                    analysis_id=analysis_id,
                    session_id=session_id,
                    brand=str(match['brand']),
                    pencil_name=str(match['name']),
                    pencil_code=str(match['code']),
                    target_rgb=target_rgb,
                    pencil_rgb=pencil_rgb,
                    color_difference=diff,
                    match_quality=quality
                )
                db.add(pencil_match)
            
            db.commit()
        finally:
            db.close()
    
    def get_user_history(self, session_id, limit=10):
        """Get user's analysis history"""
        db = self.get_session()
        try:
            # Get recent analyses with image info
            query = db.query(
                ColorAnalysis.id,
                ColorAnalysis.analysis_time,
                ColorAnalysis.num_colors_requested,
                ColorAnalysis.colors_extracted,
                ImageUpload.filename,
                ImageUpload.width,
                ImageUpload.height
            ).join(
                ImageUpload, ColorAnalysis.image_id == ImageUpload.id
            ).filter(
                ColorAnalysis.session_id == session_id
            ).order_by(
                ColorAnalysis.analysis_time.desc()
            ).limit(limit)
            
            results = query.all()
            
            history = []
            for result in results:
                # Get pencil matches for this analysis
                matches = db.query(PencilMatch).filter(
                    PencilMatch.analysis_id == result.id
                ).all()
                
                history.append({
                    'analysis_id': result.id,
                    'analysis_time': result.analysis_time,
                    'filename': result.filename,
                    'image_size': f"{result.width}x{result.height}",
                    'num_colors': result.num_colors_requested,
                    'colors_extracted': result.colors_extracted,
                    'num_matches': len(matches),
                    'matches': [{
                        'brand': match.brand,
                        'name': match.pencil_name,
                        'code': match.pencil_code,
                        'color_difference': match.color_difference,
                        'quality': match.match_quality
                    } for match in matches]
                })
            
            return history
        finally:
            db.close()
    
    def get_statistics(self):
        """Get database statistics"""
        db = self.get_session()
        try:
            total_sessions = db.query(UserSession).count()
            total_uploads = db.query(ImageUpload).count()
            total_analyses = db.query(ColorAnalysis).count()
            total_matches = db.query(PencilMatch).count()
            
            # Most popular brands
            brand_stats = db.query(
                PencilMatch.brand,
                func.count(PencilMatch.id).label('count')
            ).group_by(PencilMatch.brand).all()
            
            return {
                'total_sessions': total_sessions,
                'total_uploads': total_uploads,
                'total_analyses': total_analyses,
                'total_matches': total_matches,
                'brand_popularity': {brand: count for brand, count in brand_stats}
            }
        finally:
            db.close()
    
    def cleanup_old_data(self, days_old=30):
        """Clean up old data (optional maintenance function)"""
        db = self.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Delete old sessions and related data
            old_sessions = db.query(UserSession).filter(
                UserSession.last_activity < cutoff_date
            ).all()
            
            session_ids = [s.session_id for s in old_sessions]
            
            if session_ids:
                # Delete related data
                db.query(PencilMatch).filter(PencilMatch.session_id.in_(session_ids)).delete()
                db.query(ColorAnalysis).filter(ColorAnalysis.session_id.in_(session_ids)).delete()
                db.query(ImageUpload).filter(ImageUpload.session_id.in_(session_ids)).delete()
                db.query(UserSession).filter(UserSession.session_id.in_(session_ids)).delete()
                
                db.commit()
                return len(session_ids)
            
            return 0
        finally:
            db.close()