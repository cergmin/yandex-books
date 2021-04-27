from flask_login import LoginManager
from shutil import copyfile
from hashlib import sha256
from data.db_session import *
from data.__all_models import *


class DataController:
    def __init__(self, db_file):
        global_init(db_file)
        self.session = create_session()

    def get_password_hash(self, password, username):
        salt = 'qebwtgfpnqegponi'
        password_hash = sha256(
            salt.encode(encoding='utf8')
        ).hexdigest()

        for addition in [password, salt, username, salt]:
            password_hash = sha256(
                (password_hash + str(addition)).encode(encoding='utf8')
            ).hexdigest()
        
        return password_hash
    
    def add_user(self, login, name, surname, email, password, status=0):
        # Добавление записи о пользователе
        user = User()

        user.login = login
        user.name = name
        user.surname = surname
        user.email = email
        user.password_hash = self.get_password_hash(password, name)
        user.status = status

        self.session.add(user)
        self.session.commit()

        # Создание аватара по умлочанию,
        # пока пользователь не загрузит свой
        copyfile(
            './resources/images/avatar.jpg',
            f'./resources/images/avatars/{user.id}.jpg'
        )

        return user

    def add_author(self, name):
        author = Author()

        author.name = name

        self.session.add(author)
        self.session.commit()

    def add_series(self, name):
        series = Series()

        series.name = name

        self.session.add(series)
        self.session.commit()

    def add_book(self, name, description, author_id, price, cover_width, cover_height, short_name='', series_id=-1):
        book = Book()

        book.name = name
        book.short_name = short_name
        book.description = description
        book.author_id = author_id
        book.series_id = series_id
        book.price = price
        book.cover_width = cover_width
        book.cover_height = cover_height

        self.session.add(book)
        self.session.commit()

        return book
    
    def add_giftcode(self, code, value):
        giftcode = GiftCode()

        giftcode.code = code
        giftcode.value = value

        self.session.add(giftcode)
        self.session.commit()

    def get_author(self, author_id):
        return self.session.query(Author).get(author_id)
    
    def get_authors(self):
        return self.session.query(
            Author
        ).order_by(
            Author.name
        ).all()

    def get_book(self, book_id):
        return self.session.query(Book).get(book_id)

    def get_books(self):
        return self.session.query(Book).all()
    
    def get_series(self, series_id):
        return self.session.query(Series).get(series_id)
    
    def get_all_series(self):
        return self.session.query(
            Series
        ).order_by(
            Series.name
        ).all()

    def get_user(self, user_id):
        return self.session.query(User).filter(
            User.id == user_id
        ).first()
    
    def get_user_by_login(self, login):
        return self.session.query(User).filter(
            User.login == login
        ).first()
    
    def get_giftcode(self, giftcode):
        return self.session.query(GiftCode).filter(
            GiftCode.code == giftcode
        ).first()
    
    def check_user_password(self, user, password):
        return user.password_hash == self.get_password_hash(
            password,
            user.name
        )
    
    def add_item_to_cart(self, user_id, book_id):
        if self.is_item_in_cart(user_id, book_id):
            return

        # Борьба с garbage collector
        book = self.get_book(book_id)
        user = self.get_user(user_id)

        # Добавление книги в корзину
        user.cart.append(book)

        self.session.commit()
    
    def get_items_in_cart(self, user_id):
        user = self.get_user(user_id)
        return user.cart
    
    def is_item_in_cart(self, user_id, book_id):
        user = self.get_user(user_id)
        return any(
            [
                book.id == book_id
                for book in user.cart
            ]
        )
    
    def delete_item_from_cart(self, user_id, book_id):
        if not self.is_item_in_cart(user_id, book_id):
            return

        user = self.get_user(user_id)
        user.cart.remove(
            self.get_book(book_id)
        )

        self.session.commit()
    
    def buy_book(self, user_id, book_id):
        if self.is_book_bought(user_id, book_id):
            return {
                'is_ok': False,
                'message': 'Книгу уже куплена'
            }

        # Борьба с garbage collector
        book = self.get_book(book_id)
        user = self.get_user(user_id)

        # Проверка, достаточно ли у нас средств,
        # чтобы купить эту книгу
        if book.price > user.balance:
            return {
                'is_ok': False,
                'message': 'Недостаточно средств на счёте'
            }
        
        # Снимаем средства со счёта пользователя
        user.balance -= book.price

        # Добавление книги в список купленных
        user.bought_books.append(book)

        self.session.commit()
        return {
            'is_ok': True,
            'message': 'Книга успешно куплена'
        }
    
    def get_bought_books(self, user_id):
        user = self.get_user(user_id)
        return user.bought_books
    
    def is_book_bought(self, user_id, book_id):
        user = self.get_user(user_id)
        return any(
            [
                book.id == book_id
                for book in user.bought_books
            ]
        )
    
    def activate_giftcode(self, user_id, code):
        user = self.session.query(User).get(user_id)
        giftcode = self.get_giftcode(code)

        if not user:
            return {
                'error_message': 'Не удалось определить пользователя'
            }
        
        if not giftcode:
            return {
                'error_message': 'Такой подарочный код не найден'
            }

        user.balance += giftcode.value
        self.session.query(GiftCode).filter(
            GiftCode.code == code
        ).delete()
        
        self.session.commit()
        
        return {
            'success_message': 'Код успешно активирован'
        }
