# Что надо знать перед тем, как лезть в код

Черновик.

## 1. Слои

Код разложен по четырём папкам в `src/`.

**`delivery`: способ достучаться до приложения.**
По сути `delivery` делает одно: вызывает `use_case.act(...)` и отдаёт результат
в понятном для своего клиента формате. Способов может быть сколько угодно, а
приложение за ними одно и то же:

```python
# HTTP (FastAPI) — так сделано в проекте
@router.post("/cases/{case_id}/open")
async def open_case(case_id: UUID, ...) -> OpenCaseResponse:
    result = await use_case.act(command=OpenCaseCm(...))
    return open_case_response(result=result)            # → JSON


# CLI — так могло бы быть
async def open_case_cli(case_id: str) -> None:
    result = await use_case.act(command=OpenCaseCm(...))
    print(f"Выпало: {result.inventory_item.item.name}")  # → текст в терминал


# Telegram-бот (aiogram) — так могло бы быть
@dp.message(Command("open"))
async def open_case_bot(message: Message) -> None:
    result = await use_case.act(command=OpenCaseCm(...))
    await message.answer(f"🎁 {result.inventory_item.item.name}")  # → сообщение
```

Во всех трёх вызывается один и тот же `OpenCaseUc.act`, разный только вход и
выход.

**`application`: сама игра.**
Какие в ней есть вещи: игрок, кейс, предмет. Что с ними можно делать: открыть
кейс, подарить предмет, забрать бонус. И по каким правилам: нельзя открыть кейс
без денег, нельзя подарить чужой предмет. Здесь не важно, пришёл запрос по HTTP
или из CLI и где лежат данные. Если выкинуть все остальные папки, `application`
всё равно описывает игру целиком.

**`infra`: всё, что игре нужно, но что живёт вне нашего кода.**
Данные хранятся в Postgres. Случайное число выдаёт операционная система.
Текущее время тоже берётся у системы. Код, который умеет со всем этим работать
(SQL-запросы, вызов `random`, `datetime.now()`), лежит в `infra`.

**`bootstrap`: сборка.**
Создаёт все объекты, связывает их друг с другом и запускает приложение.

### Кто что может импортировать

```text
delivery ──→ application ←── infra

bootstrap знает обо всех
```

Стрелка значит «знает про», то есть «может импортировать».

**`delivery`** импортирует только `application`:

```python
from application.use_cases.cases.open import OpenCaseUc  # ✅
from infra.dm.player import AlchemyPlayerDm             # ❌ хендлер не лезет в базу
```

**`infra`** импортирует только `application`: берёт оттуда сущности и
интерфейсы, которые реализует.

```python
from application.entities.player import Player          # ✅
from delivery.api.v1.http.schemas import ...            # ❌
```

**`application`** импортирует только сам себя:

```python
from application.entities.case import Case              # ✅
import sqlalchemy                                       # ❌
from fastapi import ...                                 # ❌
from infra.random import SystemRandomValue              # ❌
```

**`bootstrap`** импортирует всех, его работа — всё соединить.

## 2. Что происходит, когда игрок открывает кейс

Игрок жмёт «открыть кейс», приходит `POST /api/v1/cases/{case_id}/open`.

### Хендлер (`delivery`)

`delivery/api/v1/http/handlers/cases.py`:

```python
async def open_case(case_id, player_id, use_case):
    result = await use_case.act(
        command=OpenCaseCm(player_id=player_id, case_id=case_id),
    )

    return open_case_response(result=result)
```

Хендлер ничего не решает. Он достаёт данные из запроса, вызывает `act()` и
превращает результат в JSON.

### Юзкейс (`application`)

**Юзкейс — это одно действие, которое умеет приложение:** «открыть кейс»,
«подарить предмет», «забрать бонус». `delivery` просит: «открой кейс 42 для
игрока 7». Юзкейс делает всё, что для этого нужно, от начала до конца, и
возвращает результат.

Снаружи видно только `act()`: передал команду, получил результат. Что
происходит внутри, `delivery` не знает и знать не должен. Поэтому один и тот же
юзкейс подходит и хендлеру, и CLI, и боту.

Внутри юзкейс почти ничего не делает руками. Он как рецепт: по шагам вызывает
другие части `application` и собирает из них результат.

`application/use_cases/cases/open.py`:

```python
class OpenCaseUc:
    _player_dm: IPlayerDm
    _case_dm: ICaseDm
    _random: IRandom
    _clock: IClock
    ...

    async def act(self, *, command):
        player = await self._lock_player(player_id=command.player_id)
        case = await self._get_case(case_id=command.case_id)

        player = player.spend(amount=case.price)

        inventory_item = self._drop_item(player=player, case=case)

        await self._player_dm.save(entity=player)
        self._inventory_item_dm.add(entity=inventory_item)

        await self._transaction_manager.commit()

        return OpenCaseRs(...)
```

Метод читается как текст: найти игрока, найти кейс, списать деньги, выбросить
предмет, сохранить.

Юзкейс может пользоваться чем угодно из `application`. В этом юзкейсе это:

- **сущности и их правила**. `player.spend()` сам проверяет, хватает ли денег,
  и выбрасывает `NotEnoughCoinsError`, если нет. `case.roll()` сам выбирает
  предмет по шансам;
- **интерфейсы** — поля `_player_dm`, `_random`, `_clock`.

В других местах это могут быть сервисы (правило, которое касается сразу
нескольких сущностей), ошибки, настройки и так далее.

### Интерфейсы: «что», без «как»

Интерфейс — это описание того, что компонент умеет, без того, как он это делает.

`application/interfaces/dm/player.py`:

```python
class IPlayerDm(Protocol):
    async def get_for_update(self, *, id: UUID) -> Player | None: ...
    async def save(self, *, entity: Player) -> None: ...
```

Тут написано только: «мне нужно уметь достать игрока и сохранить его».
Postgres, файл или словарь в памяти — неважно.

Реализаций у интерфейса может быть несколько, и лежать они могут где угодно.
Например, интерфейс «посчитай скидку» можно реализовать двумя правилами прямо
в `application`, ведь это бизнес-логика. В этом проекте все интерфейсы
описывают то, что нужно от внешнего мира (база, случайность, время), поэтому
их реализации лежат в `infra`.

### Реализации (`infra`)

А как именно, написано в `infra`. `infra/dm/player.py`:

```python
class AlchemyPlayerDm:
    async def get_for_update(self, *, id):
        stmt = select(PlayerOrm).where(PlayerOrm.id == id).with_for_update()
        ...
```

`AlchemyPlayerDm` выполняет обещание `IPlayerDm` через SQLAlchemy и Postgres.
Он импортирует интерфейс из `application`, отсюда стрелка `infra → application`.

| Интерфейс (`application`) | Реализация (`infra`) |
|---|---|
| `IPlayerDm` — достать и сохранить игрока | `AlchemyPlayerDm` — через Postgres |
| `IRandom` — дай случайное число | `SystemRandomValue` — через `random.SystemRandom` |
| `IClock` — скажи, который час | `SystemClock` — через `datetime.now()` |

При старте `bootstrap` подставляет `AlchemyPlayerDm` туда, где юзкейс просит
`IPlayerDm`.

Интерфейс ещё называют **портом**, а реализацию — **адаптером**. Отсюда
название подхода: «порты и адаптеры».

### Вся картина

```text
 delivery          application                              infra

 хендлер ──act()──→ юзкейс ──→ сущности (Player.spend)
                          └──→ интерфейсы (IPlayerDm) ←── реализации (AlchemyPlayerDm)
```

## 3. Почему `application` не зависит от `infra`

Потому что правила игры меняются редко, а технологии часто.

- Переехали с Postgres на что-то другое? Пишем новую реализацию `IPlayerDm`,
  юзкейсы не трогаем.
- Хотим проверить, что легендарка выпадает при «удачном» случайном числе?
  Подставляем вместо `IRandom` фейк, который всегда отдаёт `0.99`. Ни базы, ни
  настоящей случайности не нужно.
- Хотим проверить, что бонус нельзя забрать дважды за сутки? Подставляем
  `IClock` с нужным временем, ждать сутки не надо.

Если бы юзкейс сам вызывал `datetime.now()` или `select(...)`, ничего из этого
не получилось бы.

## 4. Транзакция и коммит

Когда юзкейс в первый раз обращается к базе, открывается **транзакция**.
Дальше все запросы этого сценария идут в неё же. Пока транзакция открыта,
изменения видны только ей и в базе ещё не сохранены.

Закончиться транзакция может одним из двух способов:

- `commit()` — все изменения сохраняются разом;
- `rollback()` — все изменения отменяются, в базе всё как было до начала.

`rollback()` происходит сам, если по дороге вылетела ошибка или коммит так и не
вызвали.

Поэтому `commit()` вызывает только юзкейс, один раз, в самом конце. На примере
открытия кейса:

- если `player.spend()` выбросил `NotEnoughCoinsError`, до коммита дело не
  дошло, и транзакция откатилась: деньги не списались, предмет не появился;
- если всё прошло, коммит сохраняет и списание, и предмет одновременно.

Либо всё, либо ничего. Если бы `save()` коммитил сам, могло бы выйти так:
деньги списались, а предмет не выдали.

## 5. SELECT ... FOR UPDATE

У игрока 50 монет, кейс стоит 50. Он очень быстро жмёт «открыть» два раза, и
на сервер приходят два запроса одновременно:

```text
запрос A: читает баланс → 50
запрос B: читает баланс → 50
запрос A: 50 − 50 = 0, сохраняет, выдаёт предмет
запрос B: 50 − 50 = 0, сохраняет, выдаёт предмет
```

Два предмета по цене одного.

`get_for_update` читает игрока через `SELECT ... FOR UPDATE`. Это значит «я
читаю эту строку, чтобы изменить, остальные пусть подождут». Строка
блокируется до конца транзакции:

```text
запрос A: читает баланс с блокировкой → 50
запрос B: хочет прочитать → ждёт
запрос A: списывает, коммит, блокировка снята
запрос B: читает → 0 → NotEnoughCoinsError
```

В проекте так сделано в трёх местах:

- **открытие кейса** — блокируем игрока, чтобы не списать одни монеты дважды;
- **ежедневный бонус** — блокируем игрока, чтобы бонус нельзя было забрать
  двумя кликами;
- **подарок** — блокируем предмет, чтобы его нельзя было подарить двум людям
  сразу.
