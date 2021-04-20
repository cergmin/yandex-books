class Section:
    def __init__(self, dc, title='Название секции'):
        self.dc = dc
        self.data = {
            'type': 'default',
            'title': title
        }


class BookSection(Section):
    def __init__(self, dc, books, title='Название секции'):
        self.dc = dc
        self.data = {
            'type': 'book',
            'title': title,
            'books': [],
            'max_cover_ratio': 0
        }

        for book in books:
            self.data['books'].append({
                'book_id': str(book.id),
                'book_name': book.name,
                'author_id': str(book.author_id),
                'author_name': dc.get_author(book.author_id).name,
                'cover_ratio': book.cover_height / book.cover_width
            })

            self.data['max_cover_ratio'] = max(
                self.data['max_cover_ratio'],
                book.cover_height / book.cover_width
            )