#PathFinding Algorithm
#finds its way to a start and ending point set by user, allows user to make obstacles
#Uses A* pathfinding algorithm to find distances between two nodes
import pygame
from tkinter import *

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (200,200,200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#THINGS TO DO: 
#Create A* algorithm, pathfinder
#make first find path between two points, no white
#add more later
#add condition that path cannot be found if path is blocked



def retrieve():
    global topInfo
    E1List = E1.get().split (",")
    E2List = E2.get().split (",")
    topInfo = []
    try:
        for i in E1List:
            topInfo.append(int(i))
        for i in E2List:
            topInfo.append(int(i))
                
        topInfo.append(Var1.get())
    except ValueError:
        print("Enter the coordinates again!")
        exit()
    if len(topInfo)>5:
        print("You entered too much information!")
        exit()
    elif len(topInfo)<=4:
        print("You entered too little information!")
        exit()

    #Set High and Low values for Coordinates using if statements
    #add other functions to get rid of errors and make topInfo streamlined for use
    for integer in topInfo:
        if integer<0 or integer>48:
            print("These numbers are too low/high!")
            exit()
    if topInfo[0] == topInfo[2] and topInfo[1] == topInfo[3]:
        print("The Start and Stop are in the same location!")
        exit()
        
    top.destroy()





def userinputwindow():

    global top, Button, E1, E2, Var1
    
    
    top= Tk()
    top.geometry("300x200")

    L1 = Label(top, text = "Start (x,y): ")
    L1.place(x = 40,y = 40)
    E1 = Entry(top, bd = 5)
    E1.insert(0,'0,0')
    E1.place(x = 100,y = 40)
    L2 = Label(top,text = "End (x,y): ")
    L2.place(x = 40,y = 80)
    E2 = Entry(top,bd = 5)
    E2.insert(0,'48,48')
    E2.place(x = 100,y = 80)

    Var1 = IntVar()
    ChkBttn = Checkbutton(top, text = "Show Steps:", width = 15, variable = Var1)
    ChkBttn.place(x=90,y=105)

    Button = Button(top, text = "Submit", command = retrieve)
    Button.place(x = 130, y = 140)

    top.mainloop()
    try:
        return topInfo
    except NameError:
        exit()




def drawGrid(win,WINDOW_WIDTH,WINDOW_HEIGHT,blockSize,borderReduc):
    win.fill(GRAY)
    pygame.draw.rect(win,(BLACK),(20,20,WINDOW_WIDTH-(2*borderReduc),WINDOW_HEIGHT-(2*borderReduc)))
    blockSize = 20 #Sets Blocks by their size 
    for x in range(0+borderReduc, WINDOW_WIDTH-borderReduc, blockSize):
        for y in range(0+borderReduc, WINDOW_HEIGHT-borderReduc, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(win, WHITE, rect, 1)
    return blockSize





def pathfinderwindow(userInput):
    pygame.init()


    WINDOW_WIDTH = 1020
    WINDOW_HEIGHT = 1020
    blockSize = 20
    borderReduc = 20
    pathFound = 0

    win = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    pygame.display.set_caption("Pathfinder Algorithm")
    run = True

    drawGrid(win,WINDOW_WIDTH,WINDOW_HEIGHT,blockSize,borderReduc)
    numofBlocks = int(((WINDOW_HEIGHT-borderReduc)/blockSize)-1)

    #PLOTTED USER POINTS
    pygame.draw.rect(win,GREEN,((userInput[0]* 20)+borderReduc,(userInput[1] * 20)+borderReduc,blockSize,blockSize))#START box printed(green)
    pygame.draw.rect(win,RED,((userInput[2]* 20)+borderReduc,(userInput[3]* 20)+borderReduc,blockSize,blockSize))#END box printed(red)


    while run:
        msElapsed = clock.tick(10000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#quit if x button is pressed
                run = False
            elif pygame.mouse.get_pressed()[0] and borderReduc<pygame.mouse.get_pos()[0]<WINDOW_WIDTH-borderReduc and borderReduc<pygame.mouse.get_pos()[1]<WINDOW_HEIGHT-borderReduc and pathFound == 0:#if moouse is pressed in the grid region
                #print(pygame.mouse.get_pos())
                if pygame.Surface.get_at(win,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))[0:3] == BLACK:#if moused over block is black only...

                    for i in range(numofBlocks):#CREATES WHITE BLOCKS
                        for j in range(numofBlocks):
                            if (i*20)+borderReduc<=pygame.mouse.get_pos()[0]<(i*20)+(2*borderReduc) and (j*20)+borderReduc<=pygame.mouse.get_pos()[1]<(j*20)+(2*borderReduc):
                                    pygame.draw.rect(win,(WHITE),((i*20)+borderReduc,(j*20)+borderReduc,blockSize,blockSize))

            elif pygame.mouse.get_pressed()[2] and borderReduc<pygame.mouse.get_pos()[0]<WINDOW_WIDTH-borderReduc and borderReduc<pygame.mouse.get_pos()[1]<WINDOW_HEIGHT-borderReduc and pathFound == 0:#if mouse is pressed in the grid region
               
                if pygame.Surface.get_at(win,(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]))[0:3] == WHITE:#If moused over block is white...
                    
                    for i in range(numofBlocks):#ERASE WHITE BLOCKS
                        for j in range(numofBlocks):
                            if (i*20)+borderReduc<=pygame.mouse.get_pos()[0]<(i*20)+(2*borderReduc) and (j*20)+borderReduc<=pygame.mouse.get_pos()[1]<(j*20)+(2*borderReduc):
                                    pygame.draw.rect(win,(BLACK),(((i*20)+borderReduc)+1,((j*20)+borderReduc)+1,blockSize-2,blockSize-2))

            elif pygame.key.get_pressed()[pygame.K_SPACE] and pathFound == 0:#If space is pressed, complete algorithm
                walldetect(win,userInput,numofBlocks,borderReduc,blockSize)#algorithm for finding path is made
                pathFound = 1

            pygame.display.update()#update the display MAY NEED THIS WHEN DRAWING ALGORITHM
    pygame.quit()





def walldetect(win, userInput,numofBlocks,borderReduc,blockSize):

    boardRead = [[0 for c in range(numofBlocks)] for r in range(numofBlocks)]

    for i in range(numofBlocks):
        for j in range(numofBlocks):
            if pygame.Surface.get_at(win,((20*j)+30,(20*i)+30))[0:3] == RED:
                boardRead[i][j] = "R"
            elif pygame.Surface.get_at(win,((20*j)+30,(20*i)+30))[0:3] == GREEN:
                boardRead[i][j] = "G"

            elif pygame.Surface.get_at(win,((20*j)+30,(20*i)+30))[0:3] == WHITE:
                boardRead[i][j] = "W"
            elif pygame.Surface.get_at(win,((20*j)+30,(20*i)+30))[0:3] == BLACK:
                boardRead[i][j] = "B"



    pathfindingalgorithm(win,boardRead,userInput,borderReduc,blockSize)





def pathfindingalgorithm(win,boardRead,userInput,borderReduc,blockSize):
    
# NOW THAT WE HAVE THE COLOR LOCATIONS BOARDREAD[48][48] AND THE COLOR THEMSELVES, CODE THE ALGORITHM TO FIND THE FASTEST PATH FROM START TO END
    #MAKE A* PATHFINDING PROGRAM BASED ON BOARDREAD[0][0] TO BOARDREAD[48][48]


    #FIRST FROM 0,0 TO 48,48 AND THEN FROM ANY POINT TO ANOTHER WITHOUT ANY WHITE BOXES
    #DISTANCE BETWEEN CURRENT POINT AND START + DISTANCE BETWEEN CURRENT POINT AND END = F

    #LOWEST F VALUE IS CHOSEN IN THE PATH AND TAKEN OUT OF AN OPEN SET
    #ITERATE THROUGH EACH POINT AND UPDATE THE SETS BASED ON NEW F,G,H
    #IF F IS EQUAL, COMPARE H, IF H IS EQUAL, CHOOSE 1ST ONE

    #foo = 0

    pathComplete = False
    openSet = []
    closedSet = []

    startCoord = [0 ,0,0,userInput[0],userInput[1],-1,-1]#REMEMBER TO CHANGE F G H TO 0
    endCoord = [0,0,0,userInput[2],userInput[3],0,0]#REMEMBER TO CHANGE F G H to 0
    showVisual = userInput[4]

    openSet.append(startCoord)

    try:
        while not pathComplete:
            
            current = openSet[0]
            indexPop = 0
            for i in range(len(openSet)):#lowest f cost check
                if current[0] > openSet[i][0]:
                    current = openSet[i]
                    indexPop = i

            for i in range(len(openSet)):#lowest Heuristic cost check
                if current[0] == openSet[i][0]:
                    if current[2] > openSet[i][2]:
                        current = openSet[i]
                        indexPop = i


            openSet.pop(indexPop)
            closedSet.append(current)

            if showVisual == 1:
                pygame.draw.rect(win,(RED),((((current[3])*20)+borderReduc)+1,(((current[4])*20)+borderReduc)+1,blockSize-2,blockSize-2))

            if current[3] == endCoord[3] and current[4] == endCoord[4]:
                pathComplete = True
                continue




            if current[3] - 1 >= 0 and boardRead[current[4]][current[3]-1] != 'W' :#LEFT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,-1,0,0)

            

            if current[3] + 1 <= 48 and boardRead[current[4]][current[3]+1] != 'W':#RIGHT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,1,0,0)
                
            

            if current[4] - 1 >= 0 and boardRead[current[4]-1][current[3]] != 'W':#TOP BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,0,-1,0)

            
            if current[4] + 1 <= 48 and boardRead[current[4]+1][current[3]] != 'W':#BOTTOM BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,0,1,0)




            if current[3] - 1 >= 0 and  current[4] - 1 >= 0 and boardRead[current[4]-1][current[3]-1] != 'W' and (boardRead[current[4]-1][current[3]] != 'W' or boardRead[current[4]][current[3]-1] != 'W'):#TOP LEFT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,-1,-1,1)



            if current[3] + 1 <= 48 and  current[4] - 1 >= 0 and boardRead[current[4]-1][current[3]+1] != 'W' and (boardRead[current[4]-1][current[3]] != 'W' or boardRead[current[4]][current[3]+1] != 'W'):#TOP RIGHT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,1,-1,1)


            if current[3] - 1 >= 0 and  current[4] + 1 <= 48 and boardRead[current[4]+1][current[3]-1] != 'W' and (boardRead[current[4]+1][current[3]] != 'W' or boardRead[current[4]][current[3]-1] != 'W'):#BOTTOM LEFT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,-1,1,1)



            if current[3] + 1 <= 48 and  current[4] + 1 <= 48 and boardRead[current[4]+1][current[3]+1] != 'W' and (boardRead[current[4]+1][current[3]] != 'W' or boardRead[current[4]][current[3]+1] != 'W'):#BOTTOM RIGHT BOX
                nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,1,1,1)

            #ADD DELAY
            if showVisual == 1:
                pygame.time.delay(75)
                pygame.display.update()


    except IndexError:
        print("There is no possible path!")
        exit()

    pathprint(win,blockSize,borderReduc,closedSet)




def nearestneighbors(win,borderReduc,blockSize,showVisual,current,openSet,closedSet,endCoord,curr3,curr4,cornerBox):

    inClosedSet = 0
    for theCompleted in closedSet:
        if theCompleted[3] == (current[3]+curr3) and theCompleted[4] == (current[4]+curr4):
            inClosedSet = 1

    if inClosedSet == 0:
        inOpenSet = 0

        if cornerBox == 0:
            gCost = current[1] + 10
        else:
            gCost = current[1] + 14

        hCost = abs(abs((current[3]+curr3) - endCoord[3]) - abs((current[4]+curr4) - endCoord[4])) * 10 + min(abs((current[3]+curr3) - endCoord[3]),abs((current[4]+curr4) - endCoord[4])) * 14
        fCost = gCost + hCost
        for fghCoord in openSet:
            if fghCoord[3] == (current[3]+curr3) and fghCoord[4] == (current[4]+curr4) and fCost < fghCoord[0]:
                fghCoord[0] = fCost
                fghCoord[1] = gCost
                fghCoord[2] = hCost
                fghCoord[5] = current[3]
                fghCoord[6] = current[4]
                inOpenSet = 1
            elif fghCoord[3] == (current[3]+curr3) and fghCoord[4] == (current[4]+curr4) and fCost >= fghCoord[0]:
                inOpenSet = 1
                break
        if inOpenSet == 0:
            test = [fCost,gCost,hCost,current[3]+curr3,current[4]+curr4,current[3],current[4]]
            openSet.append(test)
            if showVisual == 1:
                pygame.draw.rect(win,(GREEN),((((current[3]+curr3)*20)+borderReduc)+1,(((current[4]+curr4)*20)+borderReduc)+1,blockSize-2,blockSize-2))




def pathprint(win,blockSize,borderReduc,closedSet):#MAKE FUNNCTION TO SHOW PATH CANNOT BE FOUND
    currParent = []

    for i in range(len(closedSet)):
        currParent.append(closedSet[i][3:])

    path = []


    parent = currParent[len(currParent)-1][0:2]
    for i in range(len(currParent)-1,-1,-1):
        if parent == currParent[i][0:2]:
            path.append(currParent[i][0:2])
            parent = currParent[i][2:4]

    path.reverse()


    for i in range(len(path)):
        pygame.draw.rect(win,(BLUE),(((path[i][0]*20)+borderReduc)+1,((path[i][1]*20)+borderReduc)+1,blockSize-2,blockSize-2))

    #exit()






def main():
    userInput = userinputwindow()
    #print("List: ", userInput)#COMMENT THIS OUT LATER
    pathfinderwindow(userInput)

main()


