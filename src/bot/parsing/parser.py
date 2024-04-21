import asyncio
from .mixins import DataParserMixin


class Parser(DataParserMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def dates_to_keyboard(self, day):
        if day == 0:
            data = 'Сегодня'
        else:
            data = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                             class_="day__date").text
        return data


    async def get_result_data(self, day):
        tasks, result_dict = [], {}
        function_list = await asyncio.create_task(self.get_functions_list())
        for index in range(len(function_list)):
            tasks.append(asyncio.create_task(function_list[index](day)))
        for j in tasks:
            result_dict.update(await j)
        return result_dict


    async def get_days_dict_and_list(self):
        days_list, tasks = [], []
        for i in range(9):
            tasks.append(asyncio.create_task(self.dates_to_keyboard(i)))
        
        #create task for today day here
        for task in tasks:
            days_list.append(await task)
        days_dict = {days_list[i]: i for i in range(9)}
        return days_dict, days_list
        







