import pygame
import random
import cv2 as cv
import numpy as np




from pygame.version import SDLVersion
pygame.init()

# defining game parameters
screen_width=900
screen_height=600

# colors
white=(255,255,255)
blue=(0,0,255)
red=(255,0,0)
black=(0,0,0)

# Initialising a window for the game 
game_window=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption(" SANKE GAME ")
pygame.display.update()

obs_x=random.randint(20,screen_width-40)
obs_y=random.randint(20,screen_height-40)


obstacle=[]

 # defining a game loop
def game_loop():
    
    # game specific variables
    exit_game=False
    game_over=False
    # image=''
    snake_x=45
    snake_y=45
    velocity_x=0
    velocity_y=0
    # snake_size=15
    
    # Loading images like for background, snake body, food etc.
    bgimg=pygame.image.load("background images/background.png")
    bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
    # wall=pygame.image.load("background images/wall_img.png").convert_alpha()
    


    Head_Right=pygame.image.load("background images/head_right.png").convert_alpha()
    Head_left=pygame.image.load("background images/head_left.png").convert_alpha()
    Head_up=pygame.image.load("background images/head_up.png").convert_alpha()
    Head_down=pygame.image.load("background images/head_down.png").convert_alpha()

    body_horizontal=pygame.image.load("background images/body_horizontal.png").convert_alpha()
    body_vertical=pygame.image.load("background images/body_vertical.png").convert_alpha()
    
    tail_right=pygame.image.load("background images/tail_right.png").convert_alpha()
    tail_left=pygame.image.load("background images/tail_left.png").convert_alpha()
    tail_up=pygame.image.load("background images/tail_up.png").convert_alpha()
    tail_down=pygame.image.load("background images/tail_down.png").convert_alpha()

    body_tl=pygame.image.load("background images/body_tl.png").convert_alpha()
    body_bl=pygame.image.load("background images/body_bl.png").convert_alpha()
    body_br=pygame.image.load("background images/body_br.png").convert_alpha()
    body_tr=pygame.image.load("background images/body_tr.png").convert_alpha()

    food=pygame.image.load("background images/apple.png")
    food=pygame.transform.scale(food,(40,40)).convert_alpha()


    # choosing random coordinates every after when the food is eaten
    food_x=random.randint(20,screen_width-40)
    food_y=random.randint(20,screen_height-40)

    

    score=0
    fps=30
    clock = pygame.time.Clock()
    font=pygame.font.SysFont(None,55)

    def text_screen(text,color,x,y):
        screen_text= font.render(text,True,color) 
        game_window.blit(screen_text,[x,y])        

    # initialising a list for the coordinates of the snake body after every loop
    snk_list=[]
    snk_length=1  # initial length of snake is 1

    direction=''

    # creating functions for different shapes of hurdles
    def hurdle_1():
        pygame.draw.rect(game_window,black,[200,250,450,40])
        pygame.draw.rect(game_window,black,[450,100,40,400])
    def hurdle_2():
        pygame.draw.rect(game_window,black,[200,100,450,40])
        pygame.draw.rect(game_window,black,[650,100,40,400])
    def hurdle_3():
        pygame.draw.rect(game_window,black,[200,100,40,350])
        pygame.draw.rect(game_window,black,[200,450,450,40])
    def hurdle_4():
        pygame.draw.rect(game_window,black,[200,100,400,40])
        pygame.draw.rect(game_window,black,[200,100,40,400])
        pygame.draw.rect(game_window,black,[600,100,40,400])
    def hurdle_5():
        pygame.draw.rect(game_window,black,[450,100,40,340])
        pygame.draw.rect(game_window,black,[200,440,450,40])

    obstacle=[hurdle_1,hurdle_2,hurdle_3,hurdle_4,hurdle_5]
    obs=random.choice([0,1,2,3,4])
   

    index=0
    # while loop runs only when there is no chance of game over
    while not exit_game:

        if game_over:
            game_window.fill(white)
            text_screen("Game Over!! Press Enter to Continue ",red,100,100)
            for event in pygame.event.get():
                
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        game_loop()  # if player presses Enter then again run the game loop
            
        else:

            for event in pygame.event.get():
                
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    # various events possible for moving the snake
                    if event.key==pygame.K_RIGHT:
                        if direction!='left':
                            velocity_x= 5
                            velocity_y=0
                            direction="Right"
                      
                    if event.key==pygame.K_LEFT:
                        if direction!='Right':
                            velocity_x= - 5
                            velocity_y=0
                            direction="left"
                       
                    if event.key==pygame.K_UP:
                        if direction!='down':
                            velocity_x=0
                            velocity_y = - 5
                            direction="up"
                       
                    if event.key==pygame.K_DOWN:
                        if direction!='up':
                            velocity_x=0
                            velocity_y= 5
                            direction="down"
            
            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y

            # condition to check if snake has eaten the food or not
            if (abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15):
                score=score+1
                print("score: ",score)
                # generating random coordinates of food, so that it should not come over the hurdles
                if obs==0:
                    x1=random.randint(40,410)
                    x2=random.randint(500,screen_width-40)
                    food_x=random.choice([x1,x2])
                    y1=random.randint(40,210)
                    y2=random.randint(290,screen_height-40)
                    food_y=random.choice([y1,y2])
                
                elif obs==1:
                    x1=random.randint(40,610)
                    x2=random.randint(710,screen_width-40)
                    food_x=random.choice([24,x2])
                    y1=random.randint(40,100)
                    y2=random.randint(180,screen_height-40)
                    food_y=random.choice([y1,y2])

                elif obs==2:
                    x1=random.randint(40,160)
                    x2=random.randint(240,screen_width-40)
                    food_x=random.choice([x1,x2])
                    y1=random.randint(40,410)
                    y2=random.randint(490,screen_height-40)
                    food_y=random.choice([y1,y2])
                elif obs==3:
                    x1=random.randint(40,160)
                    x2=random.randint(280,560)
                    x3=random.randint(640,screen_width-40)
                    food_x=random.choice([x1,x2,x3])
                    y1=random.randint(40,60)
                    y2=random.randint(170,screen_height-40)
                    food_x=random.choice([y1,y2])
                elif obs==4:
                    x1=random.randint(40,410)
                    x2=random.randint(490,screen_width-40)
                    food_x=random.choice([x1,x2])
                    y1=random.randint(40,400)
                    y2=random.randint(480,screen_height-40)
                    food_y=random.choice([y1,y2])


                snk_length += 5 # increasing the length of snake after every time food is eaten
                index=index+1

            # blit backgroud image 
            game_window.blit(bgimg,(0,0))

            # creating the boundaries of screen
            pygame.draw.rect(game_window,black,[0,0,screen_width,40])
            pygame.draw.rect(game_window,black,[0,0,40,screen_height])
            pygame.draw.rect(game_window,black,[screen_width-40,0,40,screen_height])
            pygame.draw.rect(game_window,black,[0,screen_height-40,screen_width,40])

            obstacle[obs]()# calling the function of obstacles
            
            text_screen('score: '+str(score*10),red,5,5) # show the score on the window
        
            head=[]
            # apending the new position of snake
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            
            
            if (len(snk_list)>snk_length):
                del snk_list[0]

        # if head collides with its body or its coordinate matches with any in the list present then game over
            if head in snk_list[:-1]:
                game_over=True
            x=head[0]
            y=head[1]
            # if snake collides with the boundary
            if (y<40)or(y>screen_height-80)or(x<40) or (x>screen_width-40) :
                game_over=True

            # checking for collision with the obstacle
            if (obs==0):
                if((x>160 and x<650 and y>210 and y<290) or (x>410 and x<490 and y>60 and y<500)):
                    game_over=True
            elif(obs==1):
                if((x>160 and x<690 and y>100 and y<140) or (x>610 and x<690 and y>60 and y<500)):
                    game_over=True
            elif(obs==2):
                if((x>160 and x<240 and y>60 and y<490) or (x>160 and x<650 and y>410 and y<490) ):
                    game_over=True
            elif(obs==3):
                if((x>160 and x<640 and y>60 and y<180) or (x>160 and x<240 and y>60 and y<500) or 
                                                    (x>560 and x<640 and y>60 and y<540) ):
                    game_over=True
            elif(obs==4):
                if( (x>410 and x<490 and y>60 and y<440) or(x>160 and x<650 and y>400 and y<480) ):
                    game_over=True

            # blit image of food at random position generated
            game_window.blit(food,(food_x,food_y))
            
            # showing various configuration of head according to direction
            if direction=='Right':
                game_window.blit(Head_Right,snk_list[-1])
            elif direction=='left':
                game_window.blit(Head_left,snk_list[-1])
            elif direction=='up':
                game_window.blit(Head_up,snk_list[-1])
            elif direction=='down':
                game_window.blit(Head_down,snk_list[-1])
            else:
                game_window.blit(Head_Right,snk_list[-1])
            

            # conditions for showing different body images like straight part, curved part when snake takes turn
            if len(snk_list)>=3:
                i=1
                while(i<=(len(snk_list)-2)):

                    if ((snk_list[i-1][0]<snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) and
                        (snk_list[i+1][0]==snk_list[i][0] and snk_list[i+1][1]<snk_list[i][1]) ):
                        game_window.blit(body_tl,snk_list[i])
                    elif ((snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]<snk_list[i][1]) and
                        (snk_list[i+1][0]<snk_list[i][0] and snk_list[i+1][1]==snk_list[i][1]) ):
                        game_window.blit(body_tl,snk_list[i])

                    elif ((snk_list[i-1][0]>snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) and
                        (snk_list[i+1][0]==snk_list[i][0] and snk_list[i+1][1]<snk_list[i][1]) ):
                        game_window.blit(body_tr,snk_list[i])
                    elif ((snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]<snk_list[i][1]) and
                        (snk_list[i+1][0]>snk_list[i][0] and snk_list[i+1][1]==snk_list[i][1]) ):
                        game_window.blit(body_tr,snk_list[i])

                    elif ((snk_list[i-1][0]>snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) and
                        (snk_list[i+1][0]==snk_list[i][0] and snk_list[i+1][1]>snk_list[i][1]) ):
                        game_window.blit(body_br,snk_list[i])
                    elif ((snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]>snk_list[i][1]) and
                        (snk_list[i+1][0]>snk_list[i][0] and snk_list[i+1][1]==snk_list[i][1]) ):
                        game_window.blit(body_br,snk_list[i])

                    elif ((snk_list[i-1][0]<snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) and
                        (snk_list[i+1][0]==snk_list[i][0] and snk_list[i+1][1]>snk_list[i][1]) ):
                        game_window.blit(body_bl,snk_list[i])
                    elif ((snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]>snk_list[i][1]) and
                        (snk_list[i+1][0]<snk_list[i][0] and snk_list[i+1][1]==snk_list[i][1]) ):
                        game_window.blit(body_bl,snk_list[i])
                    
                    elif ((snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]>snk_list[i][1]) or
                        (snk_list[i-1][0]==snk_list[i][0] and snk_list[i-1][1]<snk_list[i][1]) ):
                        game_window.blit(body_vertical,snk_list[i])

                    elif ((snk_list[i-1][0]<snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) or
                        (snk_list[i-1][0]>snk_list[i][0] and snk_list[i-1][1]==snk_list[i][1]) ):
                        game_window.blit(body_horizontal,snk_list[i])
                    
                    
                    i=i+1
    

            # blitting various configuration of tail depending on the orientation
            if len(snk_list)>=2:
                if snk_list[0][1]==snk_list[1][1] and snk_list[0][0]>snk_list[1][0] :
                    game_window.blit(tail_right,snk_list[0])
                elif snk_list[0][1]==snk_list[1][1] and snk_list[0][0]<snk_list[1][0] :
                    game_window.blit(tail_left,snk_list[0])
                elif snk_list[0][0]==snk_list[1][0] and snk_list[0][1]<snk_list[1][1] :
                    game_window.blit(tail_up,snk_list[0])
                elif snk_list[0][0]==snk_list[1][0] and snk_list[0][1]>snk_list[1][1] :
                    game_window.blit(tail_down,snk_list[0])

        pygame.display.update()
        
        clock.tick(fps)

    pygame.quit()
    quit()

game_loop()
