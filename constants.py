class Constants:
    _SCREEN_WIDTH = 800
    _SCREEN_HEIGHT = 600
    _FPS = 60
    _GRAVITY = 0.5
    _PLAYER_WIDTH = 50
    _PLAYER_HEIGHT = 50
    _PLATFORM_WIDTH = 100
    _PLATFORM_HEIGHT = 20
    _ITEM_SCORE = 5
    _PLATFORM_SCORE = 1
    _ITEM_SIZE = 25
    _ITEM_XOFFSET = 38
    _ITEM_YOFFSET = 30
    _MAX_JUMP_STRENGTH = 20
    _MAX_VELOCITY = 25
    _EVEN = 2

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
    def _item_score(cls):
        return cls._ITEM_SCORE
    
    @classmethod
    def _platform_score(cls):
        return cls._PLATFORM_SCORE
    
    @classmethod
    def _item_size(cls):
        return cls._ITEM_SIZE
    
    @classmethod
    def _item_xoffset(cls):
        return cls._ITEM_XOFFSET

    @classmethod
    def _item_yoffset(cls):
        return cls._ITEM_YOFFSET

    @classmethod
    def _max_jump(cls):
        return cls._MAX_JUMP_STRENGTH

    @classmethod
    def _max_velocity(cls):
        return cls._MAX_VELOCITY

    @classmethod
    def _even(cls):
        return cls._EVEN