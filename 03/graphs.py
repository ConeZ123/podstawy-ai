
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import heapq


# =======
# GRAF
# =======

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def load(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        n = int(lines[0])
        if len(lines) != 2 * n + 1:
            raise ValueError("Nieprawidłowa liczba linii w pliku.")

        self.nodes = {}
        self.edges = {i: set() for i in range(1, n + 1)}

        for i in range(n):
            x, y = map(int, lines[i + 1].split())
            self.nodes[i + 1] = (x, y)

        for i in range(n):
            data = list(map(int, lines[n + 1 + i].split()))
            count = data[0]

            if len(data) != count + 1:
                raise ValueError("Nieprawidłowa lista sąsiadów.")

            for neighbor in data[1:]:
                if neighbor < 1 or neighbor > n:
                    raise ValueError("Nieprawidłowy numer wierzchołka.")

                if neighbor != i + 1:
                    self.edges[i + 1].add(neighbor)
                    self.edges[neighbor].add(i + 1)

    def distance(self, a, b):
        x1, y1 = self.nodes[a]
        x2, y2 = self.nodes[b]

        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


# ==========
# ALGORYTMY 
# ==========

class Search:
    def __init__(self, graph, start, goal, algorithm):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.algorithm = algorithm

        self.open = []
        self.closed = set()

        self.cost = {start: 0}
        self.parent = {}

        self.finished = False
        self.path = []

        self.counter = 0

        heapq.heappush(
            self.open,
            (self.priority(start), self.counter, start)
        )

    def heuristic(self, node):
        return self.graph.distance(node, self.goal)

    def priority(self, node):
        if self.algorithm == "Best First":
            return self.heuristic(node)

        if self.algorithm == "Dijkstra":
            return self.cost[node]

        if self.algorithm == "A*":
            return self.cost[node] + self.heuristic(node)

    def reconstruct_path(self):
        node = self.goal
        self.path = [node]

        while node != self.start:
            node = self.parent[node]
            self.path.append(node)

        self.path.reverse()

    def step(self):
        if self.finished:
            return None

        while self.open:
            priority, _, current = heapq.heappop(self.open)

            if current in self.closed:
                continue

            self.closed.add(current)
            break
        else:
            self.finished = True
            return None

        if current == self.goal:
            self.finished = True
            self.reconstruct_path()
            return current

        for neighbor in self.graph.edges[current]:

            if neighbor in self.closed:
                continue

            new_cost = (
                self.cost[current]
                + self.graph.distance(current, neighbor)
            )

            if self.algorithm == "Best First":

                if neighbor not in self.cost:
                    self.cost[neighbor] = new_cost
                    self.parent[neighbor] = current

                    self.counter += 1
                    heapq.heappush(
                        self.open,
                        (self.priority(neighbor), self.counter, neighbor)
                    )

            else:
                if new_cost < self.cost.get(neighbor, float("inf")):

                    self.cost[neighbor] = new_cost
                    self.parent[neighbor] = current

                    self.counter += 1
                    heapq.heappush(
                        self.open,
                        (self.priority(neighbor), self.counter, neighbor)
                    )

        return current


# =====
# UI
# =====

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Best First / Dijkstra / A*")
        self.root.geometry("850x700")

        self.graph = Graph()
        self.search = None
        self.current = None

        self.create_interface()

    def create_interface(self):

        controls = ttk.Frame(self.root, padding=10)
        controls.pack(fill="x")

        ttk.Button(
            controls,
            text="Wczytaj graf",
            command=self.load_graph
        ).grid(row=0, column=0, padx=5)

        ttk.Label(controls, text="Start:").grid(row=0, column=1)

        self.start = tk.StringVar(value="1")
        self.start_box = ttk.Combobox(
            controls, textvariable=self.start, width=5
        )
        self.start_box.grid(row=0, column=2, padx=5)

        ttk.Label(controls, text="Cel:").grid(row=0, column=3)

        self.goal = tk.StringVar(value="1")
        self.goal_box = ttk.Combobox(
            controls, textvariable=self.goal, width=5
        )
        self.goal_box.grid(row=0, column=4, padx=5)

        ttk.Label(controls, text="Algorytm:").grid(row=0, column=5)

        self.algorithm = tk.StringVar(value="A*")

        ttk.Combobox(
            controls,
            textvariable=self.algorithm,
            values=["Best First", "Dijkstra", "A*"],
            state="readonly",
            width=12
        ).grid(row=0, column=6, padx=5)

        ttk.Button(
            controls,
            text="Start",
            command=self.start_search
        ).grid(row=1, column=0, padx=5, pady=10)

        ttk.Button(
            controls,
            text="Następny krok",
            command=self.next_step
        ).grid(row=1, column=1, columnspan=2, padx=5)

        ttk.Button(
            controls,
            text="Reset",
            command=self.reset
        ).grid(row=1, column=3, padx=5)

        self.info = ttk.Label(
            self.root,
            text="Wczytaj graf, aby rozpocząć."
        )
        self.info.pack(pady=5)

        self.canvas = tk.Canvas(
            self.root,
            bg="white",
            width=800,
            height=520
        )
        self.canvas.pack(padx=10, pady=10, fill="both", expand=True)

        self.legend = ttk.Label(
            self.root,
            text="Niebieski - nieodwiedzony | "
                 "Żółty - kolejka | "
                 "Pomarańczowy - odwiedzony | "
                 "Zielony - ścieżka"
        )
        self.legend.pack(pady=5)

    def load_graph(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Pliki tekstowe", "*.txt")]
        )

        if not filename:
            return

        try:
            self.graph.load(filename)

            nodes = list(self.graph.nodes.keys())

            self.start_box["values"] = nodes
            self.goal_box["values"] = nodes

            self.start.set(str(nodes[0]))
            self.goal.set(str(nodes[-1]))

            self.search = None
            self.draw_graph()

            self.info.config(
                text=f"Wczytano graf: {len(nodes)} wierzchołków."
            )

        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def draw_graph(self):

        self.canvas.delete("all")

        if not self.graph.nodes:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        xs = [p[0] for p in self.graph.nodes.values()]
        ys = [p[1] for p in self.graph.nodes.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        scale = min(
            (width - 100) / max(1, max_x - min_x),
            (height - 100) / max(1, max_y - min_y)
        )

        def position(node):
            x, y = self.graph.nodes[node]

            px = 50 + (x - min_x) * scale
            py = height - 50 - (y - min_y) * scale

            return px, py

        # Rysowanie krawedzi
        for node in self.graph.nodes:
            x1, y1 = position(node)

            for neighbor in self.graph.edges[node]:
                if neighbor > node:
                    x2, y2 = position(neighbor)

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill="gray", width=2
                    )

        path = self.search.path if self.search else []
        path_edges = set(zip(path, path[1:]))

        for a, b in path_edges:
            x1, y1 = position(a)
            x2, y2 = position(b)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="green", width=5
            )

        for node in self.graph.nodes:

            x, y = position(node)

            if node in path:
                color = "green"
            elif self.search and node == self.current:
                color = "red"
            elif self.search and node in self.search.closed:
                color = "orange"
            elif self.search and any(
                item[2] == node for item in self.search.open
            ):
                color = "yellow"
            else:
                color = "lightblue"

            self.canvas.create_oval(
                x - 16, y - 16,
                x + 16, y + 16,
                fill=color,
                outline="black",
                width=2
            )

            self.canvas.create_text(
                x, y,
                text=str(node),
                font=("Arial", 10, "bold")
            )

    def start_search(self):

        if not self.graph.nodes:
            messagebox.showwarning("Uwaga", "Najpierw wczytaj graf.")
            return

        try:
            start = int(self.start.get())
            goal = int(self.goal.get())

            if start not in self.graph.nodes or goal not in self.graph.nodes:
                raise ValueError()

        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy start lub cel.")
            return

        self.search = Search(
            self.graph,
            start,
            goal,
            self.algorithm.get()
        )

        self.current = None

        self.info.config(text="Rozpoczęto wyszukiwanie.")
        self.draw_graph()

    def next_step(self):

        if not self.search:
            return

        if self.search.finished:
            return

        self.current = self.search.step()

        self.draw_graph()

        if self.search.finished:

            if self.search.path:
                cost = self.search.cost[self.search.goal]

                self.info.config(
                    text=f"Znaleziono ścieżkę: "
                         f"{self.search.path} | "
                         f"Koszt: {cost:.2f}"
                )
            else:
                self.info.config(text="Nie znaleziono ścieżki.")

        elif self.current is not None:
            self.info.config(
                text=f"Odwiedzono wierzchołek: {self.current}"
            )

    def reset(self):
        self.search = None
        self.current = None
        self.draw_graph()
        self.info.config(text="Zresetowano wyszukiwanie.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
