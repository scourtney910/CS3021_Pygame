class Constants:
    """
    When inherited, constants used as: self.<method name>
    When not inherited, constants used as: Constants.<method name>
    """
    _BG_VOLUME = 0.5
    _SCREEN_WIDTH = 800
    _SCREEN_HEIGHT = 600
    _FPS = 60
    _GRAVITY = 0.5
    _PLAYER_WIDTH = 50
    _PLAYER_HEIGHT = 50
    _PLATFORM_WIDTH = 100
    _PLATFORM_HEIGHT = 20
    _PLATFORM_TOP_LIMIT = 30
    _NUM_PLATFORMS = 8
    _PLATFORM_COLLISION_BUFFER = 20
    _ITEM_SCORE = 5
    _ITEM_VOLUME = 0.9
    _PLATFORM_SCORE = 1
    _ITEM_SIZE = 25
    _ITEM_XOFFSET = 38
    _ITEM_YOFFSET = 30
    _MAX_JUMP_STRENGTH = 20
    _JUMP_REDUCTION_FACTOR = 10
    _MAX_VELOCITY = 25
    _MOUSE_CLICK_X = 0
    _MOUSE_CLICK_Y = 1
    _EVEN = 2
    _BUTTON_WIDTH = 200
    _BUTTON_HEIGHT = 50
    _LIGHT_GREEN = (128, 239, 128)
    _DISPLAY_OFFSET = 100
    _LARGE_FONT = 55
    _SMALL_FONT = 30
    _WHITE = (255, 255, 255)
    _DARK_RED = (128, 0, 32)
    _RED = (255, 0, 0)
    _AQUA = (0, 255, 255)
    _BLACK = (0, 0, 0)
    _SCORE_DISPLAY_OFFSET = 10
    _RESTART_TEXT_X_OFFSET = 40
    _START_TEXT_X_OFFSET = 60
    _ALL_TEXT_Y_OFFSET = 5
    _LINE_SPACING = 60
    _ENLARGED_SPRITE_EXTENSION = 30
    _TRANSITION_TIME = 0.5    # Seconds

    @classmethod
    def _bg_vol(cls):
        return cls._BG_VOLUME
    
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
    def _platform_max(cls):
        return cls._PLATFORM_TOP_LIMIT

    @classmethod
    def _num_platforms(cls):
        return cls._NUM_PLATFORMS
    
    @classmethod
    def _platform_collision_buf(cls):
        return cls._PLATFORM_COLLISION_BUFFER

    @classmethod
    def _item_score(cls):
        return cls._ITEM_SCORE
    
    @classmethod
    def _item_vol(cls):
        return cls._ITEM_VOLUME

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
    def _jump_factor(cls):
        return cls._JUMP_REDUCTION_FACTOR

    @classmethod
    def _max_velocity(cls):
        return cls._MAX_VELOCITY

    @classmethod
    def _mouse_click_x(cls):
        return cls._MOUSE_CLICK_X
    
    @classmethod
    def _mouse_click_y(cls):
        return cls._MOUSE_CLICK_Y

    @classmethod
    def _even(cls):
        return cls._EVEN
    
    @classmethod
    def _button_w(cls):
        return cls._BUTTON_WIDTH
    
    @classmethod
    def _button_h(cls):
        return cls._BUTTON_HEIGHT
    
    @classmethod
    def _button_color(cls):
        return cls._LIGHT_GREEN
    
    @classmethod
    def _display_offset(cls):
        return cls._DISPLAY_OFFSET
    
    @classmethod
    def _lg_font(cls):
        return cls._LARGE_FONT
    
    @classmethod
    def _sm_font(cls):
        return cls._SMALL_FONT
    
    @classmethod
    def _white(cls):
        return cls._WHITE
    
    @classmethod
    def _dark_red(cls):
        return cls._DARK_RED
    
    @classmethod
    def _red(cls):
        return cls._RED
    
    @classmethod
    def _aqua(cls):
        return cls._AQUA
    
    @classmethod
    def _black(cls):
        return cls._BLACK
    
    @classmethod
    def _score_display(cls):
        return cls._SCORE_DISPLAY_OFFSET
    
    @classmethod
    def _restart_text_dx(cls):
        return cls._RESTART_TEXT_X_OFFSET
    
    @classmethod
    def _start_text_dx(cls):
        return cls._START_TEXT_X_OFFSET
    
    @classmethod
    def _text_dy(cls):
        return cls._ALL_TEXT_Y_OFFSET
    
    @classmethod
    def _line_spacing(cls):
        return cls._LINE_SPACING
    
    @classmethod
    def _enlarge_sprite(cls):
        return cls._ENLARGED_SPRITE_EXTENSION

    @classmethod
    def _screen_change(cls):
        return cls._TRANSITION_TIME