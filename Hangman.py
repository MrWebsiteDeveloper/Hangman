"""
Hangman Game – Kivy Edition (with Scrollbar)
Canvas centred at top, compact keyboard at bottom, fully scrollable on small screens.
"""

import random
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView          # <-- NEW
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.utils import get_color_from_hex as rgb
from kivy.metrics import dp


# ----------------------------------------------------------------------
# Hangman Drawing Canvas – upright, centred in its container
# ----------------------------------------------------------------------
class HangmanCanvas(Widget):
    """Custom widget that draws the hangman scene – corrected orientation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (300, 300)          # fixed square
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.wrong_attempts = 0
        self.bind(pos=self.redraw, size=self.redraw)

    def set_wrong_attempts(self, value):
        self.wrong_attempts = value
        self.redraw()

    def redraw(self, *args):
        """Draw the gallows and body parts with flipped y (bottom‑left origin)."""
        self.canvas.clear()
        w, h = self.size
        x0, y0 = self.pos

        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.2, 0.2, 0.2, 1)
            # Gallows
            Line(points=[x0 + 50, y0 + (h - 250),
                         x0 + 150, y0 + (h - 250)], width=4)
            Line(points=[x0 + 70, y0 + (h - 250),
                         x0 + 70, y0 + (h - 50)], width=4)
            Line(points=[x0 + 70, y0 + (h - 50),
                         x0 + 170, y0 + (h - 50)], width=4)
            Line(points=[x0 + 170, y0 + (h - 50),
                         x0 + 170, y0 + (h - 70)], width=4)
            # Body parts
            if self.wrong_attempts >= 1:
                Ellipse(pos=(x0 + 155, y0 + (h - 75 - 30)), size=(30, 30))
            if self.wrong_attempts >= 2:
                Line(points=[x0 + 170, y0 + (h - 105),
                             x0 + 170, y0 + (h - 165)], width=3)
            if self.wrong_attempts >= 3:
                Line(points=[x0 + 150, y0 + (h - 125),
                             x0 + 170, y0 + (h - 115)], width=3)
            if self.wrong_attempts >= 4:
                Line(points=[x0 + 190, y0 + (h - 125),
                             x0 + 170, y0 + (h - 115)], width=3)
            if self.wrong_attempts >= 5:
                Line(points=[x0 + 170, y0 + (h - 165),
                             x0 + 150, y0 + (h - 195)], width=3)
            if self.wrong_attempts >= 6:
                Line(points=[x0 + 170, y0 + (h - 165),
                             x0 + 190, y0 + (h - 195)], width=3)


# ----------------------------------------------------------------------
# Main Game Widget – now with size_hint_y=None and automatic height
# ----------------------------------------------------------------------
class HangmanGame(BoxLayout):
    """Contains all UI and game logic – height computed from children."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint_y = None          # <-- important for ScrollView
        self.bind(minimum_height=self.setter('height'))
        
        # -------------------- Word database (unchanged) --------------------
        self.words = [
    'TEA', 'GUN', 'BOW', 'AXE', 'OAK', 'MAP', 'TAP', 'NAP', 'ZOO', 'ZIP',
    'WAX', 'YAK', 'JOY', 'FLY', 'TRY', 'CRY', 'DRY', 'BUY', 'FUN', 'RUN',
    'SAD', 'BAD', 'MAD', 'GLAD', 'HOT', 'NOT', 'LOT', 'DOT', 'POT', 'ROT',
    'SIT', 'BIT', 'FIT', 'HIT', 'LIT', 'PIT', 'WIT', 'KIT', 'CUT', 'BUT',
    'NUT', 'OUT', 'PUT', 'RAT', 'SAT', 'EAT', 'MAT', 'PAT', 'VAT', 'WET',
    'WALK', 'RUN', 'JUMP', 'DANCE', 'SWIM', 'DRIVE', 'RIDE', 'FLY', 'COOK', 'BAKE',
    'WASH', 'CLEAN', 'FIX', 'BUILD', 'PAINT', 'DRAW', 'WRITE', 'READ', 'STUDY', 'LEARN',
    'TEACH', 'HELP', 'GIVE', 'TAKE', 'BUY', 'SELL', 'PAY', 'COST', 'SAVE', 'LOSE',
    'FIND', 'LOOK', 'SEE', 'HEAR', 'FEEL', 'SMELL', 'TASTE', 'TOUCH', 'HOLD', 'DROP',
    'PUSH', 'PULL', 'LIFT', 'CARRY', 'THROW', 'CATCH', 'KICK', 'HIT', 'FIGHT', 'PEACE',
    'LOVE', 'LIKE', 'HATE', 'FEAR', 'HOPE', 'WISH', 'DREAM', 'PLAN', 'GOAL', 'TASK',
    'JOB', 'WORK', 'PLAY', 'REST', 'SLEEP', 'WAKE', 'EAT', 'DRINK', 'CHEW', 'SWALLOW',
    'TALK', 'SAY', 'TELL', 'ASK', 'ANSWER', 'CALL', 'NAME', 'WORD', 'TEXT', 'LETTER',
    'PHONE', 'EMAIL', 'VIDEO', 'AUDIO', 'IMAGE', 'PHOTO', 'MOVIE', 'MUSIC', 'SONG', 'DANCE',
    'SPORT', 'GAME', 'CHESS', 'CARDS', 'BOARD', 'PIANO', 'GUITAR', 'DRUMS', 'VIOLIN', 'FLUTE',
    'PAINT', 'BRUSH', 'COLOR', 'WHITE', 'BLACK', 'GREEN', 'BLUE', 'RED', 'YELLOW', 'PURPLE',
    'BROWN', 'GRAY', 'PINK', 'ORANGE', 'BEIGE', 'TURQUOISE', 'SILVER', 'GOLD', 'BRONZE', 'COPPER',
    'HOUSE', 'HOME', 'ROOF', 'FLOOR', 'WALL', 'DOOR', 'WINDOW', 'TABLE', 'CHAIR', 'SOFA',
    'BED', 'PILLOW', 'BLANKET', 'SHEET', 'TOWEL', 'SHOWER', 'BATH', 'SINK', 'TOILET', 'MIRROR',
    'KITCHEN', 'FRIDGE', 'STOVE', 'OVEN', 'MICROWAVE', 'TOASTER', 'BLENDER', 'MIXER', 'DISH', 'SPOON',
    'FRIEND', 'FAMILY', 'PARENT', 'MOTHER', 'FATHER', 'SISTER', 'BROTHER', 'COUSIN', 'AUNT', 'UNCLE',
    'DOCTOR', 'NURSE', 'TEACHER', 'STUDENT', 'LAWYER', 'JUDGE', 'POLICE', 'SOLDIER', 'FARMER', 'WORKER',
    'ENGINE', 'MOTOR', 'BATTERY', 'WIRING', 'CIRCUIT', 'SWITCH', 'BUTTON', 'LEVER', 'GEAR', 'WHEEL',
    'STREET', 'ROAD', 'AVENUE', 'HIGHWAY', 'BRIDGE', 'TUNNEL', 'SIDEWALK', 'CURB', 'GUTTER', 'DRAIN',
    'FOREST', 'JUNGLE', 'DESERT', 'VALLEY', 'CANYON', 'PLATEAU', 'GLACIER', 'VOLCANO', 'CRATER', 'CAVE',
    'WEATHER', 'CLIMATE', 'TEMPERATURE', 'HUMIDITY', 'PRESSURE', 'FORECAST', 'SUNNY', 'CLOUDY', 'RAINY', 'STORMY',
    'WINDY', 'FOGGY', 'SNOWY', 'ICY', 'HOT', 'WARM', 'COOL', 'COLD', 'FREEZING', 'BOILING',
    'ANIMALS', 'MAMMALS', 'REPTILES', 'AMPHIBIANS', 'INSECTS', 'BIRDS', 'FISH', 'WHALE', 'SHARK', 'DOLPHIN',
    'OCTOPUS', 'LOBSTER', 'CRAB', 'SHRIMP', 'SCORPION', 'SPIDER', 'BEETLE', 'BUTTERFLY', 'DRAGONFLY', 'LADYBUG',
    'VEGETABLE', 'FRUIT', 'CEREAL', 'GRAIN', 'WHEAT', 'RICE', 'CORN', 'BARLEY', 'OATS', 'RYE',
    'TELEVISION', 'RADIO', 'NEWSPAPER', 'MAGAZINE', 'BOOK', 'NOVEL', 'POETRY', 'ESSAY', 'ARTICLE', 'REPORT',
    'COMPUTER', 'LAPTOP', 'TABLET', 'SMARTPHONE', 'PRINTER', 'SCANNER', 'KEYBOARD', 'MOUSE', 'MONITOR', 'SPEAKERS',
    'SOFTWARE', 'HARDWARE', 'OPERATING', 'APPLICATION', 'PROGRAM', 'ALGORITHM', 'FUNCTION', 'VARIABLE', 'CONSTANT', 'PARAMETER',
    'INTERNET', 'WEBSITE', 'WEBPAGE', 'BROWSER', 'SEARCH', 'ENGINE', 'EMAIL', 'MESSAGE', 'CHAT', 'FORUM',
    'SOCIAL', 'NETWORK', 'PROFILE', 'ACCOUNT', 'PASSWORD', 'USERNAME', 'SECURITY', 'PRIVACY', 'SETTING', 'OPTION',
    'EDUCATION', 'SCHOOL', 'COLLEGE', 'UNIVERSITY', 'COURSE', 'LESSON', 'HOMEWORK', 'EXAM', 'TEST', 'GRADE',
    'MEDICAL', 'HOSPITAL', 'CLINIC', 'DOCTOR', 'NURSE', 'PATIENT', 'MEDICINE', 'TREATMENT', 'SURGERY', 'RECOVERY',
    'TRANSPORT', 'VEHICLE', 'AUTOMOBILE', 'MOTORCYCLE', 'BICYCLE', 'AIRPLANE', 'HELICOPTER', 'TRAIN', 'BUS', 'TAXI',
    'BUILDING', 'STRUCTURE', 'FOUNDATION', 'ROOFING', 'WINDOWS', 'DOORS', 'FLOORING', 'PAINTING', 'PLUMBING', 'ELECTRICAL',
    'ECONOMY', 'FINANCE', 'BUSINESS', 'COMPANY', 'CORPORATION', 'INDUSTRY', 'MARKET', 'STOCK', 'TRADE', 'INVESTMENT',
    'RUN', 'WALK', 'TALK', 'SING', 'DANCE', 'JUMP', 'SWIM', 'FLY', 'DRIVE', 'BUILD',
    'CREATE', 'DESIGN', 'PLAN', 'ORGANIZE', 'MANAGE', 'LEAD', 'FOLLOW', 'LISTEN', 'SPEAK',
    'BIG', 'SMALL', 'TALL', 'SHORT', 'FAST', 'SLOW', 'HOT', 'COLD', 'WARM', 'COOL',
    'SOFT', 'HARD', 'ROUGH', 'SMOOTH', 'BRIGHT', 'DARK', 'LIGHT', 'HEAVY', 'LIGHT',
    'DOCTOR', 'NURSE', 'TEACHER', 'LAWYER', 'ENGINEER', 'SCIENTIST', 'ARTIST', 'MUSICIAN',
    'ACTOR', 'WRITER', 'CHEF', 'BAKER', 'FARMER', 'DRIVER', 'PILOT', 'SAILOR', 'SOLDIER',
    'EMAIL', 'SERVER', 'CLIENT', 'NETWORK', 'ROUTER', 'MODEM', 'WEBCAM', 'HEADPHONES',
    'KEYBOARD', 'MOUSE', 'MONITOR', 'PRINTER', 'SCANNER', 'SPEAKERS', 'MICROPHONE',
    'PIZZA', 'BURGER', 'SALAD', 'SANDWICH', 'SOUP', 'STEW', 'ROAST', 'GRILL', 'FRY',
    'BAKE', 'BOIL', 'STEAM', 'TOAST', 'BLEND', 'MIX', 'CHOP', 'SLICE', 'DICE', 'GRATE'
]
        
        # -------------------- Game state --------------------
        self.secret_word = ""
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.max_wrong = 6
        self.game_active = False
        
        # UI references
        self.hangman_canvas = None
        self.word_label = None
        self.message_label = None
        self.restart_btn = None
        self.keyboard_buttons = {}
        
        self.setup_ui()
        self.new_game()
    
    # ------------------------------------------------------------------
    # UI Construction – vertical, with fixed heights (dp) for scrolling
    # ------------------------------------------------------------------
    def setup_ui(self):
        """Create all widgets – all children have fixed height (dp)."""
        # Title
        title = Label(
            text="Hangman Game",
            font_size=dp(28),
            bold=True,
            color=rgb('#1a1a1a'),
            size_hint=(1, None),
            height=dp(50)
        )
        self.add_widget(title)
        
        # Top area: canvas, word, message, restart button
        top_area = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(450)   # canvas 300 + word 50 + message 35 + restart 45 + spacing
        )
        
        # Canvas container
        canvas_container = FloatLayout(size_hint=(1, None), height=dp(300))
        self.hangman_canvas = HangmanCanvas()
        canvas_container.add_widget(self.hangman_canvas)
        top_area.add_widget(canvas_container)
        
        # Word display
        self.word_label = Label(
            text="",
            font_size=dp(32),
            bold=True,
            color=rgb('#1a1a1a'),
            size_hint=(1, None),
            height=dp(50)
        )
        top_area.add_widget(self.word_label)
        
        # Message label
        self.message_label = Label(
            text="",
            font_size=dp(16),
            color=rgb('#343a40'),
            size_hint=(1, None),
            height=dp(35)
        )
        top_area.add_widget(self.message_label)
        
        # Restart button (hidden initially)
        self.restart_btn = Button(
            text="Play Again",
            font_size=dp(16),
            bold=True,
            background_color=rgb('#28a745'),
            color=(1,1,1,1),
            size_hint=(1, None),
            height=dp(45),
            background_normal=''
        )
        self.restart_btn.bind(on_release=lambda x: self.new_game())
        self.restart_btn.opacity = 0
        self.restart_btn.disabled = True
        top_area.add_widget(self.restart_btn)
        
        self.add_widget(top_area)
        
        # Bottom area: keyboard
        bottom_area = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None),
            height=dp(280)   # title 25 + keyboard rows: 9 rows * dp(40) + spacing
        )
        bottom_area.add_widget(Label(
            text="KEYBOARD",
            font_size=dp(14),
            bold=True,
            color=rgb('#343a40'),
            size_hint=(1, None),
            height=dp(25)
        ))
        
        # Keyboard grid – 3 columns, fixed row height
        keyboard_grid = GridLayout(
            cols=3,
            spacing=dp(4),
            size_hint=(1, None),
            height=dp(40) * 9,          # 9 rows, 40dp each
            row_force_default=True,
            row_default_height=dp(40)
        )
        
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in letters:
            btn = Button(
                text=letter,
                font_size=dp(14),
                bold=True,
                background_color=rgb('#007bff'),
                color=(1,1,1,1),
                background_normal=''
            )
            btn.bind(on_release=lambda instance, l=letter: self.handle_guess(l))
            keyboard_grid.add_widget(btn)
            self.keyboard_buttons[letter] = btn
        
        bottom_area.add_widget(keyboard_grid)
        self.add_widget(bottom_area)
        
        # Total height = sum of all children's heights + padding*2 + spacing between them
        # We'll rely on minimum_height binding, but for ScrollView we need explicit height.
        # The binding self.bind(minimum_height=self.setter('height')) will compute it automatically.
    
    # ------------------------------------------------------------------
    # Game Logic (unchanged)
    # ------------------------------------------------------------------
    def new_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.game_active = True
        
        self.hangman_canvas.set_wrong_attempts(0)
        
        for btn in self.keyboard_buttons.values():
            btn.disabled = False
            btn.background_color = rgb('#007bff')
            btn.opacity = 1
        
        self.restart_btn.opacity = 0
        self.restart_btn.disabled = True
        
        self.message_label.text = ""
        self.message_label.color = rgb('#343a40')
        
        self.update_word_display()
    
    def update_word_display(self):
        if not self.secret_word:
            return
        display = []
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        self.word_label.text = " ".join(display)
    
    def handle_guess(self, letter):
        if not self.game_active:
            return
        
        btn = self.keyboard_buttons[letter]
        btn.disabled = True
        btn.background_color = rgb('#aebbc5')
        
        if letter in self.secret_word:
            self.guessed_letters.add(letter)
            self.update_word_display()
            if all(l in self.guessed_letters for l in self.secret_word):
                self.end_game(win=True)
        else:
            self.wrong_attempts += 1
            self.hangman_canvas.set_wrong_attempts(self.wrong_attempts)
            if self.wrong_attempts >= self.max_wrong:
                self.end_game(win=False)
    
    def end_game(self, win):
        self.game_active = False
        for btn in self.keyboard_buttons.values():
            btn.disabled = True
        
        if win:
            self.message_label.text = "Congratulations! You won! 🎉"
            self.message_label.color = rgb('#28a745')
        else:
            self.message_label.text = f"Game Over! The word was: {self.secret_word}"
            self.message_label.color = rgb('#dc3545')
        
        self.restart_btn.opacity = 1
        self.restart_btn.disabled = False


# ----------------------------------------------------------------------
# Application Entry Point – now with ScrollView as root
# ----------------------------------------------------------------------
class HangmanApp(App):
    def build(self):
        Window.size = (dp(450), dp(700))      # typical mobile size
        Window.minimum_width = dp(350)
        Window.minimum_height = dp(500)
        Window.clearcolor = rgb('#f0f2f5')
        
        # Wrap the game in a ScrollView for small screens
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8),
            bar_color=rgb('#cccccc'),
            bar_inactive_color=rgb('#e0e0e0')
        )
        game = HangmanGame()
        scroll.add_widget(game)
        return scroll


if __name__ == '__main__':
    HangmanApp().run()