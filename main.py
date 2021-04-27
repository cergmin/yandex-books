import config
import api
from os import path
from utils import *
from sections import *
from controllers import *
from forms import *
from flask import Flask, render_template, redirect, abort, send_from_directory, request
from flask_login import login_user, logout_user, current_user, login_required
from data.__all_models import *

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER,
)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return dc.session.query(User).get(user_id)


@app.route('/')
def index():
    search_request = request.args.get("search")
    if search_request is not None:
        found_books = [
            {
                'book_id': str(book.id),
                'book_name': book.name,
                'author_id': str(book.author_id),
                'author_name': dc.get_author(book.author_id).name
            }
            for book in dc.find_books(search_request)
        ]

        return render_template(
            'search.html',
            search_request=search_request,
            books=found_books
        )

    sections = []
    sections.append(
        BookSection(dc, dc.get_books())
    )

    return render_template(
        'index.html',
        sections=sections
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = dc.get_user_by_login(form.login.data)

        if not user:
            return render_template(
                'login.html',
                message="Пользователя с таким именем не существует",
                form=form
            )

        if user and dc.check_user_password(user, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')

        return render_template(
            'login.html',
            message="Неверный пароль",
            form=form
        )

    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = dc.get_user_by_login(form.login.data)

        if user:
            return render_template(
            'registration.html',
            message="Пользователь с таким именем уже существует",
            form=form
        )

        login_user(
            dc.add_user(
                form.login.data,
                form.name.data,
                form.surname.data,
                form.email.data,
                form.password.data
            )
        )
        return redirect('/')

    return render_template('registration.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/pay', methods=['GET', 'POST'])
@login_required
def pay():
    form = PaymentForm()

    response = {}
    if form.validate_on_submit():
        if len(str(form.giftcode.data)) != 8:
            response = {
                'error_message': 'Подарочный код должен содержать 8 символов'
            }
        elif not form.giftcode.data.isdigit():
            response = {
                'error_message': 'Подарочный код может состоять только из цифр'
            }
        else:
            response = dc.activate_giftcode(
                current_user.id,
                form.giftcode.data
            )

    return render_template('pay.html', form=form, **response)


@app.route('/book/<int:book_id>')
def book(book_id):
    book = dc.get_book(book_id)
    data = {
        'book': book,
        'author': dc.get_author(book.author_id),
        'series': dc.get_series(book.series_id),
        'price': str(
            int(book.price)
            if int(book.price) == book.price else
            book.price
        ) + ' ' + plural(
            book.price, 'рубль', 'рубля', 'рублей'
        ),
        'is_in_cart': dc.is_item_in_cart(current_user.id, book_id),
        'is_bought': dc.is_book_bought(current_user.id, book_id)
    }

    return render_template(
        'book.html',
        **data
    )


@app.route('/author/<int:author_id>')
def author(author_id):
    author = dc.get_author(author_id)
    data = {
        'author_id': str(author.id),
        'author_name': author.name
    }

    return render_template(
        'author.html',
        **data
    )


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.status <= 0:
        return abort(403)

    add_book_form = AddBookForm()

    if add_book_form.validate_on_submit():
        cover = add_book_form.cover.data
        book = add_book_form.book.data
        name = add_book_form.name.data
        short_name = add_book_form.short_name.data
        description = add_book_form.description.data
        author_id = add_book_form.author_id.data
        series_id = add_book_form.series_id.data
        price = add_book_form.price.data
        
        added_book = dc.add_book(
            name,
            description,
            author_id,
            price,
            1000,
            1500,
            short_name,
            series_id
        )

        cover.save(
            path.join(
                config.STATIC_FOLDER,
                'images/covers/books',
                str(added_book.id) + '.jpg'
            )
        )

        book.save(
            path.join(
                config.UPLOAD_FOLDER,
                'books',
                str(added_book.id) + '.fb2'
            )
        )

        return render_template(
            'admin.html',
            success_message='Книга успешно добавлена!',
            add_book_form=add_book_form
        )

    return render_template(
        'admin.html',
        authors=dc.get_authors(),
        all_series=dc.get_all_series(),
        add_book_form=add_book_form
    )


@app.route('/series/<int:series_id>')
def series(series_id):
    series = dc.get_series(series_id)
    data = {
        'author_id': str(series.id),
        'author_name': series.name
    }

    return render_template(
        'author.html',
        **data
    )


@app.route('/cart')
@login_required
def cart():
    books = [
        {
            'book_id': str(book.id),
            'book_name': book.name,
            'author_id': str(book.author_id),
            'author_name': dc.get_author(book.author_id).name,
            'price': str(
                int(book.price)
                if int(book.price) == book.price else
                book.price
            ) + '₽',
            'is_bought': dc.is_book_bought(current_user.id, book.id)
        }
        for book in dc.get_items_in_cart(current_user.id)
    ]

    return render_template(
        'cart.html',
        books=books
    )


@app.route('/mybooks')
@login_required
def mybooks():
    books = [
        {
            'book_id': str(book.id),
            'book_name': book.name,
            'author_id': str(book.author_id),
            'author_name': dc.get_author(book.author_id).name
        }
        for book in dc.get_bought_books(current_user.id)
    ]

    return render_template(
        'mybooks.html',
        books=books
    )


@app.route('/download/<int:book_id>')
@login_required
def download(book_id):
    if not dc.is_book_bought(current_user.id, book_id):
        return abort(403)
    
    book = dc.get_book(book_id)
    
    return send_from_directory(
        directory=path.join(
            config.UPLOAD_FOLDER,
            'books'
        ),
        filename=(str(book.id) + '.fb2')
    )


if __name__ == '__main__':
    dc = DataController('db/data.db')
    # dc.add_giftcode(31415926, 50000)
    # dc.add_user('cergmin', 'Сергей', 'Минаков', 'cergmin@gmail.com', '123456', status=1)
    # dc.add_author('Милена Завойчинская')
    # dc.add_author('Джоан Роулинг')
    # dc.add_author('Александр Пушкин')
    # dc.add_author('Лев Толстой')
    # dc.add_author('Агата Кристи')
    # dc.add_author('Хуан Рамон')
    # dc.add_author('Роберт Рождественский')
    # dc.add_author('Николай Гоголь')
    # dc.add_author('Афанасий Фет')
    # dc.add_series('Высшая Школа Библиотекарей')
    # dc.add_series('Гарри Поттер')
    # dc.add_series('Мировая классика')
    # dc.add_series('Русская классика')
    # dc.add_series('Самые любопытные детективы')
    # dc.add_book('Высшая Школа Библиотекарей. Магия книгоходцев', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 1, 169, 317, 500, series_id=1, short_name='Магия книгоходцев')
    # dc.add_book('Высшая Школа Библиотекарей. Боевая практика книгоходцев', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 1, 199.99, 317, 500, series_id=1, short_name='Боевая практика книгоходцев')
    # dc.add_book('Высшая Школа Библиотекарей. Книгоходцы особого назначения', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 1, 200, 317, 500, series_id=1, short_name='Книгоходцы особого назначения')
    # dc.add_book('Высшая Школа Библиотекарей. Книгоходцы и тайна механического бога', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 1, 500, 317, 500, series_id=1, short_name='Книгоходцы и тайна механического бога')
    # dc.add_book('Высшая Школа Библиотекарей. Хроники книгоходцев', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 1, 100, 317, 500, series_id=1, short_name='Хроники книгоходцев')
    # dc.add_book('Гарри Поттер и философский камень', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 500, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и Тайная комната', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 299.99, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и узник Азкабана', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 560, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и Кубок огня', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 290, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и Орден Феникса', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 315, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и Принц-полукровка', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 500, 333, 500, series_id=2)
    # dc.add_book('Гарри Поттер и Дары Смерти', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et nunc venenatis, consequat nisi at, volutpat lectus. Nunc quis efficitur neque. Integer sit amet cursus justo. Fusce faucibus et arcu eu luctus. Cras iaculis ligula non ultricies porttitor. Suspendisse placerat imperdiet quam sit amet tempus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras vitae lacus placerat, placerat eros et, convallis ex. Quisque sit amet vestibulum massa, a aliquam enim. Duis scelerisque tempor tellus, id vulputate enim bibendum nec. Morbi placerat dui a suscipit maximus. Maecenas non volutpat eros. In euismod hendrerit nisl ac aliquam.', 2, 500, 333, 500, series_id=2)
    app.register_blueprint(api.blueprint)
    app.run(port=config.PORT, host=config.HOST)
