from dataclasses import dataclass
from typing import Tuple, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def show_training_info(self):
        return InfoMessage(self.training_type,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)                           
    
    def get_message(self) -> str:

        return ('Тип тренировки: {0}; '
                'Длительность: {1:.3f} ч.; '
                'Дистанция: {2:.3f} км; ' 
                'Ср. скорость: {3:.3f} км/ч; '
                'Потрачено ккал: {4:.3f}.').format(self.training_type,
                                                   self.duration,
                                                   self.distance,
                                                   self.speed,
                                                   self.calories)
        
        
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, 
                action: int, 
                duration: float,
                weight: float) -> None:

        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Формула расчета ср. скорости 
        при занятии бегом:
        (18 * средняя_скорость - 20) * вес_спортсмена / 
        M_IN_KM * время_тренировки_в_минутах.
        """
        times_in_minutes = self.duration * 60
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) 
               * self.weight / self.M_IN_KM * times_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    def __init__(self, 
                action: int, 
                duration: float, 
                weight: float, 
                height: float,) -> None:

        super().__init__(action, duration, weight)    
        self.height = height

    def get_spent_calories(self) -> float:
        """Формула расчета калорий 
        при спортивной ходьбе:
        (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес) 
        * время_тренировки_в_минутах.
        """
        time_in_minutes: float = self.duration * 60
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        return ((coeff_calorie_1 * self.weight + 
               (self.get_mean_speed() ** 2 // self.height) 
               * coeff_calorie_2 * self.weight) * time_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    LEN_STEP: float = 1.38

    def __init__(self, 
                action: int, 
                duration: float, 
                weight: float, 
                length_pool: int, 
                count_pool: int,) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Формула расчета ср. скорости 
        для занятий в бассейне: 
        длина_бассейна * кол-во проплытых бассейнов 
        / M_IN_KM / время_тренировки.
        """
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Формула расчета калорий 
        для занятий в бассейне: 
        (средняя_скорость + 1.1) * 2 * вес.
        """
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        return (self.get_mean_speed() + coeff_calorie_1) * coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]]

    training_type = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    
if __name__ == '__main__':
    packages: List[Tuple[str,List[int]]]

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

