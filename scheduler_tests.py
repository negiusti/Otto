from scheduler import *
import unittest

class SchedulerTests(unittest.TestCase):
    def test_tempo_value(self):
        self.assertEqual(tempo_value("SLO"), 0)
        self.assertEqual(tempo_value("MED UP"), 3)
        try:
            tempo_value("not a real tempo")
            self.fail()
        except:
            pass

    def test_genre_value(self):
        self.assertEqual(genre_value("french"), 0)
        self.assertEqual(genre_value("indie pop"), 6)
        try:
            genre_value("not a real genre")
            self.fail()
        except:
            pass        

    def test_choice_constructor(self):
        choice = Choice ("AJJ", "Distance.wav", "666", "folk punk", "UP")
        self.assertEqual(choice.artist, "AJJ")
        self.assertEqual(choice.file, "Distance.wav")
        self.assertEqual(choice.time, "666")
        self.assertEqual(choice.genre, "folk punk")
        self.assertEqual(choice.tempo, "UP")
        pass

    def test_choice_to_str(self):
        choice = Choice ("AJJ", "Distance.wav", "666", "folk punk", "UP")
        self.assertEqual(choice.to_str(), "AJJ|Distance.wav|666|")
        pass

    def test_fitness(self):
        choice = Choice ("AJJ", "Distance.wav", "666", "folk punk", "UP")
        previousSong = Choice ("Angel Olsen", "Forgiven, Forgotten.wav", "666", "folk", "MED")
        self.assertEqual(fitness(choice, previousSong), 0)
        pass

if __name__ == '__main__':
    unittest.main()