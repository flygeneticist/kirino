#! /usr/bin/env pyton

import copy, os, random
import item
import common, parser

npcdata={}
vendordata={}

class npc:
  """
  NPC generator and manager

  #Characteristic strings
  name=""           #Name
  secondname=""     #Second name
  personality=""    #Personality
  appearance=""     #Appearance
  job=""            #Job
  likes1=""         #Things this NPC likes (1)
  likes2=""         #Things this NPC likes (2)
  dislikes1=""      #Things this NPC dislikes (1)
  dislikes2=""      #Things this NPC dislikes (2)
  
  #Primary attributes
  STR=1             #Strenght
  DEX=1             #Dexterity
  CON=1             #Constitution
  INT=1             #Intelligence
  PER=1             #Perception
  WIL=1             #Willpower
  CHA=1             #Charisma

  #Status variables

  rel=0             #Relation with player 
                    # <-10    - bad
                    # -10,10  - neutral
                    # >10     - good
  """
  
  def __init__(self,gender,stat,total):
    """
    Constructor. Generates an NPC, as in the standalone NPC generator:
    https://github.com/Achifaifa/GM-Tools/tree/master/npcgenerator

    Needs:

    Gender
      0 female
      1 male
      Anything else defaults at a random genre

    Maximum stat level
      A number smaller than 1 defaults to 5

    Total attribute points
      A number smaller than 1 defaults to 16
    """

    #Sanitize input
    if stat<1: stat=5
    if total<1: total=16
    if gender not in [0,1]: gender=random.choice([0,1])

    self.STR=self.DEX=self.CON=self.INT=self.PER=self.WIL=self.CHA=1 
    self.rel=0
    
    for i in range(total-6):
      rnd=random.randint(1,7)
      if rnd==1:
        if self.STR<stat: self.STR=self.STR+1
      elif rnd==2:
        if self.DEX<stat: self.DEX=self.DEX+1
      elif rnd==3:
        if self.CON<stat: self.CON=self.CON+1
      elif rnd==4:
        if self.INT<stat: self.INT=self.INT+1
      elif rnd==5:
        if self.PER<stat: self.PER=self.PER+1
      elif rnd==6:
        if self.WIL<stat: self.WIL=self.WIL+1
      elif rnd==7:
        if self.CHA<stat: self.CHA=self.CHA+1

    if gender==0: self.name=random.choice(npcdata["namefemale"])
    if gender==1: self.name=random.choice(npcdata["namemale"])
    self.secondname=random.choice(npcdata["secondnames"])
    self.personality=random.choice(npcdata["personality"])
    self.appearance=random.choice(npcdata["appearance"])
    self.job=random.choice(npcdata["jobs"])
    self.likes1=random.choice(npcdata["things"])
    self.likes2=random.choice(npcdata["things"])
    self.dislikes1=random.choice(npcdata["things"])
    self.dislikes2=random.choice(npcdata["things"])

class vendor:
  """
  Vendor class. Creates and manages vendors (shops) in a dungeon floor.
  """

  def __init__(self):
    """
    Vendor constructor. 

    Generates a random NPC (The shopkeeper) and generates items to be sold.
    """

    self.keeper=npc(0,0,0)
    self.forsale=[]
    self.potforsale=[]
    for i in range(random.randrange(4,7)): self.forsale.append(item.item(random.randrange(1,12)))
    for i in range(random.randrange(1,4)): self.potforsale.append(item.consumable(random.choice([0,0,3,1]),0))

  def commerce(self,player):
    while 1:
      common.version()
      print "Shop\n"
      print random.choice(vendordata["welcomemsg"])
      print "\n1.- Sell"
      print "2.- Buy items"
      print "3.- Buy food/potions"
      print "4.- Chat"
      print "--"
      print "0.- Back"
      print "\n->",
      commenu=common.getch()

      if commenu=="1":self.sell(player)
      if commenu=="2":self.buyit(player)
      if commenu=="3":self.buypot(player)
      if commenu=="4":parser.chat(self.keeper,player)
      if commenu=="0":
        print random.choice(vendordata["byemsg"])
        common.getch()
        break
      else: pass

  def buypot(self,player):
    """
    Sells potions to the player. Three random potions are generated by the vendor.
    """
    
    while 1:
      common.version()
      print "Shop - Buy potions ("+str(player.pocket)+"G)\n"
      for i in range(len(self.potforsale)): print str(i+1)+".- "+self.potforsale[i].name+" ("+str(round(self.pricecalc(player)*self.potforsale[i].price))+"G)"
      print "--"
      print "0.- Back"
      print "\n->",
      buypotmenu=common.getch()

      if buypotmenu=="0":
        print "Nice doing business with you!"
        common.getch()
        break

      try:
       
          if len(self.potforsale)!=0:
            if player.pocket>=round(self.pricecalc(player)*self.potforsale[int(buypotmenu)-1].price):
              if player.belt[0].name=="--EMPTY--":
                player.belt[0]=copy.copy(self.potforsale[int(buypotmenu)-1])
              elif player.belt[1].name=="--EMPTY--":
                player.belt[1]=copy.copy(self.potforsale[int(buypotmenu)-1])
              elif player.belt[2].name=="--EMPTY--":
                player.belt[2]=copy.copy(self.potforsale[int(buypotmenu)-1])
              elif player.belt[3].name=="--EMPTY--":
                player.belt[3]=copy.copy(self.potforsale[int(buypotmenu)-1])
              elif player.belt[3].name=="--EMPTY--":
                player.belt[3]=copy.copy(self.potforsale[int(buypotmenu)-1])
              elif player.belt[3].name=="--EMPTY--":
                player.belt[3]=copy.copy(self.potforsale[int(buypotmenu)-1])
              player.pocket-=self.potforsale[int(buypotmenu)-1].price
              player.totalspn+=self.potforsale[int(buypotmenu)-1].price
              del self.potforsale[int(buypotmenu)-1]
              self.keeper.rel+=1
              print random.choice(vendordata["okmsg"])
              player.totalbuy+=1
              common.getch()

            else:
              print random.choice(vendordata["failmsg"])
              common.getch()

      except (ValueError,IndexError): pass
        

  def pricecalc(self,player):
    """
    Calculates the trading multiplier based on the player charisma and the player-NPC relationship

    Base multiplier: 2

    Additional multipliers: 

    Charisma: +- 0.1 for each point
    Relationship with vendor: +-0.5 for every 10 points
    """

    #Base modifier
    modifier=2

    #Charisma modifiers
    modifier-=(player.CHA+player.chaboost-2/10)

    #Relationship modifiers
    modifier-=(self.keeper.rel/15)

    if modifier<0.5: modifier=0.5

    return modifier

  def buyit(self,player):
    """
    Display the list of items available for buying from the vendor
    """

    while 1:
      common.version()
      print "Shop - Buy items ("+str(player.pocket)+"G)\n"
      for i in range(len(self.forsale)): print str(i+1)+".- "+self.forsale[i].name+" ("+str(round(self.pricecalc(player)*self.forsale[i].price))+"G)"
      print "--"
      print "0.- Back"
      print "\n->",

      try:
          buymenuc=common.getch()
          if buymenuc=="0":
            print "Nice doing business with you!"
            common.getch()
            break

          if player.pocket>=round(self.pricecalc(player)*self.forsale[int(buymenuc)-1].price):
            player.pocket-=(round(self.pricecalc(player)*self.forsale[int(buymenuc)-1].price))
            player.totalspn+=(round(self.pricecalc(player)*self.forsale[int(buymenuc)-1].price))
            if player.pickobject(self.forsale[int(buymenuc)-1]):
              print random.choice(vendordata["okmsg"])
              self.keeper.rel+=1
              del self.forsale[int(buymenuc)-1]
              player.totalbuy+=1
              common.getch()
            else:
              print random.choice(vendordata["failmsg"])
              common.getch()
          else:
            print random.choice(vendordata["failmsg"])
            common.getch()
      except (ValueError, IndexError): pass

  def sell(self,player):
    """
    Display the list of items in the inventory to sell
    """

    while 1:
      common.version()
      print "Shop - Sell items ("+str(player.pocket)+"G)\n"
      for i in range(len(player.inventory)):print str(i+1)+".- "+player.inventory[i].name+" ("+str(round(player.inventory[i].price/self.pricecalc(player)))+"G)"
      print "--"
      print "0.- Back"
      print "\n->",

      try:
          sellmenuc=common.getch()
          if sellmenuc=="0":
            print "Nothing else? I can pay you with roaches!"
            common.getch()
            break
          player.pocket+=round(player.inventory[int(sellmenuc)-1].price/self.pricecalc(player))
          player.totalgld+=round(player.inventory[int(sellmenuc)-1].price/self.pricecalc(player))
          player.totalsll+=1
          self.forsale.append(copy.copy(player.inventory[int(sellmenuc)-1]))
          del player.inventory[int(sellmenuc)-1]
          self.keeper.rel+=1
          print random.choice(vendordata["okmsg"])
          common.getch()
      except (ValueError, IndexError): pass

def sanitize(): 
  """
  Rewrite the NPC data files to follow formatting standards.
  """

  try:
    print "Sanitizing NPC files...    ",
    with open("../data/npcs/firstnames_male","r+") as firstnamesmale:
      lines=firstnamesmale.readlines()
      firstnamesmale.seek(0,0)
      for line in lines: firstnamesmale.write(line.title())
       
    with open("../data/npcs/firstnames_female","r+") as firstnamesfemale:
      lines=firstnamesfemale.readlines()
      firstnamesfemale.seek(0,0)
      for line in lines: firstnamesfemale.write(line.title())

    with open("../data/npcs/secondnames","r+") as secondnames:
      lines=secondnames.readlines()
      secondnames.seek(0,0)
      for line in lines: secondnames.write(line.title())

    #First letter on the first selected thing will be capped later.
    with open("../data/npcs/things","r+") as things:
      lines=things.readlines()
      things.seek(0,0)
      for line in lines: things.write(line.lower())

  except IOError:
    print "error sanitizing NPC data files"
    common.getch()

def load(): 
  """
  Load the data from the files into a dictionary. 
  The arrays with the data is stored in a dictionary.
  The dictionary is global in the module and is used by default in the NPC class.
  """

  global npcdata
  global vendordata

  try:
    print "Loading NPC data files...  ",
    with open("../data/npcs/firstnames_male","r") as file:
      namemale = []
      for line in file: namemale.append(line.rstrip('\n'))
    npcdata["namemale"]=namemale
     
    with open("../data/npcs/firstnames_female","r") as file:
      namefemale = []
      for line in file: namefemale.append(line.rstrip('\n'))
    npcdata["namefemale"]=namefemale

    with open("../data/npcs/secondnames","r") as file:
      secondnames = []
      for line in file: secondnames.append(line.rstrip('\n'))
    npcdata["secondnames"]=secondnames

    with open("../data/npcs/appearance","r") as file:
      appearance = []
      for line in file: appearance.append(line.rstrip('\n'))
    npcdata["appearance"]=appearance

    with open("../data/npcs/personality","r") as file:
      personality = []
      for line in file: personality.append(line.rstrip('\n'))
    npcdata["personality"]=personality

    with open("../data/npcs/things","r") as file:
      things = []
      for line in file: things.append(line.rstrip('\n'))
    npcdata["things"]=things

    with open("../data/npcs/jobs","r") as file:
      jobs = []
      for line in file: jobs.append(line.rstrip('\n'))
    npcdata["jobs"]=jobs

  except IOError:
    print "error loading NPC data files"
    common.getch()

  try:
    print "Loading NPC messages...    ",
    with open("../data/vendor/vendormsg","r") as file:
      welcomemsg=[]
      byemsg=[]
      okmsg=[]
      failmsg=[]
      for line in file:
        line=line.strip()
        if not line.startswith("#"):
          if line.partition(':')[0]=="W":
            welcomemsg.append(line.partition(':')[2])
            vendordata["welcomemsg"]=welcomemsg
          if line.partition(':')[0]=="G":
            byemsg.append(line.partition(':')[2])
            vendordata["byemsg"]=byemsg
          if line.partition(':')[0]=="S":
            okmsg.append(line.partition(':')[2])
            vendordata["okmsg"]=okmsg
          if line.partition(':')[0]=="F":
            failmsg.append(line.partition(':')[2])
            vendordata["failmsg"]=failmsg

  except IOError:
    print "error loading vendor data files"
    common.getch()

if __name__=="__main__":
  try: os.chdir(os.path.dirname(__file__))
  except OSError: pass 
  sanitize()
  load()
  common.version()
  print "NPC module test"
  while 1:
    new=npc(0,0,0)
    print "Name: %s %s"               %(new.name,new.secondname)
    print "Personality: %s"           %(new.personality)
    print "Appearance: %s"            %(new.appearance)
    print "Works as: %s \n\n---\n\n"  %(new.job)
    common.getch()