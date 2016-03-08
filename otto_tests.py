import os
import unittest
import subprocess
import time

class OttoTests(unittest.TestCase):
    def test_GUI_interaction(self):
        actual = []
        ### make sure otto is sending song info to the GUI correctly ###
        expected = ['Tyler the Creator 03 Cowboy.wav 195.333333333\n', 'Childish Gambino 01 New Prince (Crown On the Ground).wav 229.350498866\n', 'Danny Brown 16 - - EWNESW.wav 143.09877551\n']
        proc = subprocess.Popen(['./portaudio/SenProj', '-s', "Tyler the Creator|03 Cowboy.wav|195.333333333|Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866|Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        while proc.poll() == None:
            actual += proc.stdout.readlines()
        self.assertEqual(actual, expected)

    def test_bad_song_input(self):
        ### this should not work (file does not exist) ###
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Childish Gambino|NOT_A_REAL_SONG.wav|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        proc.wait()
        ### make sure it crashed ###
        self.assertEqual(proc.returncode, -11)

        ### this should also not work (file is wrong format) ###
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Childish Gambino|REAL_TEXT_FILE.txt|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stderr=subprocess.PIPE, universal_newlines=True)
        ### make sure it crashed ###
        self.assertEqual(proc.stderr.readlines(), ["otto.cpp:139: failure at: freadStr(wavfile, 4) == \"RIFF\"\n"])
    
    def test_start_song(self):
        ### this should work ###
        proc = subprocess.Popen(['./portaudio/SenProj', '-p', "Childish Gambino|01 New Prince (Crown On the Ground).wav|229.350498866||Danny Brown|16 - - EWNESW.wav|143.09877551|\n"], bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)
        ### play some music for 5 seconds ###
        time.sleep(5)
        ### fail if it crashed ###
        if (proc.poll() != None):
            self.fail()
        else:
            proc.terminate()
            pass

if __name__ == '__main__':
    unittest.main()