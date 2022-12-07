class Node:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.children = {}
        self.parent = None

    def get_name(self):
        return self.name

    def print(self, indent: int = 0):
        print(" "*indent+f"- {self.name} (file, size={self.size})")

    def set_parent(self, parent):
        self.parent = parent

    def get_size(self) -> int:
        return self.size

    def get_child(self, name: str):
        if name == "..":
            return self.parent
        else:
            return self.children[name]

    def get_children(self):
        return self.children

    def add_child(self, child):
        child_name = child.get_name()
        if child_name in self.children:
            raise ValueError(f"Child {child_name} already exists")
        self.children[child_name] = child
        self.children[child_name].set_parent(self)

    def traverse(self):
        yield self
        for _, child in self.children.items():
            yield from child.traverse()


class File(Node):
    def __init__(self, name: str, size: int):
        super().__init__(name, size)

    def as_string(self, indent: int = 0):
        return " "*indent + f"- {self.name} (file, size={self.size})"

    def __str__(self):
        return self.as_string(0)


class Directory(Node):
    def __init__(self, name: str):
        super().__init__(name, 0)
        self.recursive_size = 0   # cache size

    def as_string(self, indent: int = 0, recursive: bool = True):
        out = " "*indent + f"- {self.name} (dir)"
        for name, child in self.children.items():
            if recursive and isinstance(child, Directory):
                out += "\n" + child.as_string(indent+2, recursive=True)
            else:
                out += "\n" + child.as_string(indent+2)

        return out

    def get_size(self) -> int:
        size = 0
        for _, child in self.children.items():
            size += child.get_size()

        return size

    def __str__(self):
        return self.as_string(0, True)


def parse_command(cmd: str, curr_dir):
    cmd_list = cmd.splitlines()
    if cmd_list[0] == "ls":
        for line in cmd_list[1:]:
            size_or_dir, name = line.split(" ")
            if size_or_dir == "dir":
                curr_dir.add_child(Directory(name))
            else:
                curr_dir.add_child(File(name, int(size_or_dir)))

        return curr_dir # stay in same directory

    elif cmd_list[0].startswith("cd"):
        return curr_dir.get_child(cmd_list[0].split(" ")[1])
    else:
        raise ValueError(f"Unknown command {cmd_list[0]}")


def sum_up_directory_sizes(root_node, max_size=None):
    total_size = 0
    for child in root_node.traverse():
        if isinstance(child, Directory):
            child_size = child.get_size()
            if max_size is None or child_size < max_size:
                total_size += child_size

    return total_size


test_input = """ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

test_structure = """- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)"""


def test_input_to_structure():
    root_node = Directory("/")
    curr_node = root_node

    # Parse input
    for cmd in test_input.split("$ "):
        curr_node = parse_command(cmd, curr_node)

    assert str(root_node) == test_structure


def test_directory_sizes():
    root_node = Directory("/")
    curr_node = root_node

    # Parse input
    for cmd in test_input.split("$ "):
        curr_node = parse_command(cmd, curr_node)

    node_a = root_node.get_child("a")
    node_d = root_node.get_child("d")
    node_e = node_a.get_child("e")

    assert node_a.get_size() == 94853
    assert node_d.get_size() == 24933642
    assert node_e.get_size() == 584
    assert root_node.get_size() == 48381165

    assert sum_up_directory_sizes(root_node, 100000) == 95437


def main():
    with open("input.txt", "r") as f:
        actual_input = f.read()

    root_node = Directory("/")
    curr_node = root_node

    for cmd in actual_input.split("$ "):
        curr_node = parse_command(cmd, curr_node)

    print(sum_up_directory_sizes(root_node, 100000))

    # Part 2
    total_space = 70000000
    unused_space_required = 30000000
    free_space = total_space-root_node.get_size()
    min_space_delete = unused_space_required-free_space
    del_node = root_node
    del_size = root_node.get_size()
    for node in root_node.traverse():
        if isinstance(node, Directory):
            size = node.get_size()
            if size >= min_space_delete and size < del_size:
                del_size = size
                del_node = node

    print(del_node.get_name(), del_size, del_node.get_size())


if __name__ == "__main__":
    main()
