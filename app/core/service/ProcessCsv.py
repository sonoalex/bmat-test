from inspect import _void
import os
from django.conf import settings
import csv
from datetime import datetime
import sys
import shutil


class ProcessCsv:
    """
    Service that generated a single file with all
    Total Number of Plays for Date
    """

    temp_dir = None
    raw_dir = None
    process_id = None
    fields = ["Song", "date", "Total Number of Plays for Date"]

    """
    Process the input CSV File
    """

    def process(self, filename, task_id):
        self.setup(task_id)

        sys.stdout.write("saving at %s" % (self.temp_dir))

        path_file = self.move_from_tmp_to_raw_dir(filename)

        sys.stdout.write("moved to  %s" % (self.raw_dir))

        headers_shown = False
        headers = None
        songname_list = []

        for line in self.read_file(path_file):
            if not headers_shown:
                headers_shown = True
                headers = line
                continue

            columns = [col.strip() for col in line.split(",")]

            if not self.is_valid_line(columns):
                # Append to a some kind of invalid_lines_file...
                pass

            song_name = columns[0]
            sys.stdout.write("Appending to file: %s,csv..." % format(song_name))

            with open(
                "%s_%s.csv" % (os.path.join(self.raw_dir, song_name), self.process_id),
                "a",
            ) as write_file:
                if song_name not in songname_list:
                    write_file.write(headers)
                    songname_list.append(song_name)

                write_file.write(line)

        split_but_calculated = self.perfom_calculation(songname_list)

        x = datetime.now()

        output_file = os.path.join(
            settings.PROCESSED_CSV_DIR,
            "%s_%s_%s.csv" % (self.process_id, "processed", x.strftime("%f")),
        )
        sys.stdout.write("Creating output file....")

        self.merge_files(split_but_calculated, output_file)

        return output_file

    def perfom_calculation(self, songname_list):

        sorted_file_list = []

        for filename in songname_list:
            path_file = os.path.join(self.raw_dir, filename)
            path_file = "%s_%s.csv" % (path_file, self.process_id)
            song_plays_date = {}
            total = {}
            headers_shown = False

            for line in self.read_file(path_file):
                if not headers_shown:
                    headers_shown = True
                    continue
                columns = line.split(",")
                song_plays_date.update({columns[1]: song_plays_date.get(columns[1], 0) + int(columns[2])})

            total.update({columns[0]: song_plays_date})

            computed_path_file = os.path.join(self.raw_dir, filename)
            computed_path_file = "%s_%s.csv" % (computed_path_file, "sorted")

            """
            total looks like this:
            {'Umbrella': {'2020-01-02': 250, '2020-01-01': 150, '2022-01-27': 5374, '2022-01-07': 5811}}
            So, for Song Umbrella, we have for each day, the total number of plays
            """
            self.sort_and_write_file(computed_path_file, total)
            sorted_file_list.append(computed_path_file)

        return sorted_file_list

    """
        Read file line by line
        Returns: Generator
    """
    def read_file(self, file_path):
        with open(file_path, "r") as read_file:
            while True:
                data = read_file.readline()
                if not data:
                    break
                yield data

    def sort_and_write_file(self, filename, data):
        print(data)
        song = str(list(data.keys())[0])
        with open(filename, "w") as output_csv:
            writer = csv.writer(output_csv)
            for key, value in sorted(data[song].items()):
                writer.writerow([song, key, value])

    def merge_files(self, file_list, resultant_file):
        with open(resultant_file, "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(self.fields)
            for fname in file_list:
                for line in self.read_file(fname):
                    outfile.write(line)

        return resultant_file

    def is_valid_line(self, columns):
        """Dummy validation"""
        return True

    def move_from_tmp_to_raw_dir(self, filename):
        path_file_from = os.path.join(self.temp_dir, filename)
        path_file_raw = os.path.join(self.raw_dir, filename)
        shutil.move(path_file_from, path_file_raw)

        return path_file_raw

    def setup(self, task_id):
        self.process_id = task_id
        self.temp_dir = os.path.join(settings.UPLOADS_TMP_DIR)
        self.raw_dir = os.path.join(settings.UPLOADS_RAW_DIR, self.process_id)
        os.mkdir(self.raw_dir)
