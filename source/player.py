#usr/bin/env python 
import copy, os, random, sys
import common, dungeon, item

class player:
  """
  Player class. Creates and manages player objects

  #Main characteristics

  name="_"      #Name
  pocket=0      #Money
  exp=0         #EXP
  lv=1          #Level
  points=0      #Expendable points
  race="_"      #Race
  charclass="_" #Class
  inventory=[]  #10 slot inventory
  equiparr=[]   #Equipped item inventory
  belt=[]       #Quick access consumable items
  totalfl=0     #Total floors explored
  status=0      #Paralyzed, burned, bleeding, etc
  prestige=0    #Prestige points
  prestigelv=1  #Prestige level (unused)

  #Attribute and attribute booster variables

  INT=1         #Intelligence
  DEX=1         #Dexterity
  PER=1         #Perception
  WIL=1         #Willpower
  STR=1         #Strenght
  CON=1         #Constitution
  CHA=1         #Charisma
  intboost=0    #
  dexboost=0    #
  perboost=0    #
  wilboost=0    # Extra attributes given by equipped items
  strboost=0    #
  conboost=0    #
  chaboost=0    #

  totatk=1      #Total attack power
  totdefn=1     #Total defense power

  #Secondary and status variables

  HP=0          #Maximum hit points
  hp2=0         #Current hit points
  MP=0          #Maximum mana points
  mp2=0         #Current mana points
  END=0         #Endurance
  SPD=0         #Speed
  
  #Position
  xpos=0
  ypos=0
  zpos=0
  """

  def __init__(self,dungeon,randomv):
    """
    Initialization of the player objects. 

    Receives a dungeon object, then sets the coordinates of the player object in the entrance tile
    It also chooses a random race and class from the ./data/races and ./data/classes files

    Needs a random parameter. if 1, the character is generated randomly.
    """

    #Main characteristics
    self.name="_"      #Name
    self.pocket=0      #Money
    self.exp=0         #EXP
    self.lv=1          #Level
    self.points=40     #Expendable points
    if randomv: self.points=0
    self.race="_"      #Race
    self.charclass="_" #Class
    self.totalfl=0     #Total floors explored
    self.status=0      #Paralyzed, burned, bleeding, etc
    self.prestige=0    #Prestige points
    self.prestigelv=1  #Prestige level (unused)

    #Initializing inventory arrays
    self.belt=[]
    for i in range(3): self.belt.append(item.consumable(4,0))
    self.inventory=[]
    self.equiparr=[]
    for i in range(11):
      new=item.item(0)
      self.equiparr.append(new)

    #Set attributes to 1, set secondary attributes
    self.STR=self.INT=self.CON=self.WIL=self.PER=self.DEX=self.CHA=1

    #Set attribute boosters to 0
    self.strboost=self.intboost=self.conboost=self.wilboost=self.perboost=self.dexboost=self.chaboost=0

    #Secondary attributes
    self.HP=self.hp2=0
    self.MP=self.mp2=0
    self.END=self.SPD=0
    self.totatk=self.totdefn=1
    self.secondary()
    self.mp2=self.MP
    self.hp2=self.HP
    
    #Initialize position at the entrance
    for i in dungeon.dungarray:
      for j in i:
        if j=="A":
          self.ypos=dungeon.dungarray.index(i)
          self.xpos=i.index(j)
          self.zpos=0

    #Random race
    if randomv==1:
      namearray=[]
      with open("../data/player/names","r") as names:
        for line in names: namearray.append(line.strip())
      self.name=random.choice(namearray)

      with open("../data/player/races","r") as file:
        racesarray=strarray=intarray=dexarray=perarray=conarray=chaarray=[]
        for line in file:
          if not line.startswith('#'):
            racesarray.append(line.rstrip('\n').partition(':')[0])
            strarray.append(line.rstrip('\n').partition(':')[2].partition(':')[0])
            intarray.append(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[0])
            dexarray.append(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
            perarray.append(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
            conarray.append(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
            chaarray.append(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
      
      randrac=random.randrange(len(racesarray))
      self.race=racesarray[randrac]
      if not strarray[randrac]=="": self.STR+=int(strarray[randrac])
      if not strarray[randrac]=="": self.INT+=int(intarray[randrac])
      if not strarray[randrac]=="": self.DEX+=int(dexarray[randrac])
      if not strarray[randrac]=="": self.PER+=int(perarray[randrac])
      if not strarray[randrac]=="": self.CON+=int(conarray[randrac])
      if not strarray[randrac]=="": self.CHA+=int(chaarray[randrac])

      #Random class
      with open("../data/player/classes","r") as file:
        classesarray=[]
        for line in file: classesarray.append(line.rstrip('\n'))
      self.charclass=random.choice(classesarray) 

      #Random initial attributes
      for i in range(9):
        randstat=random.randrange(7)
        if   randstat==0: self.STR+=1
        elif randstat==1: self.INT+=1
        elif randstat==2: self.DEX+=1
        elif randstat==3: self.PER+=1
        elif randstat==4: self.CON+=1
        elif randstat==5: self.WIL+=1
        elif randstat==6: self.CHA+=1
        else: pass

    #add two random items to the inventory
    for i in range(2): self.inventory.append(item.item(random.randint(1,11)))

  def pickobject(self,object):
    """
    Pick item from the floor. 

    This receives an item and adds it to the inventory if the inventory is not full.
    Returns 1 and adds the object to the inventory if the object was correctly picked, returns 0 if it wasn't.
    """

    #If the inventory is not full, it adds it. 
    if len(self.inventory)>=9:
      pass
      return 0,("Your inventory is full!\n")
    #If the inventory is full, passes.
    if len(self.inventory)<9:
      self.inventory.append(object)
      return 1,("You picked "+object.name+"\n")
    
  def getatr(self):
    """
    Prints the player attributes on screen.
    """

    print "HP: %i/%i, MP: %i/%i      "  %(self.hp2,self.HP,self.mp2,self.MP)
    print "INT: %i(+%i)  DEX: %i(+%i)"  %(self.INT,self.intboost,self.DEX,self.dexboost)
    print "CON: %i(+%i)  STR: %i(+%i)"  %(self.CON,self.conboost,self.STR,self.strboost)
    print "WIL: %i(+%i)  PER: %i(+%i)"  %(self.WIL,self.wilboost,self.PER,self.perboost)
    print "CHA: %i(+%i)              "  %(self.CHA,self.chaboost)
    print "END: %i SPD: %i           "  %(self.END,self.SPD)
    
  def move(self,dungeon,direction):
    """
    Move function. 

    Receives a dungeon object to check for obstacles and an integer [1,4] indicating the direction
      1 north
      2 west
      3 south
      4 east
      5 northwest
      6 northeast
      7 southwest
      8 southeast

    Returns an integer:
      0 Can't move (Wall or other obstacle)
      1 Moved successfully
      2 Mob present (Not moved, signaled for attack)
    """

    #This gives 1 base move 
    #It used to add 1 extra move for every 10 SPD but this caused bugs
    moves=1
    try:
      #Checks the direction and moves
      if direction==1:
        if dungeon.dungarray[self.ypos-1][self.xpos]=="#" or dungeon.dungarray[self.ypos-1][self.xpos]=="|": return 0
        if dungeon.filled[self.ypos-1][self.xpos]=="i": return 2
        else:
          self.ypos-=moves
          return 1
      elif direction==2:
        if dungeon.dungarray[self.ypos][self.xpos-1]=="#": return 0
        if dungeon.filled[self.ypos][self.xpos-1]=="i": return 2
        elif dungeon.dungarray[self.ypos][self.xpos-1]=="|": dungeon.vendorvar.commerce(self)
        else:
          self.xpos-=moves
          return 1  
      elif direction==3:
        if dungeon.dungarray[self.ypos+1][self.xpos]=="#" or dungeon.dungarray[self.ypos+1][self.xpos]=="|": return 0
        if dungeon.filled[self.ypos+1][self.xpos]=="i": return 2
        else:     
          self.ypos+=moves
          return 1
      elif direction==4:
        if dungeon.dungarray[self.ypos][self.xpos+1]=="#": return 0
        if dungeon.filled[self.ypos][self.xpos+1]=="i": return 2
        elif dungeon.dungarray[self.ypos][self.xpos+1]=="|": dungeon.vendorvar.commerce(self)
        else:
          self.xpos+=moves
          return 1
      elif direction==5:
        if dungeon.dungarray[self.ypos-1][self.xpos-1]=="#" or dungeon.dungarray[self.ypos-1][self.xpos-1]=="|": return 0
        if dungeon.filled[self.ypos-1][self.xpos-1]=="i": return 2
        else:
          self.ypos-=moves
          self.xpos-=moves
          return 1
      elif direction==6:
        if dungeon.dungarray[self.ypos-1][self.xpos+1]=="#" or dungeon.dungarray[self.ypos-1][self.xpos+1]=="|": return 0
        if dungeon.filled[self.ypos-1][self.xpos+1]=="i": return 2
        else:
          self.ypos-=moves
          self.xpos+=moves
          return 1
      elif direction==7:
        if dungeon.dungarray[self.ypos+1][self.xpos-1]=="#" or dungeon.dungarray[self.ypos+1][self.xpos-1]=="|": return 0
        if dungeon.filled[self.ypos+1][self.xpos-1]=="i": return 2
        else:
          self.ypos+=moves
          self.xpos-=moves
          return 1
      elif direction==8:
        if dungeon.dungarray[self.ypos+1][self.xpos+1]=="#" or dungeon.dungarray[self.ypos+1][self.xpos+1]=="|": return 0
        if dungeon.filled[self.ypos+1][self.xpos+1]=="i": return 2
        else:
          self.ypos+=moves
          self.xpos+=moves
          return 1
      else: return 0
    except IndexError: return 0

  def secondary(self):
    """
    Calculates and sets the secondary attributes from the primary ones.
 
    Receives a player object and recalculates HP, MP, END and SPD from the primary attributes. 
    It also adds the extra HP and MP gained after adding an attribute point or leveling up.
    """

    temp=self.HP-self.hp2
    self.HP=((self.CON+self.conboost+self.STR+self.strboost)*4)+10
    self.hp2=(self.HP-temp)

    temp2=self.MP-self.mp2
    self.MP=(self.INT+self.intboost+self.WIL+self.wilboost)
    self.mp2=(self.MP-temp2)

    self.END=((self.CON+self.conboost+self.STR+self.strboost+self.wilboost+self.WIL)*3)+5
    self.SPD=(self.CON+self.conboost+self.DEX+self.dexboost)*3

  def charsheet(self):
    """
    Character sheet. 

    Main menu to edit, view and configure characters and player options
    """

    menu=0
    while 1:
      self.secondary()
      common.version()
      print "%s - Character sheet\n"              %(self.name)
      print "Level %i %s %s"                      %(self.lv,self.race,self.charclass)
      if self.lv==1: print "%i/5 xp, %i points"   %(self.exp,self.points)
      if self.lv>1:  print "%i/%i xp, %i points"  %(self.exp,3*self.lv+(2*(self.lv-1)),self.points)
      print "%i floors explored \n\n"             %(self.totalfl)
      self.getatr()
      print "1.- Spend points"
      print "2.- Inventory"
      print "3.- Character options"
      print "4.- Save"
      print "5.- Load"
      print "\n0.- Exit"
      print "->",
      menu=common.getch()
      if menu=="1": self.spend()
      elif menu=="2": self.invmenu()
      elif menu=="3": self.optmenu()
      elif menu=="4":
        print "saving..."
        print self.save()
        common.getch()
      elif menu=="5":
        print "loading..."
        print self.load()
        common.getch()
      elif menu=="0": break
      pass

  def spend(self):
    """
    Point spending menu.
    """

    choice=-1
    while choice!="0": 
      self.secondary()
      common.version()
      print "%s - Character sheet \n"%(self.name)
      print "Spend points"
      if self.points==0:  print "No points left! \n"
      else:               print "%i points left \n"%(self.points)

      #Determining cost of improving attributes (Based on AFMBE rules, sort of)  
      if self.STR<5:  coststr=5
      if self.STR>=5: coststr=((self.STR/5)+1)*5
      if self.INT<5:  costint=5
      if self.INT>=5: costint=((self.INT/5)+1)*5
      if self.DEX<5:  costdex=5
      if self.DEX>=5: costdex=((self.DEX/5)+1)*5
      if self.CON<5:  costcon=5
      if self.CON>=5: costcon=((self.CON/5)+1)*5
      if self.PER<5:  costper=5
      if self.PER>=5: costper=((self.PER/5)+1)*5
      if self.WIL<5:  costwil=5
      if self.WIL>=5: costwil=((self.WIL/5)+1)*5
      if self.CHA<5:  costcha=5
      if self.CHA>=5: costcha=((self.CHA/5)+1)*5

      #printing menu
      print "1.- [%i] STR %i (+%i)"%(coststr,self.STR,self.strboost)
      print "2.- [%i] INT %i (+%i)"%(costint,self.INT,self.intboost)
      print "3.- [%i] DEX %i (+%i)"%(costdex,self.DEX,self.dexboost)
      print "4.- [%i] CON %i (+%i)"%(costcon,self.CON,self.conboost)
      print "5.- [%i] PER %i (+%i)"%(costper,self.PER,self.perboost)
      print "6.- [%i] WIL %i (+%i)"%(costwil,self.WIL,self.wilboost)
      print "7.- [%i] CHA %i (+%i)"%(costcha,self.CHA,self.chaboost)
      print "\nSecondary attributes:"
      print 'END:', self.END, '     SPD:', self.SPD
      print "Max. HP: %i"%(self.HP)
      print "Max. MP: %i"%(self.MP)
      print "---"
      print "0.- Exit"
      print "\n->",
      choice=common.getch()

      #Choice cases
      if self.points==0: pass
      else:
        if choice=="1":
          if self.points>=coststr:
            self.STR+=1
            self.points-=coststr
        elif choice=="2":
          if self.points>=costint:
            self.INT+=1
            self.points-=costint
        elif choice=="3":
          if self.points>=costdex:
            self.DEX+=1
            self.points-=costdex
        elif choice=="4":
          if self.points>=costcon:
            self.CON+=1
            self.points-=costcon
        elif choice=="5":
          if self.points>=costper:
            self.PER+=1
            self.points-=costper
        elif choice=="6":
          if self.points>=costwil:
            self.WIL+=1
            self.points-=costwil
        elif choice=="7":
          if self.points>=costcha:
            self.CHA+=1
            self.points-=costcha
        elif choice=="0": pass
        else: pass

  def optmenu(self):
    """
    Player options menu
    """

    coptmen=-1
    while coptmen!="0": 
      common.version()
      print "%s - Character sheet \n"%(self.name)
      print "1.- Change name"
      print "---"
      print "0.- Back"
      print "->",
      coptmen=common.getch()
      if coptmen=="1": self.name=raw_input("New name? ")
      if coptmen=="0": break

  def calcbonus(self,item):
    """
    Generates the string with the attribute boosts for the inventory
    """

    calcarray=[]
    if item.strbonus>0: calcarray.append("+"+str(item.strbonus)+" STR")
    if item.intbonus>0: calcarray.append("+"+str(item.intbonus)+" INT")
    if item.dexbonus>0: calcarray.append("+"+str(item.dexbonus)+" DEX")
    if item.perbonus>0: calcarray.append("+"+str(item.perbonus)+" PER")
    if item.conbonus>0: calcarray.append("+"+str(item.conbonus)+" CON")
    if item.wilbonus>0: calcarray.append("+"+str(item.wilbonus)+" WIL")
    if item.chabonus>0: calcarray.append("+"+str(item.chabonus)+" CHA")
    if len(calcarray)>0: return "("+(', '.join(map(str,calcarray)))+")"
    if len(calcarray)==0: return ""

  def willtest(self):
    """
    Tests if the player has enough willpower to move.

    Roll a die [1,20] and add the total willpower
    If the roll is less than 20/remaining HP, the test fails 

    If the player's health is bigger than 5, the player automatically passes the test.
    """

    if self.hp2<=5:
      roll=random.randint(1,21)+self.WIL+self.wilboost
      if self.hp2>0:
        if roll<20/self.hp2: return 0,"Your body refuses to move"
    return 1,""

  def use(self,item):
    """
    Takes an item object from the player belt and uses it.

    Returns a message to be displayed.
    """

    if item.type==0:
      hppool=int(item.hpr)
      mppool=int(item.mpr)
      mpres=hpres=0
      nam=item.name

      #restore HP
      while hppool>0 and self.hp2<self.HP:
        hppool-=1
        self.hp2+=1
        hpres+=1

      #restore MP
      while mppool>0 and self.mp2<self.MP:
        mppool-=1
        self.mp2+=1
        mpres+=1

      #restore status
      if item.statusr: self.status=0

      #reset item
      item.reset()

      #Message generation
      msg="You drank "+item.name+". "
      if hpres>0 or mpres>0: msg=msg+"You recovered "
      if hpres>0: msg=msg+str(hpres)+" HP"
      if hpres>0 and mpres>0: msg=msg+" and "
      if mpres>0: msg=msg+str(mpres)+" MP"
      if hpres>0 or mpres>0: msg=msg+"."
      return msg

    if item.type==1:
      self.INT+=item.intbst
      self.DEX+=item.dexbst
      self.PER+=item.perbst
      self.CON+=item.conbst
      self.WIL+=item.wilbst
      self.CHA+=item.chabst
      self.STR+=item.strbst
      item.reset()

      #Message generation
      msg="You drank "+item.name+". "
      if item.intbst>0: msg=msg+"INT +"+str(item.intbst)+" "
      if item.dexbst>0: msg=msg+"DEX +"+str(item.dexbst)+" "
      if item.perbst>0: msg=msg+"PER +"+str(item.perbst)+" "
      if item.conbst>0: msg=msg+"CON +"+str(item.conbst)+" "
      if item.wilbst>0: msg=msg+"WIL +"+str(item.wilbst)+" "
      if item.chabst>0: msg=msg+"CHA +"+str(item.chabst)+" "
      if item.strbst>0: msg=msg+"STR +"+str(item.strbst)+" "
      msg=msg+"\n"

    if item.type==4:
      return ""

  def invmenu(self):
    """
    Inventory menu. 
    """

    while 1: 
      common.version()
      print "%s - Character sheet"%(self.name)
      print "\nEquipped\n"
      print "01 [+%i/+%i] Head: %s %s"       %(self.equiparr[0].atk,self.equiparr[0].defn,self.equiparr[0].name,self.calcbonus(self.equiparr[0]))
      print "02 [+%i/+%i] Face: %s %s"       %(self.equiparr[1].atk,self.equiparr[1].defn,self.equiparr[1].name,self.calcbonus(self.equiparr[1]))
      print "03 [+%i/+%i] Neck: %s %s"       %(self.equiparr[2].atk,self.equiparr[2].defn,self.equiparr[2].name,self.calcbonus(self.equiparr[2]))
      print "04 [+%i/+%i] Shoulders: %s %s"  %(self.equiparr[3].atk,self.equiparr[3].defn,self.equiparr[3].name,self.calcbonus(self.equiparr[3]))
      print "05 [+%i/+%i] Chest: %s %s"      %(self.equiparr[4].atk,self.equiparr[4].defn,self.equiparr[4].name,self.calcbonus(self.equiparr[4]))
      print "06 [+%i/+%i] Left hand: %s %s"  %(self.equiparr[5].atk,self.equiparr[5].defn,self.equiparr[5].name,self.calcbonus(self.equiparr[5]))
      print "07 [+%i/+%i] Right hand: %s %s" %(self.equiparr[6].atk,self.equiparr[6].defn,self.equiparr[6].name,self.calcbonus(self.equiparr[6]))
      print "08 [+%i/+%i] Ring: %s %s"       %(self.equiparr[7].atk,self.equiparr[7].defn,self.equiparr[7].name,self.calcbonus(self.equiparr[7]))
      print "09 [+%i/+%i] Belt: %s %s"       %(self.equiparr[8].atk,self.equiparr[8].defn,self.equiparr[8].name,self.calcbonus(self.equiparr[8]))
      print "10 [+%i/+%i] Legs: %s %s"       %(self.equiparr[9].atk,self.equiparr[9].defn,self.equiparr[9].name,self.calcbonus(self.equiparr[9]))
      print "11 [+%i/+%i] Feet: %s %s"       %(self.equiparr[10].atk,self.equiparr[10].defn,self.equiparr[10].name,self.calcbonus(self.equiparr[10]))
      print "\n[+%i/+%i]"                    %(self.totatk,self.totdefn)

      #Print everything in the inventory array
      print "\nInventory (+"+str(self.pocket)+" G)\n"
      for i in range(len(self.inventory)): print "0"+str(i+1)+" [+"+str(self.inventory[i].atk)+"/+"+str(self.inventory[i].defn)+"] "+self.inventory[i].name+" ("+str(self.inventory[i].price)+"G)" 

      #Print the belt items
      print "\nBelt\n"
      print "B1 - %s" %(self.belt[0].name)
      print "B2 - %s" %(self.belt[1].name)
      print "B3 - %s" %(self.belt[2].name)

      #Print the inventory action menu
      print "\nq - destroy item"
      print "w - enchant item"
      print "a - unequip item"
      print "b - use belt item"
      print "0 - Back"
      print "\n->",
      invmenu=common.getch()

      #Belt using menu
      if invmenu=="b":
        try:
          print "Which item? ",
          beltmen=common.getch
          self.use(belt[int(beltmen)-1])
        except IndexError: pass

      #Item flipping (Inventory <-> Equip)
      if "0"<invmenu<=str(len(self.inventory)):
        invmenu=int(invmenu)        
        if len(self.inventory)>=invmenu:
          if not self.equiparr[self.inventory[invmenu-1].type-1].name==" ":
            temp=self.equiparr[self.inventory[invmenu-1].type-1]
            self.strboost-=self.equiparr[self.inventory[invmenu-1].type-1].strbonus
            self.intboost-=self.equiparr[self.inventory[invmenu-1].type-1].intbonus
            self.conboost-=self.equiparr[self.inventory[invmenu-1].type-1].conbonus
            self.wilboost-=self.equiparr[self.inventory[invmenu-1].type-1].wilbonus
            self.perboost-=self.equiparr[self.inventory[invmenu-1].type-1].perbonus
            self.dexboost-=self.equiparr[self.inventory[invmenu-1].type-1].dexbonus
            self.chaboost-=self.equiparr[self.inventory[invmenu-1].type-1].chabonus
            self.totatk-=self.equiparr[self.inventory[invmenu-1].type-1].atk
            self.totdefn-=self.equiparr[self.inventory[invmenu-1].type-1].defn
          else: temp=item.item(0)
          self.inventory[invmenu-1].equip=1
          temp.equip=0
          self.strboost+=self.inventory[invmenu-1].strbonus
          self.intboost+=self.inventory[invmenu-1].intbonus
          self.conboost+=self.inventory[invmenu-1].conbonus
          self.wilboost+=self.inventory[invmenu-1].wilbonus
          self.perboost+=self.inventory[invmenu-1].perbonus
          self.dexboost+=self.inventory[invmenu-1].dexbonus
          self.chaboost+=self.inventory[invmenu-1].chabonus
          self.totatk+=self.inventory[invmenu-1].atk
          self.totdefn+=self.inventory[invmenu-1].defn
          self.equiparr[self.inventory[invmenu-1].type-1]=self.inventory[invmenu-1]
          del self.inventory[invmenu-1]
          self.inventory.append(temp)
          if self.inventory[len(self.inventory)-1].name==" ": del self.inventory[len(self.inventory)-1]

      #Destroy an item from inventory
      if invmenu=="q":
        print "Which item? "
        itdst=common.getch()
        if "0"<itdst<=str(len(self.inventory)):
          itemdestroyed=self.inventory[int(itdst)-1].name
          print "Destroy "+itemdestroyed+"? (y/n)"
          confirm=common.getch()
          if confirm=="y":
            del self.inventory[int(itdst)-1]
            raw_input(itemdestroyed+" destroyed")

      #Enchanting menu
      if invmenu=="w":
        try:
          print "Which item? "
          itech=int(common.getch())
          if 0<itech<=len(self.inventory):
            self.inventory[int(itech)-1].enchant(self)
            if self.inventory[int(itech)-1].name==" ": del self.inventory[int(itech)-1]
        except ValueError: pass

      #Unequip menu
      if invmenu=="a":
        try:
          unitem=int(raw_input("which item? "))
          if 0<int(unitem)<=len(self.equiparr) and self.equiparr[int(unitem)-1].name!=" ":
            temp=copy.copy(self.equiparr[int(unitem)-1])
            self.strboost-=self.equiparr[int(unitem)-1].strbonus
            self.intboost-=self.equiparr[int(unitem)-1].intbonus
            self.conboost-=self.equiparr[int(unitem)-1].conbonus
            self.wilboost-=self.equiparr[int(unitem)-1].wilbonus
            self.perboost-=self.equiparr[int(unitem)-1].perbonus
            self.dexboost-=self.equiparr[int(unitem)-1].dexbonus
            self.chaboost-=self.equiparr[int(unitem)-1].chabonus
            self.totatk-=self.equiparr[int(unitem)-1].atk
            self.totdefn-=self.equiparr[int(unitem)-1].defn
            self.inventory.append(temp)
            self.equiparr[int(unitem)-1].reset()
        except ValueError: print "Invalid choice"

      #Exit from inventory menu
      elif invmenu=="0": break

  def attack(self,mob):
    """
    attacks the mob object specified

    Returns a string to be displayed in the crawl screen
    """

    atkpow=(self.totatk*self.STR)-mob.defn
    if atkpow<=0: atkpow=1
    mob.HP-=atkpow
    mob.hit=1
    if mob.HP<=0:
      self.exp+=mob.exp
      if self.lv<=mob.lv+3: self.prestige+=mob.pres
      return "You attack "+mob.name+" for "+str(atkpow)+" damage!\nYou killed "+mob.name+" for "+str(mob.exp)+" experience!\nYou earn "+str(mob.pres)+" prestige points.\n"
    else: return "You attack "+mob.name+" for "+str(atkpow)+" damage!\n"

  def save(self):
    """
    Save function. Takes the player attributes and saves them into a text file in ../player/save
    If the path or the file do not exist they are created.
    """

    if not os.path.exists("../player/"): os.makedirs("../player/")
    with open("../player/save","w+") as savefile:
      savefile.write("# \n# Player \n# \n")
      savefile.write("Name:"+str(self.name)+"\n")
      savefile.write("Race:"+self.race+"\n")
      savefile.write("Class:"+self.charclass+"\n")
      savefile.write("Money:"+str(self.pocket)+"\n")
      savefile.write("Level:"+str(self.lv)+"\n")
      savefile.write("Exp:"+str(self.exp)+"\n")
      savefile.write("Points:"+str(self.points)+"\n")
      savefile.write("Floors:"+str(self.totalfl)+"\n")
      savefile.write("HP:"+str(self.hp2)+"\n")
      savefile.write("MP:"+str(self.mp2)+"\n")
      savefile.write("INT:"+str(self.INT)+"\n")
      savefile.write("DEX:"+str(self.DEX)+"\n")
      savefile.write("PER:"+str(self.PER)+"\n")
      savefile.write("WIL:"+str(self.WIL)+"\n")
      savefile.write("STR:"+str(self.STR)+"\n")
      savefile.write("CON:"+str(self.CON)+"\n")
      savefile.write("CHA:"+str(self.CHA)+"\n")

      savefile.write("#\n# Equipped items \n#\n")
      for a in self.equiparr: savefile.write("E:"+a.name+":"+str(a.enchantlv)+":"+str(a.type)+":"+str(a.atk)+":"+str(a.defn)+":"+str(a.strbonus)+":"+str(a.intbonus)+":"+str(a.dexbonus)+":"+str(a.perbonus)+":"+str(a.conbonus)+":"+str(a.wilbonus)+":"+str(a.chabonus)+":"+str(a.price)+"\n")
      
      savefile.write("#\n# Inventory items \n#\n")
      for a in self.inventory: savefile.write("I:"+a.name+":"+str(a.enchantlv)+":"+str(a.type)+":"+str(a.atk)+":"+str(a.defn)+":"+str(a.strbonus)+":"+str(a.intbonus)+":"+str(a.dexbonus)+":"+str(a.perbonus)+":"+str(a.conbonus)+":"+str(a.wilbonus)+":"+str(a.chabonus)+":"+str(a.price)+"\n")

      savefile.write("#\n# Belt items \n#\n")
      for a in self.belt:
        if a.type==4: savefile.write("B:"+str(a.type)+":"+a.name+"\n")
        if a.type==0: savefile.write("B:"+str(a.type)+":"+str(a.subtype)+":"+a.name+":"+str(a.hpr)+":"+str(a.mpr)+":"+str(a.price)+"\n")
    return "Player saved"

  def bury(self):
    """
    Saves the character into a cemetery file 

    This file is ../player/cemetery and contains all the player's dead characters.
    Similar to save, except more verbose.

    Unlike save it does not record things like maximum HP, items or stats, so buried characters can NOT be recovered.
    """

    if not os.path.exists("../player/"): os.makedirs("../player/")
    with open("../player/cemetery","a+") as cemetery:
      cemetery.write("RIP "+self.name+", the "+self.race+" "+self.charclass+" ("+str(self.prestige)+" prestige).\n")
      cemetery.write("Died at level "+str(self.lv)+" after exploring "+str(self.totalfl)+" floors.\n")
      cemetery.write("His body rots under "+str(self.pocket)+" gold.\n")
      cemetery.write('"'+raw_input("Your last words?")+'" \n \n')

  def reset(self):
    self.name="_"    
    self.pocket=0      
    self.exp=0
    self.lv=1
    self.points=0      
    self.race="_"
    self.charclass="_"

    self.inventory=[] 
    self.belt=[]
    self.equiparr=[]
    for i in range(11):
      new=item.item(0)
      self.equiparr.append(new)

    self.totalfl=0    
    self.prestige=0
    self.prestigelv=1

    self.INT     =self.DEX     =self.PER     =self.WIL     =self.STR     =self.CON     =self.CHA     =1
    self.intboost=self.dexboost=self.perboost=self.wilboost=self.strboost=self.conboost=self.chaboost=0
    self.totatk=self.totdefn=0
    self.HP=self.hp2=0
    self.MP=self.mp2=0
    self.END=self.SPD=0
    
    self.xpos=self.ypos=self.zpos=0

  def load(self):
    """
    Takes the information from the save file stored in ../player/save and loads it into the player object.
    """

    try:
      with open("../player/save","r") as savefile:
        if not savefile.readline().startswith("No character"):

          #Save current position
          tempx=self.xpos
          tempy=self.ypos
          tempz=self.zpos

          #Reset all the variables
          self.reset()

          #Load values from file
          for line in savefile:
            if not line.startswith("#"):
              #Load stats and player details
              parA=line.partition(':')[0]
              parB=line.strip().partition(':')[2]
              if   parA=="Name":  self.name=      parB
              elif parA=="Level": self.lv=        parB
              elif parA=="Exp":   self.exp=       parB
              elif parA=="Money": self.pocket=    parB
              elif parA=="INT":   self.INT=       parB
              elif parA=="DEX":   self.DEX=       parB
              elif parA=="PER":   self.PER=       parB
              elif parA=="WIL":   self.WIL=       parB
              elif parA=="STR":   self.STR=       parB
              elif parA=="CON":   self.CON=       parB
              elif parA=="CHA":   self.CHA=       parB
              elif parA=="Race":  self.race=      parB
              elif parA=="Class": self.charclass= parB
              elif parA=="HP":    self.HP=        parB
              elif parA=="hp2":   self.hp2=       parB
              elif parA=="MP":    self.MP=        parB
              elif parA=="mp2":   self.mp2=       parB
              elif parA=="Points":self.points=    parB
              elif parA=="Floors":self.totalfl=   parB

              #Load equipped items
                                                                                                                                                              #E:name:enchantlv:type:atk:defn:strbonus:intbonus:dexbonus:perbonus:conbonus:wilbonus:chabonus:price
              elif line.startswith("E:"):
                if not line.rstrip("\n").partition(':')[2].partition(':')[0]==" ":
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].name=           line.rstrip('\n').partition(':')[2].partition(':')[0]
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].enchantlv=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].type=       int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].atk=        int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].defn=       int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].strbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].intbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].dexbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].perbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].conbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].wilbonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].chabonus=   int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  self.equiparr[int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])-1].price=      int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2])

              #Load inventory
              elif line.startswith("I:"):
                temp=item.item(0)

                #E:name:enchantlv:type:atk:defn:strbonus:intbonus:dexbonus:perbonus:conbonus:wilbonus:chabonus:price
                temp.name=          line.rstrip('\n').partition(':')[2].partition(':')[0]
                temp.enchantlv= int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[0])
                temp.type=      int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.atk=       int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.defn=      int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.strbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.intbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.dexbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.perbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.conbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.wilbonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.chabonus=  int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                temp.price=     int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2])
                self.inventory.append(copy.copy(temp))

              #Load belt items
              elif line.startswith("B:"):
                line=line.lstrip("B:")
                if line.partition(':')[0]=="4": self.belt.append(item.consumable(4,0))
                if line.partition(':')[0]=="0":
                  temp=item.consumable(0,0)
                  temp.subtype=int(line.partition(':')[2].partition(':')[0])
                  temp.name=line.partition(':')[2].partition(':')[2].partition(':')[0]
                  temp.hpr=int(line.partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  temp.mpr=int(line.partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[0])
                  temp.price=int(line.rstrip('\n').partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2].partition(':')[2])
                  self.belt.append(copy.copy(temp))

          #Add empty items to belt until it's full
          while len(self.belt)<3: self.belt.append(item.consumable(4,0))

          #Update player bonuses
          for a in self.equiparr:
            self.strboost+=(a.strbonus)
            self.intboost+=(a.intbonus)
            self.dexboost+=(a.dexbonus)
            self.perboost+=(a.perbonus)
            self.conboost+=(a.conbonus)
            self.wilboost+=(a.wilbonus)
            self.chaboost+=(a.chabonus)
            self.totatk+=(a.atk)
            self.totdefn+=(a.defn)

          #Restore position values
          self.xpos=tempx
          self.ypos=tempy
          self.zpos=tempz

          return "Player loaded"
        else:return "Save file is empty"
    except IOError: return "Error loading character"