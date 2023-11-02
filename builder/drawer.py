import pathlib

from pyvis.network import Network

DEFAULT_FILENAME = 'graph.html'
DEFAULT_PATH = str(pathlib.Path().resolve()) + '/' + DEFAULT_FILENAME


def make_indexes(x: str) -> str:
    """
    Заменяет числа в строке на "подстрочные знаки"
    :param x: Исходная строка
    :return: Строка с индексами
    """
    normal = "0123456789"
    sub_s = "₀₁₂₃₄₅₆₇₈₉"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)


def draw(n: int, data: list[list], directed=False, size: int = 30, font_size: int = 30) -> int:
    """
    Создание файла с графом
    :param n: количество ребер
    :param data: ребра
    :param directed: Ориентированный граф или нет
    :param size: Размер вершины
    :param font_size: Размер шрифта
    :return: Количество вершин в построенном графе
    """
    net = Network(directed=directed)
    nodes = set()
    edges = dict()
    for i in range(n):
        node_from, node_to, edge_name = map(str, data[i])
        nodes.add(node_from)
        nodes.add(node_to)
        key = (node_from, node_to)
        edges[key] = [edge_name, ]
    for i in nodes:
        net.add_node(i, label=make_indexes(i), shape='circle', size=100)

    for n in net.nodes:
        n["size"] = size
        n["font"] = {"size": font_size}

    for key in edges:
        for edge in edges[key]:
            if edge:
                net.add_edge(key[0], key[1], label=f"{edge}")
            else:
                net.add_edge(key[0], key[1])

    c = net.generate_html()
    filename = DEFAULT_FILENAME
    f = open(filename, 'w')
    c = c.replace('style="width: 100%"', '')  # ширину задавать не надо
    f.write(c)
    return len(nodes)
