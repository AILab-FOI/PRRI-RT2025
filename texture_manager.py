import pygame as pg
import os
from settings import *
from collections import defaultdict

class TextureManager:
    """
    Manages texture loading and caching to improve performance.
    Ensures textures are only loaded once and reused when needed.
    """
    def __init__(self):
        self.textures = {}  # Cache for loaded textures
        self.missing_texture = self._create_missing_texture()  # Fallback texture
    
    def _create_missing_texture(self):
        """Create a checkerboard pattern for missing textures"""
        size = TEXTURE_SIZE
        surface = pg.Surface((size, size), pg.SRCALPHA)
        
        # Create a purple/black checkerboard pattern
        color1 = (255, 0, 255)  # Purple
        color2 = (0, 0, 0)      # Black
        box_size = size // 8
        
        for y in range(0, size, box_size):
            for x in range(0, size, box_size):
                color = color1 if (x // box_size + y // box_size) % 2 == 0 else color2
                pg.draw.rect(surface, color, (x, y, box_size, box_size))
                
        # Add a border
        pg.draw.rect(surface, (255, 0, 0), (0, 0, size, size), 2)
        
        return surface
    
    def get_texture(self, path, res=(TEXTURE_SIZE, TEXTURE_SIZE), use_cache=True):
        """
        Load a texture from path and scale it to the specified resolution.
        If use_cache is True, will return cached texture if available.
        """
        # Create a cache key that includes the path and resolution
        cache_key = f"{path}_{res[0]}x{res[1]}"
        
        # Return cached texture if available and caching is enabled
        if use_cache and cache_key in self.textures:
            return self.textures[cache_key]
        
        # Try to load the texture
        try:
            if os.path.isfile(path):
                texture = pg.image.load(path).convert_alpha()
                scaled_texture = pg.transform.scale(texture, res)
                
                # Cache the texture if caching is enabled
                if use_cache:
                    self.textures[cache_key] = scaled_texture
                
                return scaled_texture
            else:
                print(f"Warning: Texture not found at {path}")
                return self.missing_texture
        except Exception as e:
            print(f"Error loading texture {path}: {e}")
            return self.missing_texture
    
    def get_animation_frames(self, directory_path, use_cache=True):
        """
        Load all images from a directory as animation frames.
        Returns a list of loaded images.
        """
        # Check if we already have these frames cached
        if use_cache and directory_path in self.textures:
            return self.textures[directory_path].copy()  # Return a copy to avoid modifying the cache
        
        frames = []
        
        try:
            if os.path.isdir(directory_path):
                # Get all files in the directory
                files = sorted([f for f in os.listdir(directory_path) 
                               if os.path.isfile(os.path.join(directory_path, f)) and 
                               f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
                
                # Load each file
                for file_name in files:
                    file_path = os.path.join(directory_path, file_name)
                    try:
                        img = pg.image.load(file_path).convert_alpha()
                        frames.append(img)
                    except Exception as e:
                        print(f"Error loading animation frame {file_path}: {e}")
            else:
                print(f"Warning: Animation directory not found at {directory_path}")
        except Exception as e:
            print(f"Error accessing animation directory {directory_path}: {e}")
        
        # If no frames were loaded, add a missing texture
        if not frames:
            frames.append(self.missing_texture)
        
        # Cache the frames if caching is enabled
        if use_cache:
            self.textures[directory_path] = frames.copy()
        
        return frames
    
    def preload_textures(self, texture_list):
        """
        Preload a list of textures to improve performance.
        texture_list should be a list of (path, resolution) tuples.
        """
        for path, res in texture_list:
            self.get_texture(path, res)
    
    def clear_cache(self):
        """Clear the texture cache to free memory"""
        self.textures.clear()
