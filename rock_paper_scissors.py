import random
import time

IN_GAME = True

def main():
    var = {1 : "Rock", 2 : "Paper", 3 : "Scissors"}

    while IN_GAME:
        print(" #---Game---#\n",
                "1. Rock\n",
                "2. Paper\n",
                "3. Scissors\n")

        pl_choose = int(input("Your choose?\n>>> "))
        pc_choose = random.choice([1,2,3])

        for i in range(3):
            print(i + 1)
            time.sleep(1)

        print("You: " + var[pl_choose] + "\n",
              "PC: " + var[pc_choose])

        if pl_choose == pc_choose:
            print("Draw")

        elif (pl_choose == 1 and pc_choose == 2) or (pl_choose == 2 and pc_choose == 3) \
                        or (pl_choose == 3 and pc_choose == 1):
            print("You loose\n")
            wheel()

        elif (pl_choose == 1 and pc_choose == 3) or (pl_choose == 2 and pc_choose == 1) \
                        or (pl_choose == 3 and pc_choose == 2):
            print("You win\n")
            wheel()


def wheel():
    global IN_GAME

    cont = str(input("Do you want to continue? (y/n)\n> "))
    if cont == "n":
        IN_GAME = False


if __name__ == "__main__":
    main()