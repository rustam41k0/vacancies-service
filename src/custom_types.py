from enum import Enum


class ExperienceEnum(Enum):
    without_experience = 'Без опыта'
    less_than_one_year = 'Меньше 1 года'
    one_to_three_years = 'От 1 до 3 лет'
    over_three_years = 'Больше 3 лет'


class EmploymentEnum(Enum):
    fulltime = 'Полная занятость'
    parttime = 'Частичная занятость'
    intern = 'Стажировка'


class SalaryEnum(Enum):
    desc = 'desc'
    asc = 'asc'
