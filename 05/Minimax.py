import math

def create_board(size):
    return [[" " for _ in range(size)] for _ in range(size)]


def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * (len(row) * 4 - 3))


def check_winner(board):
    n = len(board)

    lines = []

    lines.extend(board)

    for col in range(n):
        lines.append([board[row][col] for row in range(n)])

    lines.append([board[i][i] for i in range(n)])
    lines.append([board[i][n - 1 - i] for i in range(n)])

    for line in lines:
        if line[0] != " " and all(x == line[0] for x in line):
            return line[0]

    return None


def evaluate(board, depth):
    winner = check_winner(board)

    if winner == "O":
        return 10000 + depth

    if winner == "X":
        return -10000 - depth

    if all(cell != " " for row in board for cell in row):
        return 0

    score = 0
    n = len(board)

    lines = list(board)

    for col in range(n):
        lines.append([board[row][col] for row in range(n)])

    lines.append([board[i][i] for i in range(n)])
    lines.append([board[i][n - 1 - i] for i in range(n)])

    for line in lines:
        computer = line.count("O")
        human = line.count("X")

        if human == 0:
            score += computer ** 2

        if computer == 0:
            score -= human ** 2

    return score


def minimax(board, depth, maximizing):
    winner = check_winner(board)

    if winner or depth == 0:
        return evaluate(board, depth)

    if all(cell != " " for row in board for cell in row):
        return 0

    n = len(board)

    if maximizing:
        best_score = -math.inf

        for i in range(n):
            for j in range(n):
                if board[i][j] == " ":
                    board[i][j] = "O"

                    score = minimax(board, depth - 1, False)

                    board[i][j] = " "
                    best_score = max(best_score, score)

        return best_score

    else:
        best_score = math.inf

        for i in range(n):
            for j in range(n):
                if board[i][j] == " ":
                    board[i][j] = "X"

                    score = minimax(board, depth - 1, True)

                    board[i][j] = " "
                    best_score = min(best_score, score)

        return best_score


def computer_move(board, depth):
    n = len(board)
    best_score = -math.inf
    best_move = None

    for i in range(n):
        for j in range(n):
            if board[i][j] == " ":
                board[i][j] = "O"

                score = minimax(board, depth - 1, False)

                board[i][j] = " "

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        board[best_move[0]][best_move[1]] = "O"


def human_move(board):
    n = len(board)

    while True:
        try:
            row = int(input("Podaj wiersz: ")) - 1
            col = int(input("Podaj kolumne: ")) - 1

            if 0 <= row < n and 0 <= col < n:
                if board[row][col] == " ":
                    board[row][col] = "X"
                    break

            print("Nieprawidlowy ruch!")

        except ValueError:
            print("Podaj liczby!")


def main():
    size = int(input("Rozmiar planszy (np. 3): "))
    depth = int(input("Maksymalna glebokosc Minimax: "))

    if size < 3 or depth < 1:
        print("Nieprawidlowe parametry!")
        return

    first = input("Kto zaczyna? (u - uzytkownik, k - komputer): ").lower()

    board = create_board(size)
    current_player = first

    while True:
        print_board(board)

        if current_player == "u":
            human_move(board)
            current_player = "k"
        else:
            print("Ruch komputera...")
            computer_move(board, depth)
            current_player = "u"

        winner = check_winner(board)

        if winner:
            print_board(board)
            if winner == "O":
                print("Wygrywa komputer!")
            else:
                print("Wygrywa uzytkownik!")
            break

        if all(cell != " " for row in board for cell in row):
            print_board(board)
            print("Remis!")
            break

if __name__ == "__main__":
    main()
