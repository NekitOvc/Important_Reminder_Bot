import emoji

class ConfigTask:
    welcome_text = emoji.emojize("Привет! :wave: Я бот!\
    \nМоя задача - записать твои важные дела.\
    \nНачнём? :wink:\
    \n\n:point_right:Нажми на /help, чтобы узнать о моих возможностях.", language="alias")

    help_text = emoji.emojize(":one: /add - добавить задачу. Ввод команды осуществляется в формате '/add дата задача'\
        \n:two: /show - показать все задачи на определенную дату. Ввод команды осуществляется в формате '/show дата'", language="alias")

    no_task = emoji.emojize('Задач на выбранную дату нет :neutral_face:. Добавь новую задачу!')
