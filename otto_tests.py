import os
import unittest
import subprocess
import time

class OttoTests(unittest.TestCase):
    def test_get_more_songs(self):
        actual = []
        expected = ['Tyler the Creator 03 Cowboy.wav 195.333333333\n', 'Childish Gambino 01 New Prince (Crown On the Ground).wav 229.350498866\n', 'Danny Brown 16 - - EWNESW.wav 143.09877551\n']
        proc = subprocess.Popen(['./portaudio/SenProj', '-s', "Tyler the Creator|03 Cowboy.wav|195.333333333|Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866|Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        while proc.poll() == None:
            actual += proc.stdout.readlines()
        self.assertEqual(actual, expected)

    def test_bad_song_input(self):
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Tyler the Creator|NOT_A_REAL_SONG.wav|195.333333333|Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        proc.wait()
        self.assertEqual(proc.returncode, -11)
    
    def test_start_song(self):
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Tyler the Creator|03 Cowboy.wav|195.333333333|Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        time.sleep(5)
        if (proc.poll() != None):
            self.fail()
            proc.terminate()
        else:
            proc.terminate()
            pass

    def test_start_song(self):
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Tyler the Creator|03 Cowboy.wav|195.333333333|Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        time.sleep(5)
        if (proc.poll() != None):
            self.fail()
            proc.terminate()
        else:
            proc.terminate()
            pass

if __name__ == '__main__':
    unittest.main()