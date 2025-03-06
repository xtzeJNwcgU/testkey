import json
import os

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.yes = None
        self.no = None

# Fungsi untuk menyimpan pohon ke file JSON dengan indentasi
def save_tree(node, filename="akinator_tree.json"):
    if node is None:
        return None
    tree_dict = {
        "data": node.data,
        "yes": save_tree(node.yes, filename) if node.yes else None,
        "no": save_tree(node.no, filename) if node.no else None
    }
    with open(filename, "w") as file:
        json.dump(tree_dict, file, indent=4)  # Menambahkan indentasi
    return tree_dict

# Fungsi untuk memuat pohon dari file JSON dengan penanganan kesalahan
def load_tree(filename="akinator_tree.json"):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r") as file:
            tree_dict = json.load(file)
        return dict_to_tree(tree_dict)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading tree: {e}")
        return None

# Fungsi untuk mengonversi dictionary menjadi objek TreeNode
def dict_to_tree(tree_dict):
    if not tree_dict:
        return None
    node = TreeNode(tree_dict["data"])
    node.yes = dict_to_tree(tree_dict["yes"]) if tree_dict["yes"] else None
    node.no = dict_to_tree(tree_dict["no"]) if tree_dict["no"] else None
    return node

# Fungsi untuk mendapatkan input dari pengguna dengan validasi
def get_input(question):
    while True:
        response = input(question + " (y/n): ").lower()
        if response in ["y", "n"]:
            return response == "y"
        print("Masukkan y atau n saja!")

# Fungsi utama untuk menjalankan permainan
def play_game(node):
    if node.yes is None and node.no is None:
        if get_input(f"Apakah karaktermu {node.data}?"):
            print("Aku menebak dengan benar! 🎉")
            return True
        return False

    if get_input(node.data):
        if play_game(node.yes):
            return True
    else:
        if play_game(node.no):
            return True

    return False

# Fungsi untuk menambahkan karakter baru dengan pembatasan kedalaman
MAX_DEPTH = 10

def add_new_character(node, current_depth=0):
    if current_depth >= MAX_DEPTH:
        print("Pohon telah mencapai kedalaman maksimum. Tidak dapat menambahkan karakter baru.")
        return

    print("🤔 Siapa karakter yang kamu pikirkan?")
    new_char = input("> ").strip()
    while not new_char:
        print("Nama karakter tidak boleh kosong!")
        new_char = input("> ").strip()

    print(f"Berikan pertanyaan yang MEMBEDAKAN {new_char} dengan {node.data}")
    new_question = input("> ").strip()
    while not new_question or len(new_question) < 5:  # Minimal 5 karakter
        print("Pertanyaan tidak boleh kosong dan harus lebih dari 5 karakter!")
        new_question = input("> ").strip()

    print(f"Jawaban untuk {new_char} adalah? (y/n)")
    new_answer = get_input("> ")

    old_char = node.data
    node.data = new_question

    if new_answer:
        node.yes = TreeNode(new_char)
        node.no = TreeNode(old_char)
    else:
        node.yes = TreeNode(old_char)
        node.no = TreeNode(new_char)

# Fungsi utama program
def main():
    root = load_tree()

    if not root:
        root = TreeNode("Goku")

    while True:
        print("\n=== Pikirkan sebuah karakter ===")
        if not play_game(root):
            print("🧠 Aku mau belajar...")
            add_new_character(root)

        save_tree(root)

        action = input("Apa yang ingin kamu lakukan? (main/reset/view/exit): ").lower()
        if action == "main":
            continue
        elif action == "reset":
            print("Resetting tree to initial state...")
            root = TreeNode("Goku")
        elif action == "view":
            print(json.dumps(save_tree(root), indent=4))
        elif action == "exit":
            print("Sampai jumpa!")
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()