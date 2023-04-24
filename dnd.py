import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    install("numpy")

# playable DnD? We'll see
import numpy as np
from math import ceil

def roll(n):
    """
    Simulate a roll of any size dice
    """
    return np.random.randint(1,n + 1)

class NoDiceError(Exception):
    "Raised when an input was not in the array of dice"
    pass

def readscores(rolls):
    scorearray = [8,8,8,8,8,8] # str, dex, con, int, wis, cha
    for i, title in enumerate(["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]):
        while True:
            try:
                temp =  int(input(f"{title}: "))
                if temp in rolls:
                    scorearray[i] = temp
                    rolls.remove(temp)
                else:
                    raise NoDiceError

            except ValueError:
                print("Error: must be an integer")

            except NoDiceError:
                print(f"Error: Input not in the rolls obtained, which are: {str(rolls)}")

            else:
                break

        print(f"remaining rolls: {rolls}")
    
    return scorearray

class Character:
    def __init__(self, name):
        self.name = name
        self.stre = 8
        self.dex = 8
        self.con = 8
        self.int = 8
        self.wis = 8
        self.cha = 8
        self.strmod = ceil(self.stre / 2) - 5
        self.dexmod = ceil(self.dex / 2) - 5
        self.conmod = ceil(self.con / 2) - 5
        self.intmod = ceil(self.int / 2) - 5
        self.wismod = ceil(self.wis / 2) - 5
        self.chamod = ceil(self.cha / 2) - 5
        self.level = 1
        self.clas = ""
        self.hitdie = 0
        self.armorprof = []
        self.weaponprof = []
        self.toolprof = []
        self.hp = 0
        self.savingthrow = []
        self.equipment = []
        self.prof = 2
        self.skills = []
    
    def stats(self, mode):
        """
        Different ways of getting stats for your character
        roll = 4d6 drop lowest
        standard array = [15,14,13,12,10,8]
        pont buy = 27 points, point per score changes
        """
        self.mode = mode
        if mode == "roll":
            rolls = [0,0,0,0,0,0]
            for i in range(len(rolls)):
                a = roll(6)
                b = roll(6)
                c = roll(6)
                d = roll(6)
                rolls[i] = a+b+c+d - min(a,b,c,d)
            print(f"Rolled stats: {str(rolls)}")
            print("What would you like to assign to each ability score?")
            
            self.stre, self.dex, self.con, self.int, self.wis, self.cha = readscores(rolls)
          
        elif mode == "standard array":
            rolls = [15,14,13,12,10,8]
            print("Stats: " + str(rolls))
            print("What would you like to assign to each ability score?")

            self.stre, self.dex, self.con, self.int, self.wis, self.cha = readscores(rolls)

        elif mode == "point buy":
            points = {"8" : 0, "9" : 1, "10" : 2, "11" : 3, "12" : 4, "13" : 5, "14" : 7, "15" : 9}
            pointstotal = 27
            rolls = [8,8,8,8,8,8]
            rolltable = "Score  | Point Cost\n"+"  8    |    0  \n" + "  9    |    1  \n" + "  10   |    2  \n" + "  11   |    3  \n" + "  12   |    4  \n" + "  13   |    5  \n" + "  14   |    7  \n"+"  15   |    9  \n"
            print("The ability score and point costs are as follows: \n" + rolltable)
            while True:
                print("Current stats: " + str(rolls) + ", [str, dex, con, int, wis, cha]" + ", Points available: " + str(pointstotal))
                if pointstotal == 0:
                    print("Your stats are: " + str(rolls))
                    break
                tochange = str(input("Enter the position of stat you'd like to change and the stat you'd like to change it to or 'done' if done (ie to change 8 in [12,13,10,8,9] to a 9, enter 4,9) : "))
                if tochange == "done":
                    print("Your stats are: " + str(rolls))
                    break
                else:
                    """
                    issues:
                    not in format #,#
                    #1 not between 1 and 6
                    #2 would result in lower than 0 points
                    """
                    try:
                        if int(tochange[0]) > 6 or int(tochange[0]) < 1:
                            print("Error: position value must be between 1 and 6, inclusive\n")
                            continue
                        if tochange[1] != ',':
                            print("Error: input must be of type #,#\n")
                        if int(tochange[2:]) < 8 or int(tochange[2:]) > 15:
                            print("Error: new stat must be between 8 and 15, inclusive\n")
                            continue
                    except ValueError:
                        print("Error: input must be of type #,#\n")
                        continue
                    
                    newvalue = int(tochange[2:])
                    newvaluepoints = points[str(newvalue)]
                    newpos = int(tochange[0])-1
                    currentpoints = points[str(rolls[newpos])]
                    if pointstotal - abs(newvaluepoints - currentpoints) >= 0:                    
                        if newvalue > rolls[newpos]:
                            rolls[newpos] = newvalue
                            pointstotal -= abs(newvaluepoints-currentpoints)
                        elif newvalue < rolls[newpos]:
                            rolls[newpos] = newvalue
                            pointstotal += abs(newvaluepoints-currentpoints)
                    else:
                        print("Error: too many points allocated")
                        continue 
                self.stre = rolls[0]
                self.dex = rolls[1]
                self.con = rolls[2]
                self.int = rolls[3]
                self.wis = rolls[4]
                self.cha = rolls[5]
        elif roll not in ["roll", "standard array", "point buy"]:
            print("Error: stats argument must be one of 'roll', 'standard array', or 'point buy'")
            return
        self.strmod = ceil(self.stre / 2) - 5
        self.dexmod = ceil(self.dex / 2) - 5
        self.conmod = ceil(self.con / 2) - 5
        self.intmod = ceil(self.int / 2) - 5
        self.wismod = ceil(self.wis / 2) - 5
        self.chamod = ceil(self.cha / 2) - 5

    # def __str__(self):
    #     return "Level =  %, class = %, race = %, background = %" % (self.level, self.cls, self.race, self.background)
    
    def get_class(self):
        print(
            """The available classes to choose from are:
            Artificer
            Barbarian
            Bard
            Cleric
            Druid
            Fighter
            Monk
            Paladin
            Ranger
            Rogue
            Sorceror
            Warlock
            Wizard
            """)
        while self.clas == "":
            inputclass = input(f"Which class is {self.name}? Choosing from the list above: ")
            inputclass.lower()
            possibleclass = ["artificer", "barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorceror", "warlock", "wizard"]
            if inputclass.lower() not in possibleclass:
                print("Error: must choose one of the available classes")
            else:
                self.clas = inputclass
                
        if self.clas == "artificer":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield"]
            self.weaponprof = ["simple"]
            self.toolprof = ["thieves", "tinkers"]
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod + self.prof
            self.intsav = self.intmod + self.prof
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "barbarian":
            self.hitdie = 12
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield"]
            self.weaponprof = ["simple", "martial"]
            self.toolprof = []
            self.strsav = self.strmod + self.prof
            self.dexsav = self.dexmod
            self.consav = self.conmod + self.prof
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "bard":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light"]
            self.weaponprof = ["simple", "hand crossbow", "longsword", "rapier", "shortsword"]
            self.toolprof = ["musical"]
            self.strsav = self.strmod
            self.dexsav = self.dexmod + self.prof
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod + self.prof

        elif self.clas == "cleric":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield"]
            self.weaponprof = ["simple"]
            self.toolprof = []
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod + self.prof
            self.chasav = self.chamod + self.prof

        elif self.clas == "druid":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield"]
            self.weaponprof = ["club", "dagger", "dart", "javelin", "mace", "quarterstaff", "scimitar", "sickle", "sling", "spear"]
            self.toolprof = ["herbalism"]
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod
            self.intsav = self.intmod + self.prof
            self.wissav = self.wismod + self.prof
            self.chasav = self.chamod

        elif self.clas == "fighter":
            self.hitdie = 10
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield", "heavy"]
            self.weaponprof = ["simple", "martial"]
            self.toolprof = []
            self.strsav = self.strmod + self.prof
            self.dexsav = self.dexmod
            self.consav = self.conmod + self.prof
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "monk":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = []
            self.weaponprof = ["simple", "shortsword"]
            self.toolprof = [] # one type of artisan/musical instrument
            self.strsav = self.strmod + self.prof
            self.dexsav = self.dexmod + self.prof
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "paladin":
            self.hitdie = 10
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield", "heavy"]
            self.weaponprof = ["simple", "martial"]
            self.toolprof = []
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod + self.prof
            self.chasav = self.chamod + self.prof

        elif self.clas == "ranger":
            self.hitdie = 10
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light", "medium", "shield"]
            self.weaponprof = ["simple", "martial"]
            self.toolprof = []
            self.strsav = self.strmod + self.prof
            self.dexsav = self.dexmod + self.prof
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "rogue":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light"]
            self.weaponprof = ["simple", "hand crossbow", "longsword", "rapier", "shortsword"]
            self.toolprof = ["thieves"]
            self.strsav = self.strmod
            self.dexsav = self.dexmod + self.prof
            self.consav = self.conmod
            self.intsav = self.intmod + self.prof
            self.wissav = self.wismod
            self.chasav = self.chamod

        elif self.clas == "sorceror":
            self.hitdie = 6
            self.hp = self.hitdie + self.conmod
            self.armorprof = []
            self.weaponprof = ["dagger", "dart", "sling", "quarterstaff", "light crossbow"]
            self.toolprof = []
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod + self.prof
            self.intsav = self.intmod
            self.wissav = self.wismod
            self.chasav = self.chamod + self.prof

        elif self.clas == "warlock":
            self.hitdie = 8
            self.hp = self.hitdie + self.conmod
            self.armorprof = ["light"]
            self.weaponprof = ["simple"]
            self.toolprof = []
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod
            self.intsav = self.intmod
            self.wissav = self.wismod + self.prof
            self.chasav = self.chamod + self.prof

        elif self.clas == "wizard":
            self.hitdie = 6
            self.hp = self.hitdie + self.conmod
            self.armorprof = []
            self.weaponprof = ["dagger", "dart", "sling", "quarterstaff", "light crossbow"]
            self.toolprof = []
            self.strsav = self.strmod
            self.dexsav = self.dexmod
            self.consav = self.conmod
            self.intsav = self.intmod + self.prof
            self.wissav = self.wismod
            self.chasav = self.chamod + self.prof
    
    def get_skills(self):
        if self.clas == "artificer":
            nstats = 2
            statoptions = ["arcana", "history", "investigation", "medicine", "nature", "perception", "sleight of hand"]
        elif self.clas == "barbarian":
            nstats = 2
            statoptions = ["animal handing", "athletics", "intimidation", "nature", "perception", "survival"]
        elif self.clas == "bard":
            nstats = 3
            statoptions = ["acrobatics", "animal handling", "arcana", "athletics", "deception", "history", "insight", "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion", "religion", "sleight of hand", "stealth", "survival"]
        elif self.clas == "cleric":
            nstats = 2
            statoptions = ["history", "insight", "medicine", "perception", "religion"]
        elif self.clas == "druid":
            nstats = 2
            statoptions = ["animal handling", "arcana", "insight", "medicine", "nature", "perception", "religion", "survival"]
        elif self.clas == "fighter":
            nstats = 2
            statoptions = ["acrobatics", "animal handling", "athletics", "history", "insight", "intimidation", "perception", "survival"]
        elif self.clas == "monk":
            nstats = 2
            statoptions = ["acrobatics", "athletics", "history", "insight", "religion", "stealth"]
        elif self.clas == "paladin":
            nstats = 2
            statoptions = ["athletics", "insight", "intimidation", "medicine", "persuasion", "religion"]
        elif self.clas == "ranger":
            nstats = 3
            statoptions = ["animal handling", "athletics", "insight", "investigation", "nature", "perception", "stealth", "survival"]
        elif self.clas == "rogue":
            nstats = 4
            statoptions = ["acrobatics", "athletics", "deception", "insight", "intimidation", "investigation", "perception", "performance", "persuasion", "sleight of hand", "stealth"]
        elif self.clas == "sorceror":
            nstats = 2
            statoptions = ["arcana", "deception", "insight", "intimidation", "persuasion", "religion"]
        elif self.clas == "warlock":
            nstats = 2
            statoptions = ["arcana", "deception", "history", "insight", "intimidation", "investigation", "nature", "religion"]
        elif self.clas == "wizard":
            nstats = 2
            statoptions = ["arcana", "history", "insight", "investigation", "medicine", "religion"]
        
        print(f"As a(n) {self.clas}, you can choose {nstats} skills from ", end = "")
        for i in range(len(statoptions)):
            print(statoptions[i], end = "")
            if i != len(statoptions) - 1:
                print(", ", end = "")
        print("\n")
        
        for i in range(nstats):
            while True:
                skill = input(f"Skill {i + 1}: ")
                if skill not in statoptions:
                    print(f"Error: skill must be one of {statoptions}")
                else:
                    break
            self.skills.append(skill)
