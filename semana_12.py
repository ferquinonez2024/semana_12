import json

# Clase Book: representa un libro con atributos inmutables
class Book:
    def _init_(self, title, writer, genre, isbn_code):
        self.title = title  # Título del libro (tupla)
        self.writer = writer  # Autor del libro (tupla)
        self.genre = genre  # Categoría del libro
        self.isbn_code = isbn_code  # ISBN único

# Clase Member: representa a un usuario de la biblioteca con nombre, ID y lista de libros prestados
class Member:
    def _init_(self, name, member_id):
        self.name = name  # Nombre del usuario
        self.member_id = member_id  # ID único
        self.borrowed_books = []  # Lista de libros actualmente prestados

# Clase Library: gestiona libros, usuarios y registros de préstamo
class Library:
    def _init_(self):
        self.available_books = {}  # Almacena libros disponibles, ISBN como clave
        self.members = set()  # IDs únicos de miembros
        self.loan_history = {}  # Registra los préstamos: {ID_usuario: [ISBNs prestados]}

    # Agregar un nuevo libro a la colección
    def add_book(self, title, writer, genre, isbn_code):
        if isbn_code not in self.available_books:
            new_book = Book(title, writer, genre, isbn_code)  # Crea un nuevo libro
            self.available_books[isbn_code] = new_book  # Añade el libro a la biblioteca
            print(f"Libro '{title}' agregado correctamente.")
        else:
            print(f"El libro con ISBN {isbn_code} ya existe.")

    # Eliminar un libro de la colección
    def remove_book(self, isbn_code):
        if isbn_code in self.available_books:
            del self.available_books[isbn_code]  # Elimina el libro del diccionario
            print(f"Libro con ISBN {isbn_code} eliminado.")
        else:
            print(f"No se encontró el libro con ISBN {isbn_code}.")

    # Registrar un nuevo usuario en el sistema
    def register_member(self, name, member_id):
        if member_id not in self.members:
            new_member = Member(name, member_id)  # Crea un nuevo usuario
            self.members.add(member_id)  # Añade el usuario al conjunto
            self.loan_history[member_id] = []  # Inicializa el historial de préstamos
            print(f"Miembro '{name}' registrado con éxito.")
        else:
            print(f"El miembro con ID {member_id} ya está registrado.")

    # Eliminar a un usuario del sistema
    def unregister_member(self, member_id):
        if member_id in self.members:
            self.members.remove(member_id)  # Elimina el usuario del conjunto
            del self.loan_history[member_id]  # Borra el historial de préstamos del usuario
            print(f"Miembro con ID {member_id} eliminado.")
        else:
            print(f"El miembro con ID {member_id} no existe.")

    # Prestar un libro a un usuario
    def loan_book(self, member_id, isbn_code):
        if member_id in self.members and isbn_code in self.available_books:
            if isbn_code not in self.loan_history[member_id]:
                self.loan_history[member_id].append(isbn_code)  # Añade el libro al historial de préstamos
                print(f"Libro con ISBN {isbn_code} prestado a {member_id}.")
            else:
                print(f"El miembro ya tiene prestado el libro con ISBN {isbn_code}.")
        else:
            print(f"ID de miembro o ISBN no válido.")

    # Devolver un libro prestado
    def return_book(self, member_id, isbn_code):
        if member_id in self.members and isbn_code in self.loan_history[member_id]:
            self.loan_history[member_id].remove(isbn_code)  # Remueve el libro del historial
            print(f"Libro con ISBN {isbn_code} devuelto por {member_id}.")
        else:
            print(f"El miembro no tiene prestado el libro con ISBN {isbn_code}.")

    # Buscar libros por diferentes criterios
    def search_books(self, key, value):
        results = [book for book in self.available_books.values()
                   if getattr(book, key, '').lower() == value.lower()]
        if results:
            for book in results:
                print(f"Encontrado: '{book.title}' de {book.writer}")
        else:
            print(f"No se encontraron libros por {key}: {value}")

    # Mostrar los libros prestados por un miembro
    def show_loaned_books(self, member_id):
        if member_id in self.members:
            borrowed = self.loan_history.get(member_id, [])
            if borrowed:
                print(f"Libros prestados a {member_id}:")
                for isbn in borrowed:
                    book = self.available_books.get(isbn)
                    print(f"  - '{book.title}' por {book.writer}")
            else:
                print(f"{member_id} no tiene libros prestados.")
        else:
            print(f"Miembro con ID {member_id} no encontrado.")

    # Guardar los datos en un archivo
    def save_data(self, filename):
        with open(filename, 'w') as file:
            data = {
                'books': {isbn: book._dict_ for isbn, book in self.available_books.items()},
                'members': list(self.members),
                'loans': self.loan_history
            }
            json.dump(data, file)
            print(f"Datos guardados en '{filename}'.")

    # Cargar los datos desde un archivo
    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.available_books = {isbn: Book(**book) for isbn, book in data['books'].items()}
                self.members = set(data['members'])
                self.loan_history = data['loans']
                print(f"Datos cargados desde '{filename}'.")
        except FileNotFoundError:
            print(f"El archivo '{filename}' no existe.")

# Menú interactivo de la biblioteca

def interactive_menu():
    library = Library()
    data_file = 'library_data.json'
    library.load_data(data_file)

    while True:
        print("\n--- Menú Biblioteca ---")
        print("1. Agregar libro")
        print("2. Eliminar libro")
        print("3. Registrar miembro")
        print("4. Eliminar miembro")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libros")
        print("8. Mostrar libros prestados")
        print("9. Guardar y salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            title = input("Título: ")
            writer = input("Autor: ")
            genre = input("Género: ")
            isbn_code = input("ISBN: ")
            library.add_book(title, writer, genre, isbn_code)
        elif choice == '2':
            isbn_code = input("ISBN del libro a eliminar: ")
            library.remove_book(isbn_code)
        elif choice == '3':
            name = input("Nombre del miembro: ")
            member_id = input("ID del miembro: ")
            library.register_member(name, member_id)
        elif choice == '4':
            member_id = input("ID del miembro: ")
            library.unregister_member(member_id)
        elif choice == '5':
            member_id = input("ID del miembro: ")
            isbn_code = input("ISBN del libro a prestar: ")
            library.loan_book(member_id, isbn_code)
        elif choice == '6':
            member_id = input("ID del miembro: ")
            isbn_code = input("ISBN del libro a devolver: ")
            library.return_book(member_id, isbn_code)
        elif choice == '7':
            key = input("Buscar por (title/writer/genre): ")
            value = input(f"Introduce el valor para buscar por {key}: ")
            library.search_books(key, value)
        elif choice == '8':
            member_id = input("ID del miembro: ")
            library.show_loaned_books(member_id)
        elif choice == '9':
            library.save_data(data_file)
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")


interactive_menu()
