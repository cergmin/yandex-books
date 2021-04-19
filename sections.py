class Section:
    def __init__(self, title='Название секции'):
        self.data = {
            'type': 'default',
            'title': title
        }


class BookSection(Section):
    def __init__(self, books, title='Название секции'):
        self.data = {
            'type': 'book',
            'title': title,
            'books': [],
            'max_cover_ratio': 0
        }

        for book in books:
            self.data['books'].append({
                'book_id': str(book['book_id']),
                'book_name': book['book_name'],
                'author_id': str(book['author_id']),
                'author_name': book['author_name'],
                'cover_ratio': book['cover_height'] / book['cover_width']
            })

            self.data['max_cover_ratio'] = max(
                self.data['max_cover_ratio'],
                book['cover_height'] / book['cover_width']
            )