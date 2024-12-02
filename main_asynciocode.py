import pygame, sys, random, time, string, json, asyncio
from pygame.locals import *
from pathlib import Path
from data.classes import Button, Textbox
pygame.init()
pygame.mixer.init()

 
# Music
background_music = pygame.mixer.music.load('data/sounds/two_left_socks.ogg')
pygame.mixer.music.set_volume(0.2)

# Sfx
sfx_won = pygame.mixer.Sound('data/sounds/gold_sack.ogg')
sfx_lost = pygame.mixer.Sound('data/sounds/mixkit-8-bit-lose-2031.ogg')
sfx_end = pygame.mixer.Sound('data/sounds/Game Over II ~ v1.ogg')
pygame.mixer.Sound.set_volume(sfx_end, 0.2)

# Colours
COLOR_BACKGROUND = (40, 133, 45)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Blackjack')








#Starting Screen
class starting_screen:
  def __init__(self):

    """Prepares Variables"""

    # colors
    self.COLOR_SS_BACKGROUND = COLOR_BACKGROUND
    self.COLOR_SS_TITLE = (255, 195, 43)
    self.COLOR_SS_TITLE_BACKGROUND = (35, 196, 44)
    self.COLOR_SS_PLAYBUTTON = (222, 138, 20)
    self.COLOR_SS_PLAYBUTTON_HOVER = (250, 179, 80)
    self.COLOR_SS_PLAYBUTTON_PRESS = (189, 112, 4)
    self.COLOR_SS_PLAYBUTTON_TEXT = (255, 255, 255)

    # title
    self.SS_TITLE_FONT = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', 150)
    self.ss_title = self.SS_TITLE_FONT.render('BLACKJACK', True, self.COLOR_SS_TITLE, None)
    self.ss_title_rect = self.ss_title.get_rect()
    self.ss_title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//4)

    # title backdrop
    self.ss_title_bg_rect = pygame.Rect(0, 0, self.ss_title_rect.width + 100, self.ss_title_rect.height + 50)
    self.ss_title_bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//4)

    # card animation
    self.card_speed = 8
    self.card_scale = 0.5

    # middle card
    self.ss_card1 = pygame.image.load('data/images/jack_of_spades.png').convert_alpha()
    self.ss_card1 = pygame.transform.scale(self.ss_card1, (self.ss_card1.get_width()*self.card_scale, self.ss_card1.get_height()*self.card_scale))
    self.ss_card1X = WINDOW_WIDTH//2 - self.ss_card1.get_width()//2
    self.ss_card1Y = WINDOW_HEIGHT

    # left card
    self.ss_card2 = pygame.image.load('data/images/ace_of_clubs.png').convert_alpha()
    self.ss_card2 = pygame.transform.scale(self.ss_card2, (self.ss_card2.get_width()*self.card_scale, self.ss_card2.get_height()*self.card_scale))
    self.ss_card2X = WINDOW_WIDTH//2 - self.ss_card1.get_width()//2 - 200
    self.ss_card2Y = WINDOW_HEIGHT
    self.ss_card2 = pygame.transform.rotate(self.ss_card2, 25)

    # right card
    self.ss_card3 = pygame.image.load('data/images/10_of_diamonds.png').convert_alpha()
    self.ss_card3 = pygame.transform.scale(self.ss_card3, (self.ss_card3.get_width()*self.card_scale, self.ss_card3.get_height()*self.card_scale))
    self.ss_card3X = WINDOW_WIDTH//2 - self.ss_card1.get_width()//2 + 90
    self.ss_card3Y = WINDOW_HEIGHT
    self.ss_card3 = pygame.transform.rotate(self.ss_card3, -25)

    # play button
    self.SS_PLAYBUTTON_TEXT_FONT = pygame.font.Font('data/fonts/MouldyCheeseRegular-WyMWG.ttf', 40)
    self.ss_playbutton = Button((WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2+30-40), (200, 80), self.COLOR_SS_PLAYBUTTON)
    self.ss_playbutton.add_border(3, self.COLOR_SS_PLAYBUTTON_TEXT)
    self.ss_playbutton.add_text(self.SS_PLAYBUTTON_TEXT_FONT, 'PLAY', self.COLOR_SS_PLAYBUTTON_TEXT)

    # Order of Animations
    self.cards_anim = True
    self.text_appear = False
    self.text_bg_appear = False
    self.text_bg_appear_a = False
    self.text_bg_appear_b = True
    self.playbutton_appear = False
    self.playbutton_appear_a = False
    self.playbutton_appear_b = True
    self.final_anim = False

    # Mouse States
    self.mouse_is_down = False
    self.mouse_up = False

    # Misc.
    self.LEAVE_SPEED = 10
    self.ss_delay = 0
    self.frames = 0


  ###############################################
  def run(self, events):
    """EVENTS"""

    self.mouse_up = False
    for event in events :
      if event.type == QUIT :  # Closes program if user exits
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:  # Checks if mouse is down
        self.mouse_is_down = True
      if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse has been released
        self.mouse_is_down = False
        self.mouse_up = True
    
    mousePos = pygame.mouse.get_pos()  # Gets position of mouse



    """PROCESSING"""
    # Changes color of button based on state
    if self.playbutton_appear == True:
      self.ss_playbutton.update(self.COLOR_SS_PLAYBUTTON_HOVER, self.COLOR_SS_PLAYBUTTON_PRESS, mousePos, self.mouse_is_down)
    
    # Checks if the button has been pressed
    if self.ss_playbutton.check_press(mousePos, self.mouse_up):
      self.final_anim = True

    # Animates the Cards
    if self.cards_anim == True:
      if self.ss_card1Y >= WINDOW_HEIGHT//3*2:
        self.ss_card1Y -= self.card_speed
        self.ss_card2Y -= self.card_speed
        self.ss_card3Y -= self.card_speed
        self.frames = 0
      else:
        self.frames += 1
        if self.frames == 30:
          self.text_bg_appear = True
          self.cards_anim = False
          self.frames = 0

    """DISPLAY"""
    WINDOW.fill(self.COLOR_SS_BACKGROUND)

    WINDOW.blit(self.ss_card2, (self.ss_card2X, self.ss_card2Y))
    WINDOW.blit(self.ss_card3, (self.ss_card3X, self.ss_card3Y))
    WINDOW.blit(self.ss_card1, (self.ss_card1X, self.ss_card1Y))

    # Runs when the title background needs to appear
    if self.text_bg_appear == True:
      pygame.draw.rect(WINDOW, self.COLOR_SS_TITLE_BACKGROUND, self.ss_title_bg_rect)
      if self.text_bg_appear_b == True:
        self.text_bg_appear_a = True
        self.text_bg_appear_b = False

    # Runs when the text needs to appear
    if self.text_appear == True:
      WINDOW.blit(self.ss_title, self.ss_title_rect)
      if self.playbutton_appear_b == True:
        self.playbutton_appear_a = True
        self.playbutton_appear_b = False
    
    # Runs when the button needs to appear
    if self.playbutton_appear == True:
      self.ss_playbutton.draw(WINDOW)

    pygame.display.update()
    fpsClock.tick(FPS)

    # Runs after the player has clicked the play button
    if self.final_anim == True:
      self.ss_title_bg_rect.y -= self.LEAVE_SPEED
      self.ss_title_rect.y -= self.LEAVE_SPEED
      self.ss_playbutton.y -= self.LEAVE_SPEED
      self.ss_card1Y += self.LEAVE_SPEED
      self.ss_card2Y += self.LEAVE_SPEED
      self.ss_card3Y += self.LEAVE_SPEED
      if self.ss_playbutton.y + self.ss_playbutton.height <= 0:
        self.ss_delay += 1
        if self.ss_delay == 60:
          self.ss_delay = 0
          return 'main_screen'

    # Activates the next part after waiting
    if self.text_bg_appear_a == True:
      self.frames += 1
      if self.frames == 30:
        self.text_appear = True
        self.frames = 0
        self.text_bg_appear_a = False
    if self.playbutton_appear_a == True:
      self.frames += 1
      if self.frames == 30:
        self.playbutton_appear = True
        self.playbutton_appear_a = False
        self.frames = 0
    
    return 'starting_screen'
      












class Card:
  def __init__(self, deck:list, position:tuple, shown:bool=True):
    number = ""
    suit = ""
    card = random.choice(deck)
    deck.remove(card)

    if card[0] == 'a':
      number = "ace"
      self.value = 'A'
    elif card[0] == 'j':
      number = "jack"
      self.value = 'J'
    elif card[0] == 'q':
      number = 'queen'
      self.value = 'Q'
    elif card[0] == 'k':
      number = 'king'
      self.value = 'K'
    elif card[0] == 't':
      number = '10'
      self.value = '10'
    else:
      number = card[0]
      self.value = card[0]

    if card[1] == 'c':
      suit = 'clubs'
    elif card[1] == 'h':
      suit = 'hearts'
    elif card[1] == 'd':
      suit = 'diamonds'
    elif card[1] == 's':
      suit = 'spades'
    
    self.x = position[0]
    self.y = position[1]
    self.suit = suit
    self.number = number
    self.image = pygame.image.load(f'data/images/{number}_of_{suit}.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (self.image.get_width()//3, self.image.get_height()//3))
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.shown = shown
    self.card_back = pygame.image.load('data/images/card_back.png').convert_alpha()
    self.card_back = pygame.transform.scale(self.card_back, (self.card_back.get_width()//1, self.image.get_height()//1))

  def draw(self, surface):
    if self.shown:
      surface.blit(self.image, (self.x, self.y))
    else:
      surface.blit(self.card_back, (self.x, self.y))
  
  def shift(self):
    self.x -= self.image.get_width()//2


# Adds an extra card to a hand
def draw_card(cards):
  cards.append(Card(deck, (cards[len(cards)-1].x+cards[len(cards)-1].width, cards[len(cards)-1].y)))
  for card in cards:
    card.shift()

# Computes the value of a hand of cards
def compute(cards):
    total = 0
    num_aces = 0
    for card in cards:
        if card.value == 'J' or card.value == 'Q' or card.value == 'K':
            total += 10
        elif card.value == "A":
            total += 11
            num_aces += 1
        else:
            total += int(card.value)
    while True:
        if total >= 22:
            if num_aces == 0:
                return "bust"
            elif num_aces >= 1:
                total -= 10
                num_aces -= 1
        else:
            return total

        














# The main function that controls the game
class main_screen:
  def __init__(self, balance, profit, deck) :
    """GAME VARIABLES"""

    # Colors
    self.COLOR_PLAYER_CARD_BG = (18, 84, 21)
    self.COLOR_BOTTOM_BAR = (105, 105, 105)
    self.COLOR_BOTTOM_BAR_BG = (125, 125, 125)

    # Screen Elements
    self.font_card_values = pygame.font.Font('data/fonts/coolvetica rg.otf', 30)


    # Bottom Bar
    self.bottom_bar = pygame.Rect(0, WINDOW_HEIGHT-100, WINDOW_WIDTH, 100)
    self.balance_display_bg = pygame.Rect(0, 0, 300, 60)
    self.balance_display_bg.center = (WINDOW_WIDTH//5, 750)
    self.profit_display_bg = pygame.Rect(0, 0, 300, 60)
    self.profit_display_bg.center = (WINDOW_WIDTH//5*4, 750)
    self.current_bet_display_bg = pygame.Rect(0, 0, 300, 60)
    self.current_bet_display_bg.center = (WINDOW_WIDTH//2, 750)

    # Bet Box
    self.bet_box_rect = pygame.Rect(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 500, 75)
    self.bet_box_rect.center = (WINDOW_WIDTH//2-50, (WINDOW_HEIGHT-100)//2)
    self.bet_box_font = pygame.font.Font('data/fonts/Money-w16D8.ttf', 45)
    self.numbers = [num for num in string.digits]
    self.bet_box = Textbox(self.bet_box_rect, self.COLOR_PLAYER_CARD_BG, self.bet_box_font, (222, 168, 31), 20, 2, whitelist=self.numbers, prefix='$ ')
    self.bet_box.add_border(5, (222, 168, 31))
    self.bet_box.add_description('Enter Bet Here')

    self.bet_box_btn = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (75, 75), (4, 204, 17))
    self.bet_box_btn.x = WINDOW_WIDTH//2+300-75
    self.bet_box_btn.y = (WINDOW_HEIGHT-100)//2-75//2
    self.bet_box_btn.add_border(5, (27, 99, 31))
    


    # Action Buttons
    self.hit_button = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (200, 60), (255, 0, 0))
    self.hit_button.add_border(4, (255, 255, 255))
    self.hit_button_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
    self.hit_button.add_text(self.hit_button_font, 'HIT', (255, 255, 255))
    self.hit_button.change_center((WINDOW_WIDTH//2-125, (WINDOW_HEIGHT-100)//2))

    self.stay_button = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (200, 60), (0, 0, 0))
    self.stay_button.add_border(4, (255, 255, 255))
    self.stay_button_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
    self.stay_button.add_text(self.stay_button_font, 'STAY', (255, 255, 255))
    self.stay_button.change_center((WINDOW_WIDTH//2+125, (WINDOW_HEIGHT-100)//2))

    # Card Positions
    self.pos_player_card_left = (WINDOW_WIDTH//2-166, WINDOW_HEIGHT-342)
    self.pos_player_card_right = (WINDOW_WIDTH//2, WINDOW_HEIGHT-342)
    self.pos_dealer_card_left = (WINDOW_WIDTH//2-166, 0)
    self.pos_dealer_card_right = (WINDOW_WIDTH//2, 0)

    # Cards
    self.player_cards = []
    self.player_cards.append(Card(deck, self.pos_player_card_left, False))
    self.player_cards.append(Card(deck, self.pos_player_card_right, False))
    self.dealer_cards = []
    self.dealer_cards.append(Card(deck, self.pos_dealer_card_left, False))
    self.dealer_cards.append(Card(deck, self.pos_dealer_card_right, False))

    # Result Display
    self.result_display = ""
    self.result_display_font_size = 5
    self.display_y = WINDOW_HEIGHT

    # Save Prompt
    self.save_display_bg = pygame.Rect(0, 0, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
    self.save_display_bg.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    self.save_display_font = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', 40)
    self.save_display_text = self.save_display_font.render('Do You Want to Save?', True, (255, 255, 255), None)
    self.save_display_text_rect = self.save_display_text.get_rect()
    self.save_display_text_rect.centerx = self.save_display_bg.centerx
    self.save_display_text_rect.centery = self.save_display_bg.centery - 50

    self.save_prompt_yes = Button((0, 0), (100, 100), (8, 232, 0))
    self.save_prompt_yes.add_border(5, (7, 105, 3))
    self.save_prompt_yes.change_center((WINDOW_WIDTH//2-100, WINDOW_HEIGHT//3+200))
    self.save_prompt_no = Button((0, 0), (100, 100), (255, 4, 0))
    self.save_prompt_no.add_border(5, (79, 1, 0))
    self.save_prompt_no.change_center((WINDOW_WIDTH//2+100, WINDOW_HEIGHT//3+200))



    # Misc
    self.mouseIsDown = False
    self.current_bet = 0
    self.status = ''
    self.frames = 0
    self.save = None
    self.balance = balance
    self.profit = profit


    # Phases
    self.p_show_basic = False
    self.p_enter_bet = True
    self.p_hit_or_stay = False
    self.show_dealer_cards = False
    self.temp = False
    self.p_save_prompt = False

  
  """MAIN GAME LOOP"""
  def run(self, events):

    """USER INPUT"""
    mouseUp = False
    mouseDown = False
    mousePos = pygame.mouse.get_pos()
    for event in events:
      if event.type == MOUSEBUTTONDOWN:
        self.mouseIsDown = True
        mouseDown = True
      if event.type == MOUSEBUTTONUP:
        self.mouseIsDown = False
        mouseUp = True
      if event.type == QUIT :
        # Asks if the user wants to save
        self.end = False
        self.p_save_prompt = True
      
      if self.p_enter_bet and self.p_save_prompt == False:
        self.bet_box.update(mousePos, mouseDown, (49, 163, 54), event)

    


    """PROCESSING"""
    
    # Creates the background for the cards
    self.player_cards_bg = pygame.Rect(WINDOW_WIDTH//2-200, WINDOW_HEIGHT-400, 68+len(self.player_cards)*166, 300)
    self.dealer_cards_bg = pygame.Rect(WINDOW_WIDTH//2-200, 0, 68+len(self.dealer_cards)*166, 300)
    self.player_cards_bg.centerx = WINDOW_WIDTH//2
    self.dealer_cards_bg.centerx = WINDOW_WIDTH//2

    # Creates the text above the player's cards
    self.player_cards_value = compute(self.player_cards)
    self.player_cards_value_text = self.font_card_values.render(f"Your Cards' Value: ({self.player_cards_value})", True, (255, 255, 255), None)
    self.player_cards_value_text_rect = self.player_cards_value_text.get_rect()
    self.player_cards_value_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-375)

    #Creates the text below the dealer's cards
    self.dealer_cards_value = compute(self.dealer_cards)
    if self.show_dealer_cards:
      self.dealer_cards_value_text = self.font_card_values.render(f"Dealer Cards' Value: ({self.dealer_cards_value})", True, (255, 255, 255), None)
    else:
      self.dealer_cards_value_text = self.font_card_values.render(f"Dealer Cards' Value: ({self.dealer_cards[0].value} + ?)", True, (255, 255, 255), None)
    self.dealer_cards_value_text_rect = self.dealer_cards_value_text.get_rect()
    self.dealer_cards_value_text_rect.center = (WINDOW_WIDTH//2, 275)

    #Creates balance and profit texts
    self.balance_display_text = self.font_card_values.render(f'Balance: ${self.balance}', True, (255, 255, 255), None)
    self.balance_display_text_rect = self.balance_display_text.get_rect()
    self.balance_display_text_rect.center = self.balance_display_bg.center

    if self.profit > 0:
      self.color_profit_text = (12, 250, 0)
      self.profit_text_op = '+'
    elif self.profit < 0:
      self.color_profit_text = (255, 0, 0)
      self.profit_text_op = '-'
    else:
      self.color_profit_text = (255, 255, 255)
      self.profit_text_op = '+'
    self.profit_display_text = self.font_card_values.render(f'Profit: {self.profit_text_op}{self.profit}%', True, self.color_profit_text, None)
    self.profit_display_text_rect = self.profit_display_text.get_rect()
    self.profit_display_text_rect.center = self.profit_display_bg.center

    self.current_bet_display_text = self.font_card_values.render(f'Bet: ${self.current_bet}', True, (255, 255, 255), None)
    self.current_bet_display_text_rect = self.current_bet_display_text.get_rect()
    self.current_bet_display_text_rect.center = self.current_bet_display_bg.center

    # Updates save screen display and exits
    if self.p_save_prompt:
      self.save_prompt_no.update((255, 87, 84), (163, 8, 5), mousePos, self.mouseIsDown)
      self.save_prompt_yes.update((121, 255, 94), (24, 143, 0), mousePos, self.mouseIsDown)
      if self.save_prompt_no.check_press(mousePos, mouseUp):
        self.save = False
      if self.save_prompt_yes.check_press(mousePos, mouseUp):
        self.save = True
      self.path = Path('data/save.json')
      if self.save:
        self.contents = json.dumps([balance + self.current_bet, highest_balance])
        self.path.write_text(self.contents)
        self.end = True
      elif self.save == False:
        self.end = True
      if self.end:
        pygame.quit()
        sys.exit()



    # Runs when the player needs to enter a bet
    if self.p_enter_bet and self.p_save_prompt == False:
      self.bet_box_btn.update((96, 255, 77), (24, 168, 7), mousePos, self.mouseIsDown)
      if self.bet_box.user_input != "" and self.bet_box_btn.check_press(mousePos, mouseUp):
        if int(self.bet_box.user_input) <= self.balance and int(self.bet_box.user_input) >= 0:
          self.p_enter_bet = False
          self.current_bet = int(self.bet_box.user_input)
          self.balance -= self.current_bet
          self.p_hit_or_stay = True
          self.p_show_basic = True

    
    # Runs when the cards and player buttons appear
    if self.p_hit_or_stay and self.p_save_prompt == False:
      for self.card in self.player_cards:
        self.card.shown = True
      self.dealer_cards[0].shown = True

      self.hit_button.update((255, 71, 71), (133, 0, 0), mousePos, self.mouseIsDown)
      if self.hit_button.check_press(mousePos, mouseUp):
        draw_card(self.player_cards)
        if compute(self.player_cards) != 'bust':
          pass
        else:
          self.p_hit_or_stay = False
          self.status = 'bust'
      
      self.stay_button.update((100, 100, 100), (51, 51, 51), mousePos, self.mouseIsDown)
      if self.stay_button.check_press(mousePos, mouseUp):
        self.p_hit_or_stay = False
        self.status = 'play'


    # Runs after player stays w/ good hand
    if self.status == 'play' and self.p_save_prompt == False:
      self.frames += 1
      if self.frames >= 60:
        self.show_dealer_cards = True
        self.dealer_cards[1].shown = True

        if self.frames % 60 == 0 and self.frames > 60:
          if self.dealer_cards_value != 'bust' and self.dealer_cards_value <= 16:
            draw_card(self.dealer_cards)
          elif self.dealer_cards_value == 'bust':
            self.status = 'win'
            self.frames = 0
          else:
            if self.dealer_cards_value < self.player_cards_value:
              self.status = 'win'
              self.frames = 0
            elif self.dealer_cards_value == self.player_cards_value:
              self.status = 'tie'
              self.frames = 0
            else:
              self.status = 'lost'
              self.frames = 0
    
    # Runs after the outcome of the hand is decided
    if self.p_save_prompt == False:
      if self.status == 'win':
        pygame.mixer.Sound.play(sfx_won)
        self.result_display = f"+${self.current_bet}"
        self.result_display_color = (12, 255, 0)
        self.balance += self.current_bet * 2
        self.profit = self.balance // 10 - 100
        self.current_bet = 0
        self.status = None
      elif self.status == 'tie':
        self.result_display_color = (255, 255, 255)
        self.result_display = f"+$0"
        self.balance += self.current_bet
        self.current_bet = 0
        self.status = None
      elif self.status == 'lost' or self.status == 'bust':
        pygame.mixer.Sound.play(sfx_lost)
        self.result_display_color = (255, 0, 0)
        self.result_display = f"-${self.current_bet}"
        self.profit = self.balance // 10 - 100
        self.current_bet = 0
        self.status = None
    
    # Runs to display results and reset
    if self.status == None and self.p_save_prompt == False:
      self.result_display_font = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', self.result_display_font_size)
      self.result_display_text = self.result_display_font.render(self.result_display, True, self.result_display_color, None)
      self.result_display_text_rect = self.result_display_text.get_rect()
      self.result_display_text_rect.midtop = (WINDOW_WIDTH//2, self.display_y)

      if self.temp == False:
        if self.result_display_text_rect.centery > 350:
          self.display_y -= 10
          self.result_display_font_size += 2
        else:
          self.frames = 0
          self.temp = True
      if self.temp == True:
        if self.frames >= 60:
          if self.result_display_text_rect.midtop[1] < WINDOW_HEIGHT:
            self.display_y += 10
            self.result_display_font_size -= 2
          else:
            self.frames = -2
      self.frames += 1
      if self.frames == -1:
        if self.balance == 0:
          return 'lost'
        else:
          return 'end_hand'


        

    """RENDER GAME ELEMENTS"""
    WINDOW.fill(COLOR_BACKGROUND)
    
    # Displays elements in the bottom bar
    pygame.draw.rect(WINDOW, self.COLOR_BOTTOM_BAR, self.bottom_bar)
    pygame.draw.rect(WINDOW, self.COLOR_BOTTOM_BAR_BG, self.balance_display_bg)
    pygame.draw.rect(WINDOW, self.COLOR_BOTTOM_BAR_BG, self.profit_display_bg)
    pygame.draw.rect(WINDOW, self.COLOR_BOTTOM_BAR_BG, self.current_bet_display_bg)
    WINDOW.blit(self.balance_display_text, self.balance_display_text_rect)
    WINDOW.blit(self.profit_display_text, self.profit_display_text_rect)
    WINDOW.blit(self.current_bet_display_text, self.current_bet_display_text_rect)

    # Displays the backgrounds of the cards
    pygame.draw.rect(WINDOW, self.COLOR_PLAYER_CARD_BG, self.player_cards_bg, 0, 0, 10, 10, 0, 0)
    pygame.draw.rect(WINDOW, self.COLOR_PLAYER_CARD_BG, self.dealer_cards_bg, 0, 0, 0, 0, 10, 10)

    # Displays the Buttons
    if self.p_hit_or_stay:
      self.hit_button.draw(WINDOW)
      self.stay_button.draw(WINDOW)

    # Displays the cards
    for card in self.player_cards:
      card.draw(WINDOW)
    for card in self.dealer_cards:
      card.draw(WINDOW)

    # Creates the text that shows the values of the hands
    if self.p_show_basic:
      WINDOW.blit(self.player_cards_value_text, self.player_cards_value_text_rect)
      WINDOW.blit(self.dealer_cards_value_text, self.dealer_cards_value_text_rect)

    # Creates the betting box
    if self.p_enter_bet:
      self.bet_box.draw(WINDOW)
      self.bet_box_btn.draw(WINDOW)
      pygame.draw.line(WINDOW, (27, 99, 31), (self.bet_box_btn.x+15, self.bet_box_btn.y+45), (self.bet_box_btn.x+self.bet_box_btn.width//2-10, self.bet_box_btn.y+self.bet_box_btn.height-15), 10)
      pygame.draw.line(WINDOW, (27, 99, 31), (self.bet_box_btn.x+self.bet_box_btn.width//2-10, self.bet_box_btn.y+self.bet_box_btn.height-15), (self.bet_box_btn.x+self.bet_box_btn.width-20, self.bet_box_btn.y+15), 10)
    
    # Result Display
    if self.status == None:
      WINDOW.blit(self.result_display_text, self.result_display_text_rect)

    # Display Misc.
    pygame.draw.line(WINDOW, (247, 194, 2), (0, 700), (WINDOW_WIDTH, 700), 5)

    # Save Prompt
    if self.p_save_prompt:
      pygame.draw.rect(WINDOW, (100, 100, 100), self.save_display_bg)
      pygame.draw.rect(WINDOW, (0, 0, 0), self.save_display_bg, 5)
      WINDOW.blit(self.save_display_text, self.save_display_text_rect)
      self.save_prompt_yes.draw(WINDOW)
      self.save_prompt_no.draw(WINDOW)

    pygame.display.update()
    fpsClock.tick(FPS)



class end_screen():
  def __init__(self):

    # Misc
    self.COLOR_END_SCREEN_BG = (212, 13, 6)
    self.COLOR_OUTLINE = (107, 4, 0)
    self.outline = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Game Over Text
    self.game_over_text_font = pygame.font.Font('data/fonts/ChicagoPolice-w1deZ.ttf', 140)
    self.game_over_text = self.game_over_text_font.render('GAME OVER', True, self.COLOR_OUTLINE, None)
    self.game_over_text_rect = self.game_over_text.get_rect()
    self.game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//7*2)

    # Score Text
    self.score_text_font = pygame.font.Font('data/fonts/Heavitas.ttf', 40)

    # Play Again Text
    self.play_text_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
    self.play_text = self.play_text_font.render(f'Play Again?', True, self.COLOR_OUTLINE, None)
    self.play_text_rect = self.play_text.get_rect()
    self.play_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//13*8)

    # Buttons
    self.play_again_button = Button((WINDOW_WIDTH//2-250, 525), (500, 100), (235, 98, 0))
    self.play_again_button.add_border(10, self.COLOR_OUTLINE)

    # New background
    self.new_bg = pygame.Rect(0, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Phases
    self.button_pressed = False

    # Misc
    self.mouseIsDown = False

  """MAIN GAME LOOP"""
  def run(self, highest_balance, events):
    self.highest_balance = highest_balance

    mouseUp = False
    """USER INPUT"""
    mousePos = pygame.mouse.get_pos()
    for event in events:
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        self.mouseIsDown = True
      if event.type == MOUSEBUTTONUP:
        self.mouseIsDown = False
        mouseUp = True
    


    """PROCESSING"""
    self.play_again_button.update((255, 155, 84), (145, 60, 0), mousePos, self.mouseIsDown)
    if self.play_again_button.check_press(mousePos, mouseUp):
      self.button_pressed = True
    
    if self.button_pressed:
      self.new_bg.y -= 5
      if self.new_bg.y <= 0:
        return "starting_screen"
    
    self.score_text = self.score_text_font.render(f'Highest Balance: (${self.highest_balance})', True, self.COLOR_OUTLINE, None)
    self.score_text_rect = self.score_text.get_rect()
    self.score_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//7*3)


 
    """RENDER GAME ELEMENTS"""
    WINDOW.fill(self.COLOR_END_SCREEN_BG)

    pygame.draw.rect(WINDOW, self.COLOR_OUTLINE, self.outline, 40)

    WINDOW.blit(self.game_over_text, self.game_over_text_rect)
    pygame.draw.line(WINDOW, self.COLOR_OUTLINE, (200, 300), (WINDOW_WIDTH-200, 300), 10)
    WINDOW.blit(self.score_text, self.score_text_rect)
    WINDOW.blit(self.play_text, self.play_text_rect)

    self.play_again_button.draw(WINDOW)

    pygame.draw.rect(WINDOW, COLOR_BACKGROUND, self.new_bg)

    pygame.display.update()
    fpsClock.tick(FPS)

    return "end_screen"




# Loads save data if applicable
path = Path('data/save.json')
contents = path.read_text()
data = json.loads(contents)

balance = data[0]
highest_balance = data[1]
profit = balance // 10 - 100

deck = ['ac', 'ah', 'ad', 'as', '2c', '2h', '2d', '2s', '3c', '3h', '3d', '3s', '4c', '4h', '4d', '4s', '5c', '5h', 
        '5d', '5s', '6c', '6h', '6d', '6s', '7c', '7h', '7d', '7s', '8c', '8h', '8d', '8s', '9c', '9h', '9d', '9s', 
        'tc', 'th', 'td', 'ts', 'jc', 'jh', 'jd', 'js', 'qc', 'qh', 'qd', 'qs', 'kc', 'kh', 'kd', 'ks']

pygame.mixer.music.play(-1)

async def main():
  current_screen = "starting_screen"
  global balance
  global highest_balance
  global profit
  global deck
  ms = main_screen(balance, profit, deck)
  es = end_screen()
  ss_in = True
  ms_in = True
  es_in = True

  # Handles which screens show up
  while True:
    """Gets Events"""
    events = []
    for event in pygame.event.get() :
      events.append(event)

    if current_screen == 'starting_screen':
      if ss_in:
        ss = starting_screen()
        ss_in = False
      current_screen = ss.run(events)

    if current_screen == 'main_screen':
      if ms_in:
        ms = main_screen(balance, profit, deck)
        ms_in = False
      state = ms.run(events)
      balance = ms.balance
      profit = ms.profit
      if state == 'end_hand':
        print(deck)
        deck = ['ac', 'ah', 'ad', 'as', '2c', '2h', '2d', '2s', '3c', '3h', '3d', '3s', '4c', '4h', '4d', '4s', '5c', '5h', 
          '5d', '5s', '6c', '6h', '6d', '6s', '7c', '7h', '7d', '7s', '8c', '8h', '8d', '8s', '9c', '9h', '9d', '9s', 
          'tc', 'th', 'td', 'ts', 'jc', 'jh', 'jd', 'js', 'qc', 'qh', 'qd', 'qs', 'kc', 'kh', 'kd', 'ks']
        ms = main_screen(balance, profit, deck)
      if balance > highest_balance:
        highest_balance = balance
      if state == 'lost':
        path = Path('data/save.json')
        contents = json.dumps([1000, 1000])
        path.write_text(contents)
        current_screen = "end_screen"

    if current_screen == 'end_screen':
      if es_in:
        es = end_screen()
        es_in = False
      if balance == 0:
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(sfx_end)
      balance = 1000
      profit = 0
      current_screen = es.run(highest_balance, events)
      if current_screen == 'starting_screen':
        highest_balance = 1000
        pygame.mixer.music.play(-1)
        ss_in = True
        ms_in = True
        es_in = True
    
    await asyncio.sleep(0)

asyncio.run(main())