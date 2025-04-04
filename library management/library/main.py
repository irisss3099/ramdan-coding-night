import json
import streamlit as st


st.set_page_config(page_title="📚 Book Collection Manager", page_icon="📖", layout="wide")

st.markdown('<h1 class="title">📚 Book Collection Manager</h1>', unsafe_allow_html=True)

#  CSS styles
st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-top: -40px; /* Adjust to move the title up */
    }

    /* Main app background - Light Peach */
    .stApp {
        background-color: #FFDAB9;
        color: black;
        transition: background-color 0.5s ease-in-out;
    }

    /* Sidebar background - Dark Peach */
    section[data-testid="stSidebar"] {
        background-color: #E9967A;
        transition: background-color 0.5s ease-in-out;
    }

    /* Styling for text elements */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: black !important;
    }

    /* Input fields and buttons */
    .stTextInput, .stNumberInput, .stSelectbox, .stRadio {
        color: black !important;
    }

    .stButton>button {
        color: white !important;
        background-color: #87CEFA !important; /* Light Blue */
        border: 1px solid #4682B4 !important;
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #5F9EA0 !important;
        border-color: #1E90FF !important;
        transform: scale(1.05);
    }

    .stProgress > div > div {
        background-color: #1db954 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define BookCollection class
class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def add_book(self, title, author, year, genre, read):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title=None, delete_all=False):
        if delete_all:
            self.book_list.clear()
            self.save_to_file()
            return True
        else:
            original_length = len(self.book_list)
            self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]
            if len(self.book_list) < original_length:
                self.save_to_file()
                return True
            return False

    def update_book(self, old_title, new_title, new_author, new_year, new_genre, new_read):
        for book in self.book_list:
            if book["title"].lower() == old_title.lower():
                book.update({"title": new_title or book["title"], "author": new_author or book["author"], "year": new_year or book["year"], "genre": new_genre or book["genre"], "read": new_read})
        self.save_to_file()

    def mark_as_read(self, title):
        title = title.strip().lower()  
        found = False  

        for book in self.book_list:
            if book["title"].lower() == title:
                book["read"] = True
                found = True

        if found:
            self.save_to_file()
            return True  
        else:
            return False  

    
    def get_all_books(self):
        return self.book_list

    def get_books_by_genre(self, genre):
        return [book for book in self.book_list if book["genre"] == genre]

    def search_books(self, search_text, search_by="title"):
        """Search books by title or author."""
        search_text = search_text.lower()
        
        if search_by == "title":
            return [book for book in self.book_list if search_text in book["title"].lower()]
        elif search_by == "author":
            return [book for book in self.book_list if search_text in book["author"].lower()]
        return []

    def get_reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        return total_books, (completed_books / total_books * 100 if total_books > 0 else 0)
    
    # Initialize manager
manager = BookCollection()

# Initialize session state for books and progress
if "books" not in st.session_state:
    st.session_state.books = manager.get_all_books()

if "reading_progress" not in st.session_state:
    st.session_state.reading_progress = manager.get_reading_progress()

manager = BookCollection()
menu = st.sidebar.selectbox("📌 Menu", ["➕ Add Book", "📖 View Books", "🔍 Search Books", "✏️ Update Book", "❌ Delete Book", "📖 Read Book", "📊 Reading Progress"])

# ➕ Add Book
if menu == "➕ Add Book":
    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        year = st.text_input("📅 Year")
        genre = st.text_input("📚 Genre")
        read = st.checkbox("✅ Read")
        submitted = st.form_submit_button("➕ Add Book")

        if submitted:
            manager.add_book(title, author, year, genre, read)
            st.session_state.books = manager.get_all_books()  # ✅ Update book list
            st.session_state.reading_progress = manager.get_reading_progress()  # ✅ Update progress
            st.success(f"✅ Book '{title}' added successfully!")

# 📖 View Books
elif menu == "📖 View Books":
    st.subheader("📚 View Books")
    books = st.session_state.books

    if books:
        for book in books:
            st.write(f"**📖 {book['title']}** by {book['author']} ({book['year']}) - Genre: {book['genre']} - {'✅ Read' if book['read'] else '📖 Not Read'}")
    else:
        st.write("❌ No books available.")

# 🔍 Search Books
elif menu == "🔍 Search Books":
    st.subheader("🔍 Search Books")

    search_by = st.radio("Search By", ["Title", "Author"])
    search_text = st.text_input(f"🔍 Search by {search_by}")

    if st.button("🔍 Search"):
        if search_text:
            results = manager.search_books(search_text, search_by.lower())
            if results:
                for book in results:
                    st.write(f"**📖 {book['title']}** by {book['author']} ({book['year']}) - Genre: {book['genre']}")
            else:
                st.write("❌ No matching books found.")

# ✏️ Update Book
elif menu == "✏️ Update Book":
    old_title = st.text_input("✏️ Current Title")
    new_title = st.text_input("🔄 New Title")
    new_author = st.text_input("🖋️ New Author")
    new_year = st.text_input("📅 New Year")
    new_genre = st.text_input("📚 New Genre")
    new_read = st.checkbox("✅ Read")
    if st.button("✏️ Update Book"):
        manager.update_book(old_title, new_title, new_author, new_year, new_genre, new_read)
        st.success("✅ Book updated successfully!")

# ❌ Delete Book
elif menu == "❌ Delete Book":
    st.subheader("🗑️ Delete Book")
    delete_option = st.radio("Select Delete Option", ["Delete by Title", "Delete All Books"])

    # Ensure delete message persists across reruns
    if "delete_message" not in st.session_state:
        st.session_state.delete_message = ""

    if delete_option == "Delete by Title":
        title = st.text_input("🗑️ Enter Book Title to Delete")
        if st.button("❌ Delete"):
            if title.strip():
                deleted = manager.delete_book(title=title)
                if deleted:
                    st.session_state.books = manager.get_all_books()  
                    st.session_state.reading_progress = manager.get_reading_progress()  
                    st.session_state.delete_message = f"🗑️ Book '{title}' deleted successfully!"  
                    st.rerun()  
                else:
                    st.session_state.delete_message = "❌ Book not found!"
                    st.rerun()  
            else:
                st.warning("⚠️ Please enter a book title.")

    elif delete_option == "Delete All Books":
        if st.button("⚠️ Delete All Books"):
            deleted = manager.delete_book(delete_all=True)
            if deleted:
                st.session_state.books = manager.get_all_books()  
                st.session_state.reading_progress = manager.get_reading_progress()  
                st.session_state.delete_message = "🗑️ All books deleted successfully!"  
                st.rerun()  
            else:
                st.session_state.delete_message = "⚠️ No books to delete!"
                st.rerun()  

    # ✅ Show the message after rerun
    if st.session_state.delete_message:
        st.success(st.session_state.delete_message)
        st.session_state.delete_message = ""  

# 📖 Read Book
elif menu == "📖 Read Book":
    title = st.text_input("📖 Enter Book Title to Mark as Read")

    if st.button("✅ Mark as Read"):
        if title.strip() == "":
            st.warning("⚠️ Please enter a book title!")
        else:
            success = manager.mark_as_read(title)
            if success:
                st.success(f"✅ '{title}' marked as read!")
            else:
                st.error(f"❌ Book '{title}' not found in collection!")

# 📊 Reading Progress
elif menu == "📊 Reading Progress":
    total, progress = st.session_state.reading_progress
    st.write(f"📚 Total Books: {total}")
    st.write(f"📈 Completion Rate: {progress:.2f}%")


# footer
st.markdown("<hr><p style='text-align: center;'>Created by SK 💖</p>", unsafe_allow_html=True)
