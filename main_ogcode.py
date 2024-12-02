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
def starting_screen():

  """Prepares Variables"""

  # colors
  COLOR_SS_BACKGROUND = COLOR_BACKGROUND
  COLOR_SS_TITLE = (255, 195, 43)
  COLOR_SS_TITLE_BACKGROUND = (35, 196, 44)
  COLOR_SS_PLAYBUTTON = (222, 138, 20)
  COLOR_SS_PLAYBUTTON_HOVER = (250, 179, 80)
  COLOR_SS_PLAYBUTTON_PRESS = (189, 112, 4)
  COLOR_SS_PLAYBUTTON_TEXT = (255, 255, 255)

  # title
  SS_TITLE_FONT = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', 150)
  ss_title = SS_TITLE_FONT.render('BLACKJACK', True, COLOR_SS_TITLE, None)
  ss_title_rect = ss_title.get_rect()
  ss_title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//4)

  # title backdrop
  ss_title_bg_rect = pygame.Rect(0, 0, ss_title_rect.width + 100, ss_title_rect.height + 50)
  ss_title_bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//4)

  # card animation
  card_speed = 8
  card_scale = 0.5

  # middle card
  ss_card1 = pygame.image.load('data/images/jack_of_spades.png').convert_alpha()
  ss_card1 = pygame.transform.scale(ss_card1, (ss_card1.get_width()*card_scale, ss_card1.get_height()*card_scale))
  ss_card1X = WINDOW_WIDTH//2 - ss_card1.get_width()//2
  ss_card1Y = WINDOW_HEIGHT

  # left card
  ss_card2 = pygame.image.load('data/images/ace_of_clubs.png').convert_alpha()
  ss_card2 = pygame.transform.scale(ss_card2, (ss_card2.get_width()*card_scale, ss_card2.get_height()*card_scale))
  ss_card2X = WINDOW_WIDTH//2 - ss_card1.get_width()//2 - 200
  ss_card2Y = WINDOW_HEIGHT
  ss_card2 = pygame.transform.rotate(ss_card2, 25)

  # right card
  ss_card3 = pygame.image.load('data/images/10_of_diamonds.png').convert_alpha()
  ss_card3 = pygame.transform.scale(ss_card3, (ss_card3.get_width()*card_scale, ss_card3.get_height()*card_scale))
  ss_card3X = WINDOW_WIDTH//2 - ss_card1.get_width()//2 + 90
  ss_card3Y = WINDOW_HEIGHT
  ss_card3 = pygame.transform.rotate(ss_card3, -25)

  # play button
  SS_PLAYBUTTON_TEXT_FONT = pygame.font.Font('data/fonts/MouldyCheeseRegular-WyMWG.ttf', 40)
  ss_playbutton = Button((WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2+30-40), (200, 80), COLOR_SS_PLAYBUTTON)
  ss_playbutton.add_border(3, COLOR_SS_PLAYBUTTON_TEXT)
  ss_playbutton.add_text(SS_PLAYBUTTON_TEXT_FONT, 'PLAY', COLOR_SS_PLAYBUTTON_TEXT)

  # Order of Animations
  cards_anim = True
  text_appear = False
  text_bg_appear = False
  text_bg_appear_a = False
  text_bg_appear_b = True
  playbutton_appear = False
  playbutton_appear_a = False
  playbutton_appear_b = True
  final_anim = False

  # Mouse States
  mouse_is_down = False
  mouse_up = False

  # Misc.
  LEAVE_SPEED = 10
  ss_delay = 0
  frames = 0

  while True:
    """EVENTS"""

    mouse_up = False
    for event in pygame.event.get() :
      if event.type == QUIT :  # Closes program if user exits
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:  # Checks if mouse is down
        mouse_is_down = True
      if event.type == pygame.MOUSEBUTTONUP:  # Checks if mouse has been released
        mouse_is_down = False
        mouse_up = True
    
    mousePos = pygame.mouse.get_pos()  # Gets position of mouse



    """PROCESSING"""
    # Changes color of button based on state
    if playbutton_appear == True:
      ss_playbutton.update(COLOR_SS_PLAYBUTTON_HOVER, COLOR_SS_PLAYBUTTON_PRESS, mousePos, mouse_is_down)
    
    # Checks if the button has been pressed
    if ss_playbutton.check_press(mousePos, mouse_up):
      final_anim = True

    # Animates the Cards
    if cards_anim == True:
      if ss_card1Y >= WINDOW_HEIGHT//3*2:
        ss_card1Y -= card_speed
        ss_card2Y -= card_speed
        ss_card3Y -= card_speed
        frames = 0
      else:
        frames += 1
        if frames == 30:
          text_bg_appear = True
          cards_anim = False
          frames = 0

    """DISPLAY"""
    WINDOW.fill(COLOR_SS_BACKGROUND)

    WINDOW.blit(ss_card2, (ss_card2X, ss_card2Y))
    WINDOW.blit(ss_card3, (ss_card3X, ss_card3Y))
    WINDOW.blit(ss_card1, (ss_card1X, ss_card1Y))

    # Runs when the title background needs to appear
    if text_bg_appear == True:
      pygame.draw.rect(WINDOW, COLOR_SS_TITLE_BACKGROUND, ss_title_bg_rect)
      if text_bg_appear_b == True:
        text_bg_appear_a = True
        text_bg_appear_b = False

    # Runs when the text needs to appear
    if text_appear == True:
      WINDOW.blit(ss_title, ss_title_rect)
      if playbutton_appear_b == True:
        playbutton_appear_a = True
        playbutton_appear_b = False
    
    # Runs when the button needs to appear
    if playbutton_appear == True:
      ss_playbutton.draw(WINDOW)

    pygame.display.update()
    fpsClock.tick(FPS)

    # Runs after the player has clicked the play button
    if final_anim == True:
      ss_title_bg_rect.y -= LEAVE_SPEED
      ss_title_rect.y -= LEAVE_SPEED
      ss_playbutton.y -= LEAVE_SPEED
      ss_card1Y += LEAVE_SPEED
      ss_card2Y += LEAVE_SPEED
      ss_card3Y += LEAVE_SPEED
      if ss_playbutton.y + ss_playbutton.height <= 0:
        ss_delay += 1
        if ss_delay == 60:
          ss_delay = 0
          break

    # Activates the next part after waiting
    if text_bg_appear_a == True:
      frames += 1
      if frames == 30:
        text_appear = True
        frames = 0
        text_bg_appear_a = False
    if playbutton_appear_a == True:
      frames += 1
      if frames == 30:
        playbutton_appear = True
        playbutton_appear_a = False
        frames = 0
      












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
def main (balance, profit) :
  looping = True

  """GAME VARIABLES"""

  # Colors
  COLOR_PLAYER_CARD_BG = (18, 84, 21)
  COLOR_BOTTOM_BAR = (105, 105, 105)
  COLOR_BOTTOM_BAR_BG = (125, 125, 125)

  # Screen Elements
  font_card_values = pygame.font.Font('data/fonts/coolvetica rg.otf', 30)


  # Bottom Bar
  bottom_bar = pygame.Rect(0, WINDOW_HEIGHT-100, WINDOW_WIDTH, 100)
  balance_display_bg = pygame.Rect(0, 0, 300, 60)
  balance_display_bg.center = (WINDOW_WIDTH//5, 750)
  profit_display_bg = pygame.Rect(0, 0, 300, 60)
  profit_display_bg.center = (WINDOW_WIDTH//5*4, 750)
  current_bet_display_bg = pygame.Rect(0, 0, 300, 60)
  current_bet_display_bg.center = (WINDOW_WIDTH//2, 750)

  # Bet Box
  bet_box_rect = pygame.Rect(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 500, 75)
  bet_box_rect.center = (WINDOW_WIDTH//2-50, (WINDOW_HEIGHT-100)//2)
  bet_box_font = pygame.font.Font('data/fonts/Money-w16D8.ttf', 45)
  numbers = [num for num in string.digits]
  bet_box = Textbox(bet_box_rect, COLOR_PLAYER_CARD_BG, bet_box_font, (222, 168, 31), 20, 2, whitelist=numbers, prefix='$ ')
  bet_box.add_border(5, (222, 168, 31))
  bet_box.add_description('Enter Bet Here')

  bet_box_btn_font = pygame.font.SysFont('data/fonts/Blackjack-nA1R.ttf', 40)
  bet_box_btn = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (75, 75), (4, 204, 17))
  bet_box_btn.x = WINDOW_WIDTH//2+300-75
  bet_box_btn.y = (WINDOW_HEIGHT-100)//2-75//2
  bet_box_btn.add_border(5, (27, 99, 31))
  


  # Action Buttons
  hit_button = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (200, 60), (255, 0, 0))
  hit_button.add_border(4, (255, 255, 255))
  hit_button_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
  hit_button.add_text(hit_button_font, 'HIT', (255, 255, 255))
  hit_button.change_center((WINDOW_WIDTH//2-125, (WINDOW_HEIGHT-100)//2))

  stay_button = Button((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), (200, 60), (0, 0, 0))
  stay_button.add_border(4, (255, 255, 255))
  stay_button_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
  stay_button.add_text(stay_button_font, 'STAY', (255, 255, 255))
  stay_button.change_center((WINDOW_WIDTH//2+125, (WINDOW_HEIGHT-100)//2))

  # Card Positions
  pos_player_card_left = (WINDOW_WIDTH//2-166, WINDOW_HEIGHT-342)
  pos_player_card_right = (WINDOW_WIDTH//2, WINDOW_HEIGHT-342)
  pos_dealer_card_left = (WINDOW_WIDTH//2-166, 0)
  pos_dealer_card_right = (WINDOW_WIDTH//2, 0)

  # Cards
  player_cards = []
  player_cards.append(Card(deck, pos_player_card_left, False))
  player_cards.append(Card(deck, pos_player_card_right, False))
  dealer_cards = []
  dealer_cards.append(Card(deck, pos_dealer_card_left, False))
  dealer_cards.append(Card(deck, pos_dealer_card_right, False))

  # Result Display
  result_display = ""
  result_display_font_size = 5
  display_y = WINDOW_HEIGHT

  # Save Prompt
  save_display_bg = pygame.Rect(0, 0, WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
  save_display_bg.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
  save_display_font = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', 40)
  save_display_text = save_display_font.render('Do You Want to Save?', True, (255, 255, 255), None)
  save_display_text_rect = save_display_text.get_rect()
  save_display_text_rect.centerx = save_display_bg.centerx
  save_display_text_rect.centery = save_display_bg.centery - 50

  save_prompt_yes = Button((0, 0), (100, 100), (8, 232, 0))
  save_prompt_yes.add_border(5, (7, 105, 3))
  save_prompt_yes.change_center((WINDOW_WIDTH//2-100, WINDOW_HEIGHT//3+200))
  save_prompt_no = Button((0, 0), (100, 100), (255, 4, 0))
  save_prompt_no.add_border(5, (79, 1, 0))
  save_prompt_no.change_center((WINDOW_WIDTH//2+100, WINDOW_HEIGHT//3+200))



  # Misc
  mouseUp = False
  mouseIsDown = False
  mouseDown = False
  current_bet = 0
  status = ''
  frames = 0
  save = None


  # Phases
  p_show_basic = False
  p_enter_bet = True
  p_hit_or_stay = False
  show_dealer_cards = False
  temp = False
  p_save_prompt = False

  #Updates beforehand
  #bet_box.update(mousePos, mouseDown, (49, 163, 54), event)
  
  """MAIN GAME LOOP"""
  while looping :

    """USER INPUT"""
    mouseUp = False
    mouseDown = False
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get() :

      if event.type == MOUSEBUTTONDOWN:
        mouseIsDown = True
        mouseDown = True
      if event.type == MOUSEBUTTONUP:
        mouseIsDown = False
        mouseUp = True
      if event.type == QUIT :
        # Asks if the user wants to save
        end = False
        p_save_prompt = True
      
      if p_enter_bet and p_save_prompt == False:
        bet_box.update(mousePos, mouseDown, (49, 163, 54), event)

    


    """PROCESSING"""
    
    # Creates the background for the cards
    player_cards_bg = pygame.Rect(WINDOW_WIDTH//2-200, WINDOW_HEIGHT-400, 68+len(player_cards)*166, 300)
    dealer_cards_bg = pygame.Rect(WINDOW_WIDTH//2-200, 0, 68+len(dealer_cards)*166, 300)
    player_cards_bg.centerx = WINDOW_WIDTH//2
    dealer_cards_bg.centerx = WINDOW_WIDTH//2

    # Creates the text above the player's cards
    player_cards_value = compute(player_cards)
    player_cards_value_text = font_card_values.render(f"Your Cards' Value: ({player_cards_value})", True, (255, 255, 255), None)
    player_cards_value_text_rect = player_cards_value_text.get_rect()
    player_cards_value_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-375)

    #Creates the text below the dealer's cards
    dealer_cards_value = compute(dealer_cards)
    if show_dealer_cards:
      dealer_cards_value_text = font_card_values.render(f"Dealer Cards' Value: ({dealer_cards_value})", True, (255, 255, 255), None)
    else:
      dealer_cards_value_text = font_card_values.render(f"Dealer Cards' Value: ({dealer_cards[0].value} + ?)", True, (255, 255, 255), None)
    dealer_cards_value_text_rect = dealer_cards_value_text.get_rect()
    dealer_cards_value_text_rect.center = (WINDOW_WIDTH//2, 275)

    #Creates balance and profit texts
    balance_display_text = font_card_values.render(f'Balance: ${balance}', True, (255, 255, 255), None)
    balance_display_text_rect = balance_display_text.get_rect()
    balance_display_text_rect.center = balance_display_bg.center

    if profit > 0:
      color_profit_text = (12, 250, 0)
      profit_text_op = '+'
    elif profit < 0:
      color_profit_text = (255, 0, 0)
      profit_text_op = '-'
    else:
      color_profit_text = (255, 255, 255)
      profit_text_op = '+'
    profit_display_text = font_card_values.render(f'Profit: {profit_text_op}{profit}%', True, color_profit_text, None)
    profit_display_text_rect = profit_display_text.get_rect()
    profit_display_text_rect.center = profit_display_bg.center

    current_bet_display_text = font_card_values.render(f'Bet: ${current_bet}', True, (255, 255, 255), None)
    current_bet_display_text_rect = current_bet_display_text.get_rect()
    current_bet_display_text_rect.center = current_bet_display_bg.center

    # Updates save screen display and exits
    if p_save_prompt:
      save_prompt_no.update((255, 87, 84), (163, 8, 5), mousePos, mouseIsDown)
      save_prompt_yes.update((121, 255, 94), (24, 143, 0), mousePos, mouseIsDown)
      if save_prompt_no.check_press(mousePos, mouseUp):
        save = False
      if save_prompt_yes.check_press(mousePos, mouseUp):
        save = True
      path = Path('data/save.json')
      if save:
        contents = json.dumps([balance + current_bet, highest_balance])
        path.write_text(contents)
        end = True
      elif save == False:
        end = True
      if end:
        pygame.quit()
        sys.exit()



    # Runs when the player needs to enter a bet
    if p_enter_bet and p_save_prompt == False:
      bet_box_btn.update((96, 255, 77), (24, 168, 7), mousePos, mouseIsDown)
      if bet_box.user_input != "" and bet_box_btn.check_press(mousePos, mouseUp):
        if int(bet_box.user_input) <= balance and int(bet_box.user_input) >= 0:
          p_enter_bet = False
          current_bet = int(bet_box.user_input)
          balance -= current_bet
          p_hit_or_stay = True
          p_show_basic = True

    
    # Runs when the cards and player buttons appear
    if p_hit_or_stay and p_save_prompt == False:
      for card in player_cards:
        card.shown = True
      dealer_cards[0].shown = True

      hit_button.update((255, 71, 71), (133, 0, 0), mousePos, mouseIsDown)
      if hit_button.check_press(mousePos, mouseUp):
        draw_card(player_cards)
        if compute(player_cards) != 'bust':
          pass
        else:
          p_hit_or_stay = False
          status = 'bust'
      
      stay_button.update((100, 100, 100), (51, 51, 51), mousePos, mouseIsDown)
      if stay_button.check_press(mousePos, mouseUp):
        p_hit_or_stay = False
        status = 'play'


    # Runs after player stays w/ good hand
    if status == 'play' and p_save_prompt == False:
      frames += 1
      if frames >= 60:
        show_dealer_cards = True
        dealer_cards[1].shown = True

        if frames % 60 == 0 and frames > 60:
          if dealer_cards_value != 'bust' and dealer_cards_value <= 16:
            draw_card(dealer_cards)
          elif dealer_cards_value == 'bust':
            status = 'win'
            frames = 0
          else:
            if dealer_cards_value < player_cards_value:
              status = 'win'
              frames = 0
            elif dealer_cards_value == player_cards_value:
              status = 'tie'
              frames = 0
            else:
              status = 'lost'
              frames = 0
    
    # Runs after the outcome of the hand is decided
    if p_save_prompt == False:
      if status == 'win':
        pygame.mixer.Sound.play(sfx_won)
        result_display = f"+${current_bet}"
        result_display_color = (12, 255, 0)
        balance += current_bet * 2
        profit = balance // 10 - 100
        current_bet = 0
        status = None
      elif status == 'tie':
        result_display_color = (255, 255, 255)
        result_display = f"+$0"
        balance += current_bet
        current_bet = 0
        status = None
      elif status == 'lost' or status == 'bust':
        pygame.mixer.Sound.play(sfx_lost)
        result_display_color = (255, 0, 0)
        result_display = f"-${current_bet}"
        profit = balance // 10 - 100
        current_bet = 0
        status = None
    
    # Runs to display results and reset
    if status == None and p_save_prompt == False:
      result_display_font = pygame.font.Font('data/fonts/Blackjack-nA1R.ttf', result_display_font_size)
      result_display_text = result_display_font.render(result_display, True, result_display_color, None)
      result_display_text_rect = result_display_text.get_rect()
      result_display_text_rect.midtop = (WINDOW_WIDTH//2, display_y)

      if temp == False:
        if result_display_text_rect.centery > 350:
          display_y -= 10
          result_display_font_size += 2
        else:
          frames = 0
          temp = True
      if temp == True:
        if frames >= 60:
          if result_display_text_rect.midtop[1] < WINDOW_HEIGHT:
            display_y += 10
            result_display_font_size -= 2
          else:
            frames = -2
      frames += 1
      if frames == -1:
        return balance, profit


        
 
    """RENDER GAME ELEMENTS"""
    WINDOW.fill(COLOR_BACKGROUND)
    
    # Displays elements in the bottom bar
    pygame.draw.rect(WINDOW, COLOR_BOTTOM_BAR, bottom_bar)
    pygame.draw.rect(WINDOW, COLOR_BOTTOM_BAR_BG, balance_display_bg)
    pygame.draw.rect(WINDOW, COLOR_BOTTOM_BAR_BG, profit_display_bg)
    pygame.draw.rect(WINDOW, COLOR_BOTTOM_BAR_BG, current_bet_display_bg)
    WINDOW.blit(balance_display_text, balance_display_text_rect)
    WINDOW.blit(profit_display_text, profit_display_text_rect)
    WINDOW.blit(current_bet_display_text, current_bet_display_text_rect)

    # Displays the backgrounds of the cards
    pygame.draw.rect(WINDOW, COLOR_PLAYER_CARD_BG, player_cards_bg, 0, 0, 10, 10, 0, 0)
    pygame.draw.rect(WINDOW, COLOR_PLAYER_CARD_BG, dealer_cards_bg, 0, 0, 0, 0, 10, 10)

    # Displays the Buttons
    if p_hit_or_stay:
      hit_button.draw(WINDOW)
      stay_button.draw(WINDOW)

    # Displays the cards
    for card in player_cards:
      card.draw(WINDOW)
    for card in dealer_cards:
      card.draw(WINDOW)

    # Creates the text that shows the values of the hands
    if p_show_basic:
      WINDOW.blit(player_cards_value_text, player_cards_value_text_rect)
      WINDOW.blit(dealer_cards_value_text, dealer_cards_value_text_rect)

    # Creates the betting box
    if p_enter_bet:
      bet_box.draw(WINDOW)
      bet_box_btn.draw(WINDOW)
      pygame.draw.line(WINDOW, (27, 99, 31), (bet_box_btn.x+15, bet_box_btn.y+45), (bet_box_btn.x+bet_box_btn.width//2-10, bet_box_btn.y+bet_box_btn.height-15), 10)
      pygame.draw.line(WINDOW, (27, 99, 31), (bet_box_btn.x+bet_box_btn.width//2-10, bet_box_btn.y+bet_box_btn.height-15), (bet_box_btn.x+bet_box_btn.width-20, bet_box_btn.y+15), 10)
    
    # Result Display
    if status == None:
      WINDOW.blit(result_display_text, result_display_text_rect)

    # Display Misc.
    pygame.draw.line(WINDOW, (247, 194, 2), (0, 700), (WINDOW_WIDTH, 700), 5)

    # Save Prompt
    if p_save_prompt:
      pygame.draw.rect(WINDOW, (100, 100, 100), save_display_bg)
      pygame.draw.rect(WINDOW, (0, 0, 0), save_display_bg, 5)
      WINDOW.blit(save_display_text, save_display_text_rect)
      save_prompt_yes.draw(WINDOW)
      save_prompt_no.draw(WINDOW)

    pygame.display.update()
    fpsClock.tick(FPS)




def end_screen(highest_balance):
  looping = True

  # Misc
  COLOR_END_SCREEN_BG = (212, 13, 6)
  COLOR_OUTLINE = (107, 4, 0)
  outline = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

  # Game Over Text
  game_over_text_font = pygame.font.Font('data/fonts/ChicagoPolice-w1deZ.ttf', 140)
  game_over_text = game_over_text_font.render('GAME OVER', True, COLOR_OUTLINE, None)
  game_over_text_rect = game_over_text.get_rect()
  game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//7*2)

  # Score Text
  score_text_font = pygame.font.Font('data/fonts/Heavitas.ttf', 40)
  score_text = score_text_font.render(f'Highest Balance: (${highest_balance})', True, COLOR_OUTLINE, None)
  score_text_rect = score_text.get_rect()
  score_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//7*3)

  # Play Again Text
  play_text_font = pygame.font.Font('data/fonts/Heavitas.ttf', 30)
  play_text = play_text_font.render(f'Play Again?', True, COLOR_OUTLINE, None)
  play_text_rect = play_text.get_rect()
  play_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//13*8)

  # Buttons
  play_again_button = Button((WINDOW_WIDTH//2-250, 525), (500, 100), (235, 98, 0))
  play_again_button.add_border(10, COLOR_OUTLINE)

  # New background
  new_bg = pygame.Rect(0, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT)

  # Phases
  button_pressed = False

  # Misc
  mouseIsDown = False

  """MAIN GAME LOOP"""
  while looping :

    mouseUp = False
    """USER INPUT"""
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        mouseIsDown = True
      if event.type == MOUSEBUTTONUP:
        mouseIsDown = False
        mouseUp = True
    


    """PROCESSING"""
    play_again_button.update((255, 155, 84), (145, 60, 0), mousePos, mouseIsDown)
    if play_again_button.check_press(mousePos, mouseUp):
      button_pressed = True
    
    if button_pressed:
      new_bg.y -= 5
      if new_bg.y <= 0:
        looping = False


 
    """RENDER GAME ELEMENTS"""
    WINDOW.fill(COLOR_END_SCREEN_BG)

    pygame.draw.rect(WINDOW, COLOR_OUTLINE, outline, 40)

    WINDOW.blit(game_over_text, game_over_text_rect)
    pygame.draw.line(WINDOW, COLOR_OUTLINE, (200, 300), (WINDOW_WIDTH-200, 300), 10)
    WINDOW.blit(score_text, score_text_rect)
    WINDOW.blit(play_text, play_text_rect)

    play_again_button.draw(WINDOW)

    pygame.draw.rect(WINDOW, COLOR_BACKGROUND, new_bg)

    pygame.display.update()
    fpsClock.tick(FPS)




# Loads save data if applicable
path = Path('data/save.json')
contents = path.read_text()
data = json.loads(contents)

balance = data[0]
highest_balance = data[1]
profit = balance // 10 - 100


# Handles which screens show up
while True:
  pygame.mixer.music.play(-1)
  starting_screen()
  while True:
    deck = ['ac', 'ah', 'ad', 'as', '2c', '2h', '2d', '2s', '3c', '3h', '3d', '3s', '4c', '4h', '4d', '4s', '5c', '5h', 
        '5d', '5s', '6c', '6h', '6d', '6s', '7c', '7h', '7d', '7s', '8c', '8h', '8d', '8s', '9c', '9h', '9d', '9s', 
        'tc', 'th', 'td', 'ts', 'jc', 'jh', 'jd', 'js', 'qc', 'qh', 'qd', 'qs', 'kc', 'kh', 'kd', 'ks']
    balance, profit = main(balance, profit)
    if balance > highest_balance:
      highest_balance = balance
    if balance == 0:
      path = Path('data/save.json')
      contents = json.dumps([1000, 1000])
      path.write_text(contents)

      balance = 1000
      profit = 0
      pygame.mixer.music.stop()
      pygame.mixer.Sound.play(sfx_end)
      end_screen(highest_balance)
      highest_balance = 1000
      break
