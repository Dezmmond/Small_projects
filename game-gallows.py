import os

img1 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#          |   #
#          |   #
#          |   #
#         /|\  #
################ """

img2 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#    |     |   #
#    |     |   #
#          |   #
#         /|\  #
################ """

img3 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#   /|     |   #
#    |     |   #
#          |   #
#         /|\  #
################ """

img4 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#   /|\    |   #
#    |     |   #
#          |   #
#         /|\  #
################ """

img5 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#   /|\    |   #
#    |     |   #
#   /      |   #
#         /|\  #
################ """

img6 = """
################
#              #
#    _______   #
#    |     |   #
#    O     |   #
#   /|\    |   #
#    |     |   #
#   / \    |   #
#         /|\  #
################ """

images = {1: img1, 2: img2, 3: img3, 4: img4, 5: img5, 6: img6,}

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def open_letter():
    for j in range(len(hidden_word)):
        if hidden_word[j] == letter:
            show_word[j] = letter


if __name__ == "__main__":
    hidden_word = str(input("Загадай слово: "))

    cls()

    show_word = []
    for i in range(len(hidden_word)):
        if i == 0 or i == len(hidden_word) - 1:
            show_word.append(hidden_word[i])
        elif hidden_word[i] == hidden_word[0] or hidden_word[i] == hidden_word[len(hidden_word) - 1]:
            show_word.append(hidden_word[i])
        else:
            show_word.append('_')
    print(' '.join(show_word))

    game_over = False
    game_tiks = 0
    letters_pool = ""
    while game_tiks < 6 and not game_over:
        if ''.join(show_word) == hidden_word:
            print("### Молодцом! ###")
            break

        letter = str(input("\nПопробуй угадать букву: "))
        if letter in hidden_word:
            open_letter()
            print(' '.join(show_word))
        else:
            game_tiks += 1
            letters_pool += letter + ', '
            cls()
            print(images[game_tiks])
            print("Такой буквы нет!\nКоличество оставшихся попыток: " + str(6 - game_tiks))
            print("Ошибки: " + letters_pool)
            print(' '.join(show_word))

    if game_tiks == 6:
        print("Загаданное слово: " + ''.join(hidden_word))
        print("### Ты проиграл! ###")
