
import sys
import time
from collections import deque

D = {
    "┼": "UDLR", "│": "UD", "─": "LR",
    "┐": "DL", "┘": "UL", "└": "UR", "┌": "DR",
    "┤": "UDL", "┴": "ULR", "├": "UDR", "┬": "DLR",
    "╵": "U", "╷": "D", "╴": "L", "╶": "R", " ": ""
}
M = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
O = {"U": "D", "D": "U", "L": "R", "R": "L"}
C = {"start": "\033[1;31m", "end": "\033[1;34m",
     "visited": "\033[1;32m", "waiting": "\033[1;33m"}
RESET = "\033[0m"


def draw(maze, start, end, visited, waiting):
    print("\033[2J\033[H", end="")
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            p = (r, c)
            color = (C["start"] if p == start else
                     C["end"] if p == end else
                     C["waiting"] if p in waiting else
                     C["visited"] if p in visited else "")
            print(color + ch + RESET if color else ch, end="")
        print()


def solve(maze, start, end, bfs):
    moves = deque([start])
    visited, waiting, parent = set(), {start}, {}
    steps = 0

    while moves:
        p = moves.popleft() if bfs else moves.pop()
        waiting.discard(p)

        if p in visited:
            continue

        visited.add(p)
        steps += 1
        draw(maze, start, end, visited, waiting)
        time.sleep(0.1)

        if p == end:
            path = []
            while p != start:
                path.append(p)
                p = parent[p]
            path.append(start)
            return path[::-1], steps

        r, c = p
        directions = D.get(maze[r][c], "")

        for d in directions:
            dr, dc = M[d]
            q = (r + dr, c + dc)

            if not (0 <= q[0] < len(maze) and
                    0 <= q[1] < len(maze[0])):
                continue

            if O[d] in D.get(maze[q[0]][q[1]], "") and q not in visited and q not in waiting:
                parent[q] = p
                waiting.add(q)
                moves.append(q)

    return None, steps


def main():
    if len(sys.argv) != 2:
        print(f"Użycie: python3 {sys.argv[0]} mapa.txt")
        return

    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            maze = [list(line.rstrip("\n\r")) for line in f]
    except OSError as e:
        print("Błąd pliku:", e)
        return

    if not maze:
        print("Mapa jest pusta.")
        return

    width = max(map(len, maze))
    maze = [row + [" "] * (width - len(row)) for row in maze]

    draw(maze, None, None, set(), set())
    print("Rozmiar:", len(maze), "x", width)

    def coords(text):
        while True:
            try:
                r, c = map(int, input(text).split())
                if 0 <= r < len(maze) and 0 <= c < width:
                    if D.get(maze[r][c], ""):
                        return r, c
                print("Nieprawidłowe współrzędne lub puste pole.")
            except ValueError:
                print("Podaj: wiersz kolumna")

    start = coords("Start (wiersz kolumna): ")
    end = coords("Koniec (wiersz kolumna): ")

    while True:
        alg = input("Algorytm (BFS/DFS): ").upper()
        if alg in ("BFS", "DFS"):
            break

    path, steps = solve(maze, start, end, alg == "BFS")

    if path:
        draw(maze, start, end, set(path), set())
        print("\033[1;32mZnaleziono ścieżkę!\033[0m")
        print("Kroki:", steps, "| Długość ścieżki:", len(path) - 1)
    else:
        draw(maze, start, end, set(), set())
        print("\033[1;31mNie znaleziono ścieżki.\033[0m")
        print("Kroki:", steps)


if __name__ == "__main__":
    main()
