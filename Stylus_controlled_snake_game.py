import cv2 as cv
import numpy as np
import pygame
import random


from pygame.version import SDLVersion
pygame.init()
# defining a game loop
def game_loop():
    
    # definig game parameters
    screen_width=800 #600
    screen_height=600 #500
    # colors
    white=(255,255,255)
    red=(255,0,0)
    black=(0,0,0)

    #creating a game window in which game to be played
    game_window=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption(" SANKE GAME ")
    pygame.display.update()

    exit_game=False
    game_over=False

    # initial position of snake
    snake_x=45
    snake_y=45
    # initial velocity of snake
    velocity_x=0
    velocity_y=0
    snake_size=15

    # Loading images like for background, snake body, food etc.
    bgimg=pygame.image.load("background images/background.png")
    bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
    
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


    # using random function to create a new random position of food
    food_x=random.randint(0,screen_width)
    food_y=random.randint(0,screen_height)
    # initial score
    score=0
    fps=30 # frames per second
    clock = pygame.time.Clock()
    font=pygame.font.SysFont(None,55)

    # defining a function for writing text on game window
    def text_screen(text,color,x,y):
        screen_text= font.render(text,True,color) 
        game_window.blit(screen_text,[x,y])    

    # Creatings Hurdles
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

    # making as list of hurdles and randomly picking up one at a time
    obstacle=[hurdle_1,hurdle_2,hurdle_3,hurdle_4,hurdle_5]
    obs=random.choice([0,1,2,3,4])
    
    # initialising a list for the coordinates of the snake body after every loop
    snk_list=[]
    snk_length=1 # initial length of snake 

    # capturing frame 
    cap=cv.VideoCapture(0)
    # list for storing coordinates values of centroid for every 10 iterations
    list=[]
    counter=1 # counter for 10 iterations
    direction=''


    while(exit_game==False):
        _,frame=cap.read()
        frame=cv.flip(frame,1)
        blurred_frame=cv.GaussianBlur(frame,(5,5),0)
        blurred_frame=cv.flip(blurred_frame,1)
        hsv = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
        
        lower_range = np.array([85,100,92], dtype=np.uint8) 
        upper_range = np.array([112, 255,255], dtype=np.uint8) 
        mask = cv.inRange(hsv, lower_range, upper_range)

        #morphological transformation
        kernel = np.ones((5,5),np.uint8)
        opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        dilation = cv.dilate(opening,kernel,iterations = 1)
        dilation=cv.flip(dilation,1)
        

        #finding contours
        contours, _ = cv.findContours(dilation, 1, 2)
        if len(contours)==0:
            continue
        areas = [cv.contourArea(c) for c in contours]
        
        cnt=contours[np.argmax(areas)]
        # finding moments
        M = cv.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])) # finding centroid

        #appending list with coordinates of centroid
        if (counter<=10):
            list.append(center)
            counter=counter+1
        # analysing list when counter is 10
        if(counter==10):
            counter=1
            i=0
            x_diff=0
            y_diff=0
            x_diff_max=0
            y_diff_max=0
            while(i<8):
                #  finding the difference between successive elements
                x_diff=list[i+1][0]-list[i][0]
                y_diff=list[i+1][1]-list[i][1]
                #finding maximum difference from which we can finalize the direction
                if(x_diff_max<x_diff and x_diff>0 and x_diff_max>=0):
                    x_diff_max=x_diff
                if(x_diff_max>x_diff and x_diff<0 and x_diff_max<=0):
                    x_diff_max=x_diff
                if(y_diff_max<y_diff and y_diff>0 and y_diff_max>=0):
                    y_diff_max=y_diff
                if(y_diff_max>y_diff and y_diff<0 and y_diff_max<=0):
                    y_diff_max=y_diff
                i=i+1
            # condition check for detecting direction 
            if x_diff_max>10: # if there is a significant change in the coordinates for direction to change
                cv.putText(frame, 'Right', (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                print('Right')
                direction='Right'
            elif x_diff_max<-10:
                cv.putText(frame, 'left', (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                print('left')
                direction='left'
            elif y_diff_max>10:
                cv.putText(frame, 'Down', (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                print('Down')
                direction='Down'
            elif y_diff_max<-10:
                cv.putText(frame, 'Up', (20,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                print('Up')
                direction='Up'
            list=[]

        # conditions for movement of snake in perticular direction
        if direction=='Right':
            if direction!='left':
                velocity_x= 5  # giving velocity in x direction 
                velocity_y=0  # and zero in other direction
        if direction=='left':
            if direction!='Right':
                velocity_x= -5
                velocity_y=0
        if direction=='Down':
            if direction!='Up':
                velocity_x= 0
                velocity_y=5
        if direction=='Up':
            if direction!='Down':
                velocity_x= 0
                velocity_y= -5

        # changing the position of snake with velocity
        snake_x=snake_x+velocity_x
        snake_y=snake_y+velocity_y

        # if the distance between centre of snake and food is less than 8 , then it will eat it
        if (abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15):
            score=score+1
            # creating the random position of food with the condition it don't come over the obstacle
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
            
            snk_length += 5 # increasing the length of snake by 5
        
        # displaying the background image
        game_window.blit(bgimg,(0,0))
        # creating the boundary
        pygame.draw.rect(game_window,black,[0,0,screen_width,40])
        pygame.draw.rect(game_window,black,[0,0,40,screen_height])
        pygame.draw.rect(game_window,black,[screen_width-40,0,40,screen_height])
        pygame.draw.rect(game_window,black,[0,screen_height-40,screen_width,40])
        # calling the obsatcle function to create the hurdles
        obstacle[obs]()     
        text_screen('score: '+str(score*10),red,5,5) # displaying score
        
        head=[] # making a list and appending new location of snake head
        head.append(snake_x)
        head.append(snake_y)
        snk_list.append(head) # appending these new coodinates in the snake_list

        if (len(snk_list)>snk_length):
            del snk_list[0]

        # if the coordinates of head matches with any coordinates in snk_list means it had collided, Game over
        if head in snk_list[:-1]:
            game_over=True
            
        x=head[0]
        y=head[1]

        # if the head collides with walls
        if (y<40)or(y>screen_height-80)or(x<40) or (x>screen_width-40) :
                game_over=True

        # checking for collision with the obstacle
        if (obs==0):
            if((x>160 and x<690 and y>210 and y<330) or (x>410 and x<530 and y>60 and y<540)):
                game_over=True
        elif(obs==1):
            if((x>160 and x<730 and y>100 and y<180) or (x>610 and x<730 and y>60 and y<540)):
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

        # displaying various orientation of head according to the direction 
        if direction=='Right':
            game_window.blit(Head_Right,snk_list[-1])
        elif direction=='left':
            game_window.blit(Head_left,snk_list[-1])
        elif direction=='Up':
            game_window.blit(Head_up,snk_list[-1])
        elif direction=='Down':
            game_window.blit(Head_down,snk_list[-1])
        else:
            game_window.blit(Head_Right,snk_list[-1]) # initially head in the right direction


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


        # drawing contours on detected object in the original frame
        cv.drawContours(frame,contours,-1,(0,255,0),3)
        cv.circle(frame, center, 5, (0, 0, 255), -1)
        cv.imshow('stylus detected frame',frame) 


        # condition check for when game is over,either striking with wall or with itself
        if game_over:
            #print('Game over')
            game_window.fill(white)
            text_screen("Game Over!! Press Enter to Continue ",red,40,40)
            for event in pygame.event.get():
                # if want to quit, then directly close the window
                if event.type==pygame.QUIT:
                    exit_game=True
                # press enter to play next game
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        game_loop()

        pygame.display.update()
        clock.tick(fps)

        if cv.waitKey(1)==ord('q'):
            break
    
    # releasing and destroying all windows
    cap.release()
    cv.destroyAllWindows()

# calling the game_loop function to enter into the game
game_loop()