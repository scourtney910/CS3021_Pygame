import random

class Constants:
    _SCREEN_WIDTH      = 800
    _SCREEN_HEIGHT     = 600
    _FPS               = 60
    _GRAVITY           = 0.5
    _PLAYER_WIDTH      = 50
    _PLAYER_HEIGHT     = 50
    _PLATFORM_WIDTH    = 100
    _PLATFORM_HEIGHT   = 20
    _PLATFORM_COLOR    = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    _MAX_JUMP_STRENGTH = 20
    _MAX_VELOCITY      = 25

    @classmethod
    def _screen_w(cls):
        return cls._SCREEN_WIDTH
    
    @classmethod
    def _screen_h(cls):
        return cls._SCREEN_HEIGHT
    
    @classmethod
    def _fps(cls):
        return cls._FPS
    
    @classmethod
    def _grav(cls):
        return cls._GRAVITY

    @classmethod
    def _player_w(cls):
        return cls._PLAYER_WIDTH
    
    @classmethod
    def _player_h(cls):
        return cls._PLAYER_HEIGHT

    @classmethod
    def _platform_w(cls):
        return cls._PLATFORM_WIDTH
    
    @classmethod
    def _platform_h(cls):
        return cls._PLATFORM_HEIGHT
    
    @classmethod
    def _platform_rgb(cls):
        return cls._PLATFORM_COLOR
    
    @classmethod
    def _max_jump(cls):
        return cls._MAX_JUMP_STRENGTH
    
    @classmethod
    def _max_velocity(cls):
        return cls._MAX_VELOCITY