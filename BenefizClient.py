from SuperSaaS import Client, Configuration
from datetime import datetime

from functools import lru_cache
from itertools import groupby
from operator import itemgetter
import os

class BenefizClient:
    def __init__(self, boat_schedule_name: str, training_schedule_name: str, trainer_schedule_name: str):
        self.client = Client(Configuration())
        self.boat_schedule_id = self._get_schedule_id(boat_schedule_name)
        self.training_schedule_id = self._get_schedule_id(training_schedule_name)
        self.trainer_schedule_id = self._get_schedule_id(trainer_schedule_name)

    @lru_cache
    def _get_schedule_id(self, schedule_name: str):
        schedules = self.client.schedules.list()
        return next(schedule.id for schedule in schedules if schedule.name == schedule_name)

    @lru_cache(1024)
    def appointments_range(self, schedule_id: int, from_time: datetime, to_time: datetime):
        return self.client.appointments.range(schedule_id, from_time=from_time, to=to_time)

    @lru_cache
    def get_boat_name(self, boat_id: int):
        boats = self.client.schedules.resources(schedule_id=self.boat_schedule_id)

        for boat in boats:
            if boat.id == boat_id:
                return boat.name
        return "NN"

    @lru_cache
    def get_trainer_name(self, trainer_id: int):
        trainers = self.client.schedules.resources(schedule_id=self.trainer_schedule_id)

        for trainer in trainers:
            if trainer.id == trainer_id:
                return trainer.name
        return "NN"

    def get_appointments_sorted(self, from_time: datetime, to_time: datetime):
        data = []

        apps = self.appointments_range(self.training_schedule_id, from_time, to_time)

        for app in apps:
            data.append(self.appointment_to_dict(app))
        # Sort the data by the key you want to group by

        data.sort(key=itemgetter('trainer_id'))

        return data

    def get_appointments_grouped(self, from_time: datetime, to_time: datetime):
        data = self.get_appointments_sorted(from_time, to_time)
        # Group by the 'category' key
        grouped_data = {k: list(v) for k, v in groupby(data, key=itemgetter('trainer_id'))}

        return grouped_data

    def appointment_to_dict(self, appointment):
        result = {
            "id": appointment.id,
            "start": datetime.fromisoformat(appointment.start),
            "finish": datetime.fromisoformat(appointment.finish),
            "created_by": appointment.created_by,
            "full_name": appointment.full_name,
            "mobile": appointment.mobile,
            "boat_id": appointment.resources[0],
            "trainer_id": appointment.resources[1],

        }

        boat_name = self.get_boat_name(appointment.resources[0])
        trainer_name = self.get_trainer_name(appointment.resources[1])

        if boat_name == "NN" and trainer_name == "NN":
            # swap boat and trainer
            tmp = result["boat_id"]
            result["boat_id"] = result["trainer_id"]
            result["trainer_id"] = tmp
            result["boat_name"] = self.get_boat_name(result["boat_id"])
            result["trainer_name"] = self.get_trainer_name(result["trainer_id"])
            return result
        elif boat_name != "NN" and trainer_name != "NN":
            result["boat_name"] = self.get_boat_name(result["boat_id"])
            result["trainer_name"] = self.get_trainer_name(result["trainer_id"])
            return result

        raise Exception(f"Boat or Trainer not found. Boat:{self.get_boat_name(result['boat_id'])}, Trainer: {self.get_trainer_name(result['trainer_id'])}")
