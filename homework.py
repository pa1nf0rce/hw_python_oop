from dataclasses import dataclass, asdict
from typing import Tuple, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вернуть сообщение о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action = action  # count of completed actions
        self.duration = duration  # hours
        self.weight = weight  # kilogram

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Метод в {type(self).__name__} должен быть переопредлен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLIER_CALORIE_1: int = 18
    SUBTRACT_CALORIE_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Формула расчета ср.скорости при занятии бегом:
        (18 * средняя_скорость - 20) * вес_спортсмена /
        M_IN_KM * время_тренировки_в_минутах.
        """
        return (
            (self.MULTIPLIER_CALORIE_1 * self.get_mean_speed()
             - self.SUBTRACT_CALORIE_2) * self.weight
            / self.M_IN_KM * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    MULTIPLIER_CALORIE_1: float = 0.035
    MULTIPLIER_CALORIE_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,) -> None:

        super().__init__(action, duration, weight)
        self.height = height  # meters

    def get_spent_calories(self) -> float:
        """Формула расчета калорий
        при спортивной ходьбе:
        (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах.
        """

        return (
            (self.MULTIPLIER_CALORIE_1 * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.MULTIPLIER_CALORIE_2 * self.weight)
            * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    LEN_STEP: float = 1.38
    ADDITION_CALORIE_1: float = 1.1
    MULTIPLIER_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # meters
        self.count_pool = count_pool  # count of swimming pools

    def get_mean_speed(self) -> float:
        """Формула расчета ср. скорости
        для занятий в бассейне:
        длина_бассейна * кол-во проплытых бассейнов
        / M_IN_KM / время_тренировки.
        """
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Формула расчета калорий
        для занятий в бассейне:
        (средняя_скорость + 1.1) * 2 * вес.
        """

        return (
            (self.get_mean_speed() + self.ADDITION_CALORIE_1)
            * self.MULTIPLIER_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:

        training_type: Dict[str, Type[Training]] = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking,
        }
        return training_type[workout_type](*data)

    except:
        raise ValueError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':

    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
