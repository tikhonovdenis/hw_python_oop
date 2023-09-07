class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type: str = training_type  # имя класса тренировки
        self.duration: float = duration  # длительность тренировки в часах
        self.distance: float = distance  # дистанция в км, за время тренировки
        self.speed: float = speed  # с редняя скорость
        self.calories: float = calories  # затраченное кол-во ккал
        # за тренировку

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # базовое расстояние, преодаленное за один шаг 0.65
    M_IN_KM: int = 1000  # константа для перевода значений из м в км
    TO_MINS: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action  # число шагов или гребков
        self.duration: float = duration  # длительность тренировки ч.
        self.weight: float = weight  # вес

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avr_speed = self.get_distance() / self.duration
        return avr_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # подсчёт для каждого вида тренировки будет свой

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.TO_MINS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    TO_MS_OF_KM = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
             + ((self.get_mean_speed() * self.TO_MS_OF_KM)**2
                / (self.height / self.SM_IN_M))
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
            * (self.duration * self.TO_MINS))


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2
    LEN_STEP: float = 1.38  # расстояние, преодаленное за  гребок

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна в метрах
        self.count_pool = count_pool  # сколько раз перплыл бассейн

    def get_mean_speed(self) -> float:
        """Средняя скорость плавания"""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight
                * self.duration)

    def get_distance(self) -> float:
        """Переопредеяем дистанцию в км. для плавания"""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type in workout and len(data) > 0:
        return workout[workout_type](*data)
    else:
        print('Код тренировки или данные не получены!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
