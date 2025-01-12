import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from alg_kun import max_matching_kun_algorithm, generate_random_bipartite_edges
from alg_ford_fulkerson import max_matching_ford_fulkerson


def graphics():
    def clear_output():
        output_text.delete(1.0, tk.END)

    def append_output(text):
        output_text.insert(tk.END, text + "\n")

    def draw_graph(edges, bipartite=False, n=0, m=0, matching=None):
        fig, ax = plt.subplots(figsize=(5, 4))
        G = nx.Graph()

        if bipartite:
            G.add_nodes_from(range(n), bipartite=0)
            G.add_nodes_from(range(n, n + m), bipartite=1)
            pos = nx.bipartite_layout(G, nodes=range(n))
        else:
            pos = nx.spring_layout(G)

        G.add_edges_from(edges)

        # Подсветка рёбер паросочетания
        edge_colors = []
        for edge in edges:
            if matching and edge in matching:
                edge_colors.append('red')  # Цвет для рёбер паросочетания
            else:
                edge_colors.append('gray')  # Обычный цвет для остальных рёбер

        nx.draw(G, pos, with_labels=True, ax=ax, node_color='lightblue', edge_color=edge_colors,
                node_size=500, font_size=10, width=2)
        return fig

    def handle_manual_input():
        clear_output()
        try:
            nonlocal canvas_widget
            if canvas_widget:
                canvas_widget.destroy()

            n = int(n_entry.get())
            m = int(m_entry.get())
            edges = []

            # Парсинг списка рёбер
            edges_input = input_text.get(1.0, tk.END).strip().split("\n")
            for edge_str in edges_input:
                edge = tuple(map(int, edge_str.split()))
                if len(edge) != 2:
                    raise ValueError("Каждое ребро должно содержать ровно два числа.")
                edges.append(edge)

            method = selected_method.get()
            if method == "Куна":
                matching = max_matching_kun_algorithm(n, m, edges)
            elif method == "Форда-Фалкерсона":
                matching = max_matching_ford_fulkerson(n, m, edges)
            else:
                raise ValueError("Неизвестный метод паросочетания")

            append_output(f"Максимальное паросочетание: {matching}")

            fig = draw_graph(edges, bipartite=True, n=n, m=m, matching=matching)
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()

        except Exception as e:
            append_output(f"Ошибка: {str(e)}")

    def handle_random_generation():
        clear_output()
        try:
            nonlocal canvas_widget
            if canvas_widget:
                canvas_widget.destroy()

            n = int(n_entry.get())
            m = int(m_entry.get())
            edge_probability = float(probability_entry.get())
            edges = generate_random_bipartite_edges(n, m, edge_probability)

            method = selected_method.get()
            if method == "Куна":
                matching = max_matching_kun_algorithm(n, m, edges)
            elif method == "Форда-Фалкерсона":
                matching = max_matching_ford_fulkerson(n, m, edges)
            else:
                raise ValueError("Неизвестный метод паросочетания")

            append_output(f"Сгенерированные рёбра: {edges}")
            append_output(f"Максимальное паросочетание: {matching}")

            fig = draw_graph(edges, bipartite=True, n=n, m=m, matching=matching)
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()


        except Exception as e:
            append_output(f"Ошибка: {str(e)}")

    root = tk.Tk()
    root.title("Графы: Паросочетания и Генерация")
    root.geometry("1000x700")

    selected_method = tk.StringVar(value="Куна")

    method_frame = tk.Frame(root)
    method_frame.pack(pady=10)

    tk.Label(method_frame, text="Выберите метод паросочетания:").pack(side=tk.LEFT)
    tk.Radiobutton(method_frame, text="Куна", variable=selected_method, value="Куна").pack(side=tk.LEFT)
    tk.Radiobutton(method_frame, text="Форда-Фалкерсона", variable=selected_method, value="Форда-Фалкерсона").pack(
        side=tk.LEFT)

    # Ввод данных
    tk.Label(root, text="Количество вершин в первой доле:").pack()
    n_entry = tk.Entry(root)
    n_entry.pack()

    tk.Label(root, text="Количество вершин во второй доле:").pack()
    m_entry = tk.Entry(root)
    m_entry.pack()

    tk.Label(root, text="Вероятность существования ребра (для случайного графа):").pack()
    probability_entry = tk.Entry(root)
    probability_entry.pack()

    tk.Label(root, text="Матрица смежности (строка на каждую вершину, значения через пробел):").pack()
    input_text = tk.Text(root, height=5)
    input_text.pack()

    # Кнопки
    manual_button = tk.Button(root, text="Обработать ввод вручную", command=handle_manual_input)
    manual_button.pack(pady=5)

    random_button = tk.Button(root, text="Сгенерировать случайный граф", command=handle_random_generation)
    random_button.pack(pady=5)

    # Вывод данных
    tk.Label(root, text="Результат:").pack()
    output_text = tk.Text(root, height=10)
    output_text.pack()

    # Холст для графиков
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas_widget = None

    root.mainloop()


graphics()
