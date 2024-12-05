
from news.models import User, Author, Category, PostCategory, Post, POSITIONS, Comment

user1 = User.objects.create(name = 'Пушкин')
user2 = User.objects.create(name = 'Лермонтов')

author1 = Author.objects.create(full_name = 'Иванов Иван Иванович', user = user1)
author2 = Author.objects.create(full_name = 'Петров Петр Петрович', user = user2)

category1 = Category.objects.create(name = 'Новость дня')
category2 = Category.objects.create(name = 'Новости шоубиза')
category3 = Category.objects.create(name = 'Красота и здоровье')
category4 = Category.objects.create(name = 'Спорт')

text = '''Футбол — спортивная игра на травяном поле, в которой две противоборствующие команды (по 11 человек в каждой), используя ведение и передачи мяча ногами или другой частью тела (кроме рук), стремятся забить его в ворота соперника и не пропустить в свои.

Футбольное поле имеет размеры 90–120 x 45–90 м, продолжительность игры — 90 минут (2 тайма по 45 минут с перерывом 15 минут).

Футбол — это одно из самых доступных, популярных и массовых средств физического развития и укрепления здоровья широких слоев населения. Игра занимает ведущее место в общей системе физического воспитания.'''
article1 = Post.objects.create(text_post = text, head = 'ФУТБОЛ', position = 'AR', author = author1)
article1.category.add(category3,category4)
text1 = '''Новости шоу-бизнеса являются неотъемлемой частью жизни для большинства. Они в некоторой мере проникают в каждого человека. Публичные люди всегда на виду. Их судьбы интересуют миллионы. Люди жизнь своих кумиров воспринимают как интересный сериал. Им хочется быть частью всего происходящего и контролировать ситуацию, сопереживая и поддерживая.

Яркие и харизматичные личности всегда интересовали общественность. Новости шоу-бизнеса часто носят развлекательный характер. Это своего рода альтернатива другому расслабляющему досугу. Они позволяют абстрагироваться от проблем и забот.

Обычному человеку в жизни очень часто не хватает ярких эмоций. Именно поэтому люди стремятся получить таковые извне. Им хочется верить и знать, что может быть иначе. Многие представители социума сами мечтают о том, чтобы стать знаменитыми. Они ловят манеру поведения своих кумиров и стараются им подражать. Каждое событие, связанное со знаменитостями, делает простого обывателя ближе к нему.'''
article2 = Post.objects.create(text_post = text1, head = 'ПОЧЕМУ ВСЕМ ИНТЕРЕСЕН ШОУБИЗ', position = 'AR', author = author1)
article2.category.add(category1,category2)
text2 = '''На побережье турецкого Белека отмечена вспышка заболевания, связанная с мощным вирусом. Согласно информации телеграм-канала SHOT, за последние дни несколько десятков детей и взрослых из ближайших отелей обратились в местный госпиталь с жалобами на высокую температуру. При этом отмечается, что острая форма заболевания длится примерно 4-5 дней, после чего постепенно становится легче. Также у больных в анализах крови наблюдаются значительные повышения уровней C-реактивного белка, азота мочевины и количества нейтрофилов. Основной диагноз пациентов — «острая инфекция, неуточненная». Им назначают антибиотики и противоинфекционные средства.'''
article3 = Post.objects.create(text_post = text2, head = 'ПОЧЕМУ ВСЕМ ИНТЕРЕСЕН ШОУБИЗ', position = 'NW', author = author2)
article3.category.add(category1,category3)

comment1 = Comment.objects.create(text_comment = 'Наши тела — это наши сады, а наши усилия воли — это наши садовники', post = article3, user = user1)
comment2 = Comment.objects.create(text_comment = 'Боль, которую вы чувствуете сегодня, станет силой, которую вы почувствуете завтра', post = article2, user = user2)
comment3 = Comment.objects.create(text_comment = 'Иногда вы не осознаете свою силу, пока не столкнетесь лицом к лицу со своей самой большой слабостью', post = article1, user = user2)
comment4 = Comment.objects.create(text_comment = 'Чемпион — это тот, кто встает, когда не может', post = article2, user = user1)

article1.like()
article1.save()
article2.like()
article2.save()
article1.like()
article1.save()
article3.like()
article3.save()

comment1.like()
comment2.like()
comment3.dislike()
comment4.like()
comment2.like()



Author.objects.get(user = user1).update_rating()
Author.objects.get(user = user2).update_rating()

Author.objects.order_by('-rank').first().user.values('name')

best_post = Post.objects.order_by('-rank').first()
print(f'date: {best_post.time_in.date()}, username: {best_post.author.user.values('name')}, rank: {best_post.rank_post}, title: {best_post.head}, preview: {best_post.preview()}')

Comment.objects.filter(post=best_post).values('time_in', 'name', 'rank', 'text_post')
