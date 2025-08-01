#!/usr/bin/env python3
"""
Session Manager for Organized File Output
Handles session-based directory creation and file organization
"""

import os
import shutil
from datetime import datetime
from pathlib import Path


class SessionManager:
    """Manages session-based file organization for AI image generation outputs"""
    
    def __init__(self, session_id=None, base_dir="output"):
        """
        Initialize session manager
        
        Args:
            session_id (str): Custom session ID, defaults to timestamp
            base_dir (str): Base directory for all outputs
        """
        self.base_dir = Path(base_dir)
        self.session_id = session_id or datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_path = self.base_dir / "sessions" / self.session_id
        self.paths = self._create_session_paths()
        self._ensure_directories()
    
    def _create_session_paths(self):
        """Create organized path structure for session"""
        return {
            'base': str(self.session_path),
            'products': str(self.session_path / "products"),
            'composites': str(self.session_path / "composites"),
            'final_designs': str(self.session_path / "final_designs"),
            'analysis': str(self.session_path / "analysis"),
            'shopping_lists': str(self.session_path / "shopping_lists"),
            'debug': str(self.session_path / "debug"),
            'temp': str(self.base_dir / "temp"),
            'archive': str(self.base_dir / "archive")
        }
    
    def _ensure_directories(self):
        """Create all necessary directories"""
        for path in self.paths.values():
            Path(path).mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep files to preserve empty directories
        for key, path in self.paths.items():
            if key in ['temp', 'archive']:
                gitkeep_file = Path(path) / ".gitkeep"
                gitkeep_file.touch(exist_ok=True)
    
    def get_path(self, file_type):
        """Get path for specific file type"""
        return self.paths.get(file_type, self.paths['debug'])
    
    def save_file(self, file_type, filename, content=None, source_path=None):
        """
        Save file to appropriate session directory
        
        Args:
            file_type (str): Type of file (products, composites, etc.)
            filename (str): Name of file to save
            content (bytes/str): File content (if saving new file)
            source_path (str): Path to existing file to copy
        
        Returns:
            str: Full path to saved file
        """
        target_dir = self.get_path(file_type)
        target_path = os.path.join(target_dir, filename)
        
        if source_path and os.path.exists(source_path):
            # Copy existing file
            shutil.copy2(source_path, target_path)
            print(f"📁 Copied {filename} to {file_type}/")
        elif content:
            # Save new file
            mode = 'wb' if isinstance(content, bytes) else 'w'
            with open(target_path, mode) as f:
                f.write(content)
            print(f"💾 Saved {filename} to {file_type}/")
        else:
            raise ValueError("Either content or source_path must be provided")
        
        return target_path
    
    def get_session_info(self):
        """Get information about current session"""
        return {
            'session_id': self.session_id,
            'session_path': str(self.session_path),
            'paths': self.paths,
            'created_at': datetime.now().isoformat()
        }
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_dir = Path(self.paths['temp'])
        if temp_dir.exists():
            for file in temp_dir.iterdir():
                if file.name != '.gitkeep':
                    file.unlink()
            print(f"🧹 Cleaned temp directory: {temp_dir}")
    
    def archive_session(self, archive_name=None):
        """Archive current session to archive directory"""
        if not archive_name:
            archive_name = f"session_{self.session_id}"
        
        archive_path = Path(self.paths['archive']) / archive_name
        if self.session_path.exists():
            shutil.copytree(self.session_path, archive_path)
            print(f"📦 Archived session to: {archive_path}")
            return str(archive_path)
        return None
    
    def cleanup_old_sessions(self, days=30):
        """Clean up sessions older than specified days"""
        sessions_dir = Path(self.base_dir) / "sessions"
        if not sessions_dir.exists():
            return
        
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        for session_dir in sessions_dir.iterdir():
            if session_dir.is_dir() and session_dir.name != 'latest':
                if session_dir.stat().st_mtime < cutoff_date:
                    shutil.rmtree(session_dir)
                    cleaned_count += 1
                    print(f"🗑️ Cleaned old session: {session_dir.name}")
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned {cleaned_count} old sessions")
    
    def create_latest_symlink(self):
        """Create symlink to latest session"""
        latest_path = Path(self.base_dir) / "sessions" / "latest"
        if latest_path.exists():
            latest_path.unlink()
        latest_path.symlink_to(self.session_path, target_is_directory=True)
        print(f"🔗 Created latest symlink: {latest_path} -> {self.session_path}")


def get_session_paths(session_id=None):
    """Convenience function to get session paths"""
    session_manager = SessionManager(session_id)
    return session_manager.paths


def create_session_manager(session_id=None):
    """Convenience function to create session manager"""
    return SessionManager(session_id)


# Example usage:
if __name__ == "__main__":
    # Create session manager
    session = SessionManager()
    
    # Get session info
    info = session.get_session_info()
    print("Session Info:", info)
    
    # Example file operations
    session.save_file('debug', 'test.txt', content="Test content")
    session.save_file('analysis', 'analysis.json', content='{"test": "data"}')
    
    # Create latest symlink
    session.create_latest_symlink()
    
    print("✅ Session manager test completed!") 